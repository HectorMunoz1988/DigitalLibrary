from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path(
        'books/<int:book_id>/loan/',
        views.create_loan,
        name='create_loan'
    ),

    path('my-loans/', views.my_loans, name='my_loans'),
    path(
        'loans/<int:loan_id>/return/',
        views.return_book,
        name='return_book'
    ),

    path('authors/', views.author_list, name='author_list'),
    path(
        'authors/<int:author_id>/',
        views.author_detail,
        name='author_detail'
    ),

    path(
    'books/<int:book_id>/review/',
    views.create_review,
    name='create_review'
    ),
]