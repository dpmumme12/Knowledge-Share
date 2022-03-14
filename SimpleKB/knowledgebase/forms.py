from django import forms
from tinymce.widgets import TinyMCE
from .models import Article, Folder

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'content']
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})


class FolderForm(forms.ModelForm):

    class Meta:
        model = Folder
        fields = ['name', 'parent_folder']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['parent_folder'].widget.attrs.update({'class': 'form-select'})
        self.fields['parent_folder'].label = "Folder"
        self.fields['parent_folder'].choices = [("", "(Root)")]
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
