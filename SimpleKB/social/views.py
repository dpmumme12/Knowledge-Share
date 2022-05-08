from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.views.generic import View, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import F, Value
from django.forms.models import model_to_dict
from django.core.paginator import Paginator

# Create your views here.
class DashboardView(View):
    template_name = 'social/dashboard.html'

    def get(self, request, *args, **kwargs):
        username = kwargs.pop('username', None)
        dasboard_user = get_user_model().objects.get(username=username)
        return render(request, self.template_name, {'dashboard_user': dasboard_user})
