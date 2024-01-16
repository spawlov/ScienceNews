from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.http import HttpRequest
from ..models import Tag
from ..admin import TagAdmin


class CategoryAdminTest(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client.login(username='admin', password='password')

    def test_category_model(self):
        model_admin = ModelAdmin(Tag, self.site)
        self.assertEqual(str(model_admin), 'blog.ModelAdmin')

    def test_save_model(self):
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.user
        tag = Tag(title='Test Category')
        admin = TagAdmin(Tag, self.site)
        form_class = admin.get_form(request)
        form = form_class(data={'title': 'Test Tag'}, instance=tag)
        change = True
        admin.save_model(request, tag, form, change)
        self.assertEqual(tag.slug, 'test-tag')
        self.assertEqual(tag.title, 'Test Tag')
