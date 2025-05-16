from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
import os
from dotenv import load_dotenv
from typing import TypedDict, List, Annotated
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

model = "meta-llama/llama-4-scout-17b-16e-instruct"

load_dotenv()
groq_api_key = os.getenv("API_KEY")

if not groq_api_key:
    raise ValueError("API_KEY environment variable not set.")
llm = ChatGroq(groq_api_key=groq_api_key, model_name=model)

class AgentState(TypedDict):
    question: str
    draft_answer: str
    final_answer: str
    next: str
    memory: Annotated[List[str], "Previous responses"]

def generate_answer(state: AgentState):
    question = state['question']
    memory = state.get('memory', [])
    
    # Create prompt that includes previous responses to avoid
    prompt = f"{question}. Don't return any other text than the answer. Here are previous responses to avoid repeating: {', '.join(memory)}"
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    
    # Update memory with new response
    if 'memory' not in state:
        state['memory'] = []
    state['memory'].append(response.content)
    state['draft_answer'] = response.content
    return state

def human_review(state: AgentState):
    print(state['draft_answer'])
    user_input = input("\nDo you like it? (yes/no): ").strip().lower()

    if user_input == "yes":
        state["final_answer"] = state["draft_answer"]
        state["next"] = "approve"
        return state
    else:
        state["next"] = "regenerate"
        return state

# 🔹 Build the graph
workflow = StateGraph(AgentState)

# Add memory saver
memory = MemorySaver()

workflow.add_node("generate", generate_answer)
workflow.add_node("review", human_review)

workflow.set_entry_point("generate")
workflow.add_edge("generate", "review")

# 🔹 Conditional transitions from review
workflow.add_conditional_edges(
    "review",
    lambda state: state["next"],
    {
        "approve": END,
        "regenerate": "generate"
    }
)

# 🔹 Compile and run
graph = workflow.compile()

question = input("Enter your question: ")
# Initialize with empty memory
output = graph.invoke({"question": question, "memory": []})
print("\n✅ Final Answer:", output["final_answer"])
