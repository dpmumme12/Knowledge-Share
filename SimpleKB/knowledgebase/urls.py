from django.urls import path
from .views import DashboardView, KnowledgeBaseView, EditorView

app_name = 'knowledgebase'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('KnowledgeBase', KnowledgeBaseView.as_view(), name='knowledgebase'),
    path('Editor', EditorView.as_view(), name='editor')
]
