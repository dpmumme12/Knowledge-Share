from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.views.generic import View, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import F, Value
from django.forms.models import model_to_dict
from datetime import datetime
from ..forms import (ArticleForm, FolderForm, BulkChangeFolderForm, BulkDeleteForm,
                     SearchForm, ArticleHeaderForm)
from ..models import Article, ArticleImage, Folder
from ..helpers import search_knowledgebase

# Create your views here.
class DashboardView(View):
    template_name = 'knowledgebase/dashboard.html'

    def get(self, request):
        return render(request, self.template_name)


class KnowledgeBaseView(View):
    template_name = 'knowledgebase/knowledgebase.html'

    def get(self, request, **kwargs):
        folder_id = kwargs.pop('folder_id', None)

        if folder_id:
            current_folder = (Folder
                              .objects
                              .filter(id=folder_id)
                              .select_related('parent_folder__parent_folder')
                              .get()
                              )
        else:
            current_folder = None

        search_form = SearchForm(request.GET)
        user_folders = Folder.UserFolders(request.user)
        article_header_form = ArticleHeaderForm(folders=user_folders)
        create_folder_form = FolderForm(folder_id=folder_id,
                                        folders=user_folders,
                                        prefix='create_folder')
        edit_folder_form = FolderForm(folder_id=folder_id,
                                      prefix='edit_folder')

        if 'query' in request.GET and search_form.is_valid():
            query = search_form.cleaned_data['query']
            folder_content = search_knowledgebase(query, request.user)

        else:
            folders = (Folder
                       .objects
                       .filter(owner=request.user, parent_folder=folder_id)
                       .annotate(object_type=Value('folder'), directory=F('parent_folder'))
                       .only('name')
                       )
            articles = (Article
                        .objects
                        .filter(author=request.user, folder=folder_id)
                        .annotate(name=F('title'),
                                  object_type=Value('article'),
                                  directory=F('folder'))
                        .only('id')
                        )

            folder_content = folders.union(articles)

        return render(request, self.template_name, {
            'current_folder': current_folder,
            'SearchForm': search_form,
            'ArticleHeaderForm': article_header_form,
            'CreateFolderForm': create_folder_form,
            'EditFolderForm': edit_folder_form,
            'BulkChangeFolderForm': BulkChangeFolderForm(),
            'BulkDeleteForm': BulkDeleteForm(),
            'folder_content': folder_content,
            'user_folders': [model_to_dict(folder) for folder in user_folders]
        })

    def post(self, request, **kwargs):
        folder_id = kwargs.pop('folder_id', None)
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
            return redirect('knowledgebase:knowledgebase_id', folder_id=folder_id)

        return redirect('knowledgebase:knowledgebase')


class KB_ArticleEditView(View):
    def post(self, request, **kwargs):
        article_id = kwargs.pop('pk', None)
        instance = Article.objects.get(id=article_id)
        article_header_form = ArticleHeaderForm(request.POST, instance=instance)
        if article_header_form.is_valid():
            article_header_form.save()
            messages.success(request, 'Folder updated successfully!')
        else:
            messages.error(request, article_header_form.errors.as_json(escape_html=True))

        return redirect('knowledgebase:knowledgebase')


class FolderEditView(View):
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

        return redirect('knowledgebase:knowledgebase')


class FolderDeleteView(SuccessMessageMixin, DeleteView):
    model = Folder
    success_url = reverse_lazy('knowledgebase:knowledgebase')
    success_message = 'Folder deleted successfully!'


class BulkFolderChangeView(View):
    def post(self, request):
        user_folders = Folder.UserFolders(request.user)
        change_folder_form = BulkChangeFolderForm(request.POST, folders=user_folders)
        if change_folder_form.is_valid():
            change_folder_form.update()

            messages.success(request, 'Folders updated successfully!')
            return redirect('knowledgebase:knowledgebase')

        messages.error(request, change_folder_form.errors.as_json(escape_html=True))
        return redirect('knowledgebase:knowledgebase')


class BulkDeleteView(View):
    def post(self, request):
        bulk_delete_form = BulkDeleteForm(request.POST)
        if bulk_delete_form.is_valid():
            bulk_delete_form.delete()

            messages.success(request, 'Deleted successfully!')
            return redirect('knowledgebase:knowledgebase')

        messages.error(request, bulk_delete_form.errors.as_json(escape_html=True))
        return redirect('knowledgebase:knowledgebase')