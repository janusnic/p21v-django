# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_last_login_null'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(verbose_name='user', serialize=False, related_name='profile', to=settings.AUTH_USER_MODEL, primary_key=True)),
                ('interaction', models.PositiveIntegerField(default=0, verbose_name='interaction')),
                ('avatar', models.ImageField(null=True, upload_to='images/', blank=True, verbose_name='Profile Pic')),
                ('biography', models.TextField(null=True, blank=True)),
                ('homepage', models.URLField(null=True, blank=True)),
                ('twitter', models.URLField(null=True, blank=True)),
                ('github', models.URLField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Profiles',
                'verbose_name': 'Profile',
                'ordering': ('user',),
            },
        ),
        migrations.CreateModel(
            name='SocialInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('social', models.CharField(choices=[('fa-facebook', 'Facebook'), ('fa-github', 'Github'), ('fa-twitter', 'Twitter'), ('fa-google-plus', 'Google Plus'), ('fa-weibo', 'Weibo')], max_length='128')),
                ('url', models.URLField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('-date_joined',)},
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', to='auth.Group', related_query_name='user'),
        ),
        migrations.AddField(
            model_name='socialinfo',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
