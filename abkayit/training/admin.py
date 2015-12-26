#!-*- coding:utf-8 -*-
from django.contrib import admin
from training.models import Keyword, Course, TrainessCourseRecord
# Register your models here.

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    search_fields=('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name','approved']
    list_filter = ('approved','trainer')
    search_fields = ('name','trainer')

@admin.register(TrainessCourseRecord)
class TrainessCourseRecordAdmin(admin.ModelAdmin):
    list_display = ['id','course','trainess','preference_order','approved']
    
