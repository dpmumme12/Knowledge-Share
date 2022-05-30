import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Folder, Article

USER_MODEL = get_user_model()

class ArticleModelTest(TestCase):
    def setUp(self):
        self.test_user1 = USER_MODEL.objects.create_user(
            username='test.user1', email='test.user1@test.com', password='12345')
        self.test_article1 = Article.objects.create(
            author=self.test_user1, title='test article',
            content='test article content.',
            article_status_id=Article.Article_Status.DRAFT,
            version_status_id=Article.Version_Status.ACTIVE)

    def test_publish_article(self):
        self.test_article1.publish_article()
        self.assertTrue(
            self.test_article1.article_status_id == Article.Article_Status.PUBLISHED)

    def test_create_new_version(self):
        self.test_article1.publish_article()
        new_version = self.test_article1.create_new_version()
        self.assertTrue(
            new_version.version_status_id == Article.Version_Status.NEW_VERSION)
        self.assertTrue(
            self.test_article1.version_status_id == Article.Version_Status.ACTIVE)
