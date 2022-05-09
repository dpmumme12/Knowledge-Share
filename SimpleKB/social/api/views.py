from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView, GenericAPIView
from .serializers import UserFollowSerializer, FollowUnFollowSerializer

USER_MODEL = get_user_model()


class FollowingListView(ListAPIView):
    queryset = USER_MODEL.objects.all()
    serializer_class = UserFollowSerializer

    def get_queryset(self):
        requested_user = self.request.user
        print(requested_user.id)
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
    queryset = USER_MODEL.objects.all()
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


class FollowUnfollowView(GenericAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FollowUnFollowSerializer

    def post(self, request, pk):
        try:
            user = USER_MODEL.objects.get(id=pk)
            if user in request.user.following.all():
                request.user.following.remove(user)
                user.followers.remove(request.user)
                serializer = self.serializer_class(data={'user_id': user.id,
                                                         'is_following': False})
            else:
                request.user.following.add(user)
                user.followers.add(request.user)
                serializer = self.serializer_class(data={'user_id': user.id,
                                                         'is_following': True})
            if serializer.is_valid():
                return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            raise APIException(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
