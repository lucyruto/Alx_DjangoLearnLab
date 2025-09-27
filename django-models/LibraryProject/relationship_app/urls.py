from django.urls import path
from .views import book_list, LibraryDetailView
from .views import register_view, login_view, logout_view

urlpatterns = [
    # existing views
    path("books/", book_list, name="book-list"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library-detail"),

    # authentication views
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]


