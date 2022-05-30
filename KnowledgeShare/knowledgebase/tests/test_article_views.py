from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from ..models import Article

USER_MODEL = get_user_model()


class ArticleViewsTest(TestCase):
    def setUp(self):
        self.test_user1 = USER_MODEL.objects.create_user(
            username='test.user1', email='test.user1@test.com', password='12345')
        self.test_user2 = USER_MODEL.objects.create_user(
            username='test.user2', email='test.user2@test.com', password='12345')
        self.test_article1 = Article.objects.create(
            author=self.test_user1, title='test article',
            content='test article content.',
            article_status_id=Article.Article_Status.DRAFT,
            version_status_id=Article.Version_Status.ACTIVE)
        self.test_article2 = Article.objects.create(
            author=self.test_user2, title='test article 2',
            content='test article content number 2.',
            article_status_id=Article.Article_Status.DRAFT,
            version_status_id=Article.Version_Status.ACTIVE)
        self.client.login(username=self.test_user1.username, password='12345')

    def test_get_article_view(self):
        url = reverse('knowledgebase:article', args=[self.test_article1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_foreign_article_view(self):
        url = reverse('knowledgebase:article', args=[self.test_article2.id])
        response = self.client.post(url, data={'article': self.test_article2,
                                               'user': self.test_user1})
        self.assertRedirects(response, url)

    def test_remove_foreign_article_view(self):
        url = reverse('knowledgebase:article_remove_foreign',
                      kwargs={'article_id': self.test_article2.id})
        response = self.client.post(url)
        self.assertRedirects(response, '/')

    def test_article_edit_view(self):
        url = reverse('knowledgebase:article_edit', args=[self.test_article1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_article_delete_view(self):
        url = reverse('knowledgebase:article_delete', args=[self.test_article1.id])
        response = self.client.post(url)
        redirect = reverse('knowledgebase:kb', kwargs={'username': self.test_user1.username})
        self.assertRedirects(response, redirect)
