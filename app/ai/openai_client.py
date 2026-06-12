from openai import OpenAI


# импорт переменных из config
from app.config import (
    GPT_API_KEY,
    GPT_BASE_URL,
    GPT_MODEL,
    GPT_TIMEOUT_SEC
)

client = OpenAI(
    api_key=GPT_API_KEY,
    base_url=GPT_BASE_URL,
    timeout=GPT_TIMEOUT_SEC
)

def gpt(system_prompt: str, user_prompt: str):


    try:
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
        resp = client.chat.completions.create(
            model = GPT_MODEL,
            messages=messages,
            temperature=0.2
        )

        print(resp)
        return resp.choices[0].message.content.strip()

    except Exception as e:
        return f'Что-то пошло не так. Получена ошибка от LLM: \n {e}'