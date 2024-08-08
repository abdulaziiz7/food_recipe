from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.cache import cache
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user.api.v0.serializers import (
    UserCreateSerializer,
    UserUpdateSerializer,
    FollowingCreateSerializer,
    UserLoginSerializer, FollowerListSerializer, FollowingListSerializer, UserProfileSerializer,
    UserChangePasswordSerializer, UserResetPasswordSerializer, UserResetPasswordRequestSerializer,
)
from apps.user.models import Follow, PasswordReset
from food_recipe import settings

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        email = request.data['email']
        user = User.objects.filter(email=email).first()
        if user and not user.is_active:
            serializer = self.get_serializer(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(operation_id='Create user', tags=['User'])
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


user_create = UserCreateAPIView.as_view()


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        operation_id='Update user info',
        tags=['User'],
        request_body=UserCreateSerializer,
        responses={
            status.HTTP_200_OK: UserCreateSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
            status.HTTP_404_NOT_FOUND: 'Not Found'
        }
    )
    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserCreateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_id='Partial update user info',
        tags=['User'],
        request_body=UserCreateSerializer,
        responses={
            status.HTTP_200_OK: UserCreateSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
            status.HTTP_404_NOT_FOUND: 'Not Found'
        }
    )
    def patch(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserCreateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


user_update = UserUpdateAPIView.as_view()


class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(operation_id='Login', tags=['User'])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'email': user.email
        })


user_login = UserLoginView.as_view()


class FollowingCreateAPIView(CreateAPIView):
    serializer_class = FollowingCreateSerializer
    queryset = Follow.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    @swagger_auto_schema(operation_id='Create following', tags=['User'])
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


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

    @swagger_auto_schema(operation_id='Followers list', tags=['User'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


followers_list = FollowersListAPIView.as_view()


class FollowingListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Follow.objects.all()
    serializer_class = FollowingListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(follower=self.request.user)
        return qs

    @swagger_auto_schema(operation_id='Followings list', tags=['User'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


following_list = FollowingListAPIView.as_view()


class UserProfileAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(email=self.request.user.email)
        return qs

    @swagger_auto_schema(operation_id='User profile', tags=['User'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


user_profile = UserProfileAPIView.as_view()


@swagger_auto_schema(methods=['get'], operation_id='Verify code', tags=['User'])
@api_view(['GET'])
def verify_code(request):
    user_id = request.GET.get('user_id')
    code = request.GET.get('code')

    if not user_id:
        return Response({"message": "User ID not provided!"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"message": "User with this ID not found!"}, status=status.HTTP_404_NOT_FOUND)

    code_cache = cache.get(user_id)
    if code_cache is not None and code == code_cache:
        user.is_active = True
        user.save()
        return Response({"message": "User successfully logged in"}, status=status.HTTP_200_OK)

    return Response({"message": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['post'], operation_id='Change password', tags=['User'])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserResetPasswordRequestSerializer

    @swagger_auto_schema(operation_id='Forgot password', tags=['User'])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        user = User.objects.filter(email=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset = PasswordReset(email=email, token=token)
            reset.save()
            reset_url = f"http://10.10.4.143:8000/api/v0/user/reset-password/{token}"
            subject = 'Password Reset Requested'
            message = f'Please click the link below to reset your password:\n{reset_url}'
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, message, from_email, [email])
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User with credentials not found"}, status=status.HTTP_404_NOT_FOUND)


forgot_password = UserPasswordResetRequestAPIView.as_view()


class UserResetPasswordAPIView(APIView):
    serializer_class = UserResetPasswordSerializer

    @swagger_auto_schema(operation_id='Reset password', tags=['User'])
    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        new_password = data['new_password']
        confirm_password = data['confirm_password']

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)

        reset_obj = PasswordReset.objects.filter(token=token).first()

        if not reset_obj:
            return Response({'error': 'Invalid token'}, status=400)

        user = User.objects.filter(email=reset_obj.email).first()

        if user:
            user.set_password(request.data['new_password'])
            user.save()

            reset_obj.delete()

            return Response({'success': 'Password updated'})
        else:
            return Response({'error': 'No user found'}, status=404)


reset_password = UserResetPasswordAPIView.as_view()
