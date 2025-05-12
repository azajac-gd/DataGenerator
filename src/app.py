import streamlit as st
from services.openai_service import OpenAIService
from services.ddl_service import DDLService
import os
from dotenv import load_dotenv
import io
import pandas as pd

load_dotenv()

st.set_page_config(page_title="DataFrame Generator from DDL", layout="centered")
st.title("Sample Data Generator")

ddl_service = DDLService("ddl/tables.sql")
ddl = ddl_service.get_schema()

st.markdown("### DDL Schema")
st.code(ddl, language="sql")

user_instructions = st.text_area("Additional instructions", placeholder="e.g. Generate 20 records...")

if st.button("Generate Sample Data"):
    with st.spinner("Communicating with GPT..."):
        prompt = ddl_service.create_prompt(ddl, user_instructions)

        api_key = os.getenv("OPENAI_API_KEY")
        openai_service = OpenAIService(api_key)
        generated_code = openai_service.generate_code(prompt)

        tables_data = {}
        current_table = None
        current_lines = []

        lines = generated_code.strip().splitlines()

        for line in lines:
            if line.strip().startswith("-- TABLE:"):
                if current_table and current_lines:
                    tables_data[current_table] = "\n".join(current_lines)
                current_table = line.split(":", 1)[1].strip()
                current_lines = []
            elif current_table:
                current_lines.append(line.strip())

        if current_table and current_lines:
            tables_data[current_table] = "\n".join(current_lines)

        for table_name, csv_data in tables_data.items():
            try:
                df = pd.read_csv(io.StringIO(csv_data))
                st.markdown(f"### Table: {table_name}")
                st.dataframe(df, hide_index=True)
            except Exception as e:
                st.error(f"Error reading data for table '{table_name}': {e}")
