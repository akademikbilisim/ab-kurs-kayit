from django.contrib import admin

# Register your models here.
from django_extensions.admin import ForeignKeyAutocompleteAdmin

from surman.models import Answer, AnswerGroup, Question, Survey



@admin.register(Question)
class QuestionAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ["survey", "key", "related_course", "related_trainer"]
    list_filter = ["survey", "survey__site"]
    related_search_fields = {
        'related_trainer': ["user__first_name", "user__last_name", "user__email"],
    }

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ["site", "created", "name"]
    list_filter = ["site", "created"]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["question", "group"]
    list_filter = ["question__survey", "question__survey__site"]


@admin.register(AnswerGroup)
class AnswerGroupAdmin(admin.ModelAdmin):
    list_display = ["token", "created"]
    list_filter = ["created", "answers__question__survey", "answers__question__survey__site"]
