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


class CreateFolderForm(forms.ModelForm):

    class Meta:
        model = Folder
        fields = ['name', 'parent_folder']

    def __init__(self, *args, **kwargs):
        self.folders = kwargs.pop('folders', None)
        super().__init__(*args, **kwargs)
        self.fields['parent_folder'].widget.attrs.update({'class': 'form-select'})
        self.fields['parent_folder'].label = "Folder"
        self.fields['parent_folder'].choices = [("", "(Root)")] + [(folder.id, folder.name)
                                                                   for folder in self.folders]
        self.fields['name'].widget.attrs.update({'class': 'form-control'})


class ChangeFolderForm(forms.Form):
    folder = forms.ChoiceField(required=False)
    objects = forms.JSONField(label='')

    def __init__(self, *args, **kwargs):
        self.folders = kwargs.pop('folders', None)
        super().__init__(*args, **kwargs)
        self.fields['objects'].widget.attrs.update({'hidden': ''})
        self.fields['folder'].widget.attrs.update({'class': 'form-select'})
        self.fields['folder'].choices = [("", "(Root)")] + [(folder.id, folder.name)
                                                            for folder in self.folders]
