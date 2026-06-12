from app.services.field_registry import FIELDS


def build_context(values: dict):

    parts = []

    for field_name, value in values.items():

        if not value:
            continue

        label = FIELDS[field_name]["label"]

        parts.append(
            f"{label}:\n{value}"
        )

    return "\n\n".join(parts)


def build_review_context(
    values: dict,
    response: str,
    task_name: str
):
    parts = []
    for field_name, value in values.items():
        if not value:
            continue
        label = FIELDS[field_name]["label"]
        parts.append(
            f"{label}:\n{value}"
        )
    parts.append(
        f"{task_name}:\n{response}"
    )
    return "\n\n".join(parts)