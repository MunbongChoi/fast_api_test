import openai
from src.config import settings

openai.api_key = settings.OPENAI_API_KEY

def get_gpt_response(prompt: str):
    # OpenAI API를 사용한 GPT 응답
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()
