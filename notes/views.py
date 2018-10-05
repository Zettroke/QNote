from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.utils import timezone
import re

import datetime

from .models import Note, ToDoList, Tag

# Create your views here.


def note_detail(request, note_id):
    n = get_object_or_404(Note, pk=note_id)
    if n.owner.id == request.user.id:
        return render(request, "notes/detail.html", {'note': n, 'tag_list': n.tags.all()})
    else:
        return HttpResponseForbidden()

@login_required
def note_creation(request):
    tag_list = Tag.objects.filter(owner=request.user)
    return render(request, "notes/create.html", {'tag_list': tag_list})


@login_required
def note_add(request):
    note = Note(owner=request.user)
    note.title = request.POST["title"]
    note.text = request.POST["text"]

    no_tags = re.sub("<[^>]*>", " ", request.POST["text"]).replace("&nbsp;", "")  # replace all html tags with spaces
    note.plain_text = " ".join(no_tags.split())  # replace multi-spaces with one

    note.date_created = timezone.now()
    note.save()
    tag_num = int(request.POST["count"])
    tag_list = set()
    for i in range(tag_num):
        tg = request.POST["tag" + str(i)]
        if tg and tg.replace(' ', ''):
            tag_list.add(tg)
    user_tags = Tag.objects.filter(owner=request.user)
    for tag_name in tag_list:
        q_t = user_tags.filter(name=tag_name)
        if q_t.exists():
            tag = q_t[0]
        else:
            tag = Tag(name=tag_name, owner=request.user)
            tag.save()
        note.tags.add(tag)
    note.save()
    return HttpResponseRedirect(reverse("notes:detail", args=(note.id,)))

