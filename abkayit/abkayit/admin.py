#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from abkayit.models import *
from ckeditor.widgets import CKEditorWidget
from django import forms


class ApprovalDateInline(admin.StackedInline):
    model = ApprovalDate
    extra = 0


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    inlines = [
        ApprovalDateInline,
    ]


class ContentInline(admin.TabularInline):
    content = forms.CharField(widget=CKEditorWidget())
    model = Content


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [
        ContentInline,
    ]


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'no', 'detail', 'active']
    list_filter = ['no', 'active']
    inlines = [
        AnswerInline,
    ]


@admin.register(TextBoxQuestions)
class TextBoxQuestionsAdmin(admin.ModelAdmin):
    list_display = ['questionno', 'detail', 'site', 'is_sitewide']
    list_filter = ['is_sitewide', 'active']
