# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils.uploads
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0002_image_thumbnail2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=200)),
            ],
            options={
                'verbose_name_plural': 'locations',
                'ordering': ['name'],
                'verbose_name': 'location',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=200)),
            ],
            options={
                'verbose_name_plural': 'people',
                'ordering': ['name'],
                'verbose_name': 'person',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(blank=True, verbose_name='name', max_length=200, null=True)),
                ('file', models.ImageField(upload_to=utils.uploads.get_unique_upload_path, verbose_name='file')),
            ],
            options={
                'verbose_name_plural': 'photos',
                'ordering': ['name'],
                'verbose_name': 'photo',
            },
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('size', models.CharField(db_index=True, verbose_name='size', max_length=20)),
                ('file', models.ImageField(upload_to=utils.uploads.get_unique_upload_path, verbose_name='file')),
                ('photo', models.ForeignKey(verbose_name='photo', to='photo.Photo')),
            ],
            options={
                'verbose_name_plural': 'thumbnails',
                'ordering': ['photo', 'size'],
                'verbose_name': 'thumbnail',
            },
        ),
        migrations.RemoveField(
            model_name='image',
            name='albums',
        ),
        migrations.RemoveField(
            model_name='image',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='image',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='album',
            options={'verbose_name_plural': 'albums', 'ordering': ['name'], 'verbose_name': 'album'},
        ),
        migrations.RemoveField(
            model_name='album',
            name='public',
        ),
        migrations.RemoveField(
            model_name='album',
            name='title',
        ),
        migrations.AddField(
            model_name='album',
            name='month',
            field=models.PositiveSmallIntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], verbose_name='month', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='name',
            field=models.CharField(default='', verbose_name='name', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='album',
            name='year',
            field=models.PositiveSmallIntegerField(choices=[(1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)], verbose_name='year', blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.AddField(
            model_name='photo',
            name='album',
            field=models.ForeignKey(verbose_name='album', to='photo.Album'),
        ),
        migrations.AddField(
            model_name='photo',
            name='people',
            field=models.ManyToManyField(to='photo.Person', verbose_name='people', blank=True),
        ),
        migrations.AddField(
            model_name='album',
            name='location',
            field=models.ForeignKey(to='photo.Location', on_delete=django.db.models.deletion.SET_NULL, verbose_name='location', blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='thumbnail',
            unique_together=set([('photo', 'size')]),
        ),
    ]
