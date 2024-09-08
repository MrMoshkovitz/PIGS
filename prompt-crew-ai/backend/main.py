from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from langchain_openai import ChatOpenAI
from openai import OpenAIError
import asyncio
from pydantic_settings import BaseSettings
from crewai.crews.crew_output import CrewOutput
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    model_name: str = "gpt-3.5-turbo"

    model_config = {
        'protected_namespaces': ('settings_',)
    }

settings = Settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

try:
    llm = ChatOpenAI(openai_api_key=settings.openai_api_key, model_name=settings.model_name)
except OpenAIError as e:
    logger.error(f"Failed to initialize OpenAI client: {str(e)}")
    raise

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

async def optimize_prompt(prompt: str):
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

    crew = Crew(
        agents=[prompt_engineer, analyst],
        tasks=[task1, task2],
        verbose=True,
        process=Process.sequential
    )

    try:
        result = await asyncio.to_thread(crew.kickoff)
        
        logger.debug(f"Result type: {type(result)}")
        logger.debug(f"Result content: {result}")
        
        if isinstance(result, CrewOutput):
            if hasattr(result, 'tasks_output') and len(result.tasks_output) >= 2:
                improved_prompt = result.tasks_output[0].raw
                analysis = result.tasks_output[1].raw
            else:
                improved_prompt = result.raw
                analysis = "No separate analysis provided."
        elif isinstance(result, list) and len(result) >= 2:
            improved_prompt = str(result[0])
            analysis = str(result[1])
        elif isinstance(result, str):
            parts = result.split("\n\n", 1)
            if len(parts) == 2:
                improved_prompt, analysis = parts
            else:
                improved_prompt = result
                analysis = "No separate analysis provided."
        else:
            error_msg = f"Unexpected result structure. Type: {type(result)}, Content: {str(result)[:500]}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        return improved_prompt, analysis
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=503, detail="OpenAI service unavailable")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize_prompt")
async def optimize_prompt_endpoint(request: PromptRequest):
    logger.info(f"Received prompt: {request.prompt}")
    
    try:
        improved_prompt, analysis = await optimize_prompt(request.prompt)
        
        logger.info(f"Returning result: Improved prompt: {improved_prompt[:50]}... Analysis: {analysis[:50]}...")
        return {"improved_prompt": improved_prompt, "analysis": analysis}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)