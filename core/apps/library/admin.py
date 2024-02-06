from django.contrib import admin
from .models import Genre, Book


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slug', 'is_active', 'created', 'updated']
    list_filter = ['is_active']
    list_editable = ['is_active',]
    prepopulated_fields = {'slug': ('title',)}
