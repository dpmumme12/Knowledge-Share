from django import forms
from .models import Message
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


class NewMessageForm(forms.ModelForm):
    """
    Form to create new message.
    """
    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'content']
        widgets = {
            'sender': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['sender'].initial = self.user.id
        self.fields['recipient'].empty_label = '(Please select)'
        self.fields['recipient'].widget.attrs.update({'class': 'form-select select2'})
        self.fields['recipient'].queryset = self.user.following.all()
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
