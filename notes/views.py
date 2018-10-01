from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from .models import Note, ToDoList, Tag

# Create your views here.


def note_detail(request, note_id):
    pass


@login_required
def note_creation(request):
    return render(request, "notes/create.html")


def note_add(request):
    print(

    )
    return HttpResponseRedirect(reversed("notes:create"))

