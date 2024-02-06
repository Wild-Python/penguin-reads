from django.shortcuts import get_object_or_404, render

from django.views import View
from .models import Genre, Book


class AllBooksView(View):
    def get(self, request):
        books = Book.books.all()
        return render(request, 'library/index.html', {'books': books})


class GenreBookListView(View):
    def get(self, request, genre_slug=None):
        genre = get_object_or_404(Genre, slug=genre_slug)
        books = Book.books.filter(book_genre=genre)
        return render(request, 'library/books/genre.html', {'genre': genre, 'books': books})


class BookDetailView(View):
    def get(self, request, slug):
        book = get_object_or_404(Book, slug=slug)
        fav = bool
        if book.favorites.filter(id=request.user.id).exists():
            fav = True
        return render(request, 'library/books/single.html', {'book': book, 'fav': fav})


# Navbar Area
def library(request):
    books = Book.books.all()
    return render(request, 'library/nav/library.html', {'books': books})
