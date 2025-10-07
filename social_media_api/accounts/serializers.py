from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Get the custom user model
User = get_user_model()


# ---------- User Serializer ----------
class CustomUserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'following']
        read_only_fields = ['id', 'username', 'following']

    def get_following(self, obj):
        return [user.username for user in obj.following.all()]


# ---------- Registration Serializer ----------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        
        user = get_user_model().objects.create_user(**validated_data)
        Token.objects.create(user=user)
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

        attrs['user'] = user
        return attrs
