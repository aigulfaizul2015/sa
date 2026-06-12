from nicegui import ui

from app.services.field_registry import FIELDS


def render_form(task_config):

    form_fields = {}

    required_fields = task_config.get(
        "required_fields",
        []
    )

    for field_name in task_config["fields"]:

        field = FIELDS[field_name]

        required = field_name in required_fields
        max_length = field.get("max_length")

        validation = {}

        if required:
            validation['Обязательное поле'] = (
                lambda value: bool(value and value.strip())
            )

        if max_length:
            validation[f'Максимум {max_length} символов'] = (
                lambda value, max_length=max_length:
                    not value or len(value) <= max_length
            )

        if field.get("type") == "select":
            field_widget = ui.select(
                options=field["options"],
                label=field["label"],
                validation=validation or None
            ).classes(
                'w-full'
            ).props(
                'rows=1'
            )
        else:
            field_widget = ui.textarea(
                label=field["label"],
                placeholder=field["placeholder"],
                validation=validation or None
            ).classes(
                'w-full'
            ).props(
                'rows=1'
            )

        form_fields[field_name] = field_widget

    return form_fields