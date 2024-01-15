from django.test import TestCase

from blog.models import Tag


class CategoryModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Tag.objects.create(title='Test tag', slug='test-tag')

    def test_category_title_type(self):
        field_type = Tag._meta.get_field('title').get_internal_type()
        self.assertEqual(field_type, 'CharField')

    def test_category_title_length(self):
        field_length = Tag._meta.get_field('title').max_length
        self.assertEqual(field_length, 50)

    def test_category_title_unique(self):
        field_unique = Tag._meta.get_field('title').unique
        self.assertEqual(field_unique, True)

    def test_category_title_verbose(self):
        field_verbose = Tag._meta.get_field('title').verbose_name
        self.assertEqual(field_verbose, 'название')

    def test_category_slug_type(self):
        field_type = Tag._meta.get_field('slug').get_internal_type()
        self.assertEqual(field_type, 'SlugField')

    def test_category_slug_blank(self):
        field_blank = Tag._meta.get_field('slug').blank
        self.assertEqual(field_blank, True)

    def test_category_slug_null(self):
        field_null = Tag._meta.get_field('slug').blank
        self.assertEqual(field_null, True)

    def test_category_slug_unique(self):
        field_unique = Tag._meta.get_field('slug').blank
        self.assertEqual(field_unique, True)

    def test_category_slug_length(self):
        field_length = Tag._meta.get_field('slug').max_length
        self.assertEqual(field_length, 50)

    def test_category_slug_verbose(self):
        field_verbose = Tag._meta.get_field('slug').verbose_name
        self.assertEqual(field_verbose, 'url')

    def test_category_value(self):
        category_fields_value = Tag.objects.get(slug='test-tag')
        self.assertEqual(category_fields_value.title, 'Test tag')
        self.assertEqual(category_fields_value.slug, 'test-tag')

    def test_post_meta_fields(self):
        post_meta = Tag._meta
        self.assertEqual(post_meta.verbose_name, 'тег(и)')
        self.assertEqual(post_meta.verbose_name_plural, 'теги')
        self.assertEqual(post_meta.ordering, ('title',))

    def test_post_str(self):
        post_str = Tag.objects.get(pk=1).__str__()
        self.assertEqual(post_str, 'Test tag')

    def test_post_get_absolute_url(self):
        post_url = Tag.objects.get(pk=1).get_absolute_url()
        self.assertEqual(post_url, '/tag/test-tag/')
