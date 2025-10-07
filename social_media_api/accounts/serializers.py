from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Get the custom user model
CustomUser = get_user_model()


# ---------- User Serializer ----------
class CustomUserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'following']
        read_only_fields = ['id', 'username', 'following']

    def get_following(self, obj):
        # Returns a list of usernames the user follows
        return [user.username for user in obj.following.all()]


# ---------- Registration Serializer ----------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        # create_user() automatically handles password hashing
        user = CustomUser.objects.create_user(**validated_data)
        # Generate or get authentication token
        Token.objects.get_or_create(user=user)
        return user


# ---------- Login Serializer ----------
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        # Add the user to attrs so views can access it
        attrs['user'] = user
        return attrs
