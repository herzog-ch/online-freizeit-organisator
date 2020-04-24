from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm


# Create your views here.
def index(request):
    return HttpResponse('Hello this is the index')


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password1'])
            messages.success(request, 'User %s was registered successfully' % form.cleaned_data['username'])
            return HttpResponseRedirect('/login/')
    else:
        form = RegistrationForm()

    template = loader.get_template('login/signup.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))
    # or: return render(request, 'login/signup.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
            else:
                return HttpResponseRedirect('/login/')
    else:
        form = LoginForm()

    template = loader.get_template('login/login.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))
    # or: return render(request, 'login/signup.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')
