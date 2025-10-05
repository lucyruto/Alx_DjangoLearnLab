from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from taggit.forms import TagWidget
from django.db.models import Q
from django.views.generic import ListView

# User registration form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Post form with tags
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # <-- include tags here
        widgets = {
            'tags': TagWidget(attrs={'placeholder': 'Add tags separated by commas'})
        }

# Comment form (no tags)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

# Search view (ListView)
class PostSearchView(ListView):
    model = Post
    template_name = 'blog/post_search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        return Post.objects.none()
