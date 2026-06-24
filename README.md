# sa

Веб-приложение на Python с пользовательским интерфейсом на базе [NiceGUI](https://nicegui.io/). Предоставляет набор задач, доступных через боковое меню, с защитой доступа по коду.

## Технологии

- **Python** — основной язык
- **NiceGUI** — фреймворк для веб-UI
- **FastAPI / Uvicorn** — веб-сервер
- **Anthropic API / OpenAI API** — интеграция с LLM
- **python-dotenv** — управление переменными окружения

## Установка

```bash
git clone https://github.com/aigulfaizul2015/sa.git
cd sa
pip install -r requirements.txt
```

## Настройка

Создайте файл `.env` в корне проекта:

```env
ACCESS_CODE=ваш_код_доступа
STORAGE_SECRET=секретный_ключ
MAX_HISTORY_ITEMS =максимальное кол-во записей в истории
GPT_API_KEY =ключ OpenAi
CLAUDE_API_KEY =ключ Claude
```

## Запуск

```bash
python ui_main.py
```

Приложение будет доступно по адресу `http://localhost:8080`.

## Структура

```
sa/
├── app/
│   ├── services/
│   │   └── task_registry.py   # Реестр задач
│   └── ui/
│       └── task_page.py       # Отображение задач
├── ui_main.py                 # Точка входа
└── requirements.txt
```
