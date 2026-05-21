from django.contrib import admin
from .models import Question, ChatMessage


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'category', 'correct_answer')
    list_filter = ('category',)
    search_fields = ('question_text',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_message', 'created_at')
    list_filter = ('user_name',)
    readonly_fields = ('created_at',)
