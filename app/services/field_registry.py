FIELDS = {

    "domain": {
        "label": "Предметная область",
        "placeholder": "Например: Интернет-магазин, CRM, ERP",
        "max_length": 100
    },

    "system_description": {
        "label": "Описание системы",
        "placeholder": "Краткое описание системы, её целей и границ",
        "max_length": 3000
    },

    "stakeholders": {
        "label": "Заинтересованные стороны",
        "placeholder": "Список ролей, пользователей или внешних систем",
        "max_length": 200
    },

    "constraints": {
        "label": "Ограничения и допущения",
        "placeholder": "Ограничения, бизнес-правила, контекст использования",
        "max_length": 3000
    },

    "logical_context_description": {
        "label": "Описание логического контекста",
        "placeholder": "Название и краткое описание контекста",
        "max_length": 3000
    },

    "business_goals": {
        "label": "Бизнес-цель",
        "placeholder": "Бизнес-цель",
        "max_length": 3000
    },

    "current_problems": {
        "label": "Текущие проблемы и метрики",
        "placeholder": "Описание существующих проблем, показателей и KPI",
        "max_length": 1000
    },

    "business_requirements": {
        "label": "Бизнес-требования",
        "placeholder": "Список бизнес-требований",
        "max_length": 3000
    },

    "functional_requirements": {
        "label": "Функциональные требования",
        "placeholder": "Список функциональных требований",
        "max_length": 3000
    },

    "non_functional_requirements": {
        "label": "Нефункциональные требования",
        "placeholder": "Список нефункциональных требований",
        "max_length": 3000
    },

    "entities": {
        "label": "Сущности и данные",
        "placeholder": "Список сущностей и их атрибутов",
        "max_length": 3000
    },

    "nfr_type": {
        "label": "Тип нефункциональных требований",
        "type": "select",
        "options": [
            "Производительность",
            "Надежность",
            "Безопасность",
            "Доступность",
            "Масштабируемость",
            "Удобство использования"
        ]
    },

    "load_parameters": {
        "label": "Параметры нагрузки",
        "placeholder": "Количество пользователей, RPS (запросов в секунду), описание основных операций",
        "max_length": 3000
    },

    "process_description": {
        "label": "Описание процесса / функции/ контекста",
        "placeholder": "Название и описание бизнес-процесса",
        "max_length": 10000
    },

    "architecture": {
        "label": "Архитектура",
        "placeholder": "Микросервисы, очереди, БД и т.д.",
        "max_length": 500
    },

    "integrations": {
        "label": "Интеграции",
        "placeholder": "API, внешние системы",
        "max_length": 1500
    },

    "user_stories": {
        "label": "Связанные User Stories",
        "placeholder": "Список User Story",
        "max_length": 1000
    },

    "use_case": {
        "label": "Use Case",
        "placeholder": "Полное описание Use Case",
        "max_length": 10000
    },

    "design_context": {
        "label": "Контекст",
        "placeholder": "Бизнес-требования, функциональные требования или Use Case",
        "max_length": 10000
    },

    "db_type": {
        "label": "Тип СУБД",
        "type": "select",
        "options": [
            "PostgreSQL",
            "MySQL",
            "Oracle",
            "SQLite"
        ]
    },

    "db_schema": {
        "label": "Схема БД",
        "placeholder": "Описание схемы базы данных",
        "max_length": 2000
    },

    "tables": {
        "label": "Таблицы",
        "placeholder": "Список таблиц",
        "max_length": 5000
    },

    "service_name": {
        "label": "Название системы / сервиса",
        "placeholder": "Название сервиса",
        "max_length": 100
    },

    "api_type": {
        "label": "Тип API",
        "type": "select",
        "options": [
            "public",
            "private",
            "partner",
            "internal"
        ]
    },

    "architecture_type": {
        "label": "Тип архитектуры",
        "type": "select",
        "options": [
            "monolith",
            "microservices",
            "SOA"
        ]
    },

    "auth_type": {
        "label": "Авторизация",
        "type": "select",
        "options": [
            "JWT",
            "OAuth2",
            "API Key",
            "Bearer Token",
            "None"
        ]
    },

    "api_versioning": {
        "label": "Версионирование API",
        "type": "select",
        "options": [
            "/api/v1",
            "header",
            "date"
        ]
    },

    "endpoint": {
        "label": "Endpoint",
        "placeholder": "GET /users",
        "max_length": 500
    },

    "records_count": {
        "label": "Количество записей",
        "placeholder": "Например: 10",
        "max_length": 4
    },
    "data_format": {
        "label": "Формат данных",
        "type": "select",
        "options": ["JSON"]
    }
}