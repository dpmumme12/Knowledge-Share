from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import RequestFactory, TestCase

USER_MODEL = get_user_model()


def add_middleware_to_request(request, middleware_class):
    middleware = middleware_class(request)
    middleware.process_request(request)
    return request

def add_middleware_to_response(request, middleware_class):
    middleware = middleware_class()
    middleware.process_response(request)
    return request

class UsersViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.test_user1 = USER_MODEL.objects.create_user(
            username='test.user1', email='test.user1@test.com', password='12345')
        self.test_user2 = USER_MODEL.objects.create_user(
            username='test.user2', email='test.user2@test.com', password='12345')
        self.client.login(username=self.test_user1.username, password='12345')

    def test_registeration_view(self):
        url = reverse('users:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_settings_view(self):
        url = reverse('users:settings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_account_view(self):
        url = reverse('users:delete_account')
        response = self.client.post(url)
        self.assertRedirects(response, reverse('users:login'))
