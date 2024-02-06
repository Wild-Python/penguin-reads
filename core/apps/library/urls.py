from django.urls import path
from core.apps.library import views

app_name = 'library'

urlpatterns = [
    path('', views.AllBooksView.as_view(), name='books_home'),
    path('library/', views.library, name='all_books'),
    path('<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/<slug:genre_slug>/', views.GenreBookListView.as_view(), name='genre_book_list'),
]
