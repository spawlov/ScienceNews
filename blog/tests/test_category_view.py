from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.test import TestCase

from lorem import get_paragraph

from ..models import Post, Category


class CategoryViewTests(TestCase):
    _post_count = 10
    _author = "TestAuthor"

    def setUp(self):
        bilk_post = []
        for counter in range(0, self._post_count):
            self.category = Category.objects.create(
                title=f"Test Category {counter}",
                slug=f"test-category-{counter}",
            )
            bilk_post.append(
                Post(
                    title=f"Test Post - {counter}",
                    slug=f"test-post-{counter}",
                    content=get_paragraph(
                        count=5,
                        sep="\n",
                        comma=(0, 2),
                        word_range=(4, 8),
                        sentence_range=(5, 10),
                    ),
                    category=self.category,
                    author=self._author,
                )
            )
        Post.objects.bulk_create(bilk_post)

    def test_category_exist_all(self):
        counter = 0
        for counter in range(0, self._post_count):
            response = self.client.get(f"/category/test-category-{counter}/")
            self.assertTrue(response.status_code == 200)
        self.assertEqual(counter, self._post_count - 1)

    def test_category_exist_all_by_name(self):
        counter = 0
        for counter in range(0, self._post_count):
            response = self.client.get(
                reverse(
                    viewname="category",
                    kwargs={
                        "slug": f"test-category-{counter}",
                    },
                )
            )
            self.assertTrue(response.status_code == 200)
        self.assertEqual(counter, self._post_count - 1)

    def test_category_exist_one_post_in_category(self):
        counter = 0
        for counter in range(0, self._post_count):
            response = self.client.get(f"/category/test-category-{counter}/")
            self.assertTrue(len(response.context["posts"]) == 1)
        self.assertEqual(counter, self._post_count - 1)

    def test_category_exist_one_post_in_category_by_name(self):
        counter = 0
        for counter in range(0, self._post_count):
            response = self.client.get(
                reverse(
                    viewname="category",
                    kwargs={
                        "slug": f"test-category-{counter}",
                    },
                )
            )
            self.assertTrue(len(response.context["posts"]) == 1)
        self.assertEqual(counter, self._post_count - 1)

    def test_category_exist_post_from_categories(self):
        counter = 0
        for counter in range(0, self._post_count):
            post = get_object_or_404(
                Post,
                category__slug=f"test-category-{counter}",
            )
            self.assertEqual(post.title, f"Test Post - {counter}")
            self.assertEqual(post.slug, f"test-post-{counter}")
            self.assertFalse(post.content == "")
            self.assertTrue(post.author == self._author)
            self.assertEqual(post.category.title, f"Test Category {counter}")
            self.assertEqual(post.category.slug, f"test-category-{counter}")
        self.assertEqual(counter, self._post_count - 1)

    def test_view_uses_correct_template(self):
        counter = 0
        for counter in range(0, self._post_count):
            response = self.client.get(
                reverse(
                    viewname="category",
                    kwargs={
                        "slug": f"test-category-{counter}",
                    },
                )
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "blog/index.html")
        self.assertEqual(counter, self._post_count - 1)
