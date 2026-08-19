from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Book, Author, Loan, Review
from .forms import LoanForm, ReviewForm

from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.db.models import Avg
from django.db.models import Q


def home(request):
    return render(request, 'library/home.html')


def book_list(request):
    query = request.GET.get('q', '').strip()

    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(isbn__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        ).distinct()

    return render(request, 'library/book_list.html', {
        'books': books,
        'query': query
    })


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    user_review = None

    if request.user.is_authenticated:
        user_review = book.reviews.filter(
            user=request.user
        ).first()

    average_rating = book.reviews.aggregate(
        average=Avg('rating')
    )['average']

    return render(request, 'library/book_detail.html', {
        'book': book,
        'user_review': user_review,
        'average_rating': average_rating
    })


def author_list(request):
    authors = Author.objects.all()

    return render(request, 'library/author_list.html', {
        'authors': authors
    })


def author_detail(request, author_id):
    author = get_object_or_404(
        Author,
        id=author_id
    )

    return render(
        request,
        'library/author_detail.html',
        {
            'author': author
        }
    )

@login_required
def create_loan(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if not book.available:
        messages.error(request, 'Este libro no está disponible.')
        return redirect('book_detail', book_id=book.id)

    active_loan = Loan.objects.filter(
        book=book,
        user=request.user,
        return_date__isnull=True
    ).exists()

    if active_loan:
        messages.error(
            request,
            'Ya tienes este libro en préstamo.'
        )
        return redirect('book_detail', book_id=book.id)
    

    if request.method == 'POST':
        form = LoanForm(request.POST)

        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user
            loan.book = book
            loan.save()

            book.available = False
            book.save()

            messages.success(request, 'Libro prestado correctamente.')
            return redirect('my_loans')

    else:
        form = LoanForm()

    return render(request, 'library/loan_form.html', {
        'form': form,
        'book': book
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'library/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def my_loans(request):

    active_loans = Loan.objects.filter(
        user=request.user,
        return_date__isnull=True
    )

    returned_loans = Loan.objects.filter(
        user=request.user,
        return_date__isnull=False
    )

    return render(
        request,
        'library/my_loans.html',
        {
            'active_loans': active_loans,
            'returned_loans': returned_loans
        }
    )

@login_required
def return_book(request, loan_id):
    loan = get_object_or_404(
        Loan,
        id=loan_id,
        user=request.user
    )

    if request.method == 'POST' and loan.return_date is None:
        loan.return_date = timezone.now().date()
        loan.save()

        loan.book.available = True
        loan.book.save()

        messages.success(
            request,
            f'Has devuelto "{loan.book.title}" correctamente.'
        )

    return redirect('my_loans')

@login_required
def create_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    existing_review = Review.objects.filter(
        book=book,
        user=request.user
    ).exists()

    if existing_review:
        messages.error(
            request,
            'Ya has valorado este libro.'
        )

        return redirect(
            'book_detail',
            book_id=book.id
        )

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)

            review.user = request.user
            review.book = book

            review.save()

            messages.success(
                request,
                'Tu reseña se ha añadido correctamente.'
            )

            return redirect(
                'book_detail',
                book_id=book.id
            )

    else:
        form = ReviewForm()

    return render(
        request,
        'library/review_form.html',
        {
            'form': form,
            'book': book
        }
    )