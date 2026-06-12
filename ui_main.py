from nicegui import ui

from app.services.task_registry import TASKS
from app.ui.task_page import show_task

ui.add_css('''
.task-result-header {
    min-height: 3.5rem;
    flex-shrink: 0;
}
.task-result-panel {
    height: 40rem;
    min-height: 40rem;
    max-height: 45rem;
    overflow-y: auto;
    border: 1px solid rgba(0, 0, 0, 0.12);
    border-radius: 4px;
    padding: 0.5rem 0.75rem;
    box-sizing: border-box;
}
.task-result-markdown h1 { font-size: 1.25rem; line-height: 1.35; margin: 0.5rem 0; }
.task-result-markdown h2 { font-size: 1.125rem; line-height: 1.35; margin: 0.5rem 0; }
.task-result-markdown h3 { font-size: 1rem; line-height: 1.35; margin: 0.5rem 0; }
.task-result-markdown h4,
.task-result-markdown h5,
.task-result-markdown h6 { font-size: 0.9375rem; line-height: 1.35; margin: 0.5rem 0; }
''')
with ui.row().classes('w-full h-screen items-start no-wrap'):

    with ui.column().classes(
        'w-64 h-screen p-4 border-r no-wrap'
    ).style(
        'overflow-y: auto; flex-shrink: 0;'
    ):

        for group_name, tasks in TASKS.items():

            ui.label(
                group_name
            ).classes(
                'text-h6 mt-4'
            )

            for task_name, task in tasks.items():

                ui.button(
                    task["title"],
                    on_click=lambda t=task_name:
                    show_task(
                        t,
                        content
                    )
                ).props('flat')

    content = ui.column().classes(
        'flex-grow h-screen p-6 items-stretch'
    ).style(
        'overflow-y: auto; min-height: 0;'
    )

show_task(
    "context",
    content
)

ui.run()
