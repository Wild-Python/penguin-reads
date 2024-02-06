import os
from django.db import models
from django.urls import reverse
from django.conf import settings


def generate_genre_based_upload_path(instance, filename):
    # Construct the upload path based on the book's genre
    return os.path.join('pdfs', instance.book_genre.slug, filename)


class BookManager(models.Manager):
    def get_queryset(self):
        return super(BookManager, self).get_queryset().filter(is_active=True)


class Genre(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'genres'

    def get_absolute_url(self):
        return reverse('library:genre_book_list', args=[self.slug])

    def __str__(self):
        return self.name


class Book(models.Model):
    book_genre = models.ForeignKey(Genre, related_name='book_genre', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='book_creater')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    slug = models.SlugField(max_length=255)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    books = BookManager()

    pdf_file = models.FileField(upload_to=generate_genre_based_upload_path, blank=True, null=True)
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorites', blank=True)

    class Meta:
        verbose_name_plural = 'Books'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('library:book_detail', args=[self.slug])

    def __str__(self):
        return self.title
