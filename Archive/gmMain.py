import os
import json
from openai import OpenAI
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variables for API keys
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
search_tool = SerperDevTool()

def run_prompt_test(prompt_id, user_prompt):
    # Save the initial user prompt to a file with the prompt ID as prefix
    with open(f"TestsData/initial_prompt_{prompt_id}.md", "w") as file:
        file.write(f"# Initial Prompt\n\n{user_prompt}")
    
    # Generate the initial response using OpenAI API and save it to a file
    init_response = get_prompt_response(user_prompt)
    with open(f"TestsData/initial_response_{prompt_id}.md", "w") as file:
        file.write(f"# Initial Response\n\n{init_response}")

    # Run the Crew process to generate the optimized prompt
    optimized_result = crew.kickoff(inputs={'user_prompt': user_prompt})

    # Access the actual optimized prompt from the result
    optimized_prompt = extract_optimized_prompt(optimized_result)
    
    # Save the optimized prompt to a file
    with open(f"TestsData/optimized_prompt_{prompt_id}.md", "w") as file:
        file.write(f"# Optimized Prompt\n\n{optimized_prompt}")
    
    # Generate the optimized response using OpenAI API and save it to a file
    optimized_response = get_prompt_response(optimized_prompt)
    with open(f"TestsData/optimized_response_{prompt_id}.md", "w") as file:
        file.write(f"# Optimized Response\n\n{optimized_response}")

def extract_optimized_prompt(result):
    """
    Extract the optimized prompt from the CrewOutput.
    """
    return result.raw

def get_prompt_response(prompt: str):
    """
    Function to generate a response using OpenAI API.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def load_and_test_prompts():
    """
    Load prompt options from a JSON file and test the prompt refinement process on each.
    """
    # Load the prompt options from the JSON file
    with open("prompt_options.json", "r") as file:
        prompt_data = json.load(file)
    
    # Run the prompt refinement process for each prompt
    for prompt_option in prompt_data["prompt_options"]:
        prompt_id = prompt_option["id"]
        user_prompt = prompt_option["prompt"]
        print(f"Running test for prompt ID {prompt_id}: {user_prompt}")
        run_prompt_test(prompt_id, user_prompt)

prompt_engineer = Agent(
    role="GPT Prompt Engineer",
    goal="To refine and optimize GPT prompts for maximum clarity, efficiency, and task alignment. The agent should focus on enhancing the input prompt to ensure it is concise, clear, and aligns with the user's specific objectives.",
    backstory="This agent is specialized in prompt engineering, trained to optimize prompts to maximize the effectiveness of GPT outputs.",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    output_file="prompt_engineer_report.md",
)

improve_prompt_task = Task(
    description=(
        "Refine and optimize the provided GPT prompt: '{user_prompt}' "
        "to improve clarity, efficiency, and alignment with the desired outcome. "
        "The task is to ensure the prompt is specific, unambiguous, and optimized to prevent irrelevant output."
    ),
    expected_output=(
        "A refined and optimized version of the user initial prompt '{user_prompt}' "
        "that clearly aligns with the user's objectives. "
        "The final prompt should be concise, task-specific, and structured to elicit the most relevant and accurate responses from the GPT model. "
        "Respond only with the final prompt without any additional information."
    ),
    tools=[search_tool],
    agent=prompt_engineer,
)

crew = Crew(
    agents=[prompt_engineer],
    tasks=[improve_prompt_task],
    process=Process.sequential
)

if __name__ == "__main__":
    load_and_test_prompts()
