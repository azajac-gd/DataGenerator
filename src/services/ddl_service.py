class DDLService:
    def __init__(self, ddl_path: str):
        self.ddl_path = ddl_path

    def get_schema(self) -> str:
        with open(self.ddl_path, 'r') as file:
            return file.read().strip()

    def create_prompt(self, ddl: str, user_instructions: str = "") -> str:
        base_prompt = f"""
    You are a data generation AI. Given the following SQL DDL schema, generate sample data for ALL tables, maintaining consistency across foreign keys.

    Schema:
    {ddl}

    Instructions:
    - Return only the data rows with headers in raw CSV format per table, separated clearly, e.g.:
    -- TABLE: users
    id,name,email,country
    1,John,john@example.com,USA
    2,Jane,jane@example.com,Canada

    -- TABLE: orders
    id,user_id,order_date
    1,1,2024-01-01
    2,2,2024-02-01

    - Do not include explanations or any additional text.
    """

        if user_instructions.strip():
            base_prompt += f"\nAdditional user instructions:\n{user_instructions.strip()}\n"

        return base_prompt.strip()

