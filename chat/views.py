import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Question, ChatMessage


# -------------------------------------------------------
# Логика бота: отвечает на сообщения пользователя
# -------------------------------------------------------

def get_bot_response(user_message, session):
    message = user_message.strip().lower()

    # Пустой ввод
    if not message:
        return "Пожалуйста, введите сообщение! 😊"

    # Приветствия
    if message in ['привет', 'hello', 'hi', 'здравствуй', 'салем', 'хай']:
        return ("Привет! 👋 Я QuizBot — бот для тестирования знаний!\n\n"
                "Напиши одну из команд:\n"
                "• **старт** — начать викторину\n"
                "• **категории** — список тем\n"
                "• **счёт** — твой результат\n"
                "• **помощь** — все команды")

    # Помощь
    if message in ['помощь', 'помоги', 'help', '?', 'команды']:
        return ("📋 Доступные команды:\n\n"
                "• **привет** — приветствие\n"
                "• **старт** — начать викторину\n"
                "• **категории** — список категорий\n"
                "• **python** — вопросы по Python\n"
                "• **математика** — вопросы по математике\n"
                "• **общие** — вопросы на общую тему\n"
                "• **счёт** — посмотреть результат\n"
                "• **сброс** — сбросить счёт\n"
                "• **стоп** — завершить викторину")

    # Категории
    if message in ['категории', 'темы', 'категория']:
        return ("📚 Доступные категории:\n\n"
                "1️⃣ **python** — Вопросы по языку Python\n"
                "2️⃣ **математика** — Математические задачи\n"
                "3️⃣ **общие** — Общие знания\n\n"
                "Напиши название категории чтобы начать!")

    # Счёт
    if message in ['счёт', 'счет', 'результат', 'очки']:
        score = session.get('score', 0)
        total = session.get('total', 0)
        if total == 0:
            return "Ты ещё не ответил ни на один вопрос. Напиши **старт** чтобы начать!"
        percent = round(score / total * 100)
        return (f"📊 Твой результат:\n\n"
                f"✅ Правильных ответов: {score}\n"
                f"❌ Всего вопросов: {total}\n"
                f"🏆 Процент: {percent}%")

    # Сброс
    if message in ['сброс', 'заново', 'reset']:
        session['score'] = 0
        session['total'] = 0
        session['current_question'] = None
        return "🔄 Счёт сброшен! Напиши **старт** чтобы начать заново."

    # Стоп
    if message in ['стоп', 'stop', 'выход', 'конец']:
        score = session.get('score', 0)
        total = session.get('total', 0)
        session['current_question'] = None
        if total > 0:
            return f"👋 Викторина завершена!\n\nТвой итог: {score} из {total}. Молодец!"
        return "👋 До свидания! Напиши **привет** когда захочешь поиграть снова."

    # Выбор категории или команда "старт"
    category = None
    if message in ['старт', 'начать', 'start', 'играть']:
        category = 'random'
    elif message in ['python', 'питон', 'пайтон']:
        category = 'python'
    elif message in ['математика', 'матем', 'math', 'мат']:
        category = 'math'
    elif message in ['общие', 'общее', 'general', 'знания']:
        category = 'general'

    if category:
        return ask_question(session, category)

    # Проверка ответа если есть активный вопрос
    if session.get('current_question'):
        return check_answer(user_message.strip(), session)

    # Неизвестная команда
    return ("🤔 Я не понял команду.\n\n"
            "Напиши **помощь** чтобы увидеть список команд,\n"
            "или **старт** чтобы начать викторину!")


def ask_question(session, category='random'):
    """Выбирает случайный вопрос из базы данных."""
    if category == 'random':
        questions = Question.objects.all()
    else:
        questions = Question.objects.filter(category=category)

    if not questions.exists():
        return "❌ Вопросы не найдены. Обратитесь к администратору."

    question = random.choice(list(questions))

    # Сохраняем вопрос в сессию
    session['current_question'] = {
        'id': question.id,
        'correct': question.correct_answer,
    }

    options = [question.option_a, question.option_b,
               question.option_c, question.option_d]

    response = (f"❓ {question.question_text}\n\n"
                f"A) {question.option_a}\n"
                f"B) {question.option_b}\n"
                f"C) {question.option_c}\n"
                f"D) {question.option_d}\n\n"
                f"Напиши A, B, C или D (или полный ответ)")
    return response


