# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import Client, User, Message, Image
from .forms import ImageUploadForm
from django.conf import settings
from django.contrib import messages

def index(request):
    return render(request, 'cphh/index.html')

def contact(request):
    user_id = User.objects.create_user(request.POST)
    request.session['id'] = user_id
    message = Message.objects.create_message(request.POST)
    messages.success(request, "Successfully sent! We will respond within 1 business day.")
    return redirect(reverse('cphh:index'))

def gallery(request):
    if request.method == 'POST':  
        try:
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                client = Client.objects.get(id=request.session['id'])
                image = Image.objects.create(client=client, model_pic=form.cleaned_data['image'], pet_name=request.POST['pet_name'])
                messages.success(request, "Successfully uploaded")
        except:
            messages.error(request, "Something went wrong :( Try again?")
        return redirect(reverse('cphh:gallery'))
    else:
        context = {
            'images': Image.objects.all().order_by('-created_at'),
            'media_url': settings.MEDIA_URL,
        }
        return render(request,'cphh/gallery.html', context)

def register(request):
    if request.method == "POST":
        reg_valid, reg_response = Client.objects.validate(request.POST)
        if reg_valid:
            login_valid, login_response = Client.objects.login(request.POST)
            if login_valid:
                request.session['id'] =login_response.id
                messages.success(request, "Successfully registered!")
                return redirect(reverse('cphh:gallery'))
            else: 
                messages.error(request, login_response)
        else: 
            messages.error(request, reg_response)
                
    return render(request,'cphh/login.html')

def login(request):
    if request.method == "POST":
        login_valid, login_response = Client.objects.login(request.POST)
        if login_valid:
            request.session['id'] =login_response.id
            return redirect(reverse('cphh:gallery'))
        else:
            messages.error(request, login_response)
    return render(request,'cphh/login.html')

def logout(request):
    request.session.clear()
    return redirect(reverse('cphh:gallery'))

def destroy_image(request, id):
    print id
    image = Image.objects.get(id=id).delete()
    return redirect(reverse('cphh:gallery'))