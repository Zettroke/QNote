from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.conf import settings
import os

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(max_length=70)
    text = models.TextField(null=True)
    plain_text = models.TextField(null=True)
    date_created = models.DateTimeField(null=True)

    notify = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag)

    importance = models.IntegerField(default=5)

    notification_config = models.OneToOneField('NotificationConfig', on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.plain_text:
            return self.plain_text[:min(len(self.text), 20)]
        else:
            return "EmptyNote"


class ToDoList(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class ToDoEntry(models.Model):
    text = models.CharField(max_length=200)
    is_complete = models.BooleanField(default=False)
    date_complete = models.DateTimeField(null=True)
    to_do_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)


class NotificationConfig(models.Model):
    pass  # TODO: create notification config


class File(models.Model):
    """
        File model.
        Automatically add and remove space in owner's UserStorage.
        Automatically remove real file on model delete
    """
    IMAGE = 'img'
    AUDIO = 'audio'
    FILE = 'file'

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=512)
    folder = models.CharField(max_length=20)
    size = models.IntegerField()
    type = models.CharField(max_length=20, default='file')

    def get_file_path(self):
        return os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, str(self.owner.id), self.folder, self.name)

    def get_folder_path(self):
        return os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, str(self.owner.id), self.folder)

    def get_file_url(self):
        return "/" + '/'.join((settings.MEDIA_ROOT, str(self.owner.id), self.folder, self.name))

    def get_file_thumbnail_url(self):
        return "/" + '/'.join((settings.MEDIA_ROOT, str(self.owner.id), self.folder, "thumbnail_" + self.name))

    def is_gif(self):
        return self.name[self.name.rfind("."):].lower() == ".gif"


@receiver(post_delete, sender=File)
def file_post_delete(sender, instance, **kwargs):
    os.remove(instance.get_file_path())

    try:
        dr, f = os.path.split(instance.get_file_path())
        os.remove(os.path.join(dr, "thumbnail_" + f))
    except Exception:
        pass

    if not os.listdir(instance.get_folder_path()):
        os.rmdir(instance.get_folder_path())
    instance.owner.storage.used_space -= instance.size
    instance.owner.storage.save()
    pass


@receiver(post_save, sender=File)
def file_post_save(sender, instance, created, **kwargs):
    if created:
        instance.owner.storage.used_space += instance.size
        instance.owner.storage.save()

