from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from KnowledgeShare.utils.api.pagination import SmallResultSetPagination
from KnowledgeShare.knowledgebase.models import Article
from ..filters import ArticleFeedFilter
from .serializers import ArticleFeedSerializer

USER_MODEL = get_user_model()

class ArticleFeedListView(ListAPIView):
    serializer_class = ArticleFeedSerializer
    pagination_class = SmallResultSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ArticleFeedFilter

    def get_queryset(self):
        queryset = (Article
                    .objects
                    .filter(article_status_id=Article.Article_Status.PUBLISHED)
                    .order_by('-updated_on')
                    )
        if self.request.user.is_authenticated:
            queryset = queryset.filter(~Q(author=self.request.user.id))
        return queryset
