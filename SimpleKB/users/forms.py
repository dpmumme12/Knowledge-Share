from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegisterationForm(UserCreationForm):
    """ Inherits Django's UserCreationForm to create new users with no privileges """

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'autocomplete': 'new-password',
        'class': 'form-control rounded-corners'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        'autocomplete': 'new-password',
        'class': 'form-control rounded-corners'}))
    username = forms.CharField(label='Usename', widget=forms.TextInput(attrs={
        'autocomplete': 'username',
        'maxlength': '150',
        'autocapitalize': 'none',
        'class': 'form-control rounded-corners'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control rounded-corners'}), required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    """ Inherits Django's AuthenticationForm to log a use in"""

    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'autocomplete': 'username',
        'maxlength': '150',
        'autocapitalize': 'none',
        'class': 'form-control rounded-corners'}))

    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'autocomplete': 'password',
        'class': 'form-control rounded-corners'}))
