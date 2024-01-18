import os
import sys
import tempfile
from unittest import skipIf

from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase

from lorem import get_paragraph

from ..admin import PostAdmin
from ..models import Category, Post


class CategoryAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user = User.objects.create_superuser(
            "admin", "admin@example.com", "password"
        )
        self.client.login(username="admin", password="password")
        self.category = Category.objects.create(
            title="Test Category", slug="test-category"
        )
        self.content = get_paragraph(
            count=5,
            sep="\n",
            comma=(0, 2),
            word_range=(4, 8),
            sentence_range=(5, 10),
        )
        self.photo = tempfile.NamedTemporaryFile(suffix=".jpg").name

    def test_category_model(self):
        model_admin = ModelAdmin(Post, self.site)
        self.assertEqual(str(model_admin), "blog.ModelAdmin")

    @skipIf(sys.platform.startswith("win"), "requires Linux")
    def test_upload_photo(self):
        post = Post.objects.create(
            title="Test Post",
            content=self.content,
            category=self.category,
            photo=self.photo,
        )
        self.assertEqual(post.photo.url, f"/media{self.photo}")

    @skipIf(sys.platform.startswith("win"), "requires Linux")
    def test_get_photo_with_image(self):
        post = Post.objects.create(
            title="Test Post",
            content=self.content,
            category=self.category,
            photo=self.photo,
        )
        admin = PostAdmin(Post, self.site)
        self.assertEqual(
            str(admin.get_photo(post)),
            f'<img src="/media{self.photo}" style="max-height: 200px;">'
            f"<figcaption>None</figcaption>",
        )

    def test_get_photo_without_image(self):
        post = Post.objects.create(
            title="Test Post",
            content=self.content,
            category=self.category,
            photo=None,
        )
        admin = PostAdmin(Post, self.site)
        self.assertEqual(str(admin.get_photo(post)), "-")

    @skipIf(sys.platform.startswith("win"), "requires Linux")
    def test_get_list_photo_with_image(self):
        post = Post.objects.create(
            title="Test Post",
            content=self.content,
            category=self.category,
            photo=os.path.normpath(self.photo),
        )
        admin = PostAdmin(Post, self.site)
        self.assertEqual(
            str(admin.get_list_photo(post)),
            f'<img src="/media{self.photo}" style="max-height: 50px;">',
        )

    def test_get_list_photo_without_image(self):
        post = Post.objects.create(
            title="Test Post",
            content=self.content,
            category=self.category,
            photo=None,
        )
        admin = PostAdmin(Post, self.site)
        self.assertEqual(str(admin.get_list_photo(post)), "-")

    def test_save_model(self):
        request = HttpRequest()
        request.method = "POST"
        request.user = self.user
        post = Post(title="Test Post")
        admin = PostAdmin(Post, self.site)
        form_class = admin.get_form(request)
        form = form_class(
            data={
                "title": "Test Post",
                "category": self.category,
                "content": self.content,
            },
            instance=post,
        )
        change = True
        admin.save_model(request, post, form, change)
        self.assertEqual(post.slug, "test-post")
        self.assertEqual(post.title, "Test Post")
