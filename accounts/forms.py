from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
	name = forms.CharField()
	email = forms.EmailField(label = 'College Email id')
	branch = forms.CharField()
	year = forms.IntegerField()

	class Meta:
		model = User
		fields = ['name', 'username', 'email', 'password1', 'password2', 'branch', 'year']


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	branch = forms.CharField()
	year = forms.IntegerField()

	class Meta:
		model = User
		fields = ['username', 'email', 'branch', 'year']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image', 'bio']
