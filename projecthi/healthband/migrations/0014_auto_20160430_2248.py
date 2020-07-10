# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160302004832 on 2016-05-01 05:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthband', '0013_auto_20160430_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='hContactEmail',
            field=models.EmailField(default='', max_length=30, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='hContactFName',
            field=models.CharField(default='', max_length=20, verbose_name="Contact's First Name"),
        ),
        migrations.AlterField(
            model_name='provider',
            name='hContactLName',
            field=models.CharField(default='', max_length=20, verbose_name="Contact's Last Name"),
        ),
        migrations.AlterField(
            model_name='provider',
            name='hContactPhone',
            field=models.CharField(default='', max_length=10, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='hospitalAddress',
            field=models.CharField(default='', max_length=50, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='hospitalCity',
            field=models.CharField(default='', max_length=30, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='hospitalName',
            field=models.CharField(default='', max_length=50, verbose_name='Hospital Name'),
        ),
    ]