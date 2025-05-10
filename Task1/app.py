import streamlit as st
from services.openai_service import OpenAIService
from services.ddl_service import DDLService
from utils.execution import exec_generated_code
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="DataFrame Generator from DDL", layout="centered")
st.title("Sample Data Generator")

ddl_service = DDLService("ddl/users.sql")
ddl = ddl_service.get_schema()

st.markdown("### DDL Schema")
st.code(ddl, language="sql")

if st.button("Generate Sample Data"):
    with st.spinner("Communicating with GPT..."):
        prompt = ddl_service.create_prompt(ddl)
        
        api_key=os.getenv("OPENAI_API_KEY")
        openai_service = OpenAIService(api_key)
        generated_code = openai_service.generate_code(prompt)

        st.markdown("### 🧠 GPT-Generated Code")
        st.code(generated_code, language='python')

        try:
            df = exec_generated_code(generated_code)
            st.markdown("### Data Preview")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Execution error: {e}")
