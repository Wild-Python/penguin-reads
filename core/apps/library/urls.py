from django.urls import path
from core.apps.library import views

app_name = 'library'

urlpatterns = [
    path('', views.LibraryView.as_view(), name='books_home'),
    path('library/', views.Library.as_view(), name='all_books'),
    path('<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/<slug:genre_slug>/', views.LibraryGenreListView.as_view(), name='genre_book_list'),
]
