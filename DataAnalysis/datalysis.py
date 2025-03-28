import os
import langgraph
import ollama
import streamlit as st
import subprocess
import re
import pandas as pd

def extract_code(response):
    """Extract Python code block from LLM response."""
    match = re.search(r"```python\n(.*?)\n```", response, re.DOTALL)
    return match.group(1) if match else response

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
        return str(info)
    except Exception as e:
        return "Error reading dataset: " + str(e)

def generate_code(prompt):
    """Generate Python code using Qwen2.5-coder:0.5b model served by Ollama."""
    dataset_info = get_dataset_info()
    system_prompt = f"""
    You are an AI assistant that generates Python code for data analysis and visualization using pandas and matplotlib/seaborn.
    Before generating the code, here is some information about the dataset:
    {dataset_info}
    Based on this, generate a complete Python script that loads 'uploaded_file.csv' and performs the requested analysis or visualization (graphs, charts, etc.).
    Ensure the script saves any generated plots as 'output_plot.png' if visualization is required.
    """
    response = ollama.chat(model='qwen2.5-coder:7b', messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ])
    return extract_code(response['message']['content'])

def execute_code(code):
    """Execute the generated code and capture output"""
    with open("generated_script.py", "w") as f:
        f.write(code)
    
    try:
        output = subprocess.run(["python", "generated_script.py"], capture_output=True, text=True)
        return output.stdout if output.stdout else output.stderr
    except Exception as e:
        return str(e)

def clear_old_plot():
    """Remove old plot file if it exists."""
    if os.path.exists("output_plot.png"):
        os.remove("output_plot.png")

# Streamlit UI
st.title("AI-Powered Data Analysis & Visualization with Qwen2.5")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
prompt = st.text_area("Enter your data analysis prompt (including visualizations like charts/graphs if needed):")

if uploaded_file:
    with open("uploaded_file.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded successfully!")

if st.button("Generate & Run Code"):
    if uploaded_file and prompt:
        clear_old_plot()
        code = generate_code(prompt)
        st.code(code, language="python")
        
        result = execute_code(code)
        st.text_area("Execution Output:", result, height=200)
        
        if os.path.exists("output_plot.png"):
            st.image("output_plot.png", caption="Generated Visualization", use_column_width=True)
    else:
        st.warning("Please upload a CSV file and enter a prompt.")
