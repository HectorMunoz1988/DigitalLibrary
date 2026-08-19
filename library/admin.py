from django.contrib import admin
from .models import Author, Book, Loan, Review


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'birth_date',
    )

    search_fields = (
        'first_name',
        'last_name',
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'show_authors',
        'publication_date',
        'isbn',
        'available',
    )

    search_fields = (
        'title',
        'isbn',
        'author__first_name',
        'author__last_name',
    )

    list_filter = (
        'available',
        'publication_date',
    )

    filter_horizontal = (
        'author',
    )

    def show_authors(self, obj):
        return ", ".join(
            f"{author.first_name} {author.last_name}"
            for author in obj.author.all()
        )

    show_authors.short_description = 'Autores'
    show_authors.admin_order_field = 'author__last_name'


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        'book',
        'user',
        'loan_date',
        'due_date',
        'return_date',
        'is_returned',
    )

    search_fields = (
        'book__title',
        'user__username',
    )

    list_filter = (
        'loan_date',
        'due_date',
        'return_date',
    )

    def is_returned(self, obj):
        return obj.return_date is not None

    is_returned.boolean = True
    is_returned.short_description = 'Devuelto'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'book',
        'user',
        'rating',
        'created_at',
    )

    search_fields = (
        'book__title',
        'user__username',
        'comment',
    )

    list_filter = (
        'rating',
        'created_at',
    )

    readonly_fields = (
        'created_at',
    )