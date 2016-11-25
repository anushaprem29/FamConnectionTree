# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-01 08:14
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('FamilyConnectionTree', '0004_post_family'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Name')),
                ('phone', models.CharField(max_length=10, verbose_name='Phone Number')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, verbose_name='Gender')),
                ('picture', models.ImageField(default='../static/css/images/bg.jpg', upload_to='pictures/', verbose_name='Profile Picture')),
                ('dob', models.DateField(blank=True, default=datetime.datetime.now, verbose_name='Date Of Birth')),
                ('familyName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FamilyConnectionTree.Family')),
                ('userName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]