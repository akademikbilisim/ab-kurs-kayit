#!-*- coding:utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('training.views',
                       url(r'^submit', 'submitandregister', name="submit"),
                       url(r'^controlpanel', 'control_panel', name="control_panel"),
                       url(r'^listcourses', 'list_courses', name="list_courses"),
                       url(r'^editcourse', 'edit_course', name="edit_course"),
                       url(r'^showcourse/(?P<course_id>[1-9]+)/$', 'show_course', name="show_course"),
                       url(r'^applytocourse', 'apply_to_course', name="apply_to_course"),
                       url(r'^additionprefapply/$', 'apply_course_in_addition', name="apply_to_course_in_addition"),
                       url(r'^basvurular', 'allcourseprefview', name="all_course_pref"),
                       url(r'^istatistik/$', 'statistic', name="statistic"),
                       url(r'^cancelallpreference/$', 'cancel_all_preference', name="cancel_all_preference"),
                       url(r'^getpreferredcourses/$', 'get_preferred_courses', name="get_preferred_courses"),
                       url(r'^approve_course_preference/$', 'approve_course_preference', name="approve_course_preference"),
                       )
