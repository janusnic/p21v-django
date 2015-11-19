# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='id',
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(verbose_name='Profile Pic', upload_to='images/', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='homepage',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(verbose_name='user', to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True, related_name='profile'),
        ),
    ]
