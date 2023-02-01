
import PIL.Image as Image
import numpy as np
import io
import json
import requests
import base64
from email.mime import base
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from django.dispatch import receiver
from .models import Client,Project,Role
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.core.files.storage import get_storage_class
default_storage = get_storage_class()()


@receiver(post_save, sender=User)
def post_save_create_client(sender, instance, created, **kwargs):

    if created:
        if not Token.objects.filter(user = instance).exists():
            Token.objects.create(user=instance)

        if instance.username[:2] == 'AM':
            Role.objects.create(user = instance,role="Artist Manager")
        elif instance.username[:2] == 'PM':
            Role.objects.create(user = instance,role="Product Manager")
        else:
            Role.objects.create(user = instance,role="Client")
            Client.objects.create(
                user=instance,
                name=instance.username,
                email=instance.email,
            )

@receiver(post_save,sender=Project)
def post_save_update_project(sender,instance,created,**kwargs):
    if created:
        if instance.title is None:
            instance.title = str(instance.project_template.name) + " - " + instance.stage + " - " + str(instance.id)
            instance.save()
