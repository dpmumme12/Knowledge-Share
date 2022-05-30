from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import View, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from ..forms import (FolderForm, BulkChangeFolderForm, BulkDeleteForm,
                     SearchForm, ArticleHeaderForm)
from ..models import Article, Folder
from ..helpers import search_knowledgebase, get_knowledgebase


# Create your views here.
class KnowledgeBaseView(View):
    template_name = 'knowledgebase/knowledgebase.html'

    def get(self, request, **kwargs):
        user_model = get_user_model()
        folder_id = kwargs.pop('folder_id', None)
        username = kwargs.pop('username', None)
        kb_user = user_model.objects.get(username=username)
        current_folder = None
        user_folders = Folder.UserFolders(kb_user)

        # Getting the parent folders for the breadcrumb links
        if folder_id:
            current_folder = (Folder
                              .objects
                              .filter(id=folder_id)
                              .select_related('parent_folder__parent_folder')
                              .get()
                              )

        # Initializing forms for the page
        search_form = SearchForm(request.GET)
        article_header_form = ArticleHeaderForm(folders=user_folders)
        create_folder_form = FolderForm(folder_id=folder_id,
                                        folders=user_folders,
                                        prefix='create_folder')
        edit_folder_form = FolderForm(folder_id=folder_id,
                                      prefix='edit_folder')

        # Query's to get the current folders content if search is provided
        if search_form.data.get('query') and search_form.is_valid():
            query = search_form.cleaned_data['query']
            folder_content = search_knowledgebase(query, kb_user, request.user)

        else:
            folder_content = get_knowledgebase(folder_id, kb_user, request.user)

        paginator = Paginator(folder_content, 15)
        page_number = request.GET.get('page')
        folder_content = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'current_folder': current_folder,
            'SearchForm': search_form,
            'ArticleHeaderForm': article_header_form,
            'CreateFolderForm': create_folder_form,
            'EditFolderForm': edit_folder_form,
            'BulkChangeFolderForm': BulkChangeFolderForm(),
            'BulkDeleteForm': BulkDeleteForm(),
            'folder_content': folder_content,
            'user_folders': [model_to_dict(folder) for folder in user_folders],
            'kb_user': kb_user
        })

    def post(self, request, **kwargs):
        folder_id = kwargs.pop('folder_id', None)
        username = kwargs.pop('username', None)
        user_folders = Folder.UserFolders(request.user)
        create_folder_form = FolderForm(request.POST, folders=user_folders, prefix='create_folder')

        if create_folder_form.is_valid():
            instance = create_folder_form.save(commit=False)
            instance.owner = request.user
            instance.save()
            messages.success(request, 'Folder created successfully!')
        else:
            messages.error(request, create_folder_form.errors.as_json(escape_html=True))

        if folder_id:
            return redirect('knowledgebase:kb_id', username=username, folder_id=folder_id)

        return redirect('knowledgebase:kb', username=username)


class KB_ArticleEditView(LoginRequiredMixin, View):
    """
    View to update just the header information of an Article
    """

    def post(self, request, **kwargs):
        article_id = kwargs.pop('pk', None)
        instance = Article.objects.get(id=article_id)
        article_header_form = ArticleHeaderForm(request.POST, instance=instance)
        if article_header_form.is_valid():
            article_header_form.save()
            messages.success(request, 'Article updated successfully!')
        else:
            messages.error(request, article_header_form.errors.as_json(escape_html=True))

        return redirect('knowledgebase:kb', username=request.user.username)


class FolderEditView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        folder_id = kwargs.pop('pk', None)
        user_folders = Folder.UserFolders(request.user)
        instance = Folder.objects.get(id=folder_id)
        edit_folder_form = FolderForm(request.POST,
                                      folders=user_folders,
                                      instance=instance,
                                      prefix='edit_folder')
        if edit_folder_form.is_valid():
            edit_folder_form.save()
            messages.success(request, 'Folder updated successfully!')
        else:
            messages.error(request, edit_folder_form.errors.as_json(escape_html=True))

        return redirect('knowledgebase:kb', username=request.user.username)


class FolderDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Folder
    success_message = 'Folder deleted successfully!'

    def get_success_url(self):
        return reverse_lazy('knowledgebase:kb', kwargs={'username': self.request.user.username})


class BulkFolderChangeView(LoginRequiredMixin, View):
    def post(self, request):
        user_folders = Folder.UserFolders(request.user)
        change_folder_form = BulkChangeFolderForm(request.POST, folders=user_folders)
        if change_folder_form.is_valid():
            change_folder_form.update()
            messages.success(request, 'Folders updated successfully!')
        else:
            messages.error(request, change_folder_form.errors.as_json(escape_html=True))

        return redirect('knowledgebase:kb', username=request.user.username)


class BulkDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        bulk_delete_form = BulkDeleteForm(request.POST)
        if bulk_delete_form.is_valid():
            bulk_delete_form.delete()
            messages.success(request, 'Deleted successfully!')
        else:
            messages.error(request, bulk_delete_form.errors.as_json(escape_html=True))

        return redirect('knowledgebase:kb', username=request.user.username)
