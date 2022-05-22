from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import NewsFeedView
from .api.views import NewsFeedListView


app_name = 'newsfeed'
urlpatterns = [
    path('', NewsFeedView.as_view(), name='news_feed'),
    path('api/newsfeed', NewsFeedListView.as_view(), name='newsfeed_list'),
]
