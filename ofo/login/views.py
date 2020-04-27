from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm


def signup_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(form.cleaned_data['username'], email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password1'])
                messages.success(request, 'User %s wurde erfolgreich registriert.' % form.cleaned_data['username'],
                                 extra_tags="text-success")
                return redirect('login')
            except forms.ValidationError:
                pass
    else:
        form = RegistrationForm()

    template = loader.get_template('login/signup.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('login')
            else:
                messages.error(request, 'Falscher Benutzername oder Passwort.', extra_tags="text-danger")
                return redirect('login')
    else:
        form = LoginForm()

    template = loader.get_template('login/login.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))


def logout_view(request):
    logout(request)
    return redirect('login')
