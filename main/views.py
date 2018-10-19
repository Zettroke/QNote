from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from urllib.parse import unquote

from notes.models import Note, ToDoList, Tag
from .models import UserStorage
# Create your views here.


def register_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST["login"] and not User.objects.filter(username=request.POST["login"]).exists():

                user = User.objects.create_user(request.POST["login"], '', request.POST["password"])
                user.save()

                login(request, user)
                if 'next' in request.GET.keys():
                    return HttpResponseRedirect(request.GET["next"])
                else:
                    return HttpResponseRedirect(reverse('main:index_view'))

            else:
                return render(request, "main/register.html")
        else:
            return render(request, "main/register.html")
    else:
        return HttpResponse("U already logged in")


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
                return HttpResponseRedirect(reverse('main:index_view'))
        else:

            return render(request, "main/login.html")
    else:
        return HttpResponse("U already logged in")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('main:index_view'))


def index_view(request):
    if request.user.is_authenticated:
        note_list = Note.objects.all().filter(owner=request.user).order_by('-date_created')
    else:
        note_list = []

    return render(request, "main/index.html", context={'note_list': note_list, "title": "QNote"})


@login_required
def search(request):
    n = Note.objects.filter(owner=request.user)
    query = request.META['QUERY_STRING']
    k, v = '', ''

    if query:
        for i in query.split("&"):
            if i:
                k, v = i.split("=")
                if k == "tags":
                    break
    if k == "tags":
        include = []
        exclude = []
        tags = v.split("+")
        for t in tags:
            if t:
                if t[0] == "^":
                    exclude.append(unquote(t[1:]))
                else:
                    include.append(unquote(t))
        for tag in include:
            n = n.filter(tags__name__iexact=tag)
        for tag in exclude:
            n = n.exclude(tags__name__iexact=tag)

    text = ''
    if "text" in request.GET.keys():
        text = request.GET["text"]
    if text:
        n = n.filter(plain_text__search=text)

    tag_list = Tag.objects.filter(owner=request.user)

    return render(request, "main/search.html", {'tag_list': tag_list, 'title': "Note creation", 'note_list': n.all()})


def login_check(request):
    login_str = request.GET['login']

    if User.objects.filter(username=login_str).exists() or not login_str:
        ans = "False"
    else:
        ans = "True"

    return HttpResponse(ans)
