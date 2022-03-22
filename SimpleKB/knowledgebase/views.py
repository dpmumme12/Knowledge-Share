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
from itertools import chain
from .forms import ArticleForm, CreateFolderForm, ChangeFolderForm, BulkDeleteForm
from .models import Article, ArticleImage, Folder

# Create your views here.
class DashboardView(View):
    template_name = 'knowledgebase/dashboard.html'

    def get(self, request):
        return render(request, self.template_name)


class KnowledgeBaseView(View):
    template_name = 'knowledgebase/knowledgebase.html'

    def get(self, request, folder_id=None):
        user_folders = Folder.UserFolders(request.user)
        create_folder_form = CreateFolderForm(folders=user_folders)

        folders = (Folder
                   .objects
                   .filter(owner=request.user, parent_folder=folder_id)
                   .annotate(object_type=Value('folder'))
                   .only('name')
                   )
        articles = (Article
                    .objects
                    .filter(author=request.user, folder=folder_id)
                    .annotate(name=F('title'), object_type=Value('article'))
                    .only('id')
                    )

        folder_content = folders.union(articles)

        return render(request, self.template_name, {
            'CreateFolderForm': create_folder_form,
            'ChangeFolderForm': ChangeFolderForm(),
            'BulkDeleteForm': BulkDeleteForm(),
            'folder_content': folder_content,
            'user_folders': [model_to_dict(folder) for folder in user_folders]
        })

    def post(self, request, **kwargs):
        user_folders = Folder.UserFolders(request.user)
        folder_form = CreateFolderForm(request.POST, folders=user_folders)

        if folder_form.is_valid():
            instance = folder_form.save(commit=False)
            instance.owner = request.user
            instance.save()

            messages.success(request, 'Folder created successfully!')
            return redirect('knowledgebase:knowledgebase')

        return render(request, self.template_name, {
            'CreateFolderForm': folder_form
        })


class FolderDeleteView(SuccessMessageMixin, DeleteView):
    model = Folder
    success_url = reverse_lazy('knowledgebase:knowledgebase')
    success_message = 'Folder deleted successfully!'


class FolderChangeView(View):
    def post(self, request):
        user_folders = Folder.UserFolders(request.user)
        change_folder_form = ChangeFolderForm(request.POST, folders=user_folders)
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


class ArticleEditView(View):
    template_name = 'knowledgebase/article_edit.html'

    def get(self, request, article_id=None):
        if article_id is None:
            article = Article.objects.create(
                author=request.user,
                title='Draft ' + datetime.now().strftime('%b %d %Y'),
                article_status=Article.Status.DRAFT
            )
            return redirect('knowledgebase:article_edit', article_id=article.id)

        current_article = get_object_or_404(Article, id=article_id)
        article_versions = (Article
                            .objects
                            .filter(uuid=current_article.uuid)
                            )
        return render(request, self.template_name, {
            'ArticleForm': ArticleForm(instance=current_article),
            'article_versions': article_versions,
            'article': current_article,
        })

    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        article.article_status = request.POST['SubmitButton']
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()

            return redirect('knowledgebase:knowledgebase')
        else:
            return render(request, self.template_name, {
                'ArticleForm': form,
                'article': article})


class ArticleDeleteView(SuccessMessageMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('knowledgebase:knowledgebase')
    success_message = 'Article deleted successfully!'


class ArticleImageUploadView(View):

    def post(self, request):
        if 'file' in request.FILES:
            article = (Article
                       .objects
                       .get(id=request.POST['article_id'])
                       )
            image = ArticleImage.objects.create(
                article_id=article,
                image=request.FILES['file']
            )
            return JsonResponse({'location': image.image.url})
        else:
            return JsonResponse('No image found', safe=False)
