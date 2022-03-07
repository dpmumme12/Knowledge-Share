from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View, DeleteView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime
from .forms import ArticleForm
from .models import Article, ArticleImage

# Create your views here.
class DashboardView(View):

    def get(self, request):
        return render(request, 'knowledgebase/dashboard.html')


class KnowledgeBaseView(View):

    def get(self, request):
        return render(request, 'knowledgebase/knowledgebase.html')


class EditorView(View):
    template_name = 'knowledgebase/editor.html'

    def get(self, request, article_id=None):
        if article_id is None:
            article = Article.objects.create(
                author=request.user,
                title='Draft ' + datetime.now().strftime('%b %d %Y'),
                article_status=Article.Status.DRAFT
            )
            return redirect('knowledgebase:editor_id', article_id=article.id)

        article = get_object_or_404(Article, id=article_id)
        return render(request, self.template_name, {
            'ArticleForm': ArticleForm(instance=article),
            'article': article,
        })

    def post(self, request, article_id, **kwargs):
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


class ImageUploadView(View):

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
