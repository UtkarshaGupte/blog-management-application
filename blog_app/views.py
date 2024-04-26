from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsOwnerOrReadOnly
from .pagination import CustomPagination
from .filters import BlogPostFilter
from .serializers import BlogSerializer
from .models import BlogPost


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_post_blogs(request):

    # get all blogs
    if request.method == 'GET':
        
        blogs = BlogPost.objects.all()
        filtered_blogs = BlogPostFilter(request.GET, queryset=blogs)
        
        # Pagination
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(filtered_blogs.qs, request)

        # Serialization
        serializer = BlogSerializer(paginated_queryset, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)
    
    # insert a new record for a blog
    elif request.method == 'POST':
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@permission_classes([IsAuthenticated])
@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def get_delete_update_blog(request, pk):
    
    try:
        blog =  BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single blog
    if request.method == 'GET':
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    # Check for owner permission
    if not IsOwnerOrReadOnly().has_object_permission(request, None, blog):
        return Response({"message": "You do not have permission to modify this blog post."}, status=status.HTTP_403_FORBIDDEN)
    
    # update details of a single blog
    if request.method == 'PUT':
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Partially update details of a single blog
    elif request.method == 'PATCH':
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # delete a single blog
    elif request.method == 'DELETE':
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)