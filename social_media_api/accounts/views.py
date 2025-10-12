from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, LoginSerializer, CustomUserSerializer

CustomUser = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    POST /accounts/register/
    Registers a new user and returns their token.
    """
    serializer_class = RegisterSerializer
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'User registered successfully',
            'user': CustomUserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """
    POST /accounts/login/
    Authenticates a user and returns a token.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user': CustomUserSerializer(user).data
        }, status=status.HTTP_200_OK)


class ProfileView(APIView):
    """
    GET /accounts/profile/
    Returns the logged-in user's profile.
    """
    permission_classes = [permissions.IsAuthenticated]  # use full path

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowUserView(APIView):
    """
    POST /accounts/follow/<user_id>/
    Authenticated user follows another user.
    """
    permission_classes = [permissions.IsAuthenticated]  # full path again

    def post(self, request, user_id):
        try:
            target_user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if target_user == request.user:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(target_user)
        return Response({'detail': f'You are now following {target_user.username}.'}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    """
    POST /accounts/unfollow/<user_id>/
    Authenticated user unfollows another user.
    """
    permission_classes = [permissions.IsAuthenticated]  # again for consistency

    def post(self, request, user_id):
        try:
            target_user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if target_user == request.user:
            return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(target_user)
        return Response({'detail': f'You have unfollowed {target_user.username}.'}, status=status.HTTP_200_OK)
