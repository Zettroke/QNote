from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm
# Create your views here.


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(request, username=form.cleaned_data["login"], password=form.cleaned_data["password"])
                login(request, user)
                if user is None:
                    return HttpResponse("Wrong login/password")
                elif 'next' in request.GET.keys():
                    return HttpResponseRedirect(request.GET["next"])
                else:
                    return HttpResponse("Hi {}!".format(user.username))
        else:
            form = LoginForm()
            return render(request, "login.html", {'form': form.as_table()})
    else:
        return HttpResponse("U already logged in")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('main:root_view'))


def root_view(request):
    return HttpResponse("Hey, that's main page!")