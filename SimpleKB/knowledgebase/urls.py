from django.urls import path, re_path
from .views import DashboardView, KnowledgeBaseView, EditorView, ImageUploadView

app_name = 'knowledgebase'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('KnowledgeBase', KnowledgeBaseView.as_view(), name='knowledgebase'),
    path('Editor', EditorView.as_view(), name='editor'),
    path('Editor/<int:article_id>', EditorView.as_view(), name='editor_id'),
    path('ImageUpload', ImageUploadView.as_view(), name='image'),
]
