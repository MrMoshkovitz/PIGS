# Import necessary libraries
from fastapi import FastAPI, HTTPException  # FastAPI is used to create our web server
from pydantic import BaseModel  # Pydantic helps with data validation
from crewai import Agent, Task, Crew, Process  # CrewAI for AI agent coordination
from fastapi.middleware.cors import CORSMiddleware  # Allows our frontend to communicate with this backend
import os  # For interacting with the operating system
import logging  # For logging messages and errors
from langchain_openai import ChatOpenAI  # For interacting with OpenAI's language models
from openai import OpenAIError  # For handling OpenAI-specific errors
import asyncio  # For running asynchronous code
from pydantic_settings import BaseSettings  # For managing settings
from crewai.crews.crew_output import CrewOutput  # For handling CrewAI output

# Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env into the environment

# Set up logging to help with debugging
logging.basicConfig(level=logging.DEBUG)  # DEBUG level gives us more detailed logs
logger = logging.getLogger(__name__)  # Create a logger for this module

# Define settings for our application
class Settings(BaseSettings):
    # Get the OpenAI API key from environment variables
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    # Specify which GPT model to use
    model_name: str = "gpt-3.5-turbo"

    model_config = {
        'protected_namespaces': ('settings_',)
    }

settings = Settings()  # Create an instance of our settings

# Create our FastAPI application
app = FastAPI()

# Add CORS middleware to allow our frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the structure of our prompt request
class PromptRequest(BaseModel):
    prompt: str  # The prompt field will contain the user's input

# Initialize the language model
try:
    llm = ChatOpenAI(openai_api_key=settings.openai_api_key, model_name=settings.model_name)
except OpenAIError as e:
    logger.error(f"Failed to initialize OpenAI client: {str(e)}")
    raise

# Define our AI agents
prompt_engineer = Agent(
    role='Prompt Engineer',
    goal='Improve prompts for better results',
    backstory='You are an expert in crafting effective prompts for AI models.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

analyst = Agent(
    role='Prompt Analyst',
    goal='Analyze and provide insights on prompt effectiveness',
    backstory='You specialize in evaluating and optimizing prompts for maximum impact.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Function to optimize the prompt using our AI agents
async def optimize_prompt(prompt: str):
    # Create tasks for our AI crew
    task1 = Task(
        description=f"Improve this prompt: '{prompt}'. Make it more specific, clear, and effective.",
        agent=prompt_engineer,
        expected_output="An improved version of the given prompt that is more specific, clear, and effective."
    )

    task2 = Task(
        description="Analyze the improved prompt and provide insights on its effectiveness.",
        agent=analyst,
        expected_output="An analysis of the improved prompt, highlighting its strengths and potential areas for further improvement."
    )

    # Create the AI crew
    crew = Crew(
        agents=[prompt_engineer, analyst],
        tasks=[task1, task2],
        verbose=True,
        process=Process.sequential  # Tasks will be executed one after another
    )

    try:
        # Run the crew and get the result
        result = await asyncio.to_thread(crew.kickoff)
        
        # Log detailed debug information
        logger.debug(f"Result type: {type(result)}")
        logger.debug(f"Result content: {result}")
        
        # Extract results based on the type of output we get
        if isinstance(result, CrewOutput):
            # If we get a CrewOutput object
            if hasattr(result, 'tasks_output') and len(result.tasks_output) >= 2:
                improved_prompt = result.tasks_output[0].raw
                analysis = result.tasks_output[1].raw
            else:
                improved_prompt = result.raw
                analysis = "No separate analysis provided."
        elif isinstance(result, list) and len(result) >= 2:
            # If we get a list with at least two elements
            improved_prompt = str(result[0])
            analysis = str(result[1])
        elif isinstance(result, str):
            # If we get a single string, try to split it into prompt and analysis
            parts = result.split("\n\n", 1)
            if len(parts) == 2:
                improved_prompt, analysis = parts
            else:
                improved_prompt = result
                analysis = "No separate analysis provided."
        else:
            # If we get an unexpected result type
            error_msg = f"Unexpected result structure. Type: {type(result)}, Content: {str(result)[:500]}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        return improved_prompt, analysis
    except OpenAIError as e:
        # Handle OpenAI-specific errors
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=503, detail="OpenAI service unavailable")
    except Exception as e:
        # Handle any other unexpected errors
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Define the endpoint for our API
@app.post("/optimize_prompt")
async def optimize_prompt_endpoint(request: PromptRequest):
    logger.info(f"Received prompt: {request.prompt}")
    
    try:
        # Call the optimize_prompt function with the received prompt
        improved_prompt, analysis = await optimize_prompt(request.prompt)
        
        # Log the result (first 50 characters of each for brevity)
        logger.info(f"Returning result: Improved prompt: {improved_prompt[:50]}... Analysis: {analysis[:50]}...")
        return {"improved_prompt": improved_prompt, "analysis": analysis}
    except HTTPException as http_exc:
        # Re-raise HTTP exceptions (like 503 or 500) without modification
        raise http_exc
    except Exception as e:
        # For any other exception, log it and return a 500 error
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Run the server if this file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Start the server on localhost:8000