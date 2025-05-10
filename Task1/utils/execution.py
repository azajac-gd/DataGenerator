import pandas as pd

def exec_generated_code(code: str) -> pd.DataFrame:
    local_vars = {}
    exec(code, {}, local_vars)
    for var in local_vars.values():
        if isinstance(var, pd.DataFrame):
            return var
    raise ValueError("No DataFrame found in generated code.")
