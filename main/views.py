from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from urllib.parse import unquote
from django.utils import timezone

from notes.models import Note, ToDoList, Tag
# Create your views here.


def register_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST["login"] and not get_user_model().objects.filter(username=request.POST["login"]).exists():

                user = get_user_model().objects.create_user(request.POST["login"], '', request.POST["password"])
                user.timezone_offset = request.POST["timezone_offset"]
                user.save()

                login(request, user)
                if 'next' in request.GET.keys():
                    return HttpResponseRedirect(request.GET["next"])
                else:
                    return HttpResponseRedirect(reverse('main:index_view'))

        return render(request, "main/register.html")
    else:
        return HttpResponse("U already logged in")


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            user = authenticate(request, username=request.POST["login"], password=request.POST["password"])
            if user is None:
                return render(request, "main/login.html")
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

    query = request.META['QUERY_STRING']
    k, v = '', ''
    if query:
        for i in query.split("&"):
            if i:
                k, v = i.split("=")
                if k == "tags":
                    break

    notes = Note.objects.filter(owner=request.user)
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
            notes = notes.filter(tags__name=tag)
        for tag in exclude:
            notes = notes.exclude(tags__name=tag)

    if "text" in request.GET.keys():
        text = request.GET["text"]
        notes = notes.filter(plain_text__search=text)

    tag_list = Tag.objects.filter(owner=request.user)

    return render(request, "main/search.html", {'tag_list': tag_list, 'title': "Note creation", 'note_list': notes})


def username_check(request):
    login_str = request.GET['login']

    if not login_str or get_user_model().objects.filter(username=login_str).exists():
        ans = "False"
    else:
        ans = "True"

    return HttpResponse(ans)


@login_required
def account_view(request):
    files = request.user.file_set.all()
    notes = request.user.note_set.order_by('-date_created').all()
    return render(request, "main/account.html", context={"title": "Account: " + request.user.username, "files": files, "notes": notes})


@login_required
def password_change(request):
    try:
        if request.method == "POST":
            request.user.set_password(request.POST["password"])
            request.user.save()
            logout(request)
    except Exception: pass

    return redirect("main:index_view")


@login_required
def delete_account(request):
    request.user.delete()
    return redirect('main:index_view')
