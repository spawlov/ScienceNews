from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse

from ..models import Subscriber
from ..views import delete_subscriber


class DeleteSubscriberViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_delete_subscriber_valid_email(self):
        subscriber = Subscriber.objects.create(email="test@example.com")
        request = self.factory.get(
            reverse("unsubscribe"),
            {"email": subscriber.email},
        )
        request.session = {"email": ""}
        response = delete_subscriber(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))
        self.assertFalse(
            Subscriber.objects.filter(email=subscriber.email).exists(),
        )

    def test_delete_subscriber_invalid_email(self):
        request = self.factory.get(
            reverse("unsubscribe"),
            {"email": "invalid_email"},
        )
        with self.assertRaises(Http404):
            delete_subscriber(request)
        self.assertFalse(
            Subscriber.objects.filter(email="test@example.com").exists(),
        )
