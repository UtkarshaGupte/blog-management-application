from django_filters import rest_framework as filters
from .models import BlogPost

class BlogPostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    content = filters.CharFilter(lookup_expr='icontains')
    author__first_name = filters.CharFilter(lookup_expr='icontains')
    author__last_name = filters.CharFilter(lookup_expr='icontains')
    category__name = filters.CharFilter(lookup_expr='icontains')
    tags__name = filters.CharFilter(lookup_expr='icontains')
    created_at__gt = filters.DateTimeFilter(field_name='created_at', lookup_expr='gt')
    created_at__lt = filters.DateTimeFilter(field_name='created_at', lookup_expr='lt')
    likes_count = filters.NumberFilter(method='filter_likes_count')

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'author__first_name', 'author__last_name', 'category__name', 'tags__name', 'created_at__gt', 'created_at__lt']