def check_answer(user_answer, session):
    """Проверяет ответ пользователя."""
    current = session.get('current_question')
    if not current:
        return "Нет активного вопроса. Напиши **старт** чтобы начать!"

    correct = current['correct']
    answer_upper = user_answer.upper().strip()

    # Получаем вопрос из БД чтобы сопоставить A/B/C/D
    try:
        question = Question.objects.get(id=current['id'])
        options_map = {
            'A': question.option_a,
            'B': question.option_b,
            'C': question.option_c,
            'D': question.option_d,
        }
    except Question.DoesNotExist:
        session['current_question'] = None
        return "Вопрос не найден. Напиши **старт** чтобы продолжить."

    # Проверяем ответ
    is_correct = False
    if answer_upper in options_map:
        is_correct = (options_map[answer_upper] == correct)
    else:
        is_correct = (user_answer.strip().lower() == correct.lower())

    # Обновляем счёт
    session['total'] = session.get('total', 0) + 1
    if is_correct:
        session['score'] = session.get('score', 0) + 1

    session['current_question'] = None

    score = session.get('score', 0)
    total = session.get('total', 0)

    if is_correct:
        return (f"✅ Правильно! Отличная работа!\n\n"
                f"Правильный ответ: **{correct}**\n\n"
                f"Счёт: {score}/{total}\n\n"
                f"Напиши **старт** для следующего вопроса!")
    else:
        return (f"❌ Неправильно!\n\n"
                f"Правильный ответ: **{correct}**\n\n"
                f"Счёт: {score}/{total}\n\n"
                f"Напиши **старт** для следующего вопроса!")


# -------------------------------------------------------
# Views (страницы)
# -------------------------------------------------------

def index(request):
    """Главная страница чата."""
    # История последних 20 сообщений из БД
    history = ChatMessage.objects.all()[:20]
    return render(request, 'chat/index.html', {'history': history})


def send_message(request):
    """Обработка сообщения пользователя (POST)."""
    if request.method == 'POST':
        # Имя пользователя из сессии или формы
        user_name = request.session.get('user_name', '')
        
        # Если имя не задано — предлагаем ввести
        if not user_name:
            user_name = request.POST.get('user_name', '').strip()
            if user_name:
                request.session['user_name'] = user_name
                bot_response = f"Привет, {user_name}! 👋 Я QuizBot!\nНапиши **помощь** чтобы узнать команды, или **старт** чтобы начать викторину!"
                ChatMessage.objects.create(
                    user_name=user_name,
                    user_message=f"[Вошёл как {user_name}]",
                    bot_response=bot_response,
                )
                return JsonResponse({'bot_response': bot_response, 'user_name': user_name})
            else:
                return JsonResponse({'bot_response': 'Пожалуйста, введи своё имя чтобы начать!', 'user_name': ''})

        user_message = request.POST.get('message', '').strip()

        # Пустой ввод
        if not user_message:
            return JsonResponse({'bot_response': '❗ Введи сообщение!', 'user_name': user_name})

        # Получаем ответ бота
        bot_response = get_bot_response(user_message, request.session)

        # Сохраняем в БД
        ChatMessage.objects.create(
            user_name=user_name,
            user_message=user_message,
            bot_response=bot_response,
        )

        return JsonResponse({'bot_response': bot_response, 'user_name': user_name})

    return JsonResponse({'error': 'Только POST запросы'}, status=405)


def history(request):
    """Страница истории сообщений."""
    messages = ChatMessage.objects.all()
    return render(request, 'chat/history.html', {'messages': messages})
