from django.urls import path
from .views import Index

app_name = 'knowledgebase'
urlpatterns = [
    path('', Index.as_view(), name='index')
]
