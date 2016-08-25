from django.contrib import admin

# Register your models here.
from surman.models import Answer, AnswerGroup, Question, Survey


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ["site", "created", "name"]


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(AnswerGroup)
class AnswerGroupAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ["token", "created"]
