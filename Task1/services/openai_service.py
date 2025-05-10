import openai

class OpenAIService:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def generate_code(self, prompt: str, model="gpt-4.1-mini") -> str:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message["content"]
