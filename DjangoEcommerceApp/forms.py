# forms.py
from django import forms

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
import re
from .models import *
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

class CustomUserCreationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    username = forms.CharField(
        label='Username',
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w\s.@+-]+$',
                message='Enter a valid username. This value may contain only letters, numbers, spaces, and @/./+/-/_ characters.'
            )
        ]
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email address already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("This field is required.")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.user_type = 4  # Default to 'Customer'
        if commit:
            user.save()
        return user

class CustomUserUpdateForm(forms.ModelForm):


    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("A user with that email address already exists.")
        return email


class CustomUserChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise ValidationError("Old password is incorrect.")
        return old_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if not new_password:
            raise ValidationError("This field is required.")
        return new_password

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password'])
        if commit:
            self.user.save()
        return self.user

class PasswordUpdateForm(forms.ModelForm):
    password = forms.CharField(label='New Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('password',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='Email Address',
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'mobile_number', 'image', 'address']
