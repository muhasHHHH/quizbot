from django.core.management.base import BaseCommand
from chat.models import Question


class Command(BaseCommand):
    help = 'Заполняет базу данных вопросами для викторины'

    def handle(self, *args, **kwargs):
        Question.objects.all().delete()

        questions = [
            {'category': 'python', 'question_text': 'Какой тип данных используется для хранения текста в Python?', 'correct_answer': 'str', 'option_a': 'str', 'option_b': 'int', 'option_c': 'list', 'option_d': 'dict'},
            {'category': 'python', 'question_text': 'Что выведет команда print(2 ** 3)?', 'correct_answer': '8', 'option_a': '6', 'option_b': '8', 'option_c': '9', 'option_d': '16'},
            {'category': 'python', 'question_text': 'Какая функция возвращает длину списка?', 'correct_answer': 'len()', 'option_a': 'size()', 'option_b': 'count()', 'option_c': 'len()', 'option_d': 'length()'},
            {'category': 'python', 'question_text': 'Как создать пустой список в Python?', 'correct_answer': '[]', 'option_a': '{}', 'option_b': '[]', 'option_c': '()', 'option_d': '<>'},
            {'category': 'python', 'question_text': 'Что такое "def" в Python?', 'correct_answer': 'Объявление функции', 'option_a': 'Цикл', 'option_b': 'Условие', 'option_c': 'Объявление функции', 'option_d': 'Импорт'},
            {'category': 'python', 'question_text': 'Как называется цикл с условием в Python?', 'correct_answer': 'while', 'option_a': 'for', 'option_b': 'while', 'option_c': 'loop', 'option_d': 'repeat'},
            {'category': 'python', 'question_text': 'Какой оператор сравнения в Python?', 'correct_answer': '==', 'option_a': '=', 'option_b': ':=', 'option_c': '==', 'option_d': '!='},
            {'category': 'math', 'question_text': 'Сколько будет 7 × 8?', 'correct_answer': '56', 'option_a': '54', 'option_b': '56', 'option_c': '58', 'option_d': '64'},
            {'category': 'math', 'question_text': 'Чему равен квадратный корень из 144?', 'correct_answer': '12', 'option_a': '11', 'option_b': '12', 'option_c': '13', 'option_d': '14'},
            {'category': 'math', 'question_text': 'Сколько градусов в прямом угле?', 'correct_answer': '90', 'option_a': '45', 'option_b': '60', 'option_c': '90', 'option_d': '180'},
            {'category': 'math', 'question_text': 'Чему равно число Пи (первые два знака)?', 'correct_answer': '3.14', 'option_a': '2.71', 'option_b': '3.14', 'option_c': '3.41', 'option_d': '1.41'},
            {'category': 'math', 'question_text': 'Сколько будет 2 в степени 10?', 'correct_answer': '1024', 'option_a': '512', 'option_b': '1000', 'option_c': '1024', 'option_d': '2048'},
            {'category': 'general', 'question_text': 'Сколько планет в Солнечной системе?', 'correct_answer': '8', 'option_a': '7', 'option_b': '8', 'option_c': '9', 'option_d': '10'},
            {'category': 'general', 'question_text': 'Кто создал язык Python?', 'correct_answer': 'Гвидо ван Россум', 'option_a': 'Линус Торвальдс', 'option_b': 'Гвидо ван Россум', 'option_c': 'Деннис Ричи', 'option_d': 'Билл Гейтс'},
            {'category': 'general', 'question_text': 'В каком году был создан Python?', 'correct_answer': '1991', 'option_a': '1985', 'option_b': '1991', 'option_c': '1995', 'option_d': '2000'},
            {'category': 'general', 'question_text': 'Что означает HTML?', 'correct_answer': 'HyperText Markup Language', 'option_a': 'HyperText Markup Language', 'option_b': 'High Text Machine Learning', 'option_c': 'Home Tool Markup Language', 'option_d': 'HyperText Making Links'},
            {'category': 'general', 'question_text': 'Столица Казахстана?', 'correct_answer': 'Астана', 'option_a': 'Алматы', 'option_b': 'Астана', 'option_c': 'Шымкент', 'option_d': 'Актау'},
        ]

        for q in questions:
            Question.objects.create(**q)

        self.stdout.write(self.style.SUCCESS(f'Добавлено {len(questions)} вопросов!'))
