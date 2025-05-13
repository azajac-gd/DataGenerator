class DDLService:
    def __init__(self, ddl_path: str):
        self.ddl_path = ddl_path

    def get_schema(self) -> str:
        with open(self.ddl_path, "r") as file:
            return file.read()
