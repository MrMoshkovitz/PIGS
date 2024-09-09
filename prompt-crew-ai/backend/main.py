import os
import csv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
from fastapi.middleware.cors import CORSMiddleware
import logging
from langchain_openai import ChatOpenAI
from openai import OpenAIError
import asyncio
from pydantic_settings import BaseSettings
from crewai.crews.crew_output import CrewOutput
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define settings
class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    model_name: str = "gpt-3.5-turbo"

    model_config = {
        'protected_namespaces': ('settings_',)
    }

settings = Settings()

# Create FastAPI application
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the language model
try:
    llm = ChatOpenAI(openai_api_key=settings.openai_api_key, model_name=settings.model_name)
except OpenAIError as e:
    logger.error(f"Failed to initialize OpenAI client: {str(e)}")
    raise

# Define AI agents
research_agent = Agent(
    role='Industry Research Specialist',
    goal='Gather data on job costing in the cleaning/construction industry and best practices for Excel automation',
    backstory='As an expert in industry trends, you are adept at finding and compiling essential data.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

excel_design_agent = Agent(
    role='Excel Design Specialist',
    goal='Create the layout and design for the custom pricing spreadsheet',
    backstory='You have a keen eye for design and are experienced in developing functional and aesthetically pleasing spreadsheets.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

labor_cost_agent = Agent(
    role='Labor Cost Specialist',
    goal='Develop the labor cost calculator within the spreadsheet',
    backstory='As a detail-oriented professional, you excel at breaking down complex labor costs into manageable calculations.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

materials_cost_agent = Agent(
    role='Materials Cost Specialist',
    goal='Create a section for calculating materials and equipment costs',
    backstory='You are proficient in managing and calculating costs associated with materials and equipment, ensuring accuracy and detail.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

overhead_cost_agent = Agent(
    role='Overhead Cost Specialist',
    goal='Add an overhead cost calculation section to the spreadsheet',
    backstory='With extensive experience in financial management, you excel at calculating indirect costs.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

profit_margin_agent = Agent(
    role='Profit Margin Specialist',
    goal='Integrate adjustable profit margin calculations',
    backstory='You are skilled in financial optimization, ensuring the right balance between cost and profit.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

quote_generation_agent = Agent(
    role='Quote Generation Specialist',
    goal='Develop a system within the spreadsheet to generate client-ready quotes',
    backstory='You are experienced in creating professional and polished documents that leave a lasting impression.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

ui_agent = Agent(
    role='UI/UX Specialist',
    goal='Ensure the spreadsheet is user-friendly and visually appealing',
    backstory='With a focus on user experience, you make sure that all tools are intuitive and easy to use.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

testing_agent = Agent(
    role='Quality Assurance Specialist',
    goal='Test the spreadsheet for functionality and accuracy',
    backstory='You have a sharp eye for detail and ensure that everything works perfectly before delivery.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

documentation_agent = Agent(
    role='Technical Writer',
    goal='Write detailed instructions for using the spreadsheet',
    backstory='Your clear and concise writing ensures that users can easily understand and utilize complex tools.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Helper function to generate mock data
def generate_mock_data():
    return {
        "labor": {
            "num_workers": random.randint(2, 10),
            "hourly_rate": round(random.uniform(15, 30), 2),
            "estimated_hours": random.randint(4, 12)
        },
        "materials": {
            "cleaning_supplies": round(random.uniform(50, 200), 2),
            "equipment_rental": round(random.uniform(100, 500), 2)
        },
        "overhead": {
            "vehicle": round(random.uniform(50, 150), 2),
            "insurance": round(random.uniform(100, 300), 2),
            "admin_fees": round(random.uniform(50, 200), 2)
        },
        "profit_margin": round(random.uniform(0.15, 0.30), 2)
    }

# Helper function to create CSV file
def create_csv_file(mock_data, analysis):
    filename = "cleaning_job_quote_and_analysis.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Category", "Item", "Mock Data", "Agent Calculation"])
        
        # Calculate totals based on mock data
        total_labor = mock_data['labor']['num_workers'] * mock_data['labor']['hourly_rate'] * mock_data['labor']['estimated_hours']
        total_materials = mock_data['materials']['cleaning_supplies'] + mock_data['materials']['equipment_rental']
        total_overhead = mock_data['overhead']['vehicle'] + mock_data['overhead']['insurance'] + mock_data['overhead']['admin_fees']
        total_costs = total_labor + total_materials + total_overhead
        profit_amount = total_costs * mock_data['profit_margin']
        final_quote = total_costs + profit_amount

        # Write mock data and calculated results
        for category, items in mock_data.items():
            writer.writerow([category.capitalize(), "", "", ""])
            if isinstance(items, dict):
                for item, value in items.items():
                    writer.writerow(["", item.replace('_', ' ').capitalize(), value, ""])
            else:
                writer.writerow(["", "", items, ""])
        
        # Write totals
        writer.writerow([])
        writer.writerow(["Totals", "", "Mock Calculation", "Agent Calculation"])
        writer.writerow(["", "Total Labor Cost", f"${round(total_labor, 2):,.2f}", "TBD"])
        writer.writerow(["", "Total Materials Cost", f"${round(total_materials, 2):,.2f}", "TBD"])
        writer.writerow(["", "Total Overhead Cost", f"${round(total_overhead, 2):,.2f}", "TBD"])
        writer.writerow(["", "Total Costs", f"${round(total_costs, 2):,.2f}", "TBD"])
        writer.writerow(["", "Profit Amount", f"${round(profit_amount, 2):,.2f}", "TBD"])
        writer.writerow(["", "Final Quote", f"${round(final_quote, 2):,.2f}", "TBD"])

        # Write analysis
        writer.writerow([])
        writer.writerow(["Analysis", "", "", ""])
        for line in analysis.split('\n'):
            if line.strip():
                writer.writerow(["", "", line.strip(), ""])

    return filename

# Define tasks
async def create_spreadsheet():
    # Generate mock data
    mock_data = generate_mock_data()

    tasks = [
        Task(
            description="Conduct research to gather information on job costing and Excel automation relevant to the cleaning industry.",
            agent=research_agent,
            expected_output="A comprehensive report on job costing practices and Excel automation techniques for the cleaning industry."
        ),
        Task(
            description="Design a clean and user-friendly layout for the spreadsheet, incorporating placeholders for all required sections (labor, materials, overhead, profit margins).",
            agent=excel_design_agent,
            expected_output="A detailed layout design for the Excel spreadsheet with all required sections."
        ),
        Task(
            description="Create formulas to calculate labor costs based on inputs like the number of workers, hourly rates, and estimated time.",
            agent=labor_cost_agent,
            expected_output="Excel formulas for calculating labor costs with explanations."
        ),
        Task(
            description="Develop formulas for calculating the costs of consumables, rentals, and other materials.",
            agent=materials_cost_agent,
            expected_output="Excel formulas for calculating material and equipment costs with explanations."
        ),
        Task(
            description="Integrate overhead cost calculations, including vehicle, insurance, and admin fees.",
            agent=overhead_cost_agent,
            expected_output="Excel formulas and structure for calculating overhead costs with explanations."
        ),
        Task(
            description="Develop a feature that allows for adjusting profit margins based on the company's needs.",
            agent=profit_margin_agent,
            expected_output="An adjustable profit margin calculation feature with instructions."
        ),
        Task(
            description="Automate the process of generating quotes based on the input variables in the spreadsheet.",
            agent=quote_generation_agent,
            expected_output="An automated quote generation system within the Excel spreadsheet with instructions."
        ),
        Task(
            description="Polish the design, ensuring that the spreadsheet is easy to navigate and visually appealing.",
            agent=ui_agent,
            expected_output="A list of UI/UX improvements and formatting changes for the spreadsheet."
        ),
        Task(
            description="Thoroughly test the spreadsheet, checking for any errors or usability issues.",
            agent=testing_agent,
            expected_output="A comprehensive test report highlighting any issues found and suggested fixes."
        ),
        Task(
            description="Develop comprehensive documentation, explaining how to use each feature of the spreadsheet.",
            agent=documentation_agent,
            expected_output="A user manual for the Excel spreadsheet, covering all features and functionalities."
        )
    ]

    crew = Crew(
        agents=[research_agent, excel_design_agent, labor_cost_agent, materials_cost_agent, overhead_cost_agent, 
                profit_margin_agent, quote_generation_agent, ui_agent, testing_agent, documentation_agent],
        tasks=tasks,
        verbose=True,
        process=Process.sequential
    )

    try:
        result = await asyncio.to_thread(crew.kickoff)
        
        logger.debug(f"Result type: {type(result)}")
        logger.debug(f"Result content: {result}")
        
        if isinstance(result, CrewOutput):
            final_output = result.raw
        elif isinstance(result, str):
            final_output = result
        else:
            error_msg = f"Unexpected result structure. Type: {type(result)}, Content: {str(result)[:500]}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Create CSV file with mock data and analysis
        csv_file = create_csv_file(mock_data, final_output)
        
        return {"csv_file": csv_file, "analysis": final_output}
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=503, detail="OpenAI service unavailable")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Define request model
class SpreadsheetRequest(BaseModel):
    request: str

# Define API endpoint
@app.post("/create_spreadsheet")
async def create_spreadsheet_endpoint(request: SpreadsheetRequest):
    logger.info(f"Received request to create spreadsheet: {request.request}")
    
    try:
        result = await create_spreadsheet()
        
        logger.info(f"CSV file created: {result['csv_file']}")
        logger.info(f"Analysis: {result['analysis'][:100]}...")
        return {"csv_file": result['csv_file'], "analysis": result['analysis']}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)