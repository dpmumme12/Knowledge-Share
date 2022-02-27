from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from froala_editor.widgets import FroalaEditor
from django import forms

# Create your views here.
class Index(View):

    def get(self, request):
        return render(request, 'knowledgebase/index.html')
