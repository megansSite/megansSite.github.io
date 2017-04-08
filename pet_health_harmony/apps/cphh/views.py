# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User, Message, Image
from .forms import ImageUploadForm
from django.conf import settings

def index(request):
    return render(request, 'cphh/index.html')

def contact(request):
    user_id = User.objects.create_user(request.POST)
    request.session['id'] = user_id
    message = Message.objects.create_message(request.POST)
    messages.success(request, "Successfully sent! We will respond within 1 business day.")
    return redirect(reverse('cphh:index'))

def images(request):
    img = Image.objects.all()
    return render(request,'cphh/images.html',{"img":img, 'media_url':settings.MEDIA_URL})

def upload(request):
    if request.method == 'POST':
        print "post"
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(id=request.session['id'])
            image = Image.objects.create(user=user, model_pic=form.cleaned_data['image'])
            messages.success(request, "Successfully uploaded")
            return redirect(reverse('cphh:images'))
    return redirect(reverse('cphh:images'))