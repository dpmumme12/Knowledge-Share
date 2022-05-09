from rest_framework import serializers
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()

class UserFollowSerializer(serializers.ModelSerializer):
    is_following = serializers.BooleanField(default=False)

    class Meta:
        model = USER_MODEL
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_image', 'is_following']


class FollowUnFollowSerializer(serializers.Serializer):
    is_following = serializers.BooleanField(default=False)
    user_id = serializers.IntegerField()
