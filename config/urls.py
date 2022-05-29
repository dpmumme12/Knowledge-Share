"""simpleKB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView

urlpatterns = [
    path('',
         TemplateView.as_view(template_name='landingpage/landingpage.html'),
         name='landing_page'),
    path('admin/', admin.site.urls),
    path('social/', include('KnowledgeShare.social.urls', namespace='social')),
    path('users/', include('KnowledgeShare.users.urls', namespace='users')),
    path('articlefeed/', include('KnowledgeShare.articlefeed.urls', namespace='articlefeed')),
    path('tinymce/', include('tinymce.urls')),
    path('knowledgebase/',
         include('KnowledgeShare.knowledgebase.urls', namespace='knowledgebase')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
