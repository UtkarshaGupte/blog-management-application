from django.test import TestCase
from django.contrib.auth.models import User
from ..models import BlogPost, Category, Tag, PostTag, Like, Comment

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Technology', description='All about technology')
        self.tag = Tag.objects.create(name='tech')
        self.blog_post = BlogPost.objects.create(
            title='First Post', 
            content='This is the content of the first post', 
            author=self.user, 
            category=self.category
        )
        self.post_tag = PostTag.objects.create(post=self.blog_post, tag=self.tag)
        self.like = Like.objects.create(post=self.blog_post, user=self.user)
        self.comment = Comment.objects.create(
            content='This is a comment',
            post=self.blog_post,
            author=self.user
        )

    def test_category_creation(self):
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(self.category.__str__(), 'Technology')

    def test_tag_creation(self):
        self.assertTrue(isinstance(self.tag, Tag))
        self.assertEqual(self.tag.__str__(), 'tech')

    def test_blog_post_creation(self):
        self.assertTrue(isinstance(self.blog_post, BlogPost))
        self.assertEqual(self.blog_post.__str__(), 'First Post')
        self.assertEqual(self.blog_post.get_details(), 'First Post belongs to testuser')

    def test_post_tag_creation(self):
        self.assertTrue(isinstance(self.post_tag, PostTag))
        # Ensuring the unique_together constraint works
        duplicate_post_tag_creation = False
        try:
            PostTag.objects.create(post=self.blog_post, tag=self.tag)
        except:
            duplicate_post_tag_creation = True
        self.assertTrue(duplicate_post_tag_creation)

    def test_like_creation(self):
        self.assertTrue(isinstance(self.like, Like))
        # Testing unique_together for likes
        with self.assertRaises(Exception):
            Like.objects.create(post=self.blog_post, user=self.user)

    def test_comment_creation(self):
        self.assertTrue(isinstance(self.comment, Comment))
        self.assertEqual(str(self.comment), f'Comment by testuser on First Post')
        # Testing comment count increase
        Comment.objects.create(
            content='Another comment',
            post=self.blog_post,
            author=self.user
        )
        self.assertEqual(self.blog_post.comments.count(), 2)
