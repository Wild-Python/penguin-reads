from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import Post
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404


def home(request):
    all_posts = Post.post_manager.all()
    return render(request, 'blog/index.html', {'posts': all_posts})


def post_single(request, post):
    post = get_object_or_404(Post, slug=post, status='published')
    fav = bool
    if post.favourites.filter(id=request.user.id).exists():
        fav = True
    return render(request, 'blog/single.html', {'post': post, 'fav': fav})


class FavoriteListView(LoginRequiredMixin, View):
    pass


@login_required
def add_to_favorites(request, bid):
    post = get_object_or_404(Post, id=bid)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def favorites_list(request):
    new = Post.post_manager.filter(favourites=request.user)
    return render(request, 'blog/favorites.html', {"new": new})


class CategoryListView(ListView):
    template_name = 'blog/categories.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        content = {
            'cat': self.kwargs['category'],
            'posts': Post.objects.filter(category__name=self.kwargs['category']).filter(status='published')
        }
        return content

# def post_single(request, post):
#     post = get_object_or_404(Post, slug=post, status='published')
#     comments = post.comments.filter(status=True)
#
#     user_comment = None
#
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             user_comment = comment_form.save(commit=False)
#             user_comment.post = post
#             user_comment.save()
#             return HttpResponseRedirect('/', post.slug)
#         else:
#             comment_form = CommentForm()
#     return render(
#         request, 'blog/single.html',
#         {
#             'post': post,
#             'comments': comments,
#             'user_comments': user_comment,
#             'comment_form': comment_form,
#         }
#     )
