from __future__ import unicode_literals
import re
from django.db import models

class UserManager(models.Manager):
    def create_user(self, postData):
        user = User.objects.create(email=postData['email'], first_name=postData['first_name'], last_name=postData['last_name'], phone=postData['phone'])
        return True

class MessageManager(models.Manager):
    def create_message(self, postData):
        user = User.objects.get(email=postData['email'])
        message = Message.objects.create(user=user, message=postData['message'])
        return True


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

