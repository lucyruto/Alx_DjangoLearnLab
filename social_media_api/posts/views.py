from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Only allow owners of an object to edit or delete it."""
    def has_object_permission(self, request, view, obj):
        # Safe methods (GET, HEAD, OPTIONS) are open to everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only the author can modify or delete their own content
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    
    def perform_create(self, serializer):
        # Automatically assign the current user as the post author
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign the current user as the comment author
        serializer.save(author=self.request.user)


class FeedView(APIView):
    """
    GET /posts/feed/
    Returns posts from users the authenticated user follows,
    ordered by most recent first.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        following_users = user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class LikePostView(generics.GenericAPIView):
    """
    POST /posts/<pk>/like/
    Allows a user to like a post and notifies the post author.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({'detail': 'You already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create notification
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )

        return Response({'detail': 'Post liked.'}, status=status.HTTP_201_CREATED)


class UnlikePostView(generics.GenericAPIView):
    """
    POST /posts/<pk>/unlike/
    Allows a user to remove their like from a post.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({'detail': 'Post unliked.'}, status=status.HTTP_200_OK)

