from django.test import TestCase
from django.contrib.auth import get_user_model
from ..forms import UserRegisterationForm

USER_MODEL = get_user_model()


class UserRegisterationFormTest(TestCase):
    def test_form_valid(self):
        form_data = {'username': 'new.user',
                     'email': 'newuser@test.com',
                     'password1': 'qwe1234!',
                     'password2': 'qwe1234!'}
        form = UserRegisterationForm(data=form_data)
        self.assertTrue(form.is_valid())
