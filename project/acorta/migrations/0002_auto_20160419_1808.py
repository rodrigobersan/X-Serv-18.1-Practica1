# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-19 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acorta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Direcciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccionlarga', models.CharField(max_length=256)),
                ('direccioncorta', models.CharField(max_length=128)),
            ],
        ),
        migrations.DeleteModel(
            name='URLsDB',
        ),
    ]