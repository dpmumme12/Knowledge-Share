from django.urls import path
from .views import ArticleFeedView
from .api.views import ArticleFeedListView


app_name = 'articlefeed'
urlpatterns = [
    path('', ArticleFeedView.as_view(), name='article_feed'),

    # API urls
    path('api/articlefeed', ArticleFeedListView.as_view(), name='article_list'),
]
