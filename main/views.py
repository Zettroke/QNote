from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect

from notes.models import Note, ToDoList
# Create your views here.


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            user = authenticate(request, username=request.POST["login"], password=request.POST["password"])
            if user is None:
                return HttpResponse("Wrong login/password")
            login(request, user)
            if 'next' in request.GET.keys():
                return HttpResponseRedirect(request.GET["next"])
            else:
                return HttpResponseRedirect(reverse('main:root_view'))
        else:

            return render(request, "main/login.html")
    else:
        return HttpResponse("U already logged in")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('main:root_view'))


def root_view(request):
    if request.user.is_authenticated:
        note_list = Note.objects.all().filter(owner=request.user)
    else:
        note_list = []

    return render(request, "main/index.html", context={'note_list': note_list})