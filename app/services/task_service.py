from app.services.task_registry import TASKS


def get_task(task_name: str):

    for group in TASKS.values():

        if task_name in group:
            return group[task_name]

    raise ValueError(
        f"Задача {task_name} не найдена"
    )