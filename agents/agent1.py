from langchain.tools import BaseTool,StructuredTool, tool
from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq 
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
model = "llama-3.3-70b-versatile"

# Load the environment variables from the .env file
load_dotenv()
groq_api_key = os.getenv("API_KEY")
if not groq_api_key:
    raise ValueError("API_KEY environment variable not set.")
#define the model name and API key
llm = ChatGroq(groq_api_key=groq_api_key, model_name=model)

# Define the tools
@tool
def calculator_tool(input: str) -> str:
    """
    A simple calculator tool that takes an expression as input and returns the result.
    """
    try:
        result = eval(input)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def meaning_of_life(input: str) -> str:
    """
    A tool that returns the meaning of life.
    """
    return "The meaning of life is subjective and can vary from person to person."


# Initialize the tools
agent = initialize_agent(llm=llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, tools=[calculator_tool,meaning_of_life], verbose=True)

response = agent.run("What is the meaning of life?")

# issue is that agent will not be able to use multi input tools