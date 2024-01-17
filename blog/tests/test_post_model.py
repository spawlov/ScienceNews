from django.db import models
from django.test import TestCase
from django.utils import timezone

from ..models import Category, Post, Tag


class PostModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(
            title="Test Category",
            slug="test-category",
        )
        post = Post.objects.create(
            title="Test title",
            slug="test-slug",
            content="Test content",
            author="Test author",
            category=category,
        )
        post.tag.create(title="Test tag", slug="test-tag")

    def test_post_title_field_type(self):
        field_type = Post._meta.get_field("title").get_internal_type()
        self.assertEqual(field_type, "CharField")

    def test_post_title_field_max_length(self):
        field_length = Post._meta.get_field("title").max_length
        self.assertEqual(field_length, 255)

    def test_post_title_field_verbose(self):
        field_verbose = Post._meta.get_field("title").verbose_name
        self.assertEqual(field_verbose, "название")

    def test_post_slug_field_type(self):
        field_type = Post._meta.get_field("slug").get_internal_type()
        self.assertEqual(field_type, "SlugField")

    def test_post_slug_field_max_length(self):
        field_length = Post._meta.get_field("slug").max_length
        self.assertEqual(field_length, 255)

    def test_post_slug_field_blank(self):
        field_blank = Post._meta.get_field("slug").blank
        self.assertEqual(field_blank, True)

    def test_post_slug_field_null(self):
        field_null = Post._meta.get_field("slug").null
        self.assertEqual(field_null, True)

    def test_post_slug_field_unique(self):
        field_unique = Post._meta.get_field("slug").unique
        self.assertEqual(field_unique, True)

    def test_post_slug_field_verbose(self):
        field_verbose = Post._meta.get_field("slug").verbose_name
        self.assertEqual(field_verbose, "url")

    def test_post_author_field_type(self):
        field_type = Post._meta.get_field("author").get_internal_type()
        self.assertEqual(field_type, "CharField")

    def test_post_author_field_max_length(self):
        field_length = Post._meta.get_field("author").max_length
        self.assertEqual(field_length, 100)

    def test_post_author_field_verbose(self):
        title_field_verbose = Post._meta.get_field("author").verbose_name
        self.assertEqual(title_field_verbose, "автор")

    def test_post_content_field_type(self):
        field_type = Post._meta.get_field("content").get_internal_type()
        self.assertEqual(field_type, "TextField")

    def test_post_content_field_blank(self):
        field_blank = Post._meta.get_field("content").blank
        self.assertEqual(field_blank, True)

    def test_post_content_field_null(self):
        field_null = Post._meta.get_field("content").null
        self.assertEqual(field_null, True)

    def test_post_content_field_verbose(self):
        field_verbose = Post._meta.get_field("content").verbose_name
        self.assertEqual(field_verbose, "контент")

    def test_post_created_at_field_type(self):
        field_type = Post._meta.get_field("created_at").get_internal_type()
        self.assertEqual(field_type, "DateTimeField")

    def test_post_created_at_field_auto_now_add(self):
        field_auto_now_add = Post._meta.get_field("created_at").auto_now_add
        self.assertEqual(field_auto_now_add, True)

    def test_post_created_at_field_verbose(self):
        field_verbose = Post._meta.get_field("created_at").verbose_name
        self.assertEqual(field_verbose, "опубликовано")

    def test_post_photo_field_type(self):
        field_type = Post._meta.get_field("photo").get_internal_type()
        self.assertEqual(field_type, "FileField")

    def test_post_photo_field_blank(self):
        field_blank = Post._meta.get_field("photo").blank
        self.assertEqual(field_blank, True)

    def test_post_photo_field_null(self):
        field_null = Post._meta.get_field("photo").null
        self.assertEqual(field_null, True)

    def test_post_photo_field_upload_to(self):
        field_upload_to = Post._meta.get_field("photo").upload_to
        self.assertEqual(field_upload_to, "photos/%Y/%m/%d")

    def test_post_photo_field_verbose(self):
        field_verbose = Post._meta.get_field("photo").verbose_name
        self.assertEqual(field_verbose, "фото")

    def test_post_views_field_type(self):
        field_type = Post._meta.get_field("views").get_internal_type()
        self.assertEqual(field_type, "IntegerField")

    def test_post_views_field_default(self):
        field_upload_to = Post._meta.get_field("views").default
        self.assertEqual(field_upload_to, 0)

    def test_post_views_field_verbose(self):
        title_field_verbose = Post._meta.get_field("views").verbose_name
        self.assertEqual(title_field_verbose, "количество просмотров")

    def test_post_category_field_type(self):
        field_type = Post._meta.get_field("category").get_internal_type()
        self.assertEqual(field_type, "ForeignKey")

    def test_post_category_field_to(self):
        field_to = Post._meta.get_field("category").remote_field.model
        self.assertEqual(field_to, Category)

    def test_post_category_field_on_delete(self):
        field_on_delete = Post._meta.get_field("category").remote_field
        self.assertEqual(field_on_delete.on_delete, models.PROTECT)

    def test_post_category_field_related_name(self):
        field_related_name = Post._meta.get_field("category").remote_field
        self.assertEqual(field_related_name.related_name, "categories")

    def test_post_category_field_verbose(self):
        field_verbose = Post._meta.get_field("category").verbose_name
        self.assertEqual(field_verbose, "категория")

    def test_post_tag_field_to(self):
        field_to = Post._meta.get_field("tag").remote_field.model
        self.assertEqual(field_to, Tag)

    def test_post_tag_field_blank(self):
        field_blank = Post._meta.get_field("tag").blank
        self.assertEqual(field_blank, True)

    def test_post_tag_field_related_name(self):
        field_related_name = Post._meta.get_field("tag").remote_field
        self.assertEqual(field_related_name.related_name, "tags")

    def test_post_tag_field_verbose(self):
        field_verbose = Post._meta.get_field("tag").verbose_name
        self.assertEqual(field_verbose, "теги")

    def test_post_value(self):
        post_fields_value = Post.objects.get(slug="test-slug")
        test_tag = post_fields_value.tag.get(slug="test-tag")
        self.assertEqual(post_fields_value.title, "Test title")
        self.assertEqual(post_fields_value.slug, "test-slug")
        self.assertEqual(post_fields_value.content, "Test content")
        self.assertEqual(post_fields_value.author, "Test author")
        self.assertEqual(post_fields_value.category.title, "Test Category")
        self.assertEqual(post_fields_value.category.slug, "test-category")
        self.assertEqual(post_fields_value.views, 0)
        self.assertEqual(
            post_fields_value.created_at.date(),
            timezone.now().date(),
        )
        self.assertEqual(post_fields_value.tag.all()[0], test_tag)
        self.assertEqual(test_tag.title, "Test tag")
        self.assertEqual(test_tag.slug, "test-tag")

    def test_post_meta_fields(self):
        post_meta = Post._meta
        self.assertEqual(post_meta.verbose_name, "статья(ю)")
        self.assertEqual(post_meta.verbose_name_plural, "статьи")
        self.assertEqual(post_meta.ordering, ("-created_at",))

    def test_post_str(self):
        post_str = Post.objects.get(pk=1).__str__()
        self.assertEqual(post_str, "Test title")

    def test_post_get_absolute_url(self):
        post_url = Post.objects.get(pk=1).get_absolute_url()
        self.assertEqual(post_url, "/post/test-slug/")
