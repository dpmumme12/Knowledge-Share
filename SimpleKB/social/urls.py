from django.urls import path
from rest_framework.schemas import get_schema_view
from .views import DashboardView
from .api.views import FollowerListView, FollowingListView, FollowUnfollowView
from SimpleKB.utils.schema_generators import ServerSchemaGenerator


app_name = 'social'
urlpatterns = [
    path('dashboard/<str:username>', DashboardView.as_view(), name='dashboard'),

    path('api/followers/<int:pk>', FollowingListView.as_view(), name='following'),
    path('api/following/<int:pk>', FollowerListView.as_view(), name='followers'),
    path('api/follow-unfollow/<int:pk>', FollowUnfollowView.as_view(), name='follow_unfollow'),
    path('api/openapi', get_schema_view(title='SimpleKB.Social',
                                        description='API for the Social app in the project',
                                        generator_class=ServerSchemaGenerator,
                                        version='1.0.0'), name='openapi-schema'),
]
