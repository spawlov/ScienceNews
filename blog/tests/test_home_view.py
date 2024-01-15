from django.test import TestCase
from django.urls import reverse

from lorem import get_paragraph

from ..models import Post, Category


class PostViewTests(TestCase):
    _post_count = 10
    _author = 'TestAuthor'

    def setUp(self):
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        bilk_post = []
        for counter in range(0, self._post_count):
            bilk_post.append(
                Post(
                    title=f'Test Post - {counter}',
                    slug=f'test-post-{counter}',
                    content=get_paragraph(5, sep='\n', comma=(0, 2), word_range=(4, 8), sentence_range=(5, 10)),
                    category=self.category,
                    author=self._author,
                )
            )
        Post.objects.bulk_create(bilk_post)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_pagination_is_exist(self):
        response = self.client.get(reverse('home'))
        self.assertTrue('is_paginated' in response.context)

    def test_pagination_is_correct_context_name(self):
        response = self.client.get(reverse('home'))
        self.assertTrue(response.context['is_paginated'])

    def test_pagination_is_correct_number_pages(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.context['paginator'].num_pages, 2)

    def test_pagination_count_posts_first_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['posts']), 6)

    def test_pagination_count_posts_last_page(self):
        response = self.client.get(reverse('home') + '?page=2')
        self.assertEqual(len(response.context['posts']), 4)
