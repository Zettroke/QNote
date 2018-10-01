from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(max_length=70)
    text = models.TextField(null=True)
    date_created = models.DateTimeField(null=True)

    notify = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag)

    importance = models.IntegerField(default=5)

    notification_config = models.OneToOneField('NotificationConfig', on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text[:min(len(self.text), 20)]


class ToDoList(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)


class ToDoEntry(models.Model):
    text = models.CharField(max_length=200)
    is_complete = models.BooleanField(default=False)
    date_complete = models.DateTimeField(null=True)
    to_do_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)


class NotificationConfig(models.Model):
    pass  # TODO: create notification config


class File(models.Model):
    pass # TODO: create File model
