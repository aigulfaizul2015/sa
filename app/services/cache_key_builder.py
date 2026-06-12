import hashlib
import json
import re


def normalize_text(value: str):

    value = value.lower()

    value = re.sub(
        r'\s+',
        ' ',
        value
    )

    return value.strip()


def normalize_request(data: dict):

    return {
        key: normalize_text(value)
        if isinstance(value, str)
        else value
        for key, value in data.items()
    }


def build_cache_key(
        task_name: str,
        provider: str,
        request_data: dict
):

    cache_data = {
        "task": task_name,
        "provider": provider,
        "request": normalize_request(request_data)
    }

    return hashlib.sha256(
        json.dumps(
            cache_data,
            sort_keys=True,
            ensure_ascii=False
        ).encode()
    ).hexdigest()