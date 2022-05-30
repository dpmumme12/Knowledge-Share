from django.contrib import admin
from .models import Folder, Article, ArticleImage, Article_User
# Register your models here

admin.site.register(Folder)
admin.site.register(Article)
admin.site.register(ArticleImage)
admin.site.register(Article_User)
