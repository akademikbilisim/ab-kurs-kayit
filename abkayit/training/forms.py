# -*- coding:utf-8  -*-

import datetime

from django.db.models import Q

from django.forms import HiddenInput, ModelChoiceField, Select
from django.forms.extras.widgets import SelectDateWidget
from django.forms.models import ModelForm

from training.models import Course, TrainessParticipation, TrainessCourseRecord
from userprofile.models import UserProfile


class CreateCourseForm(ModelForm):
    class Meta:
        model = Course
        exclude = []
        widgets = {
            'start_date': SelectDateWidget(
                    years=(str(datetime.datetime.now().year), str(datetime.datetime.now().year + 1))),
            'end_date': SelectDateWidget(
                    years=(str(datetime.datetime.now().year), str(datetime.datetime.now().year + 1))),
            'reg_start_date': HiddenInput(),
            'reg_end_date': HiddenInput(),
            'trainess': HiddenInput(),
            'trainer': HiddenInput(),
            'approved': HiddenInput(),
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
            'courserecord': HiddenInput(),
            'day': HiddenInput(),
        }


class AddTrainessForm(ModelForm):
    trainess = ModelChoiceField(queryset=UserProfile.objects.none(), label="Trainess",
                                widget=Select(attrs={'class': 'form-control'}))
    course = ModelChoiceField(queryset=Course.objects.none(), label="Course",
                              widget=Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.ruser = self.request.user
        self.site = self.request.site
        super(AddTrainessForm, self).__init__(*args, **kwargs)
        if self.ruser:
            self.fields['course'].queryset = Course.objects.filter(trainer=self.ruser.userprofile, site=self.site)
        self.fields['trainess'].queryset = UserProfile.objects.exclude(
                Q(trainesscourserecord__approved=True) | Q(user__is_staff=True))

    class Meta:
        model = TrainessCourseRecord
        exclude = ['instapprovedate', 'consentemailsent']
        widgets = {
            'preference_order': HiddenInput(),
            'trainess_approved': HiddenInput(),
            'approved': HiddenInput(),
        }
