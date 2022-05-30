from django.urls import path
from rest_framework.schemas import get_schema_view
from KnowledgeShare.utils.api.schema_generators import ServerSchemaGenerator
from .views import DashboardView, MessagesView, NewMessageView, MessageDetailView
from .api.views import (FollowerListView, FollowingListView, FollowUnfollowView,
                        MessagesListView, NotificationsListView)


app_name = 'social'
urlpatterns = [
    path('dashboard/<str:username>', DashboardView.as_view(), name='dashboard'),
    path('messages', MessagesView.as_view(), name='messages'),
    path('messages/create', NewMessageView.as_view(), name='new_message'),
    path('messages/detail/<str:username>', MessageDetailView.as_view(), name='message_detail'),


    # API endpoints
    path('api/following/<int:pk>', FollowingListView.as_view(), name='following'),
    path('api/followers/<int:pk>', FollowerListView.as_view(), name='followers'),
    path('api/follow-unfollow/<int:pk>', FollowUnfollowView.as_view(), name='follow_unfollow'),
    path('api/notifications', NotificationsListView.as_view(), name='notifications'),
    path('api/messages', MessagesListView.as_view(), name='message_api'),
    path('api/openapi', get_schema_view(title='KnowledgeShare.Social',
                                        description='API for the Social app in the project',
                                        generator_class=ServerSchemaGenerator,
                                        version='1.0.0'), name='openapi-schema'),
]
