from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.views.generic import View, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from datetime import datetime
from ..forms import ArticleForm
from ..models import Article, ArticleImage, Folder
from ..helpers import publish_article, create_new_version


class ArticleView(View):
    template_name = 'knowledgebase/article_view.html'

    def get(self, request, **kwargs):
        article_id = kwargs.pop('article_id', None)
        return render(request, self.template_name)


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
        form = ArticleForm(request.POST, instance=article)
        submit_type = int(request.POST['SubmitButton'])
        if submit_type == Article.Version_Status.NEW_VERSION:
            create_new_version(article)

        if form.is_valid():
            form.save()
            if submit_type == Article.Article_Status.PUBLISHED:
                publish_article(article)
                messages.success(request, 'Article published successfully!')
            else:
                messages.success(request, 'Article saved successfully!')
            return redirect('knowledgebase:kb', username=request.user.username)
        else:
            return render(request, self.template_name, {
                'ArticleForm': form,
                'article': article})


class ArticleDeleteView(SuccessMessageMixin, DeleteView):
    model = Article
    success_message = 'Article deleted successfully!'

    def get_success_url(self):
        return reverse_lazy('knowledgebase:kb', kwargs={'username': self.request.user.username})


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
