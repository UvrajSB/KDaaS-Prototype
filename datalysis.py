import os
import langgraph
import ollama
import streamlit as st
import subprocess
import re
import pandas as pd
import logging
import warnings

# Suppress warnings
warnings.simplefilter("ignore")

# Set up logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def extract_code(response):
    """Extract Python code block from LLM response."""
    match = re.search(r"```python\n(.*?)\n```", response, re.DOTALL)
    if match:
        logging.info("Extracted Python code successfully.")
        return match.group(1)
    else:
        logging.warning("No code block found in response.")
        return response

def get_dataset_info():
    """Retrieve dataset information for better query understanding."""
    try:
        df = pd.read_csv("uploaded_file.csv")
        info = {
            "columns": df.columns.tolist(),
            "num_rows": len(df),
            "num_columns": len(df.columns),
            "sample_data": df.head(3).to_dict()
        }
        logging.info(f"Dataset info retrieved: {info}")
        return str(info)
    except Exception as e:
        logging.error(f"Error reading dataset: {e}")
        return "Error reading dataset: " + str(e)

def generate_code(prompt, chat_history):
    """Generate Python code using deepseek-coder model served by Ollama with chat context."""
    dataset_info = get_dataset_info()
    system_prompt = f"""
    You are an AI assistant that generates Python code for data analysis using pandas.
    Before generating the code, here is some information about the dataset:
    {dataset_info}
    Maintain the context of previous queries and responses to provide better results.
    Based on this, generate a complete Python script that loads 'uploaded_file.csv' and performs the requested analysis 
    """
    messages = [{"role": "system", "content": system_prompt}] + chat_history + [{"role": "user", "content": prompt}]
    
    try:
        response = ollama.chat(model='qwen2.5-coder:3b', messages=messages)
        logging.info("Code generated successfully.")
        return extract_code(response['message']['content'])
    except Exception as e:
        logging.error(f"Error generating code: {e}")
        return f"Error generating code: {e}"

def execute_code(code):
    """Execute the generated code and capture output."""
    try:
        with open("generated_script.py", "w") as f:
            f.write(code)
        logging.info("Code written to generated_script.py.")

        output = subprocess.run(["python", "generated_script.py"], capture_output=True, text=True)
        
        # Only log errors, do not show them in UI
        if output.stderr:
            logging.error(f"Execution Error: {output.stderr}")
        
        return output.stdout.strip()  # Only show meaningful stdout, not warnings/errors
    except Exception as e:
        logging.error(f"Error executing code: {e}")
        return "Execution error. Check logs for details."

def clear_old_plot():
    """Remove old plot file if it exists."""
    if os.path.exists("output_plot.png"):
        os.remove("output_plot.png")
        logging.info("Previous plot deleted.")

# Streamlit UI
st.set_page_config(page_title="On-Prem Data Analysis", layout="wide")
st.sidebar.image("white_logo.png", width=200)
st.sidebar.title("Options")

if "sessions" not in st.session_state:
    st.session_state.sessions = {}
    st.session_state.current_session = "Session 1"
    st.session_state.chat_history = []

def switch_session(session_name):
    st.session_state.current_session = session_name
    st.session_state.chat_history = st.session_state.sessions.get(session_name, [])

session_name = st.sidebar.text_input("New session name")
if st.sidebar.button("Create New Session") and session_name:
    st.session_state.sessions[session_name] = []
    switch_session(session_name)

st.sidebar.subheader("Existing Sessions")
for s in st.session_state.sessions.keys():
    if st.sidebar.button(s):
        switch_session(s)

st.sidebar.subheader("Chat History")
for entry in st.session_state.chat_history:
    if entry["role"] == "user":
        st.sidebar.text(entry["content"])  # Show only user prompt

st.markdown("<h1 style='text-align: center;'>On Device Data Analysis</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
prompt = st.text_area("Enter your data analysis prompt:")

if uploaded_file:
    with open("uploaded_file.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded successfully!")
    logging.info("CSV file uploaded successfully.")

if st.button("Ask  →"):
    if uploaded_file and prompt:
        clear_old_plot()
        #prompt = "Generate python code for " + prompt
        logging.info(f"User Prompt: {prompt}")
        prompt = "Generate Python code for" + prompt
        code = generate_code(prompt, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append({"role": "assistant", "content": code})
        st.session_state.sessions[st.session_state.current_session] = st.session_state.chat_history
        logging.info("Chat history updated.")

        with st.expander("View Generated Code"):
            st.code(code, language="python")

        result = execute_code(code)
        st.text_area("Execution Output:", result, height=200)
        st.session_state.chat_history.append({"role": "assistant", "content": result})

        if os.path.exists("output_plot.png"):
            st.image("output_plot.png", caption="Generated Visualization", use_column_width=True)
            logging.info("Generated plot displayed successfully.")
    else:
        st.warning("Please upload a CSV file and enter a prompt.")
