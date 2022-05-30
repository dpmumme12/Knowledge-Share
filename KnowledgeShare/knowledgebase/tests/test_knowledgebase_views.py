from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from ..models import Article, Folder

USER_MODEL = get_user_model()

class KnowledgebaseViewsTest(TestCase):
    def setUp(self):
        self.test_user1 = USER_MODEL.objects.create_user(
            username='test.user1', email='test.user1@test.com', password='12345')
        self.test_folder = Folder.objects.create(
            name='Test folder', owner=self.test_user1)
        self.test_article1 = Article.objects.create(
            author=self.test_user1, title='test article',
            content='test article content.',
            article_status_id=Article.Article_Status.DRAFT,
            version_status_id=Article.Version_Status.ACTIVE)
        self.client.login(username=self.test_user1.username, password='12345')

    def test_get_knowledgebase_view(self):
        url = reverse('knowledgebase:kb', args=[self.test_user1.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_kb_article_edit_view(self):
        url = reverse('knowledgebase:kb_article_edit',
                      kwargs={'pk': self.test_article1.id})
        response = self.client.post(url, data={'title': 'new article title'})
        self.assertRedirects(
            response, reverse('knowledgebase:kb', args=[self.test_user1.username]))

    def test_create_folder_view(self):
        url = reverse('knowledgebase:kb', args=[self.test_user1.username])
        response = self.client.post(url, data={'name': 'test_folder_2'})
        self.assertRedirects(response, url)

    def test_folder_edit_view(self):
        url = reverse('knowledgebase:folder_edit', args=[self.test_folder.id])
        response = self.client.post(url, data={'name': 'new folder title'})
        self.assertRedirects(
            response, reverse('knowledgebase:kb', args=[self.test_user1.username]))

    def test_folder_delete_view(self):
        url = reverse('knowledgebase:folder_delete', args=[self.test_folder.id])
        response = self.client.post(url)
        redirect = reverse('knowledgebase:kb', kwargs={'username': self.test_user1.username})
        self.assertRedirects(response, redirect)
