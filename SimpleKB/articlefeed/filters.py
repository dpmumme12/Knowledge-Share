from django import forms
from django.contrib.auth import get_user_model
from django_filters import FilterSet, filters
from pkg_resources import empty_provider
from SimpleKB.knowledgebase.models import Article
from SimpleKB.knowledgebase.helpers import article_fulltext_search

USER_MODEL = get_user_model()

def get_following(request):
    if not request or not request.user.is_authenticated:
        return USER_MODEL.objects.none()

    return USER_MODEL.objects.get(id=request.user.id).following.all()

class ArticleFeedFilter(FilterSet):
    search_query = filters.CharFilter(
        label='Search:',
        method='search_filter',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'search...'})
    )
    min_date = filters.DateFilter(
        label='From date:',
        field_name="updated_on",
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    max_date = filters.DateFilter(
        label='To date:',
        field_name="updated_on",
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    author = filters.ModelMultipleChoiceFilter(
        field_name='author',
        queryset=get_following,
        widget=forms.SelectMultiple(attrs={'class': 'form-select multi-select2'})
    )

    class Meta:
        model = Article
        fields = []

    def search_filter(self, queryset, name, value):
        out_queryset = article_fulltext_search(queryset, value)
        out_queryset = out_queryset.order_by('-score')
        return out_queryset
