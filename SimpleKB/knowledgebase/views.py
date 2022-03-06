from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import PageForm
from .models import Article, ArticleImage

# Create your views here.
class DashboardView(View):

    def get(self, request):
        return render(request, 'knowledgebase/dashboard.html')


class KnowledgeBaseView(View):

    def get(self, request):
        return render(request, 'knowledgebase/knowledgebase.html')


class EditorView(View):

    def get(self, request, article_id=None):
        if article_id is None:
            article = Article.objects.create(
                author=request.user,
                article_status=Article.Status.DRAFT
            )

        return render(request, 'knowledgebase/editor.html', {
            'editor': PageForm(),
            'article': article,
        })


class ImageUploadView(View):

    def post(self, request):
        article = Article.objects.get(id=request.POST['article_id'])
        image = ArticleImage.objects.create(
            article_id=article,
            image=request.FILES['file']
        )
        return JsonResponse({'location': image.image.url})
