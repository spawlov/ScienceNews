from django.http import HttpResponseRedirect
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from ..models import Subscriber
from ..views import add_subscriber


class AddSubscriberViewTestCase(TestCase):
    def test_add_subscriber_view_post_request(self):
        factory = RequestFactory()
        client = Client()
        email = "test@example.com"
        request = factory.post(reverse("subscribe"), {"email": email})
        request.session = client.session
        response = add_subscriber(request)
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(request.session.get("email"), email)
        subscriber = Subscriber.objects.get(email=email)
        self.assertEqual(subscriber.email, email)

    def test_add_subscriber_view_invalid_email(self):
        factory = RequestFactory()
        client = Client()
        invalid_email = "test@example"  # Invalid email format
        request = factory.post(reverse("subscribe"), {"email": invalid_email})
        request.session = client.session
        response = add_subscriber(request)
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
