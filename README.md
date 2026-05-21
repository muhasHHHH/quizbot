# QuizBot — Чат-бот для тестирования знаний

## Описание
QuizBot — это веб-чат-бот на Django, который проверяет знания пользователя по трём категориям: Python, Математика и Общие знания. Бот задаёт вопросы с вариантами ответов, считает очки и сохраняет историю диалогов в базу данных.

## Используемые технологии
- Python 3.x
- Django 4.2+
- SQLite (встроенная БД)
- HTML / CSS / JavaScript

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python manage.py migrate
python manage.py fill_questions
python manage.py runserver
```

Открыть в браузере: http://127.0.0.1:8000

Админ-панель: http://127.0.0.1:8000/admin  
Логин: admin | Пароль: admin123

## Команды бота
- `привет` — приветствие
- `старт` — случайный вопрос
- `python` — вопрос по Python
- `математика` — математический вопрос
- `общие` — общий вопрос
- `счёт` — текущий результат
- `сброс` — сбросить счёт
- `помощь` — все команды
- `стоп` — завершить сессию

## Структура проекта
```
quizbot/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
├── quizbot/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── chat/
    ├── models.py       # Модели Question, ChatMessage
    ├── views.py        # Логика бота и страницы
    ├── urls.py         # Маршруты
    ├── admin.py        # Админ-панель
    ├── migrations/
    ├── management/
    │   └── commands/
    │       └── fill_questions.py
    └── templates/
        └── chat/
            ├── index.html    # Главная страница чата
            └── history.html  # История сообщений
```
