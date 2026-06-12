# получение PROMPTS
from app.services.prompt_registry import PROMPTS

# получение файла, чтение и возврат текста
from pathlib import Path

PROMPTS_DIR = Path("app/prompts")


def load_prompt(task: str):

    file_name = PROMPTS[task]

    prompt_path = PROMPTS_DIR / file_name

    print("load_prompt")

    return prompt_path.read_text(encoding="utf-8")

def load_review_check_prompt(
    review_type: str,
    task: str
):

    file_name = PROMPTS[review_type][task]

    prompt_path = PROMPTS_DIR / file_name

    return prompt_path.read_text(encoding="utf-8")