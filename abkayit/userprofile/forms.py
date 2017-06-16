# -*- coding:utf-8  -*-
import logging

from django import forms
from django.contrib.auth.models import User

from django.forms.models import ModelForm

from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import TextInput

from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import PasswordResetForm
from captcha.fields import ReCaptchaField

from userprofile.models import UserProfile, UserProfileBySite, InstructorInformation
from userprofile.dynamicfields import DynmcFields
from userprofile.userprofileops import UserProfileOPS
from cities_light.models import Region

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


class UserProfileBySiteForStaffForm(ModelForm):
    class Meta:
        model = UserProfileBySite
        exclude = ['additional_information', 'canapply', 'userpassedtest']
        widgets = {
            'user': forms.HiddenInput(),
            'site': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.ruser = kwargs.pop('ruser')
        self.site = kwargs.pop('site', None)
        self.user = kwargs.pop('user')
        super(UserProfileBySiteForStaffForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        if not self.ruser.is_staff:
            self.fields.pop('document')
            self.fields.pop('needs_document')

    def save(self, commit=True):
        if self.site is not None:
            self.instance.site = self.site
        self.instance.user = self.user
        return super(UserProfileBySiteForStaffForm, self).save(commit)


class UserProfileBySiteForm(ModelForm):
    class Meta:
        model = UserProfileBySite
        exclude = ['canapply', 'needs_document', 'userpassedtest', 'potentialinstructor']
        widgets = {
            'additional_information': forms.Textarea(
                    attrs={'placeholder': _('Additional Information'), 'class': 'form-control'}),
            'user': forms.HiddenInput(),
            'site': forms.HiddenInput(),
        }
        help_texts = {
            'document': 'Görevlendirme yazısı, veli izin yazısı vb.',
        }

    def __init__(self, *args, **kwargs):
        self.site = kwargs.pop('site', None)
        self.ruser = kwargs.pop('ruser')
        super(UserProfileBySiteForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

    def save(self, commit=True):
        if self.site is not None:
            self.instance.site = self.site
        self.instance.user = self.ruser
        return super(UserProfileBySiteForm, self).save(commit)


class StuProfileForm(ModelForm):
    class Meta:
        dyncf = DynmcFields()
        model = UserProfile
        exclude = []
        widgets = {
            'tckimlikno': forms.NumberInput(attrs={'placeholder': _('Turkish ID No'), 'class': 'form-control'}),
            'ykimlikno': forms.NumberInput(attrs={'placeholder': _('Foreigner ID No'), 'class': 'form-control'}),
            'gender': forms.Select(
                attrs={'placeholder': _('Gender'), 'class': 'form-control', 'onChange': 'genderchanged()'}),
            'mobilephonenumber': forms.TextInput(
                    attrs={'placeholder': _('Mobile Phone Number'), 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'placeholder': _('Address'), 'class': 'form-control'}),
            'job': forms.TextInput(attrs={'placeholder': _('Job'), 'class': 'form-control'}),
            'city': forms.Select(attrs={'placeholder': _('Current City'), 'class': 'form-control'},
                                 choices=Region.objects.all().values_list('name_ascii', 'name_ascii')),
            'country': CountrySelectWidget(attrs={'placeholder': _('Nationality'), 'onChange': 'countrychanged();'}),
            'title': forms.TextInput(attrs={'placeholder': _('Title'), 'class': 'form-control'}),
            'organization': forms.TextInput(attrs={'placeholder': _('Organization'), 'class': 'form-control'}),
            'occupation': forms.Select(attrs={'placeholder': _('Occupation'), 'class': 'form-control'}),
            'current_education': forms.Select(attrs={'placeholder': _('Current Education'), 'class': 'form-control'}),
            'university': forms.Select(attrs={'placeholder': _('University'), 'class': 'form-control'}),
            'department': forms.TextInput(attrs={'placeholder': _('Department'), 'class': 'form-control'}),
            'website': forms.TextInput(attrs={'placeholder': _('Website'), 'class': 'form-control'}),
            'experience': forms.TextInput(
                    attrs={'placeholder': _('Daha önce çalışılan/Staj yapılan yerler'), 'class': 'form-control'}),
            'user': forms.HiddenInput(),
            'birthdate': SelectDateWidget(years=dyncf.BirthDateYears),
        }
        help_texts = {
            'organization': 'Kurum Bilgisi; okuyorsanız okuduğunuz kurum, çalışıyorsanız çalıştığınız kurum bilgisidir',
        }

    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs: ruser: profili olusturulacak kullanıcı tckimlik no dogrulamada kullanılacak.
        """
        self.ruser = kwargs.pop('ruser', None)
        super(StuProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field in ['tckimlikno', 'ykimlikno', 'university', 'user', 'website', 'experience']:
                self.fields[field].required = False
            else:
                self.fields[field].required = True

    def clean_profilephoto(self):
        profilephoto = self.cleaned_data.get("profilephoto", False)
        if profilephoto and "profilephoto" in self.changed_data:
            # noinspection PyUnresolvedReferences,PyProtectedMember
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
                    raise forms.ValidationError(_(("Your identity information can not be verified, Please enter"
                                                   "your TC identity number, your name, your last name (with Turkish"
                                                   "characters if exist) and your birth date precisely")))
        else:
            raise forms.ValidationError(_("User not found"))
        return cleaned_data

    def save(self, commit=True):
        self.instance.user = self.ruser
        return super(StuProfileForm, self).save(commit)


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


class ChangePasswordWithSMSForm(ModelForm):
    passwordre = forms.CharField(label=_("Confirm Password"),
                                 max_length=30,
                                 widget=forms.PasswordInput(
                                         attrs={'placeholder': _('Confirm Password'), 'class': 'form-control'}))

    key = forms.CharField(label="SMS ile gonderilen kod",
                                 max_length=30,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': "Kod", 'class': 'form-control'}))
    captcha = ReCaptchaField(attrs={'theme': 'clean'})

    class Meta:
        model = User
        fields = ['password']
        widgets = {'password': forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        super(ChangePasswordWithSMSForm, self).__init__(*args, **kwargs)
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
            'arrival_date': _('Arrival Date'
                              ' (Example: If your first day at event will be 1st February, please select 1st February'),
            'departure_date': _(
                    'Departure Date (Example: If you will stay at 3rd February, please select 3rd February)')
        }

    def __init__(self, *args, **kwargs):
        self.site = kwargs.pop('site', None)
        self.request = kwargs.pop('request')
        super(InstructorInformationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
        self.fields['additional_information'].required = False

    def clean_departure_date(self):
        from django.core.exceptions import ValidationError
        if self.cleaned_data["departure_date"] < self.cleaned_data["arrival_date"]:
            raise ValidationError(_("Can't be prior to Arrival Date"))
        return self.cleaned_data["departure_date"]

    def save(self, commit=True):
        if self.site is not None:
            self.instance.site = self.site
        self.instance.user = self.request.user.userprofile
        return super(InstructorInformationForm, self).save(commit)