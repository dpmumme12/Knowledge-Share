from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import PageForm

# Create your views here.
class DashboardView(View):

    def get(self, request):
        return render(request, 'knowledgebase/dashboard.html')


class KnowledgeBaseView(View):

    def get(self, request):
        return render(request, 'knowledgebase/knowledgebase.html')


class EditorView(View):

    def get(self, request):
        return render(request, 'knowledgebase/editor.html', {
            'editor': PageForm()
        })


class ImageUploadView(View):

    def post(self, request):
        print(request.FILES['file'].content_type)
        return JsonResponse({'location': '/test'})
