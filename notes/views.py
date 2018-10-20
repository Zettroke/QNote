from django.shortcuts import render, reverse, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.utils import timezone
from thumbnailer.thumbnailer import Thumbnailer
import random
import re
import os
import time
import logging
import json

from .models import Note, ToDoList, ToDoEntry, Tag, File

logger = logging.getLogger(__name__)
thumbnailer = Thumbnailer()
image_match = re.compile('image*')


def note_detail(request, note_id):
    n = get_object_or_404(Note, pk=note_id)

    if n.owner.id == request.user.id:
        return render(request, "notes/detail.html", {'note': n})
    else:
        return HttpResponseForbidden()


@login_required
def note_creation(request):
    tag_list = Tag.objects.filter(owner=request.user)
    free_space = request.user.storage.total_space - request.user.storage.used_space
    return render(request, "notes/create.html", {'tag_list': tag_list, 'title': "Note creation", "available_space": free_space})


def html_to_plain_text(text):
    no_tags = re.sub("<[^>]*>", " ", text).replace("&nbsp;", "").replace("\n", " ")  # replace all html tags with spaces
    return " ".join(no_tags.split())


@login_required
def note_add(request):
    start = time.clock()
    note = None
    try:
        if not request.POST["title"]:
            return JsonResponse({"status": "error", "error": "no title"})

        attach_size = sum(map(lambda x: x.size, request.FILES.values()))
        free_space = request.user.storage.total_space - request.user.storage.used_space
        if attach_size > free_space:
            return JsonResponse({"status": "error", "error": "no space", "free": free_space, "required": attach_size})

        note = Note(owner=request.user)
        note.title = request.POST["title"]

        note.text = request.POST["text"]

        note.plain_text = html_to_plain_text(request.POST["text"])
        if not note.plain_text.replace(" ", ""):
            note.text = ''
            note.plain_text = ''

        note.date_created = timezone.now()
        note.save()

        # Tag processing
        tag_num = int(request.POST["tag_count"])
        tag_list = set()
        for i in range(tag_num):
            tg = request.POST["tag" + str(i)]
            if tg.replace(' ', ''):
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

        # To Do lists processing
        for todo_index in range(int(request.POST["todo_list_count"])):
            entrys = []
            for todo_entry in range(int(request.POST["todo_entry_count_" + str(todo_index)])):
                entry = request.POST["todo_entry_{}_{}".format(todo_index, todo_entry)]
                if entry.replace(" ", ""):
                    entrys.append(entry)
            if len(entrys) != 0:
                todolist = ToDoList(note=note, owner=request.user)
                todolist.save()
                for entry in entrys:
                    ToDoEntry(text=entry, to_do_list=todolist).save()

        note.save()

        # Attachment processing
        for v in request.FILES.values():
            # md5 = hashlib.md5()
            f = File(
                owner=request.user,
                note=note,
                size=v.size,
                name=v.name,
                folder=hex(random.randint(0, 2**64))[2:]
            )
            if image_match.match(v.content_type):
                f.type = File.IMAGE

            os.makedirs(f.get_folder_path(), exist_ok=True)

            with open(f.get_file_path(), "wb") as file:
                for chunk in v.chunks():
                    file.write(chunk)

            f.save()
            if f.type == File.IMAGE:
                thumbnailer.make_thumbnail(f.get_file_path())

        stop = time.clock()
        print("note created in {}s.".format(str(stop - start)))
        return JsonResponse({"status": "success"})
    except KeyError as e:

        if note and note.id:
            note.delete()

        return JsonResponse({"status": "error", "error": "miss param", "miss param": e.args[0]})
    except Exception as e:

        if note and note.id:
            note.delete()

        return JsonResponse({"status": "error", "error": "unknown"})


@login_required
def mark_todo_entry(request, entry_id):
    entry = get_object_or_404(ToDoEntry, id=entry_id)
    if entry.to_do_list.owner == request.user:
        entry.is_complete = not entry.is_complete
        if entry.is_complete:
            entry.date_complete = timezone.now()
        else:
            entry.date_complete = None
        entry.save()
        return HttpResponse("success")
    else:
        return HttpResponseForbidden()


@login_required
def remove_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    if file.owner == request.user:
        file.delete()
        return JsonResponse({'status': "success",
                             'used_space': request.user.storage.used_space,
                             'total_space': request.user.storage.total_space})
    else:
        return HttpResponseForbidden()


@login_required
def remove_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.owner == request.user:
        note.delete()
        return HttpResponse("success")
    else:
        return HttpResponseForbidden()

