import os
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Find and load environment variables from .env file
env_path = find_dotenv()
if not env_path:
    raise ValueError(".env file not found. Please create one with your OPENAI_API_KEY")
load_dotenv(env_path)

# Get OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError(
        "OpenAI API key not found. Please set it in your .env file as OPENAI_API_KEY=your-actual-key-here"
    )

def get_bdd_chain():
    prompt = PromptTemplate.from_template("""
You are a software testing expert. Based on the following requirement or functionality, generate BDD test scenarios using Gherkin syntax.

Requirement:
{context}

Format:
Feature: ...
  Scenario: ...
    Given ...
    When ...
    Then ...
""")
    llm = ChatOpenAI(model="gpt-4", temperature=0.3, openai_api_key=api_key)
    return LLMChain(prompt=prompt, llm=llm)