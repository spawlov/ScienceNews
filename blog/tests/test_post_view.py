from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from lorem import get_paragraph

from ..models import Post, Category, Tag


class PostViewTest(TestCase):
    _author = 'TestAuthor'

    def setUp(self):
        self.title = 'Test title'
        self.slug = 'test-slug'
        self.content = get_paragraph(5, sep='\n', comma=(0, 2), word_range=(4, 8), sentence_range=(5, 10))
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.tag = Tag.objects.create(title='Test Tag', slug='test-tag')
        post = Post.objects.create(
            title=self.title,
            slug=self.slug,
            category=self.category,
            content=self.content,
            author=self._author,
        )
        post.tag.add(self.tag)

    def test_post_view_url_accessible(self):
        response = self.client.get('/post/test-slug/')
        self.assertEqual(response.status_code, 200)

    def test_post_view_url_accessible_by_name(self):
        response = self.client.get(reverse('post', kwargs={'slug': 'test-slug'}))
        self.assertEqual(response.status_code, 200)

    def test_post_view_uses_correct_template(self):
        response = self.client.get(reverse('post', kwargs={'slug': 'test-slug'}))
        self.assertTemplateUsed(response, 'blog/post.html')

    def test_post_view_uses_correct_context(self):
        response = self.client.get(reverse('post', kwargs={'slug': 'test-slug'}))
        self.assertContains(response, self.title, status_code=200)
        self.assertEqual(response.context['post'].title, self.title)
        self.assertEqual(response.context['post'].slug, self.slug)
        self.assertEquals(response.context['post'].content, self.content)
        self.assertEquals(response.context['post'].author, self._author)
        self.assertEquals(response.context['post'].category, self.category)
        self.assertEquals(response.context['post'].category.title, self.category.title)
        self.assertEquals(response.context['post'].category.slug, self.category.slug)
        self.assertEquals(response.context['post'].tag.all()[0], self.tag)
        self.assertEquals(response.context['post'].tag.all()[0].title, self.tag.title)
        self.assertEquals(response.context['post'].tag.all()[0].slug, self.tag.slug)
        self.assertEquals(response.context['post'].created_at.date(), timezone.now().date())
        self.assertEquals(response.context['post'].views, 1)
