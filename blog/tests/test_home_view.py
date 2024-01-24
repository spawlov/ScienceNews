from django.test import TestCase
from django.urls import reverse

from lorem import get_paragraph

from ..models import Category, Post


class PostViewTests(TestCase):
    _post_count = 10
    _author = "TestAuthor"

    def setUp(self):
        self.category = Category.objects.create(
            title="Test Category", slug="test-category"
        )
        bilk_post = []
        for counter in range(0, self._post_count):
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

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "blog/home.html")
