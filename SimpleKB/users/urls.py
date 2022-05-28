from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import RegisterationView, UserSettingsView, DeleteAccountView
from .forms import LoginForm, ResetPasswodForm, PasswordSetForm

app_name = 'users'
urlpatterns = [
    path('', RegisterationView.as_view(), name='register'),
    path('login', auth_views.LoginView.as_view(
        template_name='users/login.html',
        authentication_form=LoginForm), name='login'),
    path('logout', auth_views.logout_then_login, name='logout'),
    path('password-reset', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        success_url=reverse_lazy('users:password_reset_done'),
        email_template_name='users/password_reset_email.html',
        form_class=ResetPasswodForm), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        post_reset_login=True,
        success_url=reverse_lazy('knowledgebase:dashboard'),
        form_class=PasswordSetForm), name='password_reset_confirm'),
    path('settings', UserSettingsView.as_view(), name='settings'),
    path('delete/Account', DeleteAccountView.as_view(), name='delete_account'),
]
