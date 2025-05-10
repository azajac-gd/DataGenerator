class DDLService:
    def __init__(self, ddl_path: str):
        self.ddl_path = ddl_path

    def get_schema(self) -> str:
        with open(self.ddl_path, 'r') as file:
            return file.read()

    def create_prompt(self, ddl: str) -> str:
        return f"""Generate 10 rows of sample data for the following table structure:\n{ddl}\n\nReturn only the rows in raw CSV format (without headers, code, or explanations). Do not include any introductory or trailing text. Use commas to separate values."""
