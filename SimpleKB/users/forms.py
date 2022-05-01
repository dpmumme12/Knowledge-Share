from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegisterationForm(UserCreationForm):
    """
    Inherits Django's UserCreationForm to create new users with no privileges
    """

    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control rounded-corners'}), required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control rounded-corners'})


class LoginForm(AuthenticationForm):
    """
    Inherits Django's AuthenticationForm to log a use in
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control rounded-corners'})


class UserSettingsForm(forms.ModelForm):
    """
    Settings form to set alter user's data
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['profile_image'].widget.attrs.update({'class': 'form-control'})
        self.fields['profile_image'].widget.clear_checkbox_label = 'Delete'
        self.fields['profile_image'].widget.initial_text = 'Current'
        self.fields['profile_image'].label = 'Profile image'
