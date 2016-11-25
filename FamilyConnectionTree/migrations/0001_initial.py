# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-01 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('familyName', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('familyPicture', models.ImageField(default='../static/css/images/bg.jpg', upload_to='pic_folder/', verbose_name='Family Picture')),
                ('aboutFamily', models.TextField(verbose_name='About Family')),
                ('numberOfMembers', models.IntegerField(default=0)),
            ],
        ),
    ]