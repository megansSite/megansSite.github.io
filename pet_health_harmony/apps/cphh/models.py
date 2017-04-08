from __future__ import unicode_literals
import re
from django.db import models
from django.conf import settings

class UserManager(models.Manager):
    def create_user(self, postData):
        user = User.objects.create(email=postData['email'], first_name=postData['first_name'], last_name=postData['last_name'], phone=postData['phone'])
        return user.id

class MessageManager(models.Manager):
    def create_message(self, postData):
        user = User.objects.get(email=postData['email'])
        message = Message.objects.create(user=user, message=postData['message'])
        return user.id


class User(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Message(models.Model):
    user = models.ForeignKey(User)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MessageManager()

class Image(models.Model):
    user = models.ForeignKey(User)
    model_pic = models.ImageField(upload_to = settings.MEDIA_URL)
    pet_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
