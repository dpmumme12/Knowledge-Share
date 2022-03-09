from django.urls import path, re_path
from .views import (DashboardView, KnowledgeBaseView, ArticleEditView,
                    ArticleDeleteView, ArticleImageUploadView)

app_name = 'knowledgebase'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('KnowledgeBase', KnowledgeBaseView.as_view(), name='knowledgebase'),
    path('Article/Create', ArticleEditView.as_view(), name='article_create'),
    path('Article/Edit/<int:article_id>', ArticleEditView.as_view(), name='article_edit'),
    path('Article/Delete.<int:pk>', ArticleDeleteView.as_view(), name='article_delete'),
    path('Article/ImageUpload', ArticleImageUploadView.as_view(), name='article_image_upload'),
]
