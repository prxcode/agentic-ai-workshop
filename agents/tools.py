from langchain.tools import BaseTool,StructuredTool, tool
from langchain_core.output_parsers import JsonOutputParser
from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq 
import os
import requests
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool
from langchain.agents import tool
from bs4 import BeautifulSoup


model = "llama-3.3-70b-versatile"
# Load the environment variables from the .env file
load_dotenv()

groq_api_key = os.getenv("API_KEY")

if not groq_api_key:
    raise ValueError("API_KEY environment variable not set.")

#define the model name and API key
llm = ChatGroq(groq_api_key=groq_api_key, model_name=model)

def meaning_of_life(input: str) -> str:
    return '42'

life_tool = Tool(
    name = "meaning_of_life",
    description= "Useful for when you want to know the meaning of life",
    func=meaning_of_life
)

@tool
def calculate(input: str) -> str:
    """Useful for when you have to Calculate the result of the mathematical expression."""
    return str(eval(input))

search = DuckDuckGoSearchRun()

@tool
def search_tool(query: str) -> str:
    """Useful for when you want to search the web."""
    return search.run(query)

class JokeTool(BaseTool):
    name : str= "joke_tool"
    description : str = "Useful for when you want to tell a joke"

    def _run(self, input: str) -> str:
        response = requests.get(f"https://official-joke-api.appspot.com/random_joke")
        return response.json()

    async def _arun(self, input: str) -> str:
        raise NotImplementedError("JokeTool does not support async yet.")

joke_tool = JokeTool()

class WebpageTool(BaseTool):
        name: str = "webpage"
        description: str = "useful when you are asked a question about a webpage. Pass in the url of the webpage"

        def _run(self, url: str) -> str:
            response = requests.get(url)
            html_content =  response.text

            def strip_html_tags(html_content):
                soup = BeautifulSoup(html_content, 'html.parser')
                return soup.get_text()
            return strip_html_tags(html_content)
        
        def _arun(self, webpage: str):
            raise NotImplementedError("This tool does not support async")

webtool = WebpageTool()

tools = [life_tool, calculate, search_tool, joke_tool, webtool]

agent = initialize_agent(
    tools,
    llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

response = agent.run("")
print(response)