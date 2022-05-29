from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Notification

USER_MODEL = get_user_model()

class SocialAPITestCases(APITestCase):
    def setUp(self):
        self.test_user = USER_MODEL.objects.create_user(
            username='testuser', password='12345', email='testuser@test.com')
        self.test_user2 = USER_MODEL.objects.create_user(
            username='testuser2', password='12345', email='testuser2r@test.com')
        self.client.login(username='testuser', password='12345')
        self.test_notification = Notification.objects.create(message='Test notification',
                                                             user=self.test_user)

    def test_get_following(self):
        """
        Test for the following API endpoint.
        """

        url = reverse('social:following', args=[self.test_user.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_followers(self):
        """
        Test for the followers API endpoint.
        """

        url = reverse('social:followers', args=[self.test_user.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_unfollow(self):
        """
        Test the Follow/Unfollow API endpoint.
        """

        url = reverse('social:follow_unfollow', args=[self.test_user2.id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_messages(self):
        """
        Test for the messages API endpoint.
        """

        url = reverse('social:message_api')
        url += f'?username={self.test_user2.username}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('social:message_api')
        response = self.client.post(url, {
            'sender': self.test_user.id,
            'recipient': self.test_user2.id,
            'content': 'Test message',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_notifications(self):
        """
        Test for the notifications API endpoint.
        """

        url = reverse('social:notifications')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url + f'?pk={self.test_notification.id}', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
