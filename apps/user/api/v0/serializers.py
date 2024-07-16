from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from apps.user.models import Follow

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=4, max_length=16, write_only=True)

    class Meta:
        model = User
        fields = ['pk', 'email', 'password', 'password2']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError("Entered passwords do not match!")
        return attrs

    def create(self, data):
        user = User(
            email=data['email'],
        )
        user.set_password(data['password'])
        user.is_active = False
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'phone',
            'birthday', 'location', 'about_me'
        ]


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(max_length=16, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if password and email:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )
            if not user:
                raise serializers.ValidationError('email and password entered incorrectly', code='authorization')
        else:
            raise serializers.ValidationError('User must have email and password!', code='authorization')
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class FollowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['following']


class FollowerListSerializer(serializers.ModelSerializer):
    follower = UserCreateSerializer()

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'created_at']


class FollowingListSerializer(serializers.ModelSerializer):
    following = UserCreateSerializer()

    class Meta:
        model = Follow
        fields = ['id', 'following', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'location',
                  'birthday', 'image','recipes']


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
        error_messages={'invalid': ('The password must be at least 4 characters long and contain a letter and a symbol.')})
    confirm_password = serializers.CharField(write_only=True, required=True)
