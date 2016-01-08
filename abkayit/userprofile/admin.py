#!-*- coding:utf-8 -*-

from django.contrib import admin
from userprofile.models import InstructorInformation, SubscribeNotice, UserProfile, Accommodation, UserAccomodationPref, UserVerification
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','is_instructor','tckimlikno','gender','mobilephonenumber']
    list_filter=('is_instructor','is_student')
    search_fields=('user__username',)

@admin.register(SubscribeNotice)
class SubscribeNoticeAdmin(admin.ModelAdmin):
    list_display = ['usertype','subnotice',]

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['id','name','gender',]
    list_filter=('gender',)
    
@admin.register(UserAccomodationPref)
class UserAccomodationPrefAdmin(admin.ModelAdmin):
    list_display = ['id','user','usertype','preference_order','approved',]
    list_filter=('usertype','preference_order','accomodation')
    search_fields=('user__username',)

@admin.register(UserVerification)
class UserVerificationAdmin(admin.ModelAdmin):
	pass

@admin.register(InstructorInformation)
class InstructorInformationAdmin(admin.ModelAdmin):
    list_display = ['id','user','transportation','arrival_date','departure_date']
    list_filter=('transportation','arrival_date','departure_date')
    search_fields=('user__username',)
