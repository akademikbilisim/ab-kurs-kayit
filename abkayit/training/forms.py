# -*- coding:utf-8  -*-
from django import forms
import datetime
from django.forms.models import ModelForm
from training.models import Course, TrainessParticipation
from django.forms.extras.widgets import SelectDateWidget


class CreateCourseForm(ModelForm):
    # numoftrainer= forms.ChoiceField(widget=Select, choices=[(1,1),(2,2),(3,3),(4,4)],label="Egitmen sayisi")
    # fulltext= forms.FileField(upload_to='%Y/%m/%d/'label='Select a file', help_text='max. 42 megabytes' )
    class Meta:
        model = Course
        exclude = []
        widgets = {
            'start_date': SelectDateWidget(
                years=(str(datetime.datetime.now().year), str(datetime.datetime.now().year + 1))),
            'end_date': SelectDateWidget(
                years=(str(datetime.datetime.now().year), str(datetime.datetime.now().year + 1))),
            'reg_start_date': forms.HiddenInput(),
            'reg_end_date': forms.HiddenInput(),
            'trainess': forms.HiddenInput(),
            'trainer': forms.HiddenInput(),
            'approved': forms.HiddenInput(),
            # 'fulltext': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CreateCourseForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
        self.fields['fulltext'].required = False
        self.fields['approved'].required = False
        self.fields['trainer'].required = False
        self.fields['trainess'].required = False
        self.fields['reg_start_date'].required = False
        self.fields['reg_end_date'].required = False

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        return end_date

    def clean_approved(self):
        approved = False
        return approved


class ParticipationForm(ModelForm):
    class Meta:
        model = TrainessParticipation
        fields = ['courserecord', 'day', 'morning', 'afternoon', 'evening']
        widgets = {
            'courserecord': forms.HiddenInput(),
            'day': forms.HiddenInput(),
        }
