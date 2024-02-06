from django.contrib import admin
from.models import Post, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'slug', 'author')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# @admin.register(Comment)
# class PostCommentAdmin(admin.ModelAdmin):
#     list_display = ('post', 'name', 'email', 'status')
#     list_filter = ('status', 'publish_date')
#     search_fields = ('name', 'email')
