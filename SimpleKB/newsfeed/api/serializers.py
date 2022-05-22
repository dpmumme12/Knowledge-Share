from django.contrib.auth import get_user_model
from django.utils.html import strip_tags
from django.utils.text import Truncator
from rest_framework import serializers
from SimpleKB.knowledgebase.models import Article

USER_MODEL = get_user_model()

class NewsFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'author', 'title', 'content', 'updated_on']
