import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from ..forms import FolderForm, BulkChangeFolderForm, BulkDeleteForm
from ..models import Folder, Article

USER_MODEL = get_user_model()


class FolderFormTest(TestCase):
    def setUp(self):
        self.test_user1 = USER_MODEL.objects.create_user(
            username='test.user1', email='test.user1@test.com', password='12345')
        self.test_folder1 = Folder.objects.create(
            name='Test folder', owner=self.test_user1)
        self.test_folder2 = Folder.objects.create(
            name='Test folder', owner=self.test_user1, parent_folder=self.test_folder1)

    def test_form_valid(self):
        form_data = {'name': 'new folder',
                     'parent_folder': self.test_folder1}
        user_folders = [self.test_folder1, self.test_folder2]
        form = FolderForm(data=form_data, folders=user_folders)
        self.assertTrue(form.is_valid())

    def test_invalid_parent_folder(self):
        self.test_folder1.parent_folder = self.test_folder2
        user_folders = [self.test_folder1, self.test_folder2]
        form = FolderForm(instance=self.test_folder1, folders=user_folders)
        self.assertFalse(form.is_valid())


class BulkChangeFolderFormTest(TestCase):
    def setUp(self):
        self.test_user1 = USER_MODEL.objects.create_user(
            username='test.user1', email='test.user1@test.com', password='12345')
        self.test_folder1 = Folder.objects.create(
            name='Test folder', owner=self.test_user1)
        self.test_folder2 = Folder.objects.create(
            name='Test folder', owner=self.test_user1, parent_folder=self.test_folder1)
        self.test_article1 = Article.objects.create(
            author=self.test_user1, title='test article',
            content='test article content.',
            article_status_id=Article.Article_Status.DRAFT,
            version_status_id=Article.Version_Status.ACTIVE)

    def test_form_valid(self):
        form_data = {'change_folder-folder': self.test_folder1.id,
                     'change_folder-objects': json.dumps(
                         [{'id': self.test_folder2.id, 'object_type': 'folder'},
                          {'id': self.test_article1.id, 'object_type': 'article'}])
                     }
        user_folders = [self.test_folder1, self.test_folder2]
        form = BulkChangeFolderForm(data=form_data, folders=user_folders)
        self.assertTrue(form.is_valid())

    def test_invalid_parent_folder(self):
        form_data = {'change_folder-folder': self.test_folder2.id,
                     'change_folder-objects': json.dumps(
                         [{'id': self.test_folder1.id, 'object_type': 'folder'},
                          {'id': self.test_article1.id, 'object_type': 'article'}])
                     }
        user_folders = [self.test_folder1, self.test_folder2]
        form = BulkChangeFolderForm(data=form_data, folders=user_folders)
        self.assertFalse(form.is_valid())


class BulkDeleteFormTest(TestCase):
    def setUp(self):
        self.test_user1 = USER_MODEL.objects.create_user(
            username='test.user1', email='test.user1@test.com', password='12345')
        self.test_folder1 = Folder.objects.create(
            name='Test folder', owner=self.test_user1)
        self.test_folder2 = Folder.objects.create(
            name='Test folder', owner=self.test_user1, parent_folder=self.test_folder1)
        self.test_article1 = Article.objects.create(
            author=self.test_user1, title='test article',
            content='test article content.',
            article_status_id=Article.Article_Status.DRAFT,
            version_status_id=Article.Version_Status.ACTIVE)

    def test_form_delete(self):
        form_data = {'bulk_delete-objects': json.dumps(
            [{'id': self.test_folder1.id, 'object_type': 'folder'},
             {'id': self.test_folder2.id, 'object_type': 'folder'},
             {'id': self.test_article1.id, 'object_type': 'article'}])}
        form = BulkDeleteForm(data=form_data)
        if form.is_valid():
            form.delete()

        with self.assertRaises(Folder.DoesNotExist):
            Folder.objects.get(id=self.test_folder1.id)
        with self.assertRaises(Folder.DoesNotExist):
            Folder.objects.get(id=self.test_folder2.id)
        with self.assertRaises(Article.DoesNotExist):
            Article.objects.get(id=self.test_article1.id)
