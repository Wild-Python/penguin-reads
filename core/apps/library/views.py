from .models import Genre, Book
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView


class LibraryView(TemplateView):
    template_name = 'library/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.books.all()
        return context


class LibraryGenreListView(ListView):
    template_name = 'library/books/genre.html'
    context_object_name = 'books'

    def get_queryset(self):
        genre = get_object_or_404(Genre, slug=self.kwargs['genre_slug'])
        return Book.books.filter(book_genre=genre)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = get_object_or_404(Genre, slug=self.kwargs['genre_slug'])
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'library/books/single.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        fav = False
        if book.favorites.filter(id=self.request.user.id).exists():
            fav = True

        context['fav'] = fav
        return context


# Navbar Area
class Library(TemplateView):
    template_name = 'library/nav/library.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.books.all()
        return context
