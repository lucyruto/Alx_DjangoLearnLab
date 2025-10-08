from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import filters

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
