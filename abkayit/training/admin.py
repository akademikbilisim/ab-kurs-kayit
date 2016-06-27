#!-*- coding:utf-8 -*-
from django.contrib import admin
from training.models import Course, TrainessCourseRecord, TrainessParticipation
from userprofile.models import TrainessNote


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['no', 'name', 'approved']
    list_filter = ('approved', 'trainer')
    search_fields = ('name', 'trainer__user__username')


@admin.register(TrainessCourseRecord)
class TrainessCourseRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'trainess', 'preference_order', 'approved', 'trainess_approved']
    search_fields = ('id', 'course__name', 'trainess__user__username')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.createdby = request.user
        if 'approved' in form.changed_data:
            if form.cleaned_data.get('approved'):
                obj.approvedby = request.user
            else:
                obj.approvedby = None
        obj.save()
        super(TrainessCourseRecordAdmin, self).save_model(request, obj, form, change)


@admin.register(TrainessParticipation)
class TrainessParticipationAdmin(admin.ModelAdmin):
    list_display = ['get_site', 'day', 'get_trainess_name', 'get_trainess_username', 'id']
    search_fields = ('courserecord__course__name', 'trainess__user__username')

    def get_trainess_name(self, obj):
        return "%s %s" % (obj.courserecord.trainess.user.first_name, obj.courserecord.trainess.user.last_name)

    def get_trainess_username(self, obj):
        return obj.courserecord.trainess.user.username

    def get_site(self, obj):
        return "%s" % (obj.courserecord.course.site)
        # accounts/showuser/2701/12824
