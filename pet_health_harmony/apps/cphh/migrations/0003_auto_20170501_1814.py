# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-01 18:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cphh', '0002_message_appt'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Inquiry',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='user',
            new_name='inquiry',
        ),
    ]
