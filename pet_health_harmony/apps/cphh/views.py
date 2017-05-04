# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import Client, Inquiry, Message, Image, Testimonial
from .forms import ImageUploadForm
from django.conf import settings


def index(request):
    return render(request, 'cphh/index.html')

def contact(request):
    if request.method == 'POST':
        try:
            inquiry_id = Inquiry.objects.create_inquiry(request.POST)
            message = Message.objects.create_message(request.POST)
            contact_success = Inquiry.objects.send_email(request.POST)
            if contact_success:
                messages.success(request, "Successfully sent! We will respond within 1 business day.")
        except: 
            messages.error(request, "Something went wrong. Please try again or call us during normal business hours.")
    return redirect(reverse('cphh:index'))
    
def gallery(request):
    if request.method == 'POST':  
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            success = Client.objects.submit_testimonial(request.POST, form.cleaned_data['image'], request.session['id'])
            if success:
                messages.success(request, "Success! Your submission is under review.")
        else:
            messages.error(request, "Something went wrong :( Try again? Please fill out all fields and include a pic!")
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
            request.session['email'] = login_response.email
            if request.session['email'] ==settings.ADMIN_EMAIL:
                return redirect(reverse('cphh:manage'))
            else:
                return redirect(reverse('cphh:gallery'))
        else:
            messages.error(request, login_response)
    return render(request,'cphh/login.html')

def logout(request):
    request.session.clear()
    return redirect(reverse('cphh:index'))


# TODO: update logic to return to referrer vs hard-coded session email logic 


def destroy_image(request, id):
    if request.session['email'] == settings.ADMIN_EMAIL:
        image = Image.objects.get(id=id).delete()
    return redirect(reverse('cphh:manage'))
    
def approve_image(request, id):
    if request.session['email'] == settings.ADMIN_EMAIL:
        image = Image.objects.get(id=id)
        image.moderated = True
        image.save()
    return redirect(reverse('cphh:manage'))

def destroy_testimonial(request, id):
    if request.session['email'] == settings.ADMIN_EMAIL:
        testimonial = Testimonial.objects.get(id=id).delete()
    return redirect(reverse('cphh:manage'))
    

def approve_testimonial(request, id):
    if request.session['email'] == settings.ADMIN_EMAIL:
        testimonial = Testimonial.objects.get(id=id)
        testimonial.moderated = True
        testimonial.save()
    return redirect(reverse('cphh:manage'))


def manage(request):
    if 'email' not in request.session or request.session['email'] != settings.ADMIN_EMAIL:
        return redirect(reverse('cphh:login'))
    elif request.session['email'] == settings.ADMIN_EMAIL:
        context = {
                'images': Image.objects.all().order_by('moderated'),
                'testimonials': Testimonial.objects.all().order_by('-created_at'),
                'clients': Client.objects.all().order_by('created_at'),
                'media_url': settings.MEDIA_URL,
            }
        return render(request, 'cphh/manage.html', context) 

        