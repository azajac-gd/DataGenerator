class DDLService:
    def __init__(self, ddl_path: str):
        self.ddl_path = ddl_path

    def get_schema(self) -> str:
        with open(self.ddl_path, 'r') as file:
            return file.read()

    def create_prompt(self, ddl: str) -> str:
        return f"""Given the following DDL schema:\n{ddl}\n\nGenerate a sample dataset with 10 rows as a pandas DataFrame (Python code only)."""
