from django.contrib import admin
from .models import Post, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    search_fields = ('content',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__title')
    list_filter = ('created_at',)
