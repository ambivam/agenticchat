import os
from dotenv import load_dotenv, find_dotenv
from langchain.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

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

# Initialize embeddings once
embeddings = OpenAIEmbeddings(openai_api_key=api_key)

# Set up Chroma directory
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
os.makedirs(DB_DIR, exist_ok=True)

def ingest_txt_file(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    try:
        loader = TextLoader(file_path, encoding='utf-8')
        docs = loader.load()
        
        if not docs:
            raise ValueError(f"No content loaded from file: {file_path}")
            
        vectordb = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=DB_DIR
        )
        vectordb.persist()
    except Exception as e:
        raise Exception(f"Error processing file {file_path}: {str(e)}")
    return vectordb

def get_retriever():
    return Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings
    ).as_retriever()