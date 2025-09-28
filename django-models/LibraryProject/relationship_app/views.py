from django.shortcuts import render,redirect
from .models import Book
# from django.views.generic import DetailView
from .models import Library
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import user_passes_test
from relationship_app.forms import BookForm

# ---------------- Role-check helper functions ----------------
# hasattr(user, "profile") ensures we don’t get errors if the user somehow doesn’t have a profile.
def is_admin(user):
    return user.is_authenticated and hasattr(user, "profile") and user.profile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, "profile") and user.profile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, "profile") and user.profile.role == 'Member'


# ---------------- Role-Based Views ----------------
# Utilize the @user_passes_test decorator to check the user’s role before granting access to each view.
@user_passes_test(is_admin, login_url='login')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian, login_url='login')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(is_member, login_url='login')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')





# ---------------- Add Book View ----------------
@permission_required('relationship_app.can_add_book', login_url='login')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book-list')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form})


# ---------------- Edit Book View ----------------
@permission_required('relationship_app.can_change_book', login_url='login')
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book-list')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form, 'book': book})


# ---------------- Delete Book View ----------------
@permission_required('relationship_app.can_delete_book', login_url='login')
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book-list')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})

    
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
