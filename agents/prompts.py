from langchain.tools import BaseTool,StructuredTool, tool
from langchain_core.output_parsers import JsonOutputParser
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

# Lets define a prompt template
prompt = PromptTemplate(
    input_variables=["fact"],
    template = "What is the animal with {fact}"
)

response = llm.invoke(prompt.format(fact="fastest speed on land?"))

print(response.content)

# Lets create a structured output using pydantic
from pydantic import BaseModel, Field

class Animal(BaseModel):
    name : str = Field(description="The name of the animal")
    fact : str = Field(description="The fact about the animal")
    size : str = Field(description="The size of the animal")

output_parser = JsonOutputParser(pydantic_object=Animal)

prompt = PromptTemplate(template =
    """{query} {format_instructions}"""
    , input_variables = ["query"],
    partial_variables = {"format_instructions": output_parser.get_format_instructions()},
    output_parser=output_parser
)

response = llm.invoke(prompt.format(query="What is the fastest animal on land?"))
print(response.content)




