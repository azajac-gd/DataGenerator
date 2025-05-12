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

ddl_service = DDLService("ddl/users.sql")
ddl = ddl_service.get_schema()

st.markdown("### DDL Schema")
st.code(ddl, language="sql")

user_instructions = st.text_area("Additional instructions", placeholder="e.g. Generate 20 records...")

if st.button("Generate Sample Data"):
    with st.spinner("Communicating with GPT..."):
        prompt = ddl_service.create_prompt(ddl, user_instructions)
        
        api_key=os.getenv("OPENAI_API_KEY")
        openai_service = OpenAIService(api_key)
        generated_code = openai_service.generate_code(prompt)

        try:
            df = pd.read_csv(io.StringIO(generated_code), header=0)
            st.markdown("### Data Preview")
            st.dataframe(df, hide_index=True)
        except Exception as e:
            st.error(f"Execution error: {e}")
