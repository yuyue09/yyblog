# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-06 03:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YYblog', '0007_auto_20170706_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='head_photo',
            field=models.ImageField(default='head_photos/no_image.jpg', height_field=100, upload_to='head_photos/', width_field=100),
        ),
        migrations.AlterField(
            model_name='statepost',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 6, 11, 44, 37, 69421)),
        ),
    ]