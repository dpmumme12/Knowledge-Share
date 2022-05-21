from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef, Q
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.schemas.openapi import AutoSchema
from SimpleKB.utils.schema_generators import SerializerSchemaMixin
from .serializers import (UserFollowSerializer, FollowUnFollowSerializer,
                          MessagesSerializer, NotificationsSerializer)
from .pagination import SmallResultSetPagination
from ..models import Message, Notification

USER_MODEL = get_user_model()


class FollowingListView(ListAPIView):
    """
    List all of the user's the user is following
    ````````````````````````````````````````````
    Returns a list of users that the user is following.
    :param integer pk: the ID of the user to retrieve following for.
    """

    schema = AutoSchema(operation_id_base='Following')
    serializer_class = UserFollowSerializer

    def get_queryset(self):
        requested_user = self.request.user
        print(self.request.method)
        query = (USER_MODEL
                 .objects
                 .get(id=self.kwargs['pk'])
                 .following
                 .all()
                 )
        if requested_user.is_authenticated:
            query = (query
                     .annotate(is_following=Exists(USER_MODEL
                                                   .objects
                                                   .get(id=requested_user.id)
                                                   .following
                                                   .filter(id=OuterRef('pk'))
                                                   )
                               )
                     )
        return query


class FollowerListView(ListAPIView):
    """
    List all of the users followers
    ```````````````````````````````
    Returns a list of users that are following the input user.
    :param integer pk: the ID of the user to retrieve followers for.
    """

    schema = AutoSchema(operation_id_base='Followers')
    serializer_class = UserFollowSerializer

    def get_queryset(self):
        requested_user = self.request.user
        query = (USER_MODEL
                 .objects
                 .get(id=self.kwargs['pk'])
                 .followers
                 .all()
                 )
        if requested_user.is_authenticated:
            query = (query
                     .annotate(is_following=Exists(USER_MODEL
                                                   .objects
                                                   .get(id=requested_user.id)
                                                   .following
                                                   .filter(id=OuterRef('pk'))
                                                   )
                               )
                     )
        return query


class FollowUnfollowView(SerializerSchemaMixin, GenericAPIView):
    """
    Will follow a user if you are not following and
    unfollow the user if you are following
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FollowUnFollowSerializer
    response_serializer = FollowUnFollowSerializer

    def post(self, request, pk):
        try:
            user = USER_MODEL.objects.get(id=pk)
            if user in request.user.following.all():
                request.user.following.remove(user)
                user.followers.remove(request.user)
                serializer = self.response_serializer(data={'user_id': user.id,
                                                            'is_following': False})
            else:
                request.user.following.add(user)
                user.followers.add(request.user)

                url = reverse('social:dashboard', args=(request.user.username,))
                Notification.objects.create(message=f"""
                                            <a href="{url}"
                                            class="text-decoration-none">
                                            @{request.user.username}</a> followed you
                                            """,
                                            user=user)
                serializer = self.response_serializer(data={'user_id': user.id,
                                                            'is_following': True})
            if serializer.is_valid():
                return Response(serializer.data, status.HTTP_201_CREATED)
        except Exception as e:
            raise APIException(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


class MessagesListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MessagesSerializer
    pagination_class = SmallResultSetPagination

    def get(self, request, *args, **kwargs):
        (Message
         .objects
         .filter(sender__username=self.request.query_params['username'],
                 recipient=self.request.user,
                 message_read=False)
         .update(message_read=True)
         )
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        foreign_username = self.request.query_params['username']
        queryset = (Message
                    .objects
                    .filter((Q(sender=self.request.user)
                             & Q(recipient__username=foreign_username))
                            | (Q(recipient=self.request.user)
                               & Q(sender__username=foreign_username)))
                    .order_by('-message_sent_date')
                    )
        return queryset


class NotificationsListView(ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationsSerializer
    pagination_class = SmallResultSetPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        (Notification.
         objects
         .filter(user=self.request.user, seen=False)
         .update(seen=True)
         )
        return response

    def delete(self, request, *args, **kwargs):
        Notification.objects.get(id=request.query_params['pk']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset = (Notification
                    .objects
                    .filter(user=self.request.user)
                    .order_by('-created_on')
                    )
        return queryset
