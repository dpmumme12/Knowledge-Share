from django import forms
from django.forms.models import model_to_dict
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
    prefix = 'change_folder'
    folder = forms.ChoiceField(required=False)
    objects = forms.JSONField(label='')

    def __init__(self, *args, **kwargs):
        self.folders = kwargs.pop('folders', None)
        super().__init__(*args, **kwargs)
        self.fields['objects'].widget.attrs.update({'hidden': ''})
        self.fields['folder'].widget.attrs.update({'class': 'form-select'})
        self.fields['folder'].choices = [("", "(Root)")]
        if self.folders:
            self.fields['folder'].choices += [(folder.id, folder.name)
                                              for folder in self.folders]

    def clean(self):
        cleaned_data = super().clean()
        folder_id = cleaned_data.get('folder')
        if not folder_id:
            return cleaned_data

        items = cleaned_data.get('objects')
        folders = filter(lambda x: x['object_type'] == 'folder', items)
        for folder in folders:
            if folder['id'] == folder_id:
                raise forms.ValidationError('Operation will cause folder inconsistency')

            sub_folders = self.get_sub_folders(folder)
            folder_id_in_sub_folders = list(filter(lambda x: x['id'] == int(folder_id),
                                                   sub_folders))
            if folder_id_in_sub_folders:
                raise forms.ValidationError('Operation will cause folder inconsistency')

        return cleaned_data

    def get_sub_folders(self, folder):
        folders = [model_to_dict(folder) for folder in self.folders]
        sub_folders = list(filter(lambda x: x['parent_folder'] == int(folder['id']), folders))
        out_sub_folders = sub_folders

        for folder in sub_folders:
            sub = self.get_sub_folders(folder)
            out_sub_folders += sub

        return out_sub_folders

    def update(self):
        folder_id = self.cleaned_data['folder']
        items = self.cleaned_data['objects']
        articles = list(filter(lambda x: x['object_type'] == 'article', items))
        articles = [article['id'] for article in articles]
        folders = list(filter(lambda x: x['object_type'] == 'folder', items))
        folders = [folder['id'] for folder in folders]

        if articles:
            Article.objects.filter(id__in=articles).update(folder=folder_id)
        if folders:
            Folder.objects.filter(id__in=folders).update(parent_folder=folder_id)


class BulkDeleteForm(forms.Form):
    prefix = 'bulk_delete'
    objects = forms.JSONField(label='', widget=forms.Textarea(attrs={'hidden': ''}))

    def delete(self):
        items = self.cleaned_data['objects']
        articles = list(filter(lambda x: x['object_type'] == 'article', items))
        articles = [article['id'] for article in articles]
        folders = list(filter(lambda x: x['object_type'] == 'folder', items))
        folders = [folder['id'] for folder in folders]

        if articles:
            Article.objects.filter(id__in=articles).delete()
        if folders:
            Folder.objects.filter(id__in=folders).delete()
