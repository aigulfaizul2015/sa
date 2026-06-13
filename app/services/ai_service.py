import os

from app.ai.openai_client import gpt
from app.ai.claude_client import claude
from app.services.prompt_loader import (
    load_prompt,
    load_review_check_prompt
)
def llm(
        system_prompt: str,
        user_prompt: str,
        provider: str = "openai"
):

    if provider == "claude":
        return claude(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

    return gpt(
        system_prompt=system_prompt,
        user_prompt=user_prompt
    )

def generate(
        task: str,
        context: str,
        provider: str = "openai"
):
    system_prompt = load_prompt(task)
    response = llm(
        system_prompt=system_prompt,
        user_prompt=context,
        provider=provider
    )

    return response


def generate_review(
        review_type: str,
        task: str,
        context: str,
        provider: str = "openai"
):
    system_prompt = load_review_check_prompt(review_type, task)
    response = llm(
        system_prompt=system_prompt,
        user_prompt=context,
        provider=provider
    )
    return response


