from __future__ import unicode_literals
import re
from django.db import models
from django.conf import settings
from smartfields import fields
from smartfields.dependencies import FileDependency
from smartfields.processors import ImageProcessor
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'[A-Za-z]{2,}')

class ClientManager(models.Manager):
    def validate(self, postData):
        try: 
            Client.objects.get(email=postData['email']) 
            response = "User already exists. Please log in instead."
        except: 
            if not re.match(NAME_REGEX, postData['first_name']) or not re.match(NAME_REGEX, postData['last_name']):
                response = ("First and last name must be 2 or more characters.")
            elif postData['password'] != postData['conf_password']:
                response = ("Passwords must match")
            elif len(postData['password']) < 8:
                response = ("Password must be 8 or more characters")
            elif not EMAIL_REGEX.match(postData['email']):
                response = ("Invalid Email Address!")
            else:
                hashed = bcrypt.hashpw(postData['password'].encode('utf-8'), bcrypt.gensalt())
                client = Client.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], phone=postData['phone'], password=hashed)
                response = ("Successfully registered.")
                return True, response
        return False, response

    def login(self, postData):
        try: 
            email = str(postData['email'])
            password = str(postData['password'])
            client = Client.objects.get(email=email)
            clientPwBytes = password.encode('utf-8')
            hashedPwBytes = client.password.encode('utf-8')
            if hashedPwBytes == (bcrypt.hashpw(clientPwBytes, hashedPwBytes)):
                return True, client
            else:
                response = "Email and password don't match."
                return False, response
        except:
            response = "Email not found."
            return False, response


class InquiryManager(models.Manager):
    def create_inquiry(self, postData):
        inquiry = Inquiry.objects.create(email=postData['email'], first_name=postData['first_name'], last_name=postData['last_name'], phone=postData['phone'])
        return inquiry.id


class MessageManager(models.Manager):
    def create_message(self, postData):
        inquiry = Inquiry.objects.get(email=postData['email'])
        message = Message.objects.create(inquiry=inquiry, message=postData['message'], appt=postData['appt'])
        return inquiry.id



class Client(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ClientManager()

# client requests two distinct models for current patients and prospectives (Inquiry)
class Inquiry(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = InquiryManager()

class Message(models.Model):
    inquiry = models.ForeignKey(Inquiry, null=True, blank=True)
    message = models.TextField()
    appt = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False);
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MessageManager()

class Image(models.Model):
    client = models.ForeignKey(Client, null=True, blank=True)
    model_pic = fields.ImageField(dependencies=[
        FileDependency(processor=ImageProcessor(
            format='PNG', scale={'max_width': 500, 'max_height': 500}))
    ])
    moderated = fields.BooleanField(default=False)
    pet_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Testimonial(models.Model):
    client = models.ForeignKey(Client, null=True, blank=True)
    testimonial = fields.TextField()
    moderated = fields.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

