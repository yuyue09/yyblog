# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-02 07:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YYblog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-create_time']},
        ),
    ]