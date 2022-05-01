from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user, get_user_model
from django.contrib import messages
from .forms import UserRegisterationForm, UserSettingsForm


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


class UserSettingsView(View):
    template_name = 'users/settings.html'

    def get(self, request):
        user = get_user(request)
        return render(request, self.template_name, {'UserForm': UserSettingsForm(instance=user)})

    def post(self, request):
        user = get_user(request)
        settings_form = UserSettingsForm(request.POST, request.FILES, instance=user)
        if settings_form.is_valid():
            settings_form.save()
            messages.success(request, 'User updated successfully!')

        return render(request, self.template_name, {'UserForm': settings_form})


class DeleteAccountView(View):
    def post(self, request):
        user = get_user(request)
        try:
            user.delete()
        except Exception as e:
            messages.error(request, str(e))
            return redirect('users:settings')
        return redirect('users:logout')
