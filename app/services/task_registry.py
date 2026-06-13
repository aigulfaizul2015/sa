TASKS = {

    "Аналитика": {

        "context": {
            "title": "Контекст",
            "fields": [
                "domain",
                "system_description",
                "stakeholders",
                "constraints"
            ],
            "required_fields": [
                "domain",
                "system_description"
            ],
            "quality_check": False,
            "acceptance_criteria": False
        },

        "business_goals": {
            "title": "Бизнес цели",
            "fields": [
                "domain",
                "logical_context_description",
                "stakeholders"
            ],
            "required_fields": [
                "domain",
                "logical_context_description"
            ],
            "quality_check": False,
            "acceptance_criteria": False
        },

        "business_requirements": {
            "title": "Бизнес требования",
            "fields": [
                "domain",
                "logical_context_description",
                "stakeholders",
                "business_goals",
                "constraints",
                "current_problems"
            ],
            "required_fields": [
                "domain",
                "business_goals"
            ],
            "quality_check": True,
            "acceptance_criteria": False
        },

        "functional_requirements": {
            "title": "ФТ",
            "fields": [
                "domain",
                "logical_context_description",
                "business_requirements",
                "entities"
            ],
            "required_fields": [
                "domain",
                "business_requirements"
            ],
            "quality_check": True,
            "acceptance_criteria": False
        },

        "non_functional_requirements": {
            "title": "НФТ",
            "fields": [
                "domain",
                "logical_context_description",
                "business_requirements",
                "functional_requirements",
                "nfr_type",
                "load_parameters"
            ],
            "required_fields": [
                "domain",
                "business_requirements",
                "functional_requirements",
                "nfr_type"
            ],
            "quality_check": True,
            "acceptance_criteria": False
        },

        "user_story": {
            "title": "User Story",
            "fields": [
                "domain",
                "logical_context_description",
                "functional_requirements",
                "stakeholders"
            ],
            "required_fields": [
                "domain",
                "logical_context_description",
                "functional_requirements"
            ],
            "quality_check": False,
            "acceptance_criteria": True
        },

        "use_case": {
            "title": "Use Case",
            "fields": [
                "domain",
                "process_description",
                "architecture",
                "integrations",
                "user_stories"
            ],
            "required_fields": [
                "domain",
                "process_description",
                "architecture",
                "integrations",
                "user_stories"
            ],
            "quality_check": False,
            "acceptance_criteria": False
        },

        "sequence_diagram": {
            "title": "Sequence диаграмма",
            "fields": [
                "use_case"
            ],
            "required_fields": [
                "use_case"
            ],
            "result_type": "plantuml",
            "quality_check": False,
            "acceptance_criteria": False
        }
    },

    "Проектирование": {

        "logical_model_data": {
            "title": "Логическая модель",
            "fields": [
                "domain",
                "design_context"
            ],
            "required_fields": [
                "domain",
                "design_context"
            ],
            "quality_check": False,
            "acceptance_criteria": False
        },

        "physical_model_data": {
            "title": "Физическая модель",
            "fields": [
                "domain",
                "design_context",
                "db_type",
                "non_functional_requirements"
            ],
            "required_fields": [
                "domain",
                "design_context",
                "db_type"
            ],
            "quality_check": False,
            "acceptance_criteria": False
        },

        "indices": {
            "title": "Индексы",
            "fields": [
                "domain",
                "tables",
                "db_type",
                "functional_requirements",
                "non_functional_requirements"
            ],
            "required_fields": [
                "domain",
                "tables",
                "db_type",
                "functional_requirements"
            ],
            "quality_check": False,
            "acceptance_criteria": False
        },

        "er_diagram": {
            "title": "ER диаграмма",
            "fields": [
                "db_schema"
            ],
            "required_fields": [
                "db_schema"
            ],
            "result_type": "mermaid",
            "quality_check": False,
            "acceptance_criteria": False
        }
    },
    "Разработка": {
        "sql_script": {
            "title": "SQL скрипт",
            "fields": [
                "db_type",
                "db_schema"
            ],
            "required_fields": [
                "db_type",
                "db_schema"
            ],
            "quality_check": False,
            "acceptance_criteria": False
        },

        "sql_script_mock_data": {
            "title": "SQL мок данные",
            "fields": [
                "db_type",
                "db_schema",
                "records_count"
            ],
            "required_fields": [
                "db_type",
                "db_schema",
                "records_count"
            ],
            "quality_check": False,
            "acceptance_criteria": False
        },

        "rest_api_list": {
            "title": "REST API список",
            "fields": [
                "domain",
                "service_name",
                "process_description",
                "api_type",
                "architecture_type",
                "auth_type",
                "api_versioning",
                "tables"
            ],
            "required_fields": [
                "domain",
                "service_name",
                "process_description",
                "api_type",
                "architecture_type",
                "auth_type",
                "api_versioning",
                "tables"
            ],
            "quality_check": False,
            "acceptance_criteria": False
        },

        "rest_api_design": {
            "title": "REST API дизайн",
            "fields": [
                "process_description",
                "api_type",
                "data_format",
                "architecture_type",
                "auth_type",
                "api_versioning",
                "tables",
                "endpoint"
            ],
            "required_fields": [
                "process_description",
                "api_type",
                "data_format",
                "architecture_type",
                "auth_type",
                "api_versioning",
                "tables",
                "endpoint"
            ],
            "quality_check": False,
            "acceptance_criteria": False
        }
    }
}