from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import ArticleFeedView
from .api.views import ArticleFeedListView


app_name = 'articlefeed'
urlpatterns = [
    path('', ArticleFeedView.as_view(), name='article_feed'),
    path('api/articlefeed', ArticleFeedListView.as_view(), name='article_list'),
]
