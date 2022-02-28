from django import forms
from froala_editor.widgets import FroalaEditor

class PageForm(forms.Form):
    content = forms.CharField(widget=FroalaEditor())
