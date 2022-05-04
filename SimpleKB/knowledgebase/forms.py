from django import forms
from django.forms.models import model_to_dict
from tinymce.widgets import TinyMCE
from .models import Article, Folder, Article_User


class ArticleForm(forms.ModelForm):
    """
    Form to create/edit an article.
    """
    class Meta:
        model = Article
        fields = ['title', 'content', 'folder']
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].required = True
        self.fields['folder'].widget.attrs.update({'class': 'form-select'})
        self.fields['folder'].empty_label = '(Root)'
        self.fields['folder'].queryset = Folder.objects.filter(owner=self.user)


class ArticleHeaderForm(forms.ModelForm):
    """
    Form to edit the title and folder for an article.

    Args:
        (folders) optional: folder options for the parent_folder field.
    """
    prefix = 'article_header'

    class Meta:
        model = Article
        fields = ['title', 'folder']

    def __init__(self, *args, **kwargs):
        self.folders = kwargs.pop('folders', None)
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['folder'].widget.attrs.update({'class': 'form-select'})
        self.fields['folder'].choices = [("", "(Root)")]
        if self.folders:
            self.fields['folder'].choices += [(folder.id, folder.name)
                                              for folder in self.folders]

class FolderForm(forms.ModelForm):
    """
    Form to create/edit folder.

    Args:
        (folders) optional: folder options for the parent_folder field.
        (folder_id) optional: Set the default selected folder.

    Raises:
        forms.ValidationError: if chosen parent_folder will cause folder structure
        inconsistency.
    """
    class Meta:
        model = Folder
        fields = ['name', 'parent_folder']

    def __init__(self, *args, **kwargs):
        self.folders = kwargs.pop('folders', None)
        self.folder_id = kwargs.pop('folder_id', None)
        super().__init__(*args, **kwargs)
        self.fields['parent_folder'].widget.attrs.update({'class': 'form-select'})
        self.fields['parent_folder'].label = "Folder"
        self.fields['parent_folder'].choices = [("", "(Root)")]
        if self.folders:
            self.fields['parent_folder'].choices += [(folder.id, folder.name)
                                                     for folder in self.folders]
        if self.folder_id:
            self.fields['parent_folder'].initial = self.folder_id
        self.fields['name'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        parent_folder = cleaned_data['parent_folder']
        if self.instance.id and parent_folder:
            if self.instance.id == parent_folder.id:
                raise forms.ValidationError('Operation will cause folder inconsistency')

            sub_folders = BulkChangeFolderForm.get_sub_folders(model_to_dict(self.instance),
                                                               self.folders)
            print(sub_folders)
            folder_id_in_sub_folders = list(filter(lambda x: x['id'] == int(parent_folder.id),
                                            sub_folders))
            print(folder_id_in_sub_folders)
            if folder_id_in_sub_folders:
                raise forms.ValidationError('Operation will cause folder inconsistency')

        return cleaned_data


class SearchForm(forms.Form):
    """
    Search form that provides one text input
    to get a query.
    """
    query = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['query'].label = ''
        self.fields['query'].required = False
        self.fields['query'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Search...'})


class BulkChangeFolderForm(forms.Form):
    """
    Form to change the folder for multiple
    folders and articles.

    Args:
        (folders) optional: folder options for the parent_folder field.

    Raises:
        forms.ValidationError: if chosen parent_folder will cause folder structure
        inconsistency.
    """
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

            sub_folders = self.get_sub_folders(folder, self.folders)
            folder_id_in_sub_folders = list(filter(lambda x: x['id'] == int(folder_id),
                                                   sub_folders))
            if folder_id_in_sub_folders:
                raise forms.ValidationError('Operation will cause folder inconsistency')

        return cleaned_data

    @staticmethod
    def get_sub_folders(folder, in_folders):
        """
        Gets all of folders that are inside the input folder.

        Args:
            folder (dict): Takes the dict of a Folder insatnce ex: model_to_dict(Folder)
            in_folders (list): Takes in a list of Folder instances ex: [folder1, folder2, folder3]

        Returns:
            list: list of all folders below the input folder
        """
        folders = [model_to_dict(folder) for folder in in_folders]
        sub_folders = list(filter(lambda x: x['parent_folder'] == int(folder['id']), folders))
        out_sub_folders = sub_folders

        for folder in sub_folders:
            sub = BulkChangeFolderForm.get_sub_folders(folder, in_folders)
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
    """
    Form to bulk delete multiple folders and articles
    at the same time.
    """
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


class ArticleUserForm(forms.ModelForm):
    """
    Form for users to add another users article to
    their knowledgebase.
    """
    class Meta:
        model = Article_User
        fields = ['article', 'user', 'folder']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['article'].widget = forms.HiddenInput()
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['folder'].widget.attrs.update({'class': 'form-select'})
        self.fields['folder'].empty_label = '(Root)'
        self.fields['folder'].queryset = Folder.objects.filter(owner=self.user)
