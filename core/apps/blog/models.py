from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from ckeditor.fields import RichTextField


def user_directory_path(instance, filename):
    return f'posts/{instance.id}/{filename}'


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Post(models.Model):

    class PostManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    excerpt = models.TextField(null=True)
    image = models.ImageField(upload_to=user_directory_path, default='posts/default.jpg')
    slug = models.SlugField(max_length=250, unique_for_date='publish_date')
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    content = RichTextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=options, default='draft')
    favourites = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='favourites', default=None, blank=True)
    objects = models.Manager()
    post_manager = PostManager()

    def get_absolute_url(self):
        return reverse('blog:post_single', args=[self.slug])

    class Meta:
        ordering = ('-publish_date',)

    def __str__(self):
        return self.title


# class Comment(models.Model):
#
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
#     name = models.CharField(max_length=50)
#     email = models.EmailField()
#     content = models.TextField()
#     publish_date = models.DateTimeField(auto_now_add=True)
#     status = models.BooleanField(default=True)
#
#     class Meta:
#         ordering = ('publish_date',)
#
#     def __str__(self):
#         return f'Comment by {self.name}'
