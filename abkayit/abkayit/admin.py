#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from abkayit.models import *
from ckeditor.widgets import CKEditorWidget
from django import forms


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
	pass


class ContentInline(admin.TabularInline):
    content = forms.CharField(widget=CKEditorWidget())
    model = Content


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
	inlines = [
		ContentInline,
	]


