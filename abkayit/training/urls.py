#!-*- coding:utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('training.views',
    url(r'^submit', 'submitandregister', name="submit"),
    url(r'^controlpanel', 'control_panel', name="controlpanel"),
    url(r'^listcourses', 'list_courses', name="listcourses"),
    url(r'^editcourse', 'edit_course', name="editcourse"),
    url(r'^showcourse/(?P<course_id>[1-9]+)/$', 'show_course', name="showcourse"),
    url(r'^applytocourse', 'apply_to_course', name="applytocourse"),
)

