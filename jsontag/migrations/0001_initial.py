# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-08 15:50
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('object_id', models.UUIDField(primary_key=True, serialize=False)),
                ('contact', django.contrib.postgres.fields.jsonb.JSONField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='ObjectTag',
            fields=[
                ('object_id', models.UUIDField()),
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('object_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('group', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('object_id', models.UUIDField(primary_key=True, serialize=False)),
                ('translation', django.contrib.postgres.fields.jsonb.JSONField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='translation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='jsontag.Translation'),
        ),
        migrations.AddField(
            model_name='objecttag',
            name='tag_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsontag.Tag'),
        ),
    ]
