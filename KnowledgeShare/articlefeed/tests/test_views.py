from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

USER_MODEL = get_user_model()

class ArticleFeedViewsTest(TestCase):

    def test_articlefeed_view(self):
        url = reverse('articlefeed:article_feed')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
