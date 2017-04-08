# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User, Message

def index(request):
    return render(request, 'cphh/index.html')

def contact(request):

    return redirect(reverse('cphh:index'))

def map(request):
    return render(request, 'cphh/map.html')