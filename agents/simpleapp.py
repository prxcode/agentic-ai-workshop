from langchain import tools
from langchain.agents import initialize_agent, AgentType
from langchain_core.messages import SystemMessage,HumanMessage
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
model = "llama-3.3-70b-versatile"
# Load the environment variables from the .env file

load_dotenv()
groq_api_key = os.getenv("API_KEY")
llm = ChatGroq(api_key=groq_api_key, model=model)

messages = [
    SystemMessage("You are a helpful assistant in cyber security. You will answer questions and provide information about cyber security topics"),
    HumanMessage("What is a SQL injection?")
]

response = llm.invoke(messages)
#print(response.content)

prompt_template = PromptTemplate(
    input_variables=["pet_type", "pet_color"],
    template = "What are some 5 good names for a {pet_type} of color {pet_color}?")

pet_type = str(input("Enter the type of pet: "))
pet_color = str(input("Enter the color of pet: "))


prompt = prompt_template.format(pet_type=pet_type, pet_color=pet_color)

response = llm.invoke(prompt)

print(response.content)

