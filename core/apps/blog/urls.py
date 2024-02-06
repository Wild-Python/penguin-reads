from django.urls import path
from django.conf import settings
from core.apps.blog import views
from django.conf.urls.static import static

app_name = 'blog'

urlpatterns = [

    path('', views.home, name='home'),
    path('category/<str:category>/', views.CategoryListView.as_view(), name='category'),

    path('favorite/<int:bid>', views.add_to_favorites, name='add_to_favorites'),
    path('favorites-list/', views.favorites_list, name='favorites_list'),

    path('<slug:post>/', views.post_single, name='post_single'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
