from .models import Category


def category_list(request):
    categories_list = Category.objects.exclude(name='default')
    context = {
        "category_list": categories_list,
    }
    return context
