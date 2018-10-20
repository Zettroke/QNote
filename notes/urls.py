from django.urls.conf import path
from . import views

app_name = 'notes'
urlpatterns = [
    path("<int:note_id>/", views.note_detail, name='detail'),
    path("create/", views.note_creation, name='creation'),
    path("create/add", views.note_add, name='add'),
    path("mark_todo_entry/<int:entry_id>/", views.mark_todo_entry, name='mark_todo_entry'),
    path("remove_file/<int:file_id>", views.remove_file, name="remove_file"),
    path("remove_note/<int:note_id>", views.remove_note, name="remove_file")
]
