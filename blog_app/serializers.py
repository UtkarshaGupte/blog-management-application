from rest_framework import serializers
from .models import BlogPost
from django.contrib.auth.models import User

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = BlogPost
        fields = ["id","title", "content", "created_at", "updated_at", "author", "tags", "category"]


class UserSerializer(serializers.ModelSerializer):
    blogs = serializers.PrimaryKeyRelatedField(many=True, queryset=BlogPost.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'blogs')
    
    