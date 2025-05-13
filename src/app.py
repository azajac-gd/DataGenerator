import streamlit as st
import os
import pandas as pd
import io
from dotenv import load_dotenv
from services.ddl_service import DDLService
from services.openai_service import OpenAIService


def initialize_session():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "tables_data" not in st.session_state:
        st.session_state.tables_data = {}


def load_services():
    ddl_service = DDLService("ddl/tables.sql")
    api_key = os.getenv("OPENAI_API_KEY")
    openai_service = OpenAIService(api_key)
    return ddl_service, openai_service


def render_chat_history():
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def handle_user_input(user_input, ddl_service, openai_service):
    if not user_input:
        return

    st.session_state.chat_history.append({"role": "user", "content": user_input})

    system_prompt = openai_service.build_system_prompt(ddl_service.get_schema())
    messages = [{"role": "system", "content": system_prompt}] + st.session_state.chat_history

    with st.chat_message("assistant"):
        with st.spinner("Generating data..."):
            response = openai_service.generate_code(messages)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            process_generated_data(response)


def process_generated_data(response):
    current_table = None
    current_lines = []

    for line in response.strip().splitlines():
        if line.startswith("-- TABLE:"):
            if current_table and current_lines:
                save_table(current_table, current_lines)
            current_table = line.split(":")[1].strip() #name of the table
            current_lines = []
        elif current_table:
            current_lines.append(line.strip())

    if current_table and current_lines:
        save_table(current_table, current_lines)


def save_table(table_name, lines):
    csv_data = "\n".join(lines)
    try:
        df = pd.read_csv(io.StringIO(csv_data))
        st.session_state.tables_data[table_name] = df
    except Exception as e:
        st.error(f"Failed to parse table `{table_name}`: {e}")


def render_tables():
    if not st.session_state.tables_data:
        st.info("No data yet. Start by sending an instruction.")
        return
    for name, df in st.session_state.tables_data.items():
        st.markdown(f"### Table: `{name}`")
        st.dataframe(df, use_container_width=True, hide_index=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat Data Generator", layout="wide")

    initialize_session()
    ddl_service, openai_service = load_services()

    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.markdown("## Chat")
        render_chat_history()
        user_input = st.chat_input("Enter an instruction...")
        handle_user_input(user_input, ddl_service, openai_service)

    with right_col:
        st.markdown("## DataFrames")
        render_tables()



if __name__ == "__main__":
    main()
