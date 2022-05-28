from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from SimpleKB.utils.api.pagination import SmallResultSetPagination
from SimpleKB.knowledgebase.models import Article
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
        return queryset
