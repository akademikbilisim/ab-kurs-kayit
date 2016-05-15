# -*- coding:utf-8  -*-


from django import forms

from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import TextInput

from django_countries.widgets import CountrySelectWidget

from userprofile.models import *
from userprofile.dynamicfields import DynmcFields


class CreateUserForm(ModelForm):
    passwordre = forms.CharField(label="Parola Doğrula",
                                 max_length=30,
                                 widget=forms.PasswordInput(
                                     attrs={'placeholder': "Parola Doğrula", 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'username']
        widgets = {
                    'first_name': forms.TextInput(attrs={'placeholder': "İsim", 'class': 'form-control'}),
                    'last_name': forms.TextInput(attrs={'placeholder': "Soyisim", 'class' : 'form-control'}),
                    'email': forms.EmailInput(attrs={'placeholder': "E-posta adresi", 'class': 'form-control'}),
                    'password': forms.PasswordInput(attrs={'placeholder': "Parola", 'class': 'form-control'}),
                    'username': forms.HiddenInput()
                  }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
        self.fields['username'].required = False
        self.fields['password'].label = "Parola"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        users = User.objects.filter(email=email)
        if len(users) > 0:
            raise forms.ValidationError("Sistemde bu e-posta adresi zaten kayıtlı!")
        return email

    def clean_passwordre(self):
        password = self.cleaned_data.get('password')
        passwordre = self.cleaned_data.get('passwordre')
        if password != passwordre:
            raise forms.ValidationError("Parolalarınız eşleşmiyor!")
        return passwordre
    
    def clean_username(self):
        username = self.cleaned_data.get('email')
        return username    


class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
                    'first_name': forms.TextInput(attrs={'placeholder': "İsim", 'class':'form-control'}),
                    'last_name': forms.TextInput(attrs={'placeholder': "Soyisim", 'class':'form-control'}),
                    'email': TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
                    'username': forms.HiddenInput()
                  }

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        self.fields['username'].required = False


class CreateInstForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'username']
        widgets = {
                    'first_name': forms.TextInput(attrs={'placeholder':_("First Name")}),
                    'last_name': forms.TextInput(attrs={'placeholder':_("Last Name")}),
                    'email': forms.EmailInput(attrs={'placeholder':_("Email")}),
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
        fields = ['job', 'title', 'organization', 'country', 'is_instructor', 'is_student', 'is_participant', 'user']
        widgets = {
                    'is_instructor':forms.HiddenInput(),
                    'is_student':forms.HiddenInput(),
                    'is_participant':forms.HiddenInput(),
                    'user':forms.HiddenInput(),
                  }

    def __init__(self, *args, **kwargs):
        super(InstProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
        self.fields['is_instructor'].required = False
        self.fields['is_student'].required = False
        self.fields['is_participant'].required = False
        self.fields['user'].required = False


class UserProfileForm(ModelForm):
    class Meta:
        dynamic_fiels = DynmcFields()
        model = UserProfile
        exclude = {'score'}
        widgets = {
            'tckimlikno': forms.NumberInput(attrs={'placeholder': "TC Kimlik Numarası", 'class': 'form-control'}),
            'ykimlikno': forms.NumberInput(attrs={'placeholder': "Yabancı Kimlik Numarası", 'class': 'form-control'}),
            'gender': forms.Select(attrs={'placeholder': "Cinsiyet", 'class': 'form-control'}),
            'mobilephonenumber': forms.TextInput(attrs={'placeholder': "Cep Telefonu", 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'placeholder': "Adres", 'class': 'form-control'}),
            'job': forms.TextInput(attrs={'placeholder': "iş", 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': "Şehir", 'class': 'form-control'}),
            'country': CountrySelectWidget(attrs={'placeholder': "Ülke"}),
            'title': forms.TextInput(attrs={'placeholder': "Ünvan", 'class': 'form-control'}),
            'organization': forms.TextInput(attrs={'placeholder': "Kurum", 'class': 'form-control'}),
            'university': forms.Select(attrs={'placeholder': "Üniversite", 'class': 'form-control'}),
            'department': forms.TextInput(attrs={'placeholder': "Bölüm", 'class': 'form-control'}),
            'additional_information': forms.Textarea(attrs={'placeholder': "Ek Bilgiler", 'class': 'form-control'}),
            'is_instructor': forms.HiddenInput(),
            'is_student': forms.HiddenInput(),
            'is_participant': forms.HiddenInput(),
            'userpassedtest': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'birthdate': SelectDateWidget(years=dynamic_fiels.BirthDateYears),
        }
        help_texts = {
            'organization': 'Kurum Bilgisi; okuyorsanız okuduğunuz kurum, çalışıyorsanız çalıştığınız kurum bilgisidir',
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
        self.fields['tckimlikno'].required = False
        self.fields['ykimlikno'].required = False
        self.fields['is_instructor'].required = False
        self.fields['is_student'].required = False
        self.fields['is_participant'].required = False
        self.fields['university'].required = False
        self.fields['userpassedtest'].required = False
        self.fields['user'].required = False
        self.fields['additional_information'].required = False


class ChangePasswordForm(ModelForm):
    password_re = forms.CharField(label="Parolayı Doğrula",
                                  max_length=30,
                                  widget=forms.PasswordInput(
                                      attrs={'placeholder': "Parolayı Doğrula", 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['password']
        widgets = {'password': forms.PasswordInput(attrs={'placeholder': "Parola", 'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
        self.fields['password'].label = "Parola"

    def clean_password_re(self):
        password = self.cleaned_data.get('password')
        password_re = self.cleaned_data.get('password_re')
        if password != password_re:
            raise forms.ValidationError("Parolalarınız eşleşmiyor")
        return password_re


class InstructorInformationForm(ModelForm):
    class Meta:
        model = InstructorInformation
        fields = ['transportation', 'additional_information', 'arrival_date', 'departure_date']
        widgets = {
            'transportation': forms.Select(attrs={'placeholder': "Ulaşım", 'class': 'form-control'}),
            'additional_information': forms.TextInput(attrs={'placeholder': "Ek bilgi", 'class': 'form-control'}),
            'arrival_date': SelectDateWidget(attrs={'placeholder': "Geliş tarihi"}),
            'departure_date': SelectDateWidget(attrs={'placeholder': "Dönüş tarihi"}),
        }
        help_texts = {
            'transportation': "Ulaşım tipinizi seçiniz",
            'additional_information': "Eğer ek bilgi eklemek istiyorsanız lütfen yazınız"
        }

    def __init__(self, *args, **kwargs):
        super(InstructorInformationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
        self.fields['additional_information'].required = False
