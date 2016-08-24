#!-*- coding:utf-8 -*-

from django.conf.urls import patterns, url

from surman.views import AnswerListView

urlpatterns = patterns('',
                       url(r'^answers', AnswerListView.as_view(), name="survey_answers"),
                       )