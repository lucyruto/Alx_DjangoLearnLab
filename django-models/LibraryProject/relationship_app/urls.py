from django.urls import path
from .views import book_list, LibraryDetailView
from .views import (
    register_view,
    login_view,
    logout_view,
    book_list,
    add_book,
    edit_book,
    delete_book,
    LibraryDetailView,
)

urlpatterns = [
    # Book views
    path("books/", book_list, name="book-list"),
    path("books/add/", add_book, name="add-book"),
    path("books/<int:book_id>/edit/", edit_book, name="edit-book"),
    path("books/<int:book_id>/delete/", delete_book, name="delete-book"),

    # authentication views
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]


