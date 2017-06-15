#!-*- coding:utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('training.views',
                       url(r'^submit', 'submitandregister', name="submit"),
                       url(r'^controlpanel/(?P<courseid>[0-9]+)/$', 'control_panel', name="controlpanel"),
                       url(r'^selectcourse/', 'select_course_for_control_panel', name="selectcoursefcp"),
                       url(r'^listcourses', 'list_courses', name="listcourses"),
                       url(r'^showcourse/(?P<course_id>[0-9]+)/$', 'show_course', name="showcourse"),
                       url(r'^applytocourse', 'apply_to_course', name="applytocourse"),
                       url(r'^additionprefapply/$', 'apply_course_in_addition', name="applytocourseinaddition"),
                       url(r'^basvurular', 'allcourseprefview', name="allcoursepref"),
                       url(r'^yoklamalar', 'allapprovedprefsview', name="allapprovedprefs"),
                       url(r'^istatistik/$', 'statistic', name="statistic"),
                       url(r'^katilimciekle/$', 'addtrainess', name="addtrainess"),
                       url(r'^cancelallpreference/$', 'cancel_all_preference', name="cancel_all_preference"),
                       # url(r'^cancelcourseapplication/$', 'cancel_course_application', name="cancel_course_application"),  ## 52 numarali issue ile kapatildi
                       url(r'^getpreferredcourses/$', 'get_preferred_courses', name="get_preferred_courses"),
                       url(r'^approve_course_preference/$', 'approve_course_preference',
                           name="approve_course_preference"),
                       url(r'^participationstatuses/$', 'participationstatuses', name='participationstatuses'),
                       url(r'^editparticipationstatus/(?P<courseid>[0-9]+)/(?P<date>[0-9]+)/$', 'editparticipationstatusebycourse', name='editparticipationstatusebycourse'),
                       url(r'^printparticipationpages/$', 'printparticipationpages', name='printparticipationpages'),
                       )
