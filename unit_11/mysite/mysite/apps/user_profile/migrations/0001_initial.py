# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('interaction', models.PositiveIntegerField(verbose_name='interaction', default=0)),
                ('user', models.OneToOneField(verbose_name='user', to=settings.AUTH_USER_MODEL, related_name='profile')),
            ],
            options={
                'verbose_name_plural': 'Profiles',
                'verbose_name': 'Profile',
                'ordering': ('user',),
            },
        ),
    ]
