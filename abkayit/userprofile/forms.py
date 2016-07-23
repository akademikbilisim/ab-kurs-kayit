# -*- coding:utf-8  -*-
import logging

from django import forms

from django.forms.models import ModelForm
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import TextInput

from django_countries.widgets import CountrySelectWidget

from userprofile.models import *
from userprofile.dynamicfields import DynmcFields
from userprofile.userprofileops import UserProfileOPS

log = logging.getLogger(__name__)


class CreateUserForm(ModelForm):
    passwordre = forms.CharField(label=_("Confirm Password"),
                                 max_length=30,
                                 widget=forms.PasswordInput(
                                     attrs={'placeholder': _('Confirm Password'), 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': _('First Name'), 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': _('Last Name'), 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': _('Email Address'), 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'form-control'}),
            'username': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
        self.fields['username'].required = False
        self.fields['password'].label = _("Password")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        users = User.objects.filter(email=email)
        if len(users) > 0:
            raise forms.ValidationError(_("This email address already exists in this system"))
        return email

    def clean_passwordre(self):
        password = self.cleaned_data.get('password')
        passwordre = self.cleaned_data.get('passwordre')
        if password != passwordre:
            raise forms.ValidationError(_("Your passwords do not match"))
        return passwordre

    def clean_username(self):
        username = self.cleaned_data.get('email')
        return username


class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': _('First Name'), 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': _('Last Name'), 'class': 'form-control'}),
            'email': TextInput(attrs={'placeholder': _('E-mail'), 'class': 'form-control'}),
            'username': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        self.fields['username'].required = False
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email in self.changed_data:
            users = User.objects.filter(email=email)
            if len(users) > 0:
                raise forms.ValidationError(_("This email address already exists in this system"))
        return email

    def clean_username(self):
        username = self.cleaned_data.get('email')
        return username


class CreateInstForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': _("First Name")}),
            'last_name': forms.TextInput(attrs={'placeholder': _("Last Name")}),
            'email': forms.EmailInput(attrs={'placeholder': _("Email")}),
            'password': forms.HiddenInput(),
            'username': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(CreateInstForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
        self.fields['username'].required = False
        self.fields['password'].required = False

    def clean_email(self):
        email = self.cleaned_data.get('email')
        users = User.objects.filter(email=email)
        if len(users) > 0:
            raise forms.ValidationError(_("This email address already exists in this system"))
        return email

    def clean_username(self):
        username = self.cleaned_data.get('email')
        return username


class InstProfileForm(ModelForm):
    # TODO: egitimci icin form
    class Meta:
        model = UserProfile
        exclude = {}
        fields = ['job', 'title', 'organization', 'country', 'user']
        widgets = {
            'user': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(InstProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
        self.fields['user'].required = False


class StuProfileForm(ModelForm):
    class Meta:
        dyncf = DynmcFields()
        model = UserProfile
        exclude = {''}
        # fields=['name','surname','username','email','password','password',]
        widgets = {
            'tckimlikno': forms.NumberInput(attrs={'placeholder': _('Turkish ID No'), 'class': 'form-control'}),
            'ykimlikno': forms.NumberInput(attrs={'placeholder': _('Foreigner ID No'), 'class': 'form-control'}),
            'gender': forms.Select(attrs={'placeholder': _('Gender'), 'class': 'form-control'}),
            'mobilephonenumber': forms.TextInput(
                attrs={'placeholder': _('Mobile Phone Number'), 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'placeholder': _('Address'), 'class': 'form-control'}),
            'job': forms.TextInput(attrs={'placeholder': _('Job'), 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': _('City'), 'class': 'form-control'}),
            'country': CountrySelectWidget(attrs={'placeholder': _('Country')}),
            'title': forms.TextInput(attrs={'placeholder': _('Title'), 'class': 'form-control'}),
            'organization': forms.TextInput(attrs={'placeholder': _('Organization'), 'class': 'form-control'}),
            'university': forms.Select(attrs={'placeholder': _('University'), 'class': 'form-control'}),
            'department': forms.TextInput(attrs={'placeholder': _('Department'), 'class': 'form-control'}),
            'website': forms.TextInput(attrs={'placeholder': _('Website'), 'class': 'form-control'}),
            'experience': forms.TextInput(
                attrs={'placeholder': _('Daha önce çalışılan/Staj yapılan yerler'), 'class': 'form-control'}),
            'additional_information': forms.Textarea(
                attrs={'placeholder': _('Additional Information'), 'class': 'form-control'}),
            'userpassedtest': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'needs_document': forms.HiddenInput(),
            'birthdate': SelectDateWidget(years=dyncf.BirthDateYears),
        }
        help_texts = {
            'organization': 'Kurum Bilgisi; okuyorsanız okuduğunuz kurum, çalışıyorsanız çalıştığınız kurum bilgisidir',
            'document': 'Görevlendirme yazısı, veli izin yazısı vb.',
        }

    def __init__(self, *args, **kwargs):
        '''

        :param args:
        :param kwargs: ruser: profili olusturulacak kullanıcı tckimlik no dogrulamada kullanılacak.
        '''
        self.ruser = kwargs.pop('ruser', None)
        super(StuProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field in ['needs_document', 'tckimlikno','ykimlikno','university', 'userpassedtest', 'user',
                         'additional_information', 'website', 'experience', 'document']:
                self.fields[field].required = False
            else:
                self.fields[field].required = True

    def clean_profilephoto(self):
        profilephoto = self.cleaned_data.get("profilephoto", False)
        if profilephoto and "profilephoto" in self.changed_data:
            if profilephoto._size > 1024 * 1024:
                raise forms.ValidationError(_("Image file size too large > 1mb )"))
        return profilephoto

    def clean(self):
        cleaned_data = super(StuProfileForm, self).clean()
        ruser = self.ruser
        if ruser:
            first_name = ruser.first_name.rstrip().lstrip()
            last_name = ruser.last_name.rstrip().lstrip()
            birthdate = cleaned_data.get('birthdate')
            byear = ""
            if birthdate:
                byear = birthdate.year
            if cleaned_data['tckimlikno'] and cleaned_data['ykimlikno']:
                raise forms.ValidationError(_("Please fill only one of them:tckimlikno,ykimlikno"))
            elif not cleaned_data['tckimlikno'] and cleaned_data['country'] == 'TR':
                raise forms.ValidationError(_("TC identity number can not be empty for Turkish citizens"))
            elif not cleaned_data.get('ykimlikno') and cleaned_data['country'] != 'TR':
                raise forms.ValidationError(_("Foreign identity number can not be empty for non Turkish citizens"))
            elif cleaned_data['tckimlikno'] and cleaned_data['country'] == 'TR':
                tcknosorgu = UserProfile.objects.filter(tckimlikno=cleaned_data['tckimlikno'])
                if tcknosorgu:
                    if tcknosorgu[0].user.username != ruser.username:
                        raise forms.ValidationError(_("Bu TC Kimlik numarasına sahip başka hesap var."))
                tckisvalid = UserProfileOPS.validateTCKimlikNo(cleaned_data['tckimlikno'].rstrip().lstrip(), first_name,
                                                               last_name, byear)
                if tckisvalid == -1:
                    raise forms.ValidationError(_("An error occured while verifing your TC identity number"))
                elif not tckisvalid:
                    raise forms.ValidationError(_("Your identity information can not be verified, Please enter \
                                                     your TC identity number, your name, your last name (with Turkish characters if exist) \
                                                     and your birth date precisely"))
        else:
            raise forms.ValidationError(_("User not found"))
        return cleaned_data


class ChangePasswordForm(ModelForm):
    passwordre = forms.CharField(label=_("Confirm Password"),
                                 max_length=30,
                                 widget=forms.PasswordInput(
                                     attrs={'placeholder': _('Confirm Password'), 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['password']
        widgets = {'password': forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
        self.fields['password'].label = _("Password")

    def clean_passwordre(self):
        password = self.cleaned_data.get('password')
        passwordre = self.cleaned_data.get('passwordre')
        if password != passwordre:
            raise forms.ValidationError(_("Your passwords do not match"))
        return passwordre


class InstructorInformationForm(ModelForm):
    class Meta:
        model = InstructorInformation
        fields = ['transportation', 'additional_information', 'arrival_date', 'departure_date']
        widgets = {
            'transportation': forms.Select(attrs={'placeholder': _('Transportation'), 'class': 'form-control'}),
            'additional_information': forms.TextInput(
                attrs={'placeholder': _('Additional Information'), 'class': 'form-control'}),
            'arrival_date': SelectDateWidget(attrs={'placeholder': _('Arrival Date')}),
            'departure_date': SelectDateWidget(attrs={'placeholder': _('Departure Date')}),
        }
        help_texts = {
            'transportation': _('Select your transportation type'),
            'additional_information': _('If you want to add additional information, please enter here'),
            'arrival_date': _(
                'Arrival Date (Example: If your first day at event will be 1st February, please select 1st February'),
            'departure_date': _(
                'Departure Date (Example: If you will stay at 3rd February, please select 3rd February)')
        }

    def __init__(self, *args, **kwargs):
        super(InstructorInformationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
        self.fields['additional_information'].required = False
