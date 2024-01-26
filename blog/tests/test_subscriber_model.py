from unittest import TestCase

from django.utils import timezone

from ..models import Subscriber


class SubscriberModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Subscriber.objects.create(email="example@test.com")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        Subscriber.objects.all().delete()

    def test_subscriber_email_field_type(self):
        field_type = Subscriber._meta.get_field("email").get_internal_type()
        self.assertEqual(field_type, "CharField")

    def test_subscriber_email_field_verbose(self):
        field_verbose = Subscriber._meta.get_field("email").verbose_name
        self.assertEqual(field_verbose, "email")

    def test_subscriber_email_field_blank(self):
        field_blank = Subscriber._meta.get_field("email").blank
        self.assertEqual(field_blank, False)

    def test_subscriber_email_field_null(self):
        field_null = Subscriber._meta.get_field("email").null
        self.assertEqual(field_null, False)

    def test_subscriber_email_field_unique(self):
        field_unique = Subscriber._meta.get_field("email").unique
        self.assertEqual(field_unique, True)

    def test_subscriber_created_at_field_type(self):
        field_type = Subscriber._meta.get_field(
            "created_at",
        ).get_internal_type()
        self.assertEqual(field_type, "DateTimeField")

    def test_subscriber_created_at_field_auto_now_add(self):
        field_auto_now_add = Subscriber._meta.get_field(
            "created_at",
        ).auto_now_add
        self.assertEqual(field_auto_now_add, True)

    def test_subscriber_created_at_field_verbose(self):
        field_verbose = Subscriber._meta.get_field("created_at").verbose_name
        self.assertEqual(field_verbose, "добавлен")

    def test_subscriber_value(self):
        subscriber_fields_value = Subscriber.objects.get(pk=1)
        self.assertEqual(subscriber_fields_value.email, "example@test.com")
        self.assertEqual(
            subscriber_fields_value.created_at.date(),
            timezone.now().date(),
        )

    def test_subscriber_meta_fields(self):
        subscriber_meta = Subscriber._meta
        self.assertEqual(subscriber_meta.verbose_name, "подписчик(а)")
        self.assertEqual(subscriber_meta.verbose_name_plural, "подписчики")
        self.assertEqual(subscriber_meta.ordering, ("-created_at",))

    def test_subscriber_str(self):
        post_str = Subscriber.objects.get(pk=1).__str__()
        self.assertEqual(post_str, "example@test.com")
