from django.urls import path
from .views import list_books, LibraryDetailView
from .views import register_view, login_view, logout_view

urlpatterns = [
    # existing views
    path("books/", book_list, name="book-list"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library-detail"),

    # Authentication views
    path("register/", register_view, name="register"),
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
]


