from django.shortcuts import render,redirect
from .models import Book
# from django.views.generic import DetailView
from .models import Library
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView


# ---------------- Function-Based View ----------------
def book_list(request):
    """Function-based view to list all books and their authors"""
    books = Book.objects.all()
    context = {"books": books}
    return render(request, "relationship_app/list_books.html", context)


# ---------------- Class-Based View ----------------


class LibraryDetailView(DetailView):
    """Class-based view to display details of a specific library"""
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"



# ---------------- User Registration ----------------
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # automatically log in after registration
            return redirect("book-list")  # redirect to books page
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


# ---------------- User Login ----------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("book-list")  # redirect after login
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})


# ---------------- User Logout ----------------
@login_required
def logout_view(request):
    logout(request)
    return render(request, "relationship_app/logout.html")
