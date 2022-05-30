from django.contrib.auth import get_user_model
from rest_framework import serializers
from KnowledgeShare.knowledgebase.models import Article

USER_MODEL = get_user_model()


class ArticleFeedSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_author_username')
    profile_img = serializers.SerializerMethodField('get_author_profile_img')
    full_name = serializers.SerializerMethodField('get_author_full_name')

    class Meta:
        model = Article
        fields = ['id', 'username', 'full_name', 'profile_img', 'title',
                  'truncated_content', 'updated_on']

    def get_author_username(self, obj):
        if obj.author:
            return obj.author.username
        return None

    def get_author_profile_img(self, obj):
        if obj.author and obj.author.profile_image:
            return obj.author.profile_image.url
        return None

    def get_author_full_name(self, obj):
        if obj.author and (obj.author.first_name or obj.author.last_name):
            return obj.author.first_name + ' ' + obj.author.last_name
        return ''
