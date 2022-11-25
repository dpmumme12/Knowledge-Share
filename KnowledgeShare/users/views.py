from datetime import datetime
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (authenticate, login, logout, get_user,
                                 update_session_auth_hash)
from django.contrib import messages
from KnowledgeShare.utils.xml import XMLParse
from .forms import UserRegisterationForm, UserSettingsForm, ChangePasswordForm


# Create your views here.
class RegisterationView(View):
    template_name = 'users/register.html'

    def get(self, request):
        RegisterForm = UserRegisterationForm()
        return render(request, self.template_name, {'RegisterForm': RegisterForm})

    def post(self, request):
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            login(request, authenticate(username=username, password=password))
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return render(request, self.template_name, {'RegisterForm': form})


class UserSettingsView(LoginRequiredMixin, View):
    template_name = 'users/settings.html'

    def get(self, request):
        user = get_user(request)
        return render(request, self.template_name,
                      {'UserForm': UserSettingsForm(instance=user),
                       'PasswordChangeForm': ChangePasswordForm(user)})

    def post(self, request):
        user = get_user(request)
        if 'user-settings-form' in request.POST:
            settings_form = UserSettingsForm(request.POST, request.FILES, instance=user)
            change_password_form = ChangePasswordForm(user)
            if settings_form.is_valid():
                settings_form.save()
                messages.success(request, 'User updated successfully!')
        elif 'change-password-form' in request.POST:
            settings_form = UserSettingsForm(instance=user)
            change_password_form = ChangePasswordForm(request.user, request.POST)
            if change_password_form.is_valid():
                change_password_form.save()
                update_session_auth_hash(request, change_password_form.user)
                messages.success(request, 'Password changed successfully!')

        return render(request, self.template_name, {'UserForm': settings_form,
                                                    'PasswordChangeForm': change_password_form})


class DeleteAccountView(LoginRequiredMixin, View):
    def post(self, request):
        user = get_user(request)
        try:
            user.delete()
            logout(request)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('users:settings')
        return redirect('users:login')


class LoginRedirectView(View):
    def get(self, request):
        return redirect('social:dashboard', request.user.username)


class LoggingView(LoginRequiredMixin, View):
    template_name = 'users/logs.html'

    def get(self, request):

        if not request.user.is_superuser:
            raise PermissionDenied()

        date = request.GET.get('date')
        log_filepath = 'logs\\log'
        if date and date != datetime.today().strftime('%Y-%m-%d'):
            log_filepath += F'.{date}'
        try:
            logs_xml = XMLParse(log_filepath)
            logs = logs_xml.serialize_xml()
        except FileNotFoundError:
            logs = None

        return render(request, self.template_name, {'logs': logs})
