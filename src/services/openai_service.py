from openai import OpenAI

class OpenAIService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate_code(self, messages: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0.2
        )
        return response.choices[0].message.content
    
    def build_system_prompt(self, ddl: str) -> str:
            return f"""
    You are a dataframe generator. Given the following SQL schema, generate realistic and consistent CSV data for each table.
    Schema:
    {ddl}

    Output format for each table:
    -- TABLE: table_name
    column1,column2,column3
    value1,value2,value3
    value4,value5,value6

    Rules:
    - Use realistic and logically consistent values (e.g. matching foreign keys, valid emails, etc).
    - Don't add any extra text or explanations — only the CSV data formatted as described above.
    - Output all tables defined in the schema.
    - If a table is already defined, do not change its structure or data.
    - Never change data in tables that are already defined unless explicitly instructed to do so.

    Example:
    -- TABLE: products
    product_id,product_name,price
    1,Widget A,19.99
    2,Widget B,30.00

    Remember to follow data types and constraints defined in the schema. Do not change decimal values to integers or vice versa.
    """