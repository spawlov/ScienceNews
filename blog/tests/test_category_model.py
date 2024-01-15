from django.test import TestCase

from blog.models import Category


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(title='Test Category', slug='test-category')

    def test_category_title_type(self):
        field_type = Category._meta.get_field('title').get_internal_type()
        self.assertEqual(field_type, 'CharField')

    def test_category_title_length(self):
        field_length = Category._meta.get_field('title').max_length
        self.assertEqual(field_length, 255)

    def test_category_title_unique(self):
        field_unique = Category._meta.get_field('title').unique
        self.assertEqual(field_unique, True)

    def test_category_title_verbose(self):
        field_verbose = Category._meta.get_field('title').verbose_name
        self.assertEqual(field_verbose, 'название')

    def test_category_slug_type(self):
        field_type = Category._meta.get_field('slug').get_internal_type()
        self.assertEqual(field_type, 'SlugField')

    def test_category_slug_blank(self):
        field_blank = Category._meta.get_field('slug').blank
        self.assertEqual(field_blank, True)

    def test_category_slug_null(self):
        field_null = Category._meta.get_field('slug').blank
        self.assertEqual(field_null, True)

    def test_category_slug_unique(self):
        field_unique = Category._meta.get_field('slug').blank
        self.assertEqual(field_unique, True)

    def test_category_slug_length(self):
        field_length = Category._meta.get_field('slug').max_length
        self.assertEqual(field_length, 255)

    def test_category_slug_verbose(self):
        field_verbose = Category._meta.get_field('slug').verbose_name
        self.assertEqual(field_verbose, 'url')

    def test_category_value(self):
        category_fields_value = Category.objects.get(slug='test-category')
        self.assertEqual(category_fields_value.title, 'Test Category')
        self.assertEqual(category_fields_value.slug, 'test-category')
