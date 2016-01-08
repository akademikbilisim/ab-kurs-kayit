#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from abkayit.models import *
from ckeditor.widgets import CKEditorWidget
from django import forms

from abkayit.forms import *


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

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id','no','detail','rightanswer','active']
    list_filter = ['no','active']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id','detail']
