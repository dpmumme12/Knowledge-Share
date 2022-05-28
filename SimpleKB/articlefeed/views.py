from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import get_user_model
from .filters import ArticleFeedFilter

USER_MODEL = get_user_model()

# Create your views here.
class ArticleFeedView(View):
    template_name = 'articlefeed/articlefeed.html'

    def get(self, request, *args, **kwargs):
        filter_form = ArticleFeedFilter(request=request)
        return render(request, self.template_name, {'filter_form': filter_form})
