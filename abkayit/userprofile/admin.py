#!-*- coding:utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User
from userprofile.models import InstructorInformation, UserProfile, Accommodation, UserAccomodationPref, \
    UserVerification, TrainessNote

admin.site.unregister(User)


class UserVerificationInline(admin.StackedInline):
    model = UserVerification
    extra = 0


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'is_instructor', 'tckimlikno', 'gender']
    list_filter = ('userprofile__is_instructor', )
    search_fields = ('username', 'first_name', 'last_name', 'userprofile__tckimlikno')
    inlines = [
        UserProfileInline,
        UserVerificationInline,
    ]

    def is_instructor(self, obj):
        if obj.userprofile.is_instructor:
            return obj.userprofile.is_instructor
        else:
            return False

    def tckimlikno(self, obj):
        return obj.userprofile.tckimlikno

    def gender(self, obj):
        return obj.userprofile.gender


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'gender', ]
    list_filter = ('gender',)


@admin.register(UserAccomodationPref)
class UserAccomodationPrefAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'usertype', 'preference_order', 'approved', ]
    list_filter = ('usertype', 'preference_order', 'accomodation')
    search_fields = ('user__user__username',)


@admin.register(InstructorInformation)
class InstructorInformationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'transportation', 'arrival_date', 'departure_date']
    list_filter = ('transportation', 'arrival_date', 'departure_date')
    search_fields = ('user__user__username',)


@admin.register(TrainessNote)
class TrainessNoteAdmin(admin.ModelAdmin):
    list_display = ['note_to_profile', 'note_from_profile', 'site', 'note', 'label']
    list_filter = ('label',)
    search_fields = ('note_from_profile__user__username', 'note_to_profile__user__username')
