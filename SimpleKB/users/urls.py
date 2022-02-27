from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterationView
from .forms import LoginForm

app_name = 'users'
urlpatterns = [
    path('', RegisterationView.as_view(), name='register'),
    path('login', auth_views.LoginView.as_view(
        template_name='users/login.html',
        authentication_form=LoginForm), name='login'),
    path('logout', auth_views.logout_then_login, name='logout'),
]
