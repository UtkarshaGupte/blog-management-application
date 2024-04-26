from django.urls import path
from .views import ( get_delete_update_blog, get_post_blogs)

urlpatterns = [
    path('', get_post_blogs, name='get_post_blogs'),
    path('<int:pk>/', get_delete_update_blog, name='get_delete_update_blogs'),
]