from django.shortcuts import get_object_or_404, get_list_or_404
from django.test import TestCase
from django.urls import reverse

from lorem import get_paragraph

from ..models import Post, Category, Tag


class CategoryViewTests(TestCase):
    _post_count = 10
    _tag_count = 4
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

        for counter in range(0, self._tag_count):
            Tag.objects.create(title=f'Test Tag {counter}', slug=f'test-tag-{counter}')

        for counter in range(1, self._post_count):
            post = Post.objects.get(slug=f'test-post-{counter}')
            if counter % 2:
                post.tag.add(Tag.objects.get(slug=f'test-tag-2'))
            else:
                post.tag.add(Tag.objects.get(slug=f'test-tag-1'))
                post.tag.add(Tag.objects.get(slug=f'test-tag-3'))

    def test_tag_exist_all(self):
        counter = 0
        for counter in range(1, self._tag_count):
            response = self.client.get(f'/tag/test-tag-{counter}/')
            self.assertEqual(response.status_code, 200)
        self.assertEqual(counter, self._tag_count - 1)

    def test_tag_exist_all_by_name(self):
        counter = 0
        for counter in range(1, self._tag_count):
            response = self.client.get(reverse('tag', kwargs={'slug': f'test-tag-{counter}'}))
            self.assertEqual(response.status_code, 200)
        self.assertEqual(counter, self._tag_count - 1)

    def test_tag_exist_posts_in_tags(self):
        counter = 0
        for counter in range(1, self._tag_count):
            response = self.client.get(f'/tag/test-tag-{counter}/')
            if counter % 2:
                self.assertEqual(len(response.context['posts']), 4)
            else:
                self.assertEqual(len(response.context['posts']), 5)
        self.assertEqual(counter, self._tag_count - 1)

    def test_tag_exist_posts_in_tags_by_name(self):
        counter = 0
        for counter in range(1, self._tag_count):
            response = self.client.get(reverse('tag', kwargs={'slug': f'test-tag-{counter}'}))
            if counter % 2:
                self.assertEqual(len(response.context['posts']), 4)
            else:
                self.assertEqual(len(response.context['posts']), 5)
        self.assertEqual(counter, self._tag_count - 1)

    def test_tag_exist_post_from_tags(self):
        counter = 0
        for counter in range(1, self._tag_count):
            post = Post.objects.filter(tag__slug=f'test-tag-{counter}')
            if counter % 2:
                self.assertEqual(post.count(), 4)
            else:
                self.assertEqual(post.count(), 5)

    def test_view_uses_correct_template(self):
        counter = 0
        for counter in range(1, self._tag_count):
            response = self.client.get(reverse('tag', kwargs={'slug': f'test-tag-{counter}'}))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'blog/index.html')
        self.assertEqual(counter, self._tag_count - 1)
