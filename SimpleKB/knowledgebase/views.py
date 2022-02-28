from django.shortcuts import render
from django.views.generic import View
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
