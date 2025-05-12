class DDLService:
    def __init__(self, ddl_path: str):
        self.ddl_path = ddl_path

    def get_schema(self) -> str:
        with open(self.ddl_path, 'r') as file:
            return file.read().strip()

    def create_prompt(self, ddl: str, user_instructions: str = "") -> str:
        prompt = f"""Generate sample data for the following DDL schema:
{ddl}
Instructions:
{user_instructions}
Return only the rows in raw CSV format.
No column headers, no explanation, no code block.
Only CSV rows with comma-separated values."""
        return prompt
