from django.urls import path
from .views.knowledgebase_views import (KnowledgeBaseView, FolderDeleteView,
                                        FolderEditView, BulkFolderChangeView, BulkDeleteView,
                                        KB_ArticleEditView)
from .views.article_views import (ArticleView, ArticleEditView, ArticleDeleteView,
                                  ArticleImageUploadView, RemoveForeignArticleView)

app_name = 'knowledgebase'
urlpatterns = [
    path('article/<int:article_id>', ArticleView.as_view(), name='article'),
    path('article/create', ArticleEditView.as_view(), name='article_create'),
    path('article/edit/<int:article_id>', ArticleEditView.as_view(), name='article_edit'),
    path('article/delete/<int:pk>', ArticleDeleteView.as_view(), name='article_delete'),
    path('article/image-upload', ArticleImageUploadView.as_view(), name='article_image_upload'),
    path('article/remove-foreign/<int:article_id>',
         RemoveForeignArticleView.as_view(),
         name='article_remove_foreign'),

    path('folder/edit/<int:pk>', FolderEditView.as_view(), name='folder_edit'),
    path('folder/delete/<int:pk>', FolderDeleteView.as_view(), name='folder_delete'),
    path('folder/bulk-change', BulkFolderChangeView.as_view(), name='bulk_folder_change'),
    path('folder/bulk-delete', BulkDeleteView.as_view(), name='bulk_delete'),

    path('kb/<str:username>', KnowledgeBaseView.as_view(), name='kb'),
    path('kb/<str:username>/<int:folder_id>', KnowledgeBaseView.as_view(), name='kb_id'),
    path('kb/<str:username>/Search', KnowledgeBaseView.as_view(), name='kb_search'),
    path('kb/article/edit/<int:pk>', KB_ArticleEditView.as_view(), name='kb_article_edit'),
]
