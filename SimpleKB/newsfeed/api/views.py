from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef, Q
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.schemas.openapi import AutoSchema
from django_filters import rest_framework as filters
from SimpleKB.utils.api.schema_generators import SerializerSchemaMixin
from SimpleKB.utils.api.pagination import SmallResultSetPagination
from SimpleKB.knowledgebase.models import Article
from .serializers import NewsFeedSerializer
from ..filters import NewsFeedFilter

USER_MODEL = get_user_model()

class NewsFeedListView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = NewsFeedSerializer
    pagination_class = SmallResultSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NewsFeedFilter
