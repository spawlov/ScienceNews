from django.test import TestCase
from django.urls import reverse

from ..models import Category, Post


class SearchViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(
            title="Test Category",
            slug="test-category",
        )
        Post.objects.create(
            title="Test Post 1",
            slug="test-post-1",
            category=category,
            content="Lorem ipsum dolor sit amet",
            published=True,
        )
        Post.objects.create(
            title="Test Post 2",
            slug="test-post-2",
            category=category,
            content="Consectetur adipiscing elit",
            published=True,
        )

    def test_search_views_url_accessible(self):
        response = self.client.get("/search/?keyword=Lorem ipsum")
        self.assertEqual(response.status_code, 200)

    def test_search_views_url_accessible_by_name(self):
        response = self.client.get(
            reverse(
                viewname="search",
            )
            + "?keyword=Lorem ipsum"
        )
        self.assertEqual(response.status_code, 200)

    def test_search_view_uses_correct_template(self):
        response = self.client.get(
            reverse(
                viewname="search",
            )
            + "?keyword=Lorem ipsum"
        )
        self.assertTemplateUsed(response, "blog/search_results.html")

    def test_search_view_uses_correct_context(self):
        response = self.client.get(
            reverse(
                viewname="search",
            )
            + "?keyword=Lorem ipsum"
        )
        search_results = response.context_data["search_results"]
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].title, "Test Post 1")
