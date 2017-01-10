#!-*- coding:utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from surman.views import AnswerListView

urlpatterns = patterns('',
                       url(r'^answers', login_required(AnswerListView.as_view()), name="survey_answers"),
                       )