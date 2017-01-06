# -*- coding:utf-8  -*-

import logging
from userprofile.forms import StuProfileForm, UserProfileBySiteForm
from django.utils.translation import ugettext_lazy as _
from userprofileops import UserProfileOPS
from userprofile.models import UserProfile, Accommodation, UserAccomodationPref, UserProfileBySite

log = logging.getLogger(__name__)


def getuserprofileforms(user, site, d):
    accomodations, accomodation_records, userprofilebysite, userprobysiteform = None, None, None, None
    try:
        user_profile = user.userprofile
        note = _("You can update your profile below")
        userproform = StuProfileForm(instance=user_profile, ruser=user)
        if not UserProfileOPS.is_instructor(user_profile):
            log.debug("egitmen olmayan kullanici icin isleme devam ediliyor", extra=d)
            accomodations = Accommodation.objects.filter(
                    usertype__in=['stu', 'hepsi'], gender__in=[user_profile.gender, 'H'], site=site).order_by(
                    'name')
            accomodation_records = UserAccomodationPref.objects.filter(user=user_profile).order_by(
                    'preference_order')
        if site.needs_document:
            try:
                userprofilebysite = UserProfileBySite.objects.get(user=user, site=site)
                userprobysiteform = UserProfileBySiteForm(instance=userprofilebysite, ruser=user, site=site)
            except UserProfileBySite.DoesNotExist:
                userprobysiteform = UserProfileBySiteForm(ruser=user, site=site)
        log.debug("Profil guncelleme islemi", extra=d)
    except UserProfile.DoesNotExist:
        note = _("If you want to continue please complete your profile.")
        userproform = StuProfileForm(ruser=user)
        if site.needs_document:
            userprobysiteform = UserProfileBySiteForm(ruser=user, site=site)
        accomodations = Accommodation.objects.filter(usertype__in=['stu', 'hepsi'],
                                                     gender__in=['K', 'E', 'H'],
                                                     site=site).order_by('name')
        log.debug("Profil oluşturma islemi", extra=d)
    return note, userprofilebysite, userproform, userprobysiteform, accomodations, accomodation_records
