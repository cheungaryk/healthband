# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160302004832 on 2016-05-01 04:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthband', '0009_auto_20160428_0652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='hContactPhone',
        ),
    ]
