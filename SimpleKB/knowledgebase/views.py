from re import template
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.views.generic import View, DeleteView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from datetime import datetime
from .forms import ArticleForm, FolderForm
from .models import Article, ArticleImage, Folder

# Create your views here.
class DashboardView(View):
    template_name = 'knowledgebase/dashboard.html'

    def get(self, request):
        return render(request, self.template_name)


class KnowledgeBaseView(View):
    template_name = 'knowledgebase/knowledgebase.html'

    def get(self, request):
        folders = list(Folder.objects.filter(owner=request.user))
        folder_form = FolderForm(user=request.user)
        folder_form.fields['parent_folder'].choices += [(folder.id, folder.name)
                                                        for folder in folders]
        return render(request, self.template_name, {
            'FolderForm': folder_form,
            'folders': folders
        })

    def post(self, request):
        folder_form = FolderForm(request.POST, user=request.user)
        if folder_form.is_valid():
            instance = folder_form.save(commit=False)
            instance.owner = request.user
            instance.save()

            messages.success(request, 'Folder created successfully!')
            return redirect('knowledgebase:knowledgebase')

        return render(request, self.template_name, {
            'FolderForm': folder_form
        })


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
        article_versions = Article.objects.filter(uuid=current_article.uuid)
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


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('knowledgebase:knowledgebase')


class ArticleImageUploadView(View):

    def post(self, request):
        if 'file' in request.FILES:
            article = Article.objects.get(id=request.POST['article_id'])
            image = ArticleImage.objects.create(
                article_id=article,
                image=request.FILES['file']
            )
            return JsonResponse({'location': image.image.url})
        else:
            return JsonResponse('No image found', safe=False)
