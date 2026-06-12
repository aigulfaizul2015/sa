PROJECT_CACHE = {}

def save_result(
    task_name,
    request,
    response,
    svg=None
):

    if task_name not in PROJECT_CACHE:

        PROJECT_CACHE[task_name] = []

    PROJECT_CACHE[task_name].append({
        "request": request,
        "response": response,
        "svg": svg
    })


def get_history(
    task_name
):

    return PROJECT_CACHE.get(
        task_name,
        [] # если раздела нет, вернуть пустой массив
    )