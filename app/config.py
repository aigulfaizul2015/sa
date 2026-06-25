# Библиотека для работы с переменными
import os

# чтение переменных из env
from dotenv import load_dotenv
load_dotenv()
# Создаем  переменные для вызова ИИ

# gpt
GPT_API_KEY = os.getenv("GPT_API_KEY")
GPT_BASE_URL = "https://api.openai.com/v1"
GPT_MODEL = os.getenv("GPT_MODEL")
GPT_TIMEOUT_SEC = 120

# claude
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_BASE_URL = "https://api.anthropic.com"
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL")
CLAUDE_TIMEOUT_SEC = 120

#gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


