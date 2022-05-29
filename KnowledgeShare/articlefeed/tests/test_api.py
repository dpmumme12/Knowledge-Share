from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

USER_MODEL = get_user_model()

class ArticleFeedAPITestCases(APITestCase):
    def setUp(self):
        self.test_user = USER_MODEL.objects.create_user(
            username='testuser', password='12345', email='testuser@test.com')
        self.client.login(username='testuser', password='12345')

    def test_get_articlefeed(self):
        """
        Test for the article feed API endpoint.
        """

        url = reverse('articlefeed:article_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
