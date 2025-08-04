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
You are a test automation architect and software quality expert with deep knowledge of the software testing life cycle. Your task is to generate BDD test scenarios using Gherkin syntax for automation using Cucumber.

Parse the context carefully. If the user specifies a number of scenarios to generate for any category (e.g., "generate 5 API scenarios" or "create 10 security tests"), you MUST generate exactly that number of scenarios for that category.

Available test categories:
- Functional (Happy Path)
- Negative Tests
- Field Validations
- Edge Cases
- API Integration
- UI Behavior
- Security Tests
- Performance Tests
- Integration Tests
- Data Handling
- Error Handling
- State Transitions
- Role-based Access

For each scenario, ensure:
- Clear, realistic, and actionable Given-When-Then steps
- Detailed preconditions in Given
- Specific actions in When
- Verifiable outcomes in Then
- Relevant examples for Scenario Outlines

Context:
{context}

Format your response as:

Feature: [High-level description of the functionality]
  Background: (if needed)
    Given [common preconditions]

  [Category Name]
  Scenario: [Descriptive Name]
    Given [precondition]
    When [action]
    Then [verifiable outcome]
    And [additional outcomes if needed]

  Scenario Outline: [For data-driven tests]
    Given [precondition with <variable>]
    When [action with <variable>]
    Then [outcome with <variable>]

    Examples:
      | variable | value | expected_result |
      | value1   | data1 | result1         |
      | value2   | data2 | result2         |

Remember:
1. Generate EXACTLY the number of scenarios requested for each category
2. Make each scenario unique and meaningful
3. Use clear, specific steps that can be automated
4. Include relevant test data and examples
""")
    llm = ChatOpenAI(model="gpt-4", temperature=0.5, openai_api_key=api_key)
    return LLMChain(prompt=prompt, llm=llm)