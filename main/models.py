from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.conf import settings
import os


class User(AbstractUser):
    total_space = models.BigIntegerField(default=1024 * 1024 * 100)
    used_space = models.BigIntegerField(default=0)
    timezone_offset = models.IntegerField(default=0)


@receiver(post_save, sender=User)
def user_post_save(instance, created, **kwargs):
    if created:
        os.makedirs(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, str(instance.id)), exist_ok=True)


@receiver(post_delete, sender=User)
def user_post_delete(instance, **kwargs):
    try:
        os.rmdir(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, str(instance.id)))
    except Exception as e:
        print(e)


