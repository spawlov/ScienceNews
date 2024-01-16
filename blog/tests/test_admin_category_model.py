from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django.http import HttpRequest
from django.test import TestCase

from ..models import Category
from ..admin import CategoryAdmin


class CategoryAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user = User.objects.create_superuser(
            "admin", "admin@example.com", "password"
        )
        self.client.login(username="admin", password="password")

    def test_category_model(self):
        model_admin = ModelAdmin(Category, self.site)
        self.assertEqual(str(model_admin), "blog.ModelAdmin")

    def test_save_model(self):
        request = HttpRequest()
        request.method = "POST"
        request.user = self.user
        category = Category(title="Test Category")
        admin = CategoryAdmin(Category, self.site)
        form_class = admin.get_form(request)
        form = form_class(data={"title": "Test Category"}, instance=category)
        change = True
        admin.save_model(request, category, form, change)
        self.assertEqual(category.slug, "test-category")
        self.assertEqual(category.title, "Test Category")
