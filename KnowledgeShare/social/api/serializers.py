from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Message, Notification

USER_MODEL = get_user_model()


class FollowUnFollowSerializer(serializers.Serializer):
    is_following = serializers.BooleanField()
    user_id = serializers.IntegerField()


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'content', 'message_sent_date']


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'user', 'seen', 'created_on']


class UserFollowSerializer(serializers.ModelSerializer):
    is_following = serializers.BooleanField(default=False)

    class Meta:
        model = USER_MODEL
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_image', 'is_following']
