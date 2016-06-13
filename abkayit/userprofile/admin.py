#!-*- coding:utf-8 -*-

from django.contrib import admin
from userprofile.models import InstructorInformation, SubscribeNotice, UserProfile, Accommodation, UserAccomodationPref, \
    UserVerification, TrainessNote


# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_instructor', 'tckimlikno', 'gender', 'mobilephonenumber']
    list_filter = ('is_instructor',)
    search_fields = ('user__username',)


@admin.register(SubscribeNotice)
class SubscribeNoticeAdmin(admin.ModelAdmin):
    list_display = ['usertype', 'subnotice', ]


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'gender', ]
    list_filter = ('gender',)


@admin.register(UserAccomodationPref)
class UserAccomodationPrefAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'usertype', 'preference_order', 'approved', ]
    list_filter = ('usertype', 'preference_order', 'accomodation')
    search_fields = ('user__user__username',)


@admin.register(UserVerification)
class UserVerificationAdmin(admin.ModelAdmin):
    search_fields = ('user_email',)


@admin.register(InstructorInformation)
class InstructorInformationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'transportation', 'arrival_date', 'departure_date']
    list_filter = ('transportation', 'arrival_date', 'departure_date')
    search_fields = ('user__user__username',)

@admin.register(TrainessNote)
class TrainessNoteAdmin(admin.ModelAdmin):
    list_display = ['note_to_profile', 'note_from_profile', 'site', 'note']
    search_fields = ('note_from_profile__user__username', 'note_to_profile__user__username')

