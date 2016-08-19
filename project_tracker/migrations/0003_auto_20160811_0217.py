# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-11 02:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_tracker', '0002_projectperson_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectperson',
            name='relationship',
            field=models.CharField(blank=True, choices=[('P', 'Primary contact')], max_length=1, null=True),
        ),
    ]