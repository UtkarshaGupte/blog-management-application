from django.contrib import admin
from .models import Category, Tag, BlogPost, Comment, PostTag, Like

# Register your models here.
class PostTagInline(admin.TabularInline):
    model = PostTag
    extra = 0

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at')
    list_filter = ('updated_at', 'created_at')
    search_fields = ('title', 'content')
    inlines = [PostTagInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    list_filter = ('post', 'user', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'updated_at')
    list_filter = ('post', 'author', 'created_at')
    search_fields = ('content',)