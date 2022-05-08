from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, GenericAPIView
from .serializers import UserFollowSerializer

USER_MODEL = get_user_model()


class FollowingListView(ListAPIView):
    queryset = USER_MODEL.objects.all()
    serializer_class = UserFollowSerializer

    def get_queryset(self):
        requested_user = self.request.user
        return (USER_MODEL
                .objects
                .get(id=self.kwargs['pk'])
                .following
                .all()
                .annotate(is_following=Exists(USER_MODEL.
                                              objects
                                              .get(id=requested_user.id)
                                              .following
                                              .filter(id=OuterRef('pk'))))
                )


class FollowerListView(ListAPIView):
    queryset = USER_MODEL.objects.all()
    serializer_class = UserFollowSerializer

    def get_queryset(self):
        requested_user = self.request.user
        return (USER_MODEL
                .objects
                .get(id=self.kwargs['pk'])
                .followers
                .all()
                .annotate(is_following=Exists(USER_MODEL.
                                              objects
                                              .get(id=requested_user.id)
                                              .following
                                              .filter(id=OuterRef('pk'))))
                )


class FollowUnfollowView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = USER_MODEL.objects.get(id=pk)
        if user in request.user.following.all():
            request.user.following.remove(user)
        else:
            request.user.following.add(user)

        return Response(status=status.HTTP_200_OK)
