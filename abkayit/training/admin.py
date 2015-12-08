from django.contrib import admin
from training.models import Keyword, Course
# Register your models here.

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    search_fields=('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name','approved','start_date','end_date',]
    list_filter = ('approved','keyword','trainer')
    search_fields = ('name','trainer')
