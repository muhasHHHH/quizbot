from django.db import models


class Question(models.Model):
    CATEGORIES = [
        ('python', 'Python'),
        ('math', 'Математика'),
        ('general', 'Общие знания'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORIES, verbose_name='Категория')
    question_text = models.TextField(verbose_name='Вопрос')
    correct_answer = models.CharField(max_length=200, verbose_name='Правильный ответ')
    option_a = models.CharField(max_length=200, verbose_name='Вариант A')
    option_b = models.CharField(max_length=200, verbose_name='Вариант B')
    option_c = models.CharField(max_length=200, verbose_name='Вариант C')
    option_d = models.CharField(max_length=200, verbose_name='Вариант D')

    def __str__(self):
        return self.question_text[:60]

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class ChatMessage(models.Model):
    user_name = models.CharField(max_length=100, verbose_name='Имя пользователя')
    user_message = models.TextField(verbose_name='Сообщение пользователя')
    bot_response = models.TextField(verbose_name='Ответ бота')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время')

    def __str__(self):
        return f"{self.user_name} — {self.created_at.strftime('%d.%m.%Y %H:%M')}"

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'История сообщений'
        ordering = ['-created_at']
