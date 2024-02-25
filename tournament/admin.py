from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Tournament, Question, Participant, Answer


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', "start_time", 'end_time')
    ordering = ['start_time', 'name']


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'score', 'tournament')
    list_display_links = ('id', 'user')
    list_editable = ('tournament',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', "correct_answer", 'tournament')
    list_display_links = ('id', 'question_text')
    ordering = ['tournament', '-id']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant', 'question_id', 'current_answer', 'answer_text', 'is_correct')

    def question_id(self, obj):
        if obj.question:
            url = reverse("admin:tournament_question_change", args=[obj.question.id])
            return format_html('<a href="{}">{}</a>', url, obj.question.id)
        return None

    def current_answer(self, obj):
        return obj.question.correct_answer

    current_answer.short_description = 'Правильный ответ'
