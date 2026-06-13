from nicegui import app
# Библиотека для работы с переменными
import os

MAX_HISTORY_ITEMS = int(os.getenv("MAX_HISTORY_ITEMS", "5"))


def get_project_cache():

    project_cache = app.storage.user.get(
        'project_cache'
    )

    if project_cache is None:
        project_cache = {}
        app.storage.user['project_cache'] = project_cache

    return project_cache


def save_result(
    task_name,
    request,
    response,
    svg=None
):

    project_cache = get_project_cache()

    if task_name not in project_cache:
        project_cache[task_name] = []

    project_cache[task_name].append({
        "request": request,
        "response": response,
        "svg": svg
    })
    project_cache[task_name] = project_cache[task_name][-MAX_HISTORY_ITEMS:]


def get_history(
    task_name
):

    project_cache = get_project_cache()

    return project_cache.get(
        task_name,
        []
    )


def delete_history_item(
    task_name,
    item
):

    project_cache = get_project_cache()

    history = project_cache.get(
        task_name,
        []
    )

    if item in history:
        history.remove(item)


def get_drafts():

    drafts = app.storage.user.get(
        'drafts'
    )

    if drafts is None:
        drafts = {}
        app.storage.user['drafts'] = drafts

    return drafts


def save_draft(task_name, values):

    drafts = get_drafts()
    drafts[task_name] = values


def get_draft(task_name):

    drafts = get_drafts()

    return drafts.get(
        task_name,
        {}
    )