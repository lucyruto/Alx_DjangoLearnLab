from django.urls import path
from .views import list_books, LibraryDetailView
from .views import register_view, login_view, logout_view

urlpatterns = [
    # existing views
    path("books/", book_list, name="book-list"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library-detail"),
    path('books/add/', views.add_book, name='add-book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit-book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete-book'),

    # Authentication views
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
]


