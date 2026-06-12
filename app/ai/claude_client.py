from anthropic import Anthropic

from app.config import (
    CLAUDE_API_KEY,
    CLAUDE_MODEL,
    CLAUDE_TIMEOUT_SEC
)

client = Anthropic(
    api_key=CLAUDE_API_KEY,
    timeout=CLAUDE_TIMEOUT_SEC
)


def claude(system_prompt: str, user_prompt: str):

    try:
        resp = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=8000,
            temperature=0.2,
            system=[
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        return resp.content[0].text.strip()

    except Exception as e:
        return f'Что-то пошло не так. Получена ошибка от Claude: \n {e}'