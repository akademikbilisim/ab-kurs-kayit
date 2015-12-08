# -*- coding:utf-8  -*-
from django import forms

from django.forms.models import ModelForm
from seminar.models import Seminar

class CreateManifestSuggestForm(ModelForm):
    class Meta:
        model= Seminar
        exclude=[]
        widgets={
                 'speaker' : forms.HiddenInput(),
                 'fulltext':forms.FileField(label='Select a file',help_text='max. 42 megabytes')
                 }
        