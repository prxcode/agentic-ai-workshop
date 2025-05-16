from langchain import tools
from langchain.agents import initialize_agent, AgentType
from langchain_core.messages import SystemMessage,HumanMessage
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
model = "llama-3.3-70b-versatile"

load_dotenv()
groq_api_key = os.getenv("API_KEY")
llm = ChatGroq(api_key=groq_api_key, model=model)

response = llm.invoke("Give me a few lines about what exactly is Artificial Intelligence?")
print(response.content) 