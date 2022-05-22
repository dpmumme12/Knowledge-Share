from django import forms
from django.contrib.auth import get_user_model
import django_filters
from SimpleKB.knowledgebase.models import Article
from SimpleKB.knowledgebase.helpers import article_fulltext_search

USER_MODEL = get_user_model()

def following(request):
    if not request.user.is_authenticated:
        return USER_MODEL.objects.none()

    return USER_MODEL.objects.get(id=request.user.id).following.all()

class NewsFeedFilter(django_filters.FilterSet):
    min_date = django_filters.filters.DateFilter(field_name="updated_on", lookup_expr='gte', widget=forms.DateInput(attrs={'type': 'date'}))
    max_date = django_filters.filters.DateFilter(field_name="updated_on", lookup_expr='lte')
    search_query = django_filters.filters.CharFilter(label='search query', method='my_custom_filter')
    author = django_filters.filters.ModelMultipleChoiceFilter(
        field_name='author',
        queryset=following,
    )

    class Meta:
        model = Article
        fields = ['updated_on']

    def my_custom_filter(self, queryset, name, value):
        out_queryset = article_fulltext_search(queryset, value)
        return out_queryset
