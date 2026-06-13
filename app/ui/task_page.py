import os
# UI для отображения задачи, формы и результата
from nicegui import ui
# из-за проблем с блокировкой кнопки Сгенерировать, переход на асинхронную функцию
from nicegui import run

from app.services.task_registry import TASKS
from app.ui.form_builder import render_form
from app.services.context_builder import (
    build_context,
    build_review_context
)
from app.services.ai_service import (
    generate,
    generate_review
)
from app.services.task_service import get_task
from app.services.project_cache import (
    save_result,
    get_history,
    delete_history_item,
    save_draft,
    get_draft
)
from app.services.bitcit_service import (
    generate_plantuml_diagram,
    generate_mermaid_diagram
)
from app.services.cache_key_builder import build_cache_key

def show_task(
        task_name: str,
        content
        ):
    result = None
    content.clear()

    with content:

        task = get_task(task_name)

        # если задан тип, то используем его, иначе - текст
        result_type = task.get(
            "result_type",
            "text"
        )
        # для отображаения markdown результата
        def put_result(text):
            text = text or ''
            if result_type in ("plantuml", "mermaid"):
                result.value = text
            else:
                result.content = text.replace('\n', '  \n')

        def get_result():
            return result.value if result_type in ("plantuml", "mermaid") else (result.content or '')

    # Экран разделение
        ui.label(
            task["title"]
        ).classes(
            'text-h5 text-weight-bold'
        )
        with ui.row().classes('w-full no-wrap items-start'):
            # Левая колонка
            with ui.column().style(
                'width: 30%'
            ):

                ui.label(
                    'Входные данные'
                ).classes(
                    'text-h6'
                )

                form_fields = render_form(task)
                # Заполнение формы из черновика
                draft = get_draft(task_name)
                for field_name, value in draft.items():
                    if field_name in form_fields:
                        form_fields[field_name].value = value
                def save_current_draft():
                    values = {}
                    for field_name, field in form_fields.items():
                        values[field_name] = field.value
                    save_draft(
                        task_name,
                        values
                    )
                for field in form_fields.values():
                    field.on(
                        'blur',
                        lambda e: save_current_draft()
                    )
                
                check_button = None
                quality_result = None
                acceptance_button = None
                acceptance_result = None

                async def generate_result(): 
                    # проверка на превышение симловов
                    for field in form_fields.values():
                        if not field.validate():
                            ui.notify(
                                'Заполните обязательные поля и исправьте ошибки',
                                type='negative'
                            )
                            return
                    # сохранение отправленных полей для отображения в истории
                    values = {}
                    for field_name, field in form_fields.items():
                        values[field_name] = field.value

                    provider = provider_select.value

                    cache_key = build_cache_key(
                        task_name,
                        provider,
                        values
                    )

                    history_values = values.copy()
                    history_values["provider"] = provider
                    history_values["cache_key"] = cache_key
                        
                    generate_button.disable()
                    generate_button.set_text(
                        'Генерация...'
                    )
                    # очистка результата
                    put_result('')
                    # кэш
                    history = get_history(task_name)
                    cached_item = next(
                        (
                            item
                            for item in reversed(history)
                            if item.get("request", {}).get("cache_key") == cache_key
                        ),
                        None
                    )
                    if cached_item:
                        put_result(cached_item["response"])
                        if diagram and cached_item.get("svg"):
                            diagram.set_content(cached_item["svg"])
                            result.visible = False
                            diagram.visible = True
                        generate_button.set_text('Сгенерировать')
                        generate_button.enable()
                        ui.notify(
                            'Ответ получен из кэша',
                            type='positive'
                        )
                        return
                    
                    context = build_context(values)

                    response = await run.io_bound( # асихронная обработка, из-за проблем с блокировкой кнопки Сгенерировать
                        generate,
                        task=task_name,
                        context=context,
                        provider=provider
                    )

                    svg = None
                    result_type = task.get("result_type")

                    if result_type == "plantuml":
                        generator = generate_plantuml_diagram
                    elif result_type == "mermaid":
                        generator = generate_mermaid_diagram
                    else:
                        generator = None

                    if generator:
                        diagram_data = generator(response)
                        svg = diagram_data.get("svgData")

                    # сохранение кэша
                    save_result(
                        task_name,
                        history_values,
                        response,
                        svg
                    )     
                    # полное обновление страницы, чтобы отобразить историю с новой генерацией
                    show_task(
                        task_name,
                        content
                    )
                with ui.row().classes(
                    'items-end gap-4'
                ):
                    provider_select = ui.select(
                        options={
                            "openai": "GPT",
                            "claude": "Claude"
                        },
                        value="openai",
                        label="Провайдер"
                    ).classes(
                        'w-40'
                    )
                    generate_button = ui.button(
                        'Сгенерировать',
                        on_click=generate_result
                    )

            # Правая колонка
            
            with ui.column().style(
                'width: 70%; align-self: flex-start;'
            ):
            
                # Заголовок результата
                with ui.row().classes(
                    'w-full items-center'
                ):
                    ui.label(
                        'Результат'
                    ).classes(
                        'text-h6'
                    )
                    ui.space()
                    # История
                    history = get_history(task_name)

                    history_options = []
                    history_map = {}
                    selected_item = None
                    for index, item in enumerate(history):
                        name = f'Запрос {index + 1}'
                        history_options.append(name)
                        history_map[name] = item

                    def history_changed(event):
                        nonlocal selected_item
                        selected_item = history_map[event.value]

                        request = selected_item["request"]
                        provider_select.value = request.get("provider", provider_select.value)
                        for field_name, value in request.items():
                            if field_name in form_fields:
                                form_fields[field_name].value = value
                        put_result(selected_item["response"])
                        if diagram and selected_item.get("svg"):
                            svg = selected_item["svg"]

                            diagram.set_content(svg)
                            result.visible = False
                            diagram.visible = True
                        if quality_result:
                            cached_quality = selected_item.get("quality_response")
                            quality_md.content = cached_quality or ''
                            quality_result.visible = bool(cached_quality)

                        if acceptance_result:
                            cached_acceptance = selected_item.get("acceptance_response")
                            acceptance_md.content = cached_acceptance or ''
                            acceptance_result.visible = bool(cached_acceptance)

                    if history_options:
                        MAX_HISTORY_ITEMS = int(os.getenv("MAX_HISTORY_ITEMS", "5"))
                        history_select = ui.select(
                            options=history_options,
                            label=f'История (сохраняется макс. {MAX_HISTORY_ITEMS})',
                            on_change=history_changed
                        ).classes('w-64')

                        def delete_selected_history():
                            if selected_item:
                                delete_history_item(
                                    task_name,
                                    selected_item
                                )
                                ui.notify(
                                    'Запрос удалён',
                                    type='positive'
                                )
                                show_task(
                                    task_name,
                                    content
                                )

                        ui.button(
                            icon='delete',
                            on_click=delete_selected_history
                        ).props(
                            'flat round'
                        )
                
                diagram = None

                if result_type in ("plantuml", "mermaid"):
                    def change_view(e):
                        show_code = e.value == "Код"
                        result.visible = show_code
                        diagram.visible = not show_code

                    ui.radio(
                        ["Код", "Диаграмма"],
                        value="Диаграмма",
                        on_change=change_view
                    ).props('inline')

                    result = ui.textarea(
                        label=''
                    ).classes(
                        'w-full'
                    ).props(
                        'rows=45'
                    )

                    diagram = ui.html('').classes(
                        'w-full task-result-panel'
                    ).style(
                        'overflow: auto;'
                    )

                    diagram.visible = False
                else:
                    with ui.element('div').classes(
                        'w-full task-result-panel'
                    ):
                        result = ui.markdown('').classes(
                            'w-full nicegui-markdown task-result-markdown'
                        )

                if history_options:
                    history_select.value = history_options[-1] # по умолчанию - последний запрос

                    selected_item = history_map[history_options[-1]]

                    request = selected_item["request"]

                    provider_select.value = request.get("provider", provider_select.value)

                    for field_name, value in request.items():
                        if field_name in form_fields:
                            form_fields[field_name].value = value

                    put_result(selected_item["response"])

                    if diagram and selected_item.get("svg"):
                            svg = selected_item["svg"]

                            diagram.set_content(svg)
                            result.visible = False
                            diagram.visible = True
                

                # Кнопка проверки качества и отображение результата
                if task.get("quality_check"):
                    async def quality_check():

                        check_button.disable()
                        check_button.set_text(
                            'Проверка...'
                        )

                        values = {}
                        for field_name, field in form_fields.items():
                            values[field_name] = field.value

                        cached_response = (
                            selected_item.get("quality_response")
                            if selected_item
                            else None
                        )

                        if cached_response:

                            quality_md.content = cached_response
                            quality_result.visible = True

                            ui.notify(
                                'Проверка качества получена из кэша',
                                type='positive'
                            )

                        else:

                            response = await run.io_bound(
                                generate_review,
                                review_type="quality_check",
                                task=task_name,
                                context=build_review_context(
                                    values,
                                    get_result(),
                                    task["title"]
                                ),
                                provider=provider_select.value
                            )

                            quality_md.content = response
                            quality_result.visible = True

                            if selected_item:
                                selected_item["quality_response"] = response

                        check_button.set_text(
                            'Проверить качество'
                        )
                        check_button.enable()
                    check_button = ui.button(
                        'Проверить качество',
                        on_click=quality_check
                    )
                    check_button.visible = bool(history_options)
                    
                    with ui.element('div').classes(
                        'w-full task-result-panel'
                    ).style(
                        'overflow-x: auto; overflow-y: auto;'
                    ) as quality_result:

                        quality_md = ui.markdown('').classes(
                            'w-full nicegui-markdown task-result-markdown'
                        )

                    quality_result.visible = False
                
                # Кнопка критериев качества и отображение результата
                if task.get("acceptance_criteria"):

                    async def acceptance_criteria():

                        acceptance_button.disable()
                        acceptance_button.set_text(
                            'Формирование...'
                        )

                        values = {}
                        for field_name, field in form_fields.items():
                            values[field_name] = field.value

                        cached_response = (
                            selected_item.get("acceptance_response")
                            if selected_item
                            else None
                        )

                        if cached_response:

                            acceptance_md.content = cached_response
                            acceptance_result.visible = True

                            ui.notify(
                                'Критерии приемки получены из кэша',
                                type='positive'
                            )

                        else:

                            response = await run.io_bound(
                                generate_review,
                                review_type="acceptance_criteria",
                                task=task_name,
                                context=build_review_context(
                                    values,
                                    get_result(),
                                    task["title"]
                                ),
                                provider=provider_select.value
                            )

                            acceptance_md.content = response
                            acceptance_result.visible = True

                            if selected_item:
                                selected_item["acceptance_response"] = response

                        acceptance_button.set_text(
                            'Критерии приемки'
                        )
                        acceptance_button.enable()

                    acceptance_button = ui.button(
                        'Критерии приемки',
                        on_click=acceptance_criteria
                    )

                    acceptance_button.visible = bool(history_options)

                    with ui.element('div').classes(
                        'w-full task-result-panel'
                    ).style(
                        'overflow-x: auto; overflow-y: auto;'
                    ) as acceptance_result:

                        acceptance_md = ui.markdown('').classes(
                            'w-full nicegui-markdown task-result-markdown'
                        )

                    acceptance_result.visible = False