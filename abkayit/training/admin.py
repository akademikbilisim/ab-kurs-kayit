#!-*- coding:utf-8 -*-

from django.utils import timezone
from django.contrib import admin

from abkayit.models import Question, TextBoxQuestions
from training.models import Course, TrainessCourseRecord, TrainessParticipation, TrainessTestAnswers
from userprofile.models import TrainessNote, UserProfile, TrainessClassicTestAnswers


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['no', 'name', 'approved']
    list_filter = ('approved', 'site')
    filter_horizontal = ('trainess', 'trainer', 'authorized_trainer',)
    search_fields = ('name', 'trainer__user__username')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "question":
            kwargs["queryset"] = Question.objects.filter(is_faq=False, active=True)
        elif db_field.name == "textboxquestion":
            kwargs["queryset"] = TextBoxQuestions.objects.filter(is_sitewide=False, active=True)
        return super(CourseAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(TrainessCourseRecord)
class TrainessCourseRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'trainess', 'preference_order', 'approved', 'trainess_approved']
    search_fields = ('id', 'course__name', 'trainess__user__username')
    list_filter = ('approved', 'trainess_approved', 'course__site')

    def save_model(self, request, obj, form, change):
        notestr = ""
        if not change:
            notestr = "Bu kullanicinin, %s kursu olan %s. tercihi yönetici tarafindan eklendi." % (obj.course.name,
                                                                                                   obj.preference_order)
        if "approved" in form.changed_data:
            if form.cleaned_data['approved']:
                notestr = "Bu kullanicinin, %s kursu olan %s. tercihi yönetici tarafindan onaylandi." % (obj.course.name,
                                                                                                   obj.preference_order)
        if notestr and not TrainessNote.objects.filter(note=notestr):
            note = TrainessNote(note=notestr, note_from_profile=request.user.userprofile, note_to_profile=obj.trainess,
                                            site=obj.course.site, note_date=timezone.now(), label="tercih")
            note.save()
        super(TrainessCourseRecordAdmin, self).save_model(request, obj, form, change)


@admin.register(TrainessParticipation)
class TrainessParticipationAdmin(admin.ModelAdmin):
    list_display = ['get_site', 'day', 'get_trainess_name', 'get_trainess_username', 'id']
    search_fields = ('courserecord__course__name', 'trainess__user__username')
    list_filter = ('courserecord__course__site',)

    def get_trainess_name(self, obj):
        return "%s %s" % (obj.courserecord.trainess.user.first_name, obj.courserecord.trainess.user.last_name)

    def get_trainess_username(self, obj):
        return obj.courserecord.trainess.user.username

    def get_site(self, obj):
        return "%s" % obj.courserecord.course.site
        # accounts/showuser/2701/12824


@admin.register(TrainessClassicTestAnswers)
class TrainessClassicTestAnswersAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'answer']
    search_fields = ('user__user__username',)