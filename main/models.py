from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.conf import settings
import os


class UserStorage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="storage")
    total_space = models.BigIntegerField(default=1024*1024*100)
    used_space = models.BigIntegerField(default=0)


@receiver(post_save, sender=UserStorage)
def user_storage_post_save(instance, created, **kwargs):
    if created:
        os.makedirs(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, str(instance.user.id)), exist_ok=True)


@receiver(post_delete, sender=UserStorage)
def user_storage_post_delete(instance, **kwargs):
    try:
        os.rmdir(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, str(instance.user.id)))
    except Exception as e:
        print(e)


@receiver(post_save, sender=User)
def user_post_save(instance, created, **kwargs):
    if created and not hasattr(instance, 'storage'):
        print("Created user storage")
        u = UserStorage(user=instance)
        u.save()
        instance.storage = u



# Create your models here.
