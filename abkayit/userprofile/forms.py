# -*- coding:utf-8  -*-
from django import forms

from django.forms.models import ModelForm
from userprofile.models import UserProfile
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from userprofileops import UserProfileOPS

class CreateUserForm(ModelForm):
	passwordre = forms.CharField(label=_("Confirm Password"),
									max_length=30,
									widget=forms.PasswordInput(attrs={'placeholder':_('Confirm Password'), 'class':'form-control'})) 
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'password', 'username']
		widgets = {
					'first_name': forms.TextInput(attrs={'placeholder':_('First Name'), 'class':'form-control'}),
					'last_name': forms.TextInput(attrs={'placeholder':_('Last Name'), 'class':'form-control'}),
					'email': forms.EmailInput(attrs={'placeholder':_('Email Address'), 'class':'form-control'}),
					'password': forms.PasswordInput(attrs={'placeholder':_('Password'), 'class':'form-control'}),
					'username': forms.HiddenInput()
				  }
	def __init__(self, *args, **kwargs):
		super(CreateUserForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = True
		self.fields['username'].required = False

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
		

class CreateInstForm(ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'password', 'username']
		widgets = {
                    'first_name': forms.TextInput(attrs={'placeholder':'Ad'}),
                    'last_name': forms.TextInput(attrs={'placeholder':'Soyad'}),
                    'email': forms.EmailInput(attrs={'placeholder':'E-posta'}),
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
		fields = ['job', 'title', 'organization', 'country', 'is_instructor', 'is_student', 'is_speaker', 'is_participant', 'user']
		widgets = {
				    'is_instructor':forms.HiddenInput(),
				    'is_student':forms.HiddenInput(),
				    'is_speaker':forms.HiddenInput(),
				    'is_participant':forms.HiddenInput(),
				    'user':forms.HiddenInput(),
				  }
	def __init__(self, *args, **kwargs):
		super(InstProfileForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = True
		self.fields['is_instructor'].required = False
		self.fields['is_student'].required = False
		self.fields['is_speaker'].required = False
		self.fields['is_participant'].required = False
		self.fields['user'].required = False

class StuProfileForm(ModelForm):
	# TODO: Kursa katılacaklar icin ayrı form
	class Meta:
		model = UserProfile
		exclude = {}
		# fields=['name','surname','username','email','password','password',]
		widgets = {
				    'is_instructor':forms.HiddenInput(),
				    'is_student':forms.HiddenInput(),
				    'is_speaker':forms.HiddenInput(),
				    'is_participant':forms.HiddenInput(),
				    'user':forms.HiddenInput(),
				 }
	def __init__(self,user=None, *args, **kwargs):
		super(StuProfileForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = True
		self.fields['is_instructor'].required = False
		self.fields['is_student'].required = False
		self.fields['is_speaker'].required = False
		self.fields['is_participant'].required = False
		self.fields['user'].required = False
		self.fields['accommodation_needed'].required = False
		if user:
			self.fields['user'].initial=User.objects.get(email=user).pk
		

class SpeProfileForm(ModelForm):
	# TODO: Seminer verecekler icin ayri form
	class Meta:
		model = UserProfile
		exclude = {}
		widgets = {
				    'is_instructor':forms.HiddenInput(),
				    'is_student':forms.HiddenInput(),
				    'is_speaker':forms.HiddenInput(),
				    'is_participant':forms.HiddenInput(),
				    'user':forms.HiddenInput(),
				  }
class ParProfileForm(ModelForm):
	# TODO: Seminer dinleyecekler icin ayrı form olusturulacak
	class Meta:
		model = UserProfile
		exclude = {}
		widgets = {
				    'is_instructor':forms.HiddenInput(),
				    'is_student':forms.HiddenInput(),
				    'is_speaker':forms.HiddenInput(),
				    'is_participant':forms.HiddenInput(),
				    'user':forms.HiddenInput(),
				  }
