from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.mail import EmailMessage

from smartfields import fields
from smartfields.dependencies import FileDependency
from smartfields.processors import ImageProcessor
import bcrypt
import re

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


    def submit_testimonial(self, postData, image, id):
        try:
            client = Client.objects.get(id=id)
            image = Image.objects.create(client=client, model_pic=image, pet_name=postData['pet_name'])
            testimonial = Testimonial.objects.create(client=client, testimonial = postData['testimonial'])
            body = "New gallery submission from {0} {1} awaiting your approval! http://chicagopethealth.com/manage".format(client.first_name, client.last_name)
            email = EmailMessage(
                'CPHH.com New Gallery Submission', 
                body,
                to=[settings.ADMIN_EMAIL]
            )
            email.send()
            return True
        except:
            return False


class InquiryManager(models.Manager):
    def create_inquiry(self, postData):
        inquiry = Inquiry.objects.create(email=postData['email'], first_name=postData['first_name'], last_name=postData['last_name'], phone=postData['phone'])
        return inquiry.id

    def send_email(self, postData):
        try: 
            body = "From: {0} {1} / Email: {2} / Phone: {3} / Appointment Prefs: {4} / Message: {5}".format(
                    str(postData['first_name']),
                    str(postData['last_name']),
                    str(postData['email']),
                    str(postData['phone']),
                    str(postData['appt']),
                    str(postData['message'])
                    )
            email = EmailMessage(
                'CPHH Website Inquiry', 
                body,
                to=[settings.ADMIN_EMAIL]
            )
            email.send()
            return True
        except:
            return False

class MessageManager(models.Manager):
    def create_message(self, postData):
        inquiry = Inquiry.objects.filter(email=postData['email'])
        message = Message.objects.create(inquiry=inquiry[0], message=postData['message'], appt=postData['appt'])
        return inquiry[0].id


# client requests two distinct models for current patients and prospectives 

# Current clients registered on site
class Client(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ClientManager()

# Prospective clients who requested information
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

