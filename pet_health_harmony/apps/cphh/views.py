# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import Client, Inquiry, Message, Image, Testimonial
from .forms import ImageUploadForm
from django.conf import settings
from django.contrib import messages

def index(request):
    return render(request, 'cphh/index.html')

def contact(request):
    inquiry_id = Inquiry.objects.create_inquiry(request.POST)
    request.session['id'] = inquiry_id
    message = Message.objects.create_message(request.POST)
    messages.success(request, "Successfully sent! We will respond within 1 business day.")
    return redirect(reverse('cphh:index'))
    
# TODO: fix testimonials creation
def gallery(request):
    if request.method == 'POST':  

        # try:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            client = Client.objects.get(id=request.session['id'])
            print "client", client
            image = Image.objects.create(client=client, model_pic=form.cleaned_data['image'], pet_name=request.POST['pet_name'])
            print "image", image
            testimonial = Testimonial.objects.create(client=client, testimonial = request.POST['testimonial'])
            print "testimonial", testimonial
            messages.success(request, "Success! Your submission is under review.")
        # except:
        #     print "didnt work"
        #     messages.error(request, "Something went wrong :( Try again?")
        return redirect(reverse('cphh:gallery'))
    else:

        context = {
            'images': Image.objects.filter(moderated=True).order_by('-created_at'),
            'testimonials': Testimonial.objects.filter(moderated=True).order_by('-created_at'),
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
            request.session['id'] = login_response.id
            return redirect(reverse('cphh:gallery'))
        else:
            messages.error(request, login_response)
    return render(request,'cphh/login.html')

def logout(request):
    request.session.clear()
    return redirect(reverse('cphh:gallery'))


# TODO: update logic to return to referrer vs hard-coded session id logic 
def destroy_image(request, id):
    image = Image.objects.get(id=id).delete()
    if request.session['id'] == 3:
        return redirect(reverse('cphh:manage'))
    else:
        return redirect(reverse('cphh:gallery'))

def approve_image(request, id):
    image = Image.objects.get(id=id)
    image.moderated = True
    image.save()
    return redirect(reverse('cphh:manage'))

def destroy_testimonial(request, id):
    testimonial = Testimonial.objects.get(id=id).delete()
    if request.session['id'] == 3:
        return redirect(reverse('cphh:manage'))
    else:
        return redirect(reverse('cphh:gallery'))

def approve_testimonial(request, id):
    testimonial = Testimonial.objects.get(id=id).delete()
    testimonial.moderated = True
    testimonial.save()
    return redirect(reverse('cphh:manage'))


def manage(request):
    if 'id' not in request.session or request.session['id'] != 3:
       return redirect(reverse('cphh:login'))
    if request.session['id'] == 3:
        context = {
                'images': Image.objects.filter(moderated=False),
                'testimonials': Testimonial.objects.filter(moderated=False),
                'media_url': settings.MEDIA_URL,
            }
        return render(request, 'cphh/manage.html', context) 