#encoding=utf8
from django import forms

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class SignInForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(SignInForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user and not user.is_active:
            raise forms.ValidationError("User is forbidden.")
        if not user:
            raise forms.ValidationError("Sign in failed.")
        return cleaned_data


class SignUpForm(forms.Form):
    username = forms.CharField(required=True, min_length=4, max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if User.objects.filter(username=username):
            raise forms.ValidationError("Username is taken.")
        if User.objects.filter(email=email):
            raise forms.ValidationError("Email is taken.")
        return cleaned_data


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    username = None

    def set_user(self, username):
        self.username = username

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        old_password = cleaned_data.get('old_password')
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError("New password confirmation failed.")
        if not authenticate(username=self.username, password=old_password):
            raise forms.ValidationError("Old password is not correct.")
        return cleaned_data


class ResetPasswordForm(forms.Form):
    email = forms.EmailField()
    email1 = None

    def set_email(self, email):
        self.email1 = email

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        email = cleaned_data.get('email')
        if self.email1 and email != self.email1:
            raise forms.ValidationError("Email is not same with account.")
        if not User.objects.filter(email=email):
            raise forms.ValidationError("Email is not signed up.")

        return cleaned_data


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=20)

