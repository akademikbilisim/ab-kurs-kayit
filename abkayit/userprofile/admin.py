#!-*- coding:utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_extensions.admin import ForeignKeyAutocompleteAdmin

from userprofile.models import InstructorInformation, UserProfile, Accommodation, UserAccomodationPref, \
    UserVerification, TrainessNote, UserProfileBySite
from training.models import Course

admin.site.unregister(User)


def make_needs_document(modeladmin, request, queryset):
    for obj in queryset:
        up = UserProfileBySite.objects.get_or_create(user=obj)
        up.needs_document = True
        up.save()


make_needs_document.short_description = "Seçili nesneleri evrak gerekiyor olarak işaretle"


def remove_needs_document(modeladmin, request, queryset):
    for obj in queryset:
        up = UserProfileBySite.objects.get_or_create(user=obj)
        up.needs_document = False
        up.save()


remove_needs_document.short_description = "Seçili nesnelerin evrak gerekiyor işaretini kaldır"


class UserVerificationInline(admin.StackedInline):
    model = UserVerification
    extra = 0


@admin.register(UserProfile)
class UserProfileAdmin(ForeignKeyAutocompleteAdmin):
    """Bu admin modeli admin arayuzunde gozukmeyecek
    fakat autocomplete'in calismasi icin register edilmesi gerekli"""
    search_fields = ["user__first_name", "user__last_name", "user__email"]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0


class UserProfileBySiteInline(admin.StackedInline):
    model = UserProfileBySite
    extra = 0


class UserSiteFilter(admin.SimpleListFilter):
    title = _('Trainees Site')
    parameter_name = 'treessite'

    def lookups(self, request, model_admin):
        return User.objects.all().values_list("userprofile__trainess__site__id",
                                              "userprofile__trainess__site__name").distinct()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(userprofile__trainess__site__in=self.value())
        else:
            return queryset


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'tckimlikno', 'gender']
    list_filter = AuthUserAdmin.list_filter + (UserSiteFilter,)
    search_fields = ('username', 'first_name', 'last_name', 'userprofile__tckimlikno')
    actions = [make_needs_document, remove_needs_document]
    inlines = [
        UserProfileInline,
        UserVerificationInline,
        UserProfileBySiteInline,
    ]

    def is_instructor(self, obj):
        if obj.userprofile:
            courses = Course.objects.filter(site__is_active=True, trainer=obj.userprofile)
            if courses:
                return True
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
