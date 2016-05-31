#!-*- coding:utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('training.views',
                       url(r'^submit', 'submitandregister', name="submit"),
                       url(r'^controlpanel', 'control_panel', name="controlpanel"),
                       url(r'^listcourses', 'list_courses', name="listcourses"),
                       url(r'^editcourse', 'edit_course', name="editcourse"),
                       url(r'^showcourse/(?P<course_id>[1-9]+)/$', 'show_course', name="showcourse"),
                       url(r'^applytocourse', 'apply_to_course', name="applytocourse"),
                       url(r'^additionprefapply/$', 'apply_course_in_addition', name="applytocourseinaddition"),
                       url(r'^basvurular', 'allcourseprefview', name="allcoursepref"),
                       url(r'^istatistik/$', 'statistic', name="statistic"),
                       url(r'^cancelallpreference/$', 'cancel_all_preference', name="cancel_all_preference"),
                       # url(r'^cancelcourseapplication/$', 'cancel_course_application', name="cancel_course_application"),  ## 52 numarali issue ile kapatildi
                       url(r'^getpreferredcourses/$', 'get_preferred_courses', name="get_preferred_courses"),
                       url(r'^approve_course_preference/$', 'approve_course_preference',
                           name="approve_course_preference"),
                       )
