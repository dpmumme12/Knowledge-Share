from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import RequestFactory, TestCase

from ..views import DashboardView, MessagesView, MessageDetailView, NewMessageView

USER_MODEL = get_user_model()

class SocialViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.test_user1 = USER_MODEL.objects.create_user(
            username='test.user1', email='test.user1@test.com', password='12345')
        self.test_user2 = USER_MODEL.objects.create_user(
            username='test.user2', email='test.user2@test.com', password='12345')

    def test_dashboard_view(self):
        url = reverse('social:dashboard', args=[self.test_user1.username])
        request = self.factory.get(url)
        request.user = self.test_user1

        response = DashboardView.as_view()(request, username=self.test_user1.username)
        self.assertEqual(response.status_code, 200)

    def test_messages_view(self):
        url = reverse('social:messages')
        request = self.factory.get(url)
        request.user = self.test_user1

        response = MessagesView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_new_message_view(self):
        url = reverse('social:new_message')
        request = self.factory.get(url)
        request.user = self.test_user1

        response = NewMessageView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_message_detail_view(self):
        url = reverse('social:message_detail', args=[self.test_user2.username])
        request = self.factory.get(url)
        request.user = self.test_user1

        response = MessageDetailView.as_view()(request, username=self.test_user2.username)
        self.assertEqual(response.status_code, 200)
