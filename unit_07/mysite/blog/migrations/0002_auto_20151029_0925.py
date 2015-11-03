# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='slug', max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='slug', max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='created_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='article',
            name='publish_date',
            field=models.DateTimeField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, verbose_name='the related tags', to='blog.Tag'),
        ),
    ]
