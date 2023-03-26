from django.shortcuts import render
from django.views.generic import (
    View,
    CreateView
)

from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from .forms import UserRegisterForm, LoginForm
from .models import User


# Create your views here.


class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password_1 = form.cleaned_data['password_1']
        password_2 = form.cleaned_data['password_2']

        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        gender = form.cleaned_data['gender']

        User.objects.create_user(
            username=username,
            email=email,
            password=password_1,
            first_name=first_name,
            last_name=last_name,
            gender=gender
        )

        return super(UserRegisterView, self).form_valid(form)


class LoginUserView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(
            username=username,
            password=password,
        )

        login(self.request, user=user)
        return super(LoginUserView, self).form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)

        return HttpResponseRedirect(
            reverse('users_app:user-login')
        )