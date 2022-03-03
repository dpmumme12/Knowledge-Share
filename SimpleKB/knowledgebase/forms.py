from django import forms
from tinymce.widgets import TinyMCE

class PageForm(forms.Form):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
