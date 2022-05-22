from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.views.generic import View, DeleteView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import F, Value, Q, Max, Sum, Subquery, OuterRef
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from SimpleKB.knowledgebase.models import Article

USER_MODEL = get_user_model()

# Create your views here.
class NewsFeedView(View):
    template_name = 'newsfeed/newsfeed.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
