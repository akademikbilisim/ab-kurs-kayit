from django.contrib import admin
from userprofile.models import SubscribeNotice, UserProfile, Accommodation
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','is_instructor','is_student','is_speaker','is_participant']
    list_filter=('accommodation_needed','is_instructor','is_student','is_speaker','is_participant')
    search_fields=('user',)

@admin.register(SubscribeNotice)
class SubscribeNoticeAdmin(admin.ModelAdmin):
    list_display = ['usertype','subnotice',]

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['id','name','gender',]
    list_filter=('gender',)