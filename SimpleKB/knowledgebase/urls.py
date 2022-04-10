from django.urls import path, re_path
from .views.knowledgebase_views import (DashboardView, KnowledgeBaseView, FolderDeleteView,
                                        FolderEditView, BulkFolderChangeView, BulkDeleteView,
                                        KB_ArticleEditView)
from .views.article_views import (ArticleEditView, ArticleDeleteView, ArticleImageUploadView)

app_name = 'knowledgebase'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('KnowledgeBase', KnowledgeBaseView.as_view(), name='knowledgebase'),
    path('KnowledgeBase/<int:folder_id>', KnowledgeBaseView.as_view(), name='knowledgebase_id'),
    path('KnowledgeBase/Search', KnowledgeBaseView.as_view(), name='knowledgebase_search'),
    path('KnowledgeBase/Article/Edit/<int:pk>',
         KB_ArticleEditView.as_view(),
         name='kb_article_edit'),
    path('Folder/Edit/<int:pk>', FolderEditView.as_view(), name='folder_edit'),
    path('Folder/Delete/<int:pk>', FolderDeleteView.as_view(), name='folder_delete'),
    path('Folder/BulkChange', BulkFolderChangeView.as_view(), name='bulk_folder_change'),
    path('Folder/BulkDelete', BulkDeleteView.as_view(), name='bulk_delete'),
    path('Article/Create', ArticleEditView.as_view(), name='article_create'),
    path('Article/Edit/<int:article_id>', ArticleEditView.as_view(), name='article_edit'),
    path('Article/Delete/<int:pk>', ArticleDeleteView.as_view(), name='article_delete'),
    path('Article/ImageUpload', ArticleImageUploadView.as_view(), name='article_image_upload'),
]
