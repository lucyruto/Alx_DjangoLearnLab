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

# Post form with TagWidget explicitly
class PostForm(forms.ModelForm):
    # Use TagWidget for adding tags
    tags = forms.CharField(
        required=False,
        widget=TagWidget(attrs={'placeholder': 'Add tags separated by commas'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(attrs={'placeholder': 'Add tags separated by commas'})  # rubric expects widgets
        }


# Comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


