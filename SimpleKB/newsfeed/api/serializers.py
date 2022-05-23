from django.contrib.auth import get_user_model
from rest_framework import serializers
from SimpleKB.knowledgebase.models import Article

USER_MODEL = get_user_model()

class NewsFeedSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_author_username')
    profile_img = serializers.SerializerMethodField('get_author_profile_img')

    class Meta:
        model = Article
        fields = ['id', 'username', 'profile_img', 'title', 'truncated_content', 'updated_on']

    def get_author_username(self, obj):
        if obj.author:
            return obj.author.username
        return None

    def get_author_profile_img(self, obj):
        if obj.author and obj.author.profile_image:
            return obj.author.profile_image.url
        return None
