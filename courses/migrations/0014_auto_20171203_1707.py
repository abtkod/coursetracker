# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-04 01:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_auto_20171203_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=25),
        ),
    ]
