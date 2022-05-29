from django.test import TestCase
from django.contrib.auth import get_user_model
from ..forms import NewMessageForm

USER_MODEL = get_user_model()


class NewMessageFormTest(TestCase):
    def setUp(self):
        self.test_user1 = USER_MODEL.objects.create_user(
            username='test.user1', email='test.user1@test.com', password='12345')
        self.test_user2 = USER_MODEL.objects.create_user(
            username='test.user2', email='test.user2@test.com', password='12345')
        self.test_user1.following.add(self.test_user2)
        self.test_user2.following.add(self.test_user1)

    def test_form_valid(self):
        form_data = {'sender': self.test_user1.id,
                     'recipient': self.test_user2.id,
                     'content': 'test message.'}
        form = NewMessageForm(data=form_data, user=self.test_user1)
        self.assertTrue(form.is_valid())
