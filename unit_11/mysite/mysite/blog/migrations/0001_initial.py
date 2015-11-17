# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, blank=True, unique=True, populate_from='title', verbose_name='slug')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('publish_date', models.DateTimeField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.')),
                ('enable_comment', models.BooleanField(default=True)),
                ('content', models.TextField()),
                ('views_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('status', models.CharField(default='D', choices=[('D', 'Not Reviewed'), ('P', 'Published'), ('E', 'Expired')], max_length=1)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='name', max_length=100)),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, blank=True, unique=True, populate_from='name', verbose_name='slug')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(max_length=255)),
                ('views_count', models.IntegerField(default=0, verbose_name='views count')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, blank=True, populate_from='name')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('views_count', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(verbose_name='the related category', to='blog.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, verbose_name='the related tags', to='blog.Tag'),
        ),
    ]
