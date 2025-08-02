from typing import TypedDict, List, Union
from langchain.schema import BaseMessage
from langgraph.graph import StateGraph, END
from memory import get_memory
from vectorstore import get_retriever
from bdd_utils import get_bdd_chain

__all__ = ['build_graph']

class State(TypedDict):
    chat_history: List[BaseMessage]
    user_input: str
    context: str
    response: str

# Initialize components
memory = get_memory()
retriever = get_retriever()
bdd_chain = get_bdd_chain()



def retrieve_context(state):
    question = state["user_input"]
    context_docs = retriever.get_relevant_documents(question)
    context = "\n".join([doc.page_content for doc in context_docs])
    return {"context": context}

def generate_bdd(state):
    context = state.get("context", "")
    result = bdd_chain.run({"context": context})
    return {"response": result}

def update_memory(state):
    user_input = state["user_input"]
    response = state["response"]
    memory.save_context({"input": user_input}, {"output": response})
    return state

def build_graph():
    graph = StateGraph(State)
    graph.add_node("RetrieveContext", retrieve_context)
    graph.add_node("GenerateBDD", generate_bdd)
    graph.add_node("UpdateMemory", update_memory)

    graph.set_entry_point("RetrieveContext")
    graph.add_edge("RetrieveContext", "GenerateBDD")
    graph.add_edge("GenerateBDD", "UpdateMemory")
    graph.add_edge("UpdateMemory", END)

    return graph.compile()