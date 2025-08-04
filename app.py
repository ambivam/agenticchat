import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv

# Debug: Find .env file
env_path = find_dotenv()
st.sidebar.write(f"Found .env at: {env_path if env_path else 'Not found'}")

# Check if .env file exists
if env_path:
    st.sidebar.success(".env file found and loaded")
else:
    st.sidebar.error(".env file not found")

# Load environment variables
load_dotenv(env_path)

# Check environment variable
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    masked_key = f"sk-...{api_key[-4:]}"
    st.sidebar.success(f"API Key loaded: {masked_key}")
else:
    st.sidebar.error("API Key not found")

from vectorstore import ingest_txt_file
from graph import build_graph
import tempfile

st.set_page_config(page_title="BDD Bot 💡", layout="wide")
st.title("📘 BDD Generator Chatbot (LangGraph + GPT-4)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "graph_app" not in st.session_state:
    st.session_state.graph_app = build_graph()

# Upload section
st.sidebar.header("📁 Upload Requirement File (.txt)")
uploaded_file = st.sidebar.file_uploader("Upload your .txt file", type=["txt"])

# Clear button in sidebar
st.sidebar.header("🔄 Reset Chat")
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.success("Chat history cleared!")
    st.rerun()

# Create a directory for temporary files if it doesn't exist
temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_uploads")
os.makedirs(temp_dir, exist_ok=True)

# Debug info
st.sidebar.text(f"Temp dir: {temp_dir}")
if uploaded_file is not None:
    # Save uploaded file with a fixed path
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getvalue())

    # Process the file
    try:
        ingest_txt_file(file_path)
        st.success("✅ File processed successfully!")
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
    finally:
        # Clean up
        try:
            os.remove(file_path)
        except:
            pass

# Chat UI
query = st.text_input("🧠 Ask something related to your requirement file...")

if query:
    st.session_state.chat_history.append(("User", query))
    result = st.session_state.graph_app.invoke({"user_input": query})
    answer = result["response"]
    st.session_state.chat_history.append(("BDD Bot", answer))

# Display chat
for role, message in st.session_state.chat_history:
    if role == "User":
        st.chat_message("user").write(message)
    else:
        st.chat_message("assistant").write(message)