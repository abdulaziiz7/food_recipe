from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user.api.v0.serializers import (
    UserCreateSerializer,
    UserUpdateSerializer,
    FollowingCreateSerializer,
    UserLoginSerializer, FollowerListSerializer, FollowingListSerializer, UserProfileSerializer,
)
from apps.user.models import Follow

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )


user_create = UserCreateAPIView.as_view()


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,)


user_update = UserUpdateAPIView.as_view()


class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'email': user.email,
            'password': user.password,
        })


user_login = UserLoginView.as_view()


class FollowingCreateAPIView(CreateAPIView):
    serializer_class = FollowingCreateSerializer
    queryset = Follow.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


following_create = FollowingCreateAPIView.as_view()


class FollowerCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, username):
        user = User.objects.filter(username=username).first()
        follow = Follow.objects.filter(follower=user, following=self.request.user).first()
        if not follow:
            return Response({"message": "not found follow user"})
        if not follow.is_following:
            follow.is_following = True
            follow.save()
            return Response({"message": "follow back"})
        return Response({"message": "already following"})


follower_create = FollowerCreateAPIView.as_view()


# class UserProfileAPIView()
class FollowersListAPIView(ListAPIView):
    queryset = Follow.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowerListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(following=self.request.user)
        return qs


followers_list = FollowersListAPIView.as_view()


class FollowingListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Follow.objects.all()
    serializer_class = FollowingListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(follower=self.request.user)
        return qs


following_list = FollowingListAPIView.as_view()


class UserProfileAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(email=self.request.user.email)
        return qs


user_profile = UserProfileAPIView.as_view()
