# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160302004832 on 2016-04-25 00:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthband', '0007_auto_20160424_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='hContactEmail',
            field=models.EmailField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='provider',
            name='hContactFName',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='provider',
            name='hContactLName',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='provider',
            name='hContactPhone',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='provider',
            name='hospitalAddress',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='provider',
            name='hospitalCity',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='provider',
            name='hospitalName',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='provider',
            name='hospitalState',
            field=models.CharField(choices=[('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'), ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'), ('FL', 'FL'), ('GA', 'GA'), ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('IA', 'IA'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'), ('MD', 'MD'), ('MA', 'MA'), ('MI', 'MI'), ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'), ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'), ('NJ', 'NJ'), ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'), ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'), ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY')], default='', max_length=2),
        ),
        migrations.AlterField(
            model_name='provider',
            name='hospitalZip',
            field=models.CharField(default='', max_length=5),
        ),
    ]
