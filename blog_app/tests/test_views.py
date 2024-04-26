from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.test import TestCase
from ..models import BlogPost
from ..serializers import BlogSerializer

class BlogPostTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        # Create some blog posts
        self.blog1 = BlogPost.objects.create(
            title='First Post', content='First Content', author=self.user)
        self.blog2 = BlogPost.objects.create(
            title='Second Post', content='Second Content', author=self.user)
        
        self.valid_data = {
            'title': 'Updated Post',
            'content': 'Updated Content'
        }
        self.invalid_data = {
            'title': '',
            'content': 'Content without a title'
        }
        
    def test_get_all_blogs(self):
        """
        Test retrieving list of all blog posts.
        """
        url = reverse('get_post_blogs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)  # assuming pagination settings allow for 2 items
        
        blogs = BlogPost.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_get_valid_single_blog(self):
        """ 
        Test to retreive single blog post by its id.
        """
        url = reverse('get_delete_update_blogs', kwargs={'pk': self.blog1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'First Post')

    def test_get_invalid_single_blog(self):
        """ 
        Test to retreive single blog post by invalid id.
        """
        url = reverse('get_delete_update_blogs', kwargs={'pk': 30})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_blog(self):
        """ 
        Test to create a blog with valid payload.
        """
        url = reverse('get_post_blogs')
        response = self.client.post(url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 3)

    def test_create_blog_with_invalid_data(self):
        """ 
        Test to create a blog with invalid payload.
        """
        url = reverse('get_post_blogs')
        response = self.client.post(url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_blog(self):
        """ 
        Test to update a blog.
        """
        url = reverse('get_delete_update_blogs', kwargs={'pk': self.blog1.pk})
        response = self.client.put(url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.blog1.refresh_from_db()
        self.assertEqual(self.blog1.title, 'Updated Post')

    def test_partial_update_blog(self):
        """ 
        Test to partially update a blog.
        """
        url = reverse('get_delete_update_blogs', kwargs={'pk': self.blog1.pk})
        partial_data = {'title': 'Partially Updated Post'}
        response = self.client.patch(url, partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog1.refresh_from_db()
        self.assertEqual(self.blog1.title, 'Partially Updated Post')

    def test_delete_blog(self):
        """ 
        Test to delete a blog.
        """
        url = reverse('get_delete_update_blogs', kwargs={'pk': self.blog1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BlogPost.objects.count(), 1)

    def test_permission_denied_for_updating_other_users_blog(self):
        """ 
        Test to validate permissions to update a blog.
        """
        another_user = User.objects.create_user(username='anotheruser', password='password123')
        self.client.force_authenticate(user=another_user)
        url = reverse('get_delete_update_blogs', kwargs={'pk': self.blog1.pk})
        response = self.client.put(url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_denied_for_deleting_other_users_blog(self):
        """ 
        Test to validate permissions to delete a blog.
        """
        another_user = User.objects.create_user(username='anotheruser', password='password123')
        self.client.force_authenticate(user=another_user)
        url = reverse('get_delete_update_blogs', kwargs={'pk': self.blog1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)