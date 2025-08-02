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
You are a test automation architect and software quality expert with deep knowledge of the software testing life cycle, including unit, integration, system, acceptance, security, API, UI, performance, and edge-case testing. Your task is to generate highly detailed and exhaustive BDD test scenarios using Gherkin syntax for automation using Cucumber.

Use the following requirement or functionality as your context and generate test scenarios for **every major phase of testing** (functional, integration, UI, API, security, performance, boundary, and negative cases). Ensure test coverage for:

- Functional flow (happy path)
- Field validations
- Edge cases
- Negative tests
- API interaction (if applicable)
- UI behavior (if applicable)
- Integration with other modules/services
- Data handling and persistence
- Security validations (auth, access control, etc.)
- Performance expectations (if mentioned or inferred)
- Role-based access control (if applicable)
- State transitions (before and after behavior)
- Error handling and fallback behavior

Use **clear**, **realistic**, and **actionable steps** in your Given-When-Then. Organize output by test category.

Context:
{context}

Format:

Feature: [High-level description of the functionality]
  Background:
    Given [any common precondition or setup]

  # Functional - Happy Path
  Scenario: [Name]
    Given ...
    When ...
    Then ...

  # Negative Scenario
  Scenario: [Name]
    Given ...
    When ...
    Then ...

  # Validation Rules
  Scenario Outline: [Field level or data validation]
    Given ...
    When ...
    Then ...

    Examples:
      | field       | input     | errorMessage                   |
      | email       | abc       | "Invalid email address"        |
      | password    | 123       | "Password too short"           |

  # API Integration (if applicable)
  Scenario: [Name]
    Given ...
    When ...
    Then ...

  # UI Behavior (if applicable)
  Scenario: [Name]
    Given ...
    When ...
    Then ...

  # Security Scenario
  Scenario: [Name]
    Given ...
    When ...
    Then ...

  # Performance (if applicable)
  Scenario: [Name]
    Given ...
    When ...
    Then ...

""")
    llm = ChatOpenAI(model="gpt-4", temperature=0.5, openai_api_key=api_key)
    return LLMChain(prompt=prompt, llm=llm)