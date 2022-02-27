from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings
from .forms import UserRegisterationForm


# Create your views here.
class RegisterationView(View):

    def get(self, request):
        RegisterForm = UserRegisterationForm()
        return render(request, 'users/register.html', {'RegisterForm': RegisterForm})

    def post(self, request):
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return render(request, 'users/register.html', {'RegisterForm': form})
