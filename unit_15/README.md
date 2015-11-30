## p21v-django unit 15

Модель Album
===============
foreman run django-admin.py startapp photo mysite/apps/photo

models.py
---------
```
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.dates import MONTHS

from utils.uploads import get_unique_upload_path
from .utils import generate_thumbnail

MONTH_CHOICES = [(key, value) for key, value in MONTHS.items()]

YEAR_CHOICES = [(year, year) for year in
                range(1950, (datetime.now().year + 1))]

class Location(models.Model):
    """A location is a physical location that can be applied to an album."""

    name = models.CharField(_('name'), max_length=200)

    class Meta:
        ordering = ['name', ]
        verbose_name = _('location')
        verbose_name_plural = _('locations')

    @models.permalink
    def get_absolute_url(self):
        return ('location', [str(self.id)])

    def __str__(self):
        return self.name

    @property
    def cover_photo(self):
        """
        Returns the cover photo for this person, which for now is just the
        first photo from the first album based on whatever ordering is the
        default.
        """
        if self.album_set.count():
            return self.album_set.first().photo_set.first()


class Person(models.Model):
    """A person is an actual person that can be tagged in photos."""

    name = models.CharField(_('name'), max_length=200)

    class Meta:
        ordering = ['name', ]
        verbose_name = _('person')
        verbose_name_plural = _('people')

    @models.permalink
    def get_absolute_url(self):
        return ('person', [str(self.id)])

    def __str__(self):
        return self.name

    @property
    def cover_photo(self):
        """
        Returns the cover photo for this person, which for now is just the
        first photo based on whatever ordering is the default.
        """
        return self.photo_set.first()

class Album(models.Model):
    """
    An album is a collection of photos. It belongs to a location and can also
    have a month and a year associated with it.
    """

    name = models.CharField(_('name'), max_length=200)
    month = models.PositiveSmallIntegerField(
        _('month'), null=True, blank=True, choices=MONTH_CHOICES)
    year = models.PositiveSmallIntegerField(
        _('year'), null=True, blank=True, choices=YEAR_CHOICES)

    location = models.ForeignKey(
        Location, null=True, blank=True,
        verbose_name=_('location'), on_delete=models.SET_NULL)

    class Meta:
        ordering = ['name', ]
        verbose_name = _('album')
        verbose_name_plural = _('albums')

    @models.permalink
    def get_absolute_url(self):
        return ('album', [str(self.id)])

    def __str__(self):
        return self.name

    @property
    def cover_photo(self):
        """
        Returns the cover photo for this album, which for now is just the
        first photo based on whatever ordering is the default.
        """
        return self.photo_set.first()

    def get_date_display(self):
        """
        Returns a pretty display of the month and year in one of the formats:
        - 'January 2014'
        - 'January'
        - '2014'
        """
        month = self.get_month_display() or ''
        year = self.get_year_display() or ''
        return '{} {}'.format(month, year).strip()


class Photo(models.Model):
    """
    A photo is just that - a single photo. It can belong to only one album.
    """

    name = models.CharField(_('name'), max_length=200, null=True, blank=True)
    file = models.ImageField(_('file'), upload_to=get_unique_upload_path)

    album = models.ForeignKey(Album, verbose_name=_('album'))
    people = models.ManyToManyField(
        Person, blank=True, verbose_name=_('people'))

    class Meta:
        ordering = ['name', ]
        verbose_name = _('photo')
        verbose_name_plural = _('photos')

    @models.permalink
    def get_absolute_url(self):
        return ('photo', [str(self.id)])

    def __str__(self):
        return self.name

    def thumbnail(self, size):
        """
        Generate and return a thumbnail with the given size. Only do this once
        in this instance to save on hits to the Thumnail model.
        """
        prop_name = '_thumb_%s' % size.replace('-', '_')
        instance, created = self.thumbnail_set.get_or_create(size=size)
        if not hasattr(self, prop_name):
            setattr(self, prop_name, instance.file)
        return getattr(self, prop_name)

    @property
    def file_thumb(self):
        """
        Shortcut to generate a '200x200-fit' thumbnail. Useful in templates.
        """
        return self.thumbnail('200x200-fit')

    @property
    def file_medium(self):
        """
        Shortcut to generate a '1024x768-thumb' thumbnail. Useful in templates.
        """
        return self.thumbnail('1024x768-thumb')


class Thumbnail(models.Model):
    """
    A thumbnail is a smaller resolution size of a photo. It knows how to
    generate itself once it has a size and a photo associated to it.
    """

    size = models.CharField(_('size'), max_length=20, db_index=True)
    file = models.ImageField(_('file'), upload_to=get_unique_upload_path)
    photo = models.ForeignKey(Photo, verbose_name=_('photo'))

    class Meta:
        ordering = ['photo', 'size', ]
        unique_together = ('photo', 'size', )
        verbose_name = _('thumbnail')
        verbose_name_plural = _('thumbnails')

    def __str__(self):
        return '%s (%s)' % (self.photo, self.size)

    def save(self, **kwargs):
        """
        If we have a photo and a size, generate a thumbnail before saving.
        """
        if self.photo and self.size:
            self.generate()
        super().save(**kwargs)

    def generate(self):
        """
        Generate the thumbnail. This happens regardless of whether we already
        have one generated. The new one will overwrite the existing one (while
        keeping the same filename).
        """
        self.file = generate_thumbnail(self.photo.file, self.size)
```
base.py
-------
```
PROJECT_APPS = (
    'apps.accounts',
    'apps.blog',
    'apps.photo',

)

########## MEDIA CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(PROJECT_ROOT, 'media'))

# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION

```

Migrations
-------------
```
foreman run django-admin.py makemigrations photo

foreman run django-admin.py migrate

```

admin.py
---------
```
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Person, Location, Album, Photo, Thumbnail


class NameOnlyAdmin(admin.ModelAdmin):
    list_display = ['name', ]


class AlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'month', 'year', 'location', ]


class ThumbnailInline(admin.TabularInline):
    model = Thumbnail
    readonly_fields = ['size', 'file', ]


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['name', 'album', ]
    inlines = [ThumbnailInline, ]


admin.site.register(Person, NameOnlyAdmin)
admin.site.register(Location, NameOnlyAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)

```

Общие представления и отображение объектов
===========================================

Django предлагает полезный и удобный набор встроенных общих представлений-классов, который позволяют отображать список объектов или конкретный объект.

CBV позволяет нам использовать особенности объектно-ориентированного программирования при разработке наших отображений. Теперь мы можем реализовывать базовые классы, несущие определенную функциональность и использовать их как примеси (mixins) для наших отображений.
```
from django.views.generic import ListView
```

получение списка объектов или индивидуального объекта
------------------------------------------------------

определить представление:
-------------------------

### views.py
```
from django.views.generic import ListView
from apps.photo.models import Album

class List(ListView):
    model = Album
```
привяжем представление к url:
------------------------------
### urls.py
```
from django.conf.urls import patterns, url
from . import views
from .views import album

urlpatterns = patterns('',
    url(r'^albums/$', Album.as_view()),
)

urlpatterns += [
    # Core URLs
    url(r'^', include('core.urls', namespace='core')),
    url(r'^blog/', include('apps.blog.urls', namespace='blog')),
    url(r'^photo/', include('apps.photo.urls', namespace='photo')),

```

Мы можем явно указать в представлении, какой шаблон мы хотим использовать. Для этого мы должны добавить в представление атрибут template_name, с указанием имени шаблона. Если явно не указывать этот атрибут, Django “вычислит” его из названия объекта. В данном случае, таким “вычисленным” шаблоном будет "photo/album_list.html" – часть “photo” берется из имени приложения, определяющего модель, а часть “album” - это просто название модели в нижнем регистре.

Таким образом, если в настройках TEMPLATE_LOADERS “включен” класс загрузчика django.template.loaders.app_directories.Loader, то путь к шаблону будет следующим : /path/to/project/templates/photo/album_list.html

При обработке шаблона (рэндеринге), будет использоваться контекст, содержащий переменную album_list. Это переменная хранит список всех объектов (album). 

шаблон album_list.html :
------------------------

```
{% extends 'base.html' %}

{% load i18n %}

{% block content %}
    <ul class="albums">
        {% for album in album_list %}
            
            <li>
                <a href="{{ url }}">
                    
                    <span class="name">{{ album.name|truncatechars:"45" }}</span>
                    
                </a>
            </li>
        {% endfor %}
    </ul>
{% endblock %}


```
Это действительно все, что нужно сделать. Все крутые “фичи” общих представлений-классов можно получить лишь устанавливая значения определенных атрибутов в представлении. 

Создание “дружелюбного” контента для шаблона
--------------------------------------------
Если вы оперируете запросом(queryset) или объектом, Django способно добавить в контекст переменную с именем модели в нижнем регистре. Эта переменная предоставляется в дополнение к стандартному значению object_list, и содержит то же самое значение, н-р, album_list.

Если этот вариант вас не устраивает, то имя переменной контекста можно задать вручную. Для этой цели служит атрибут context_object_name, который определяет имя переменной в контексте:
```
# views.py

from django.views.generic import ListView
from apps.photo.models import Album

class List(ListView):
    model = Album
    context_object_name = 'my_favourite_albums'
```

Добавление дополнительного контента
------------------------------------
Часто возникает потребность передать в контекст некоторые дополнительные данные, помимо тех, что автоматически предоставляются представлением. Представление-класс DetailView предоставляет нам только переменную контекста, содержащую данные об album, но как нам передать дополнительную информацию в шаблон?

Вы можете создать подкласс от DetailView и переопределить в нем метод get_context_data. Реализация метода по умолчанию просто добавляет объект, который будет доступен в шаблоне. Но переопределив метод, вы можете добавить любые дополнительные данные(расширить контекст):
```
class List(ListView):
    model = Album
    paginate_by = settings.PHOTOS_PER_PAGE
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Albums')
        return context

```
В общем случае, метод get_context_data объединяет(сливает вместе) данные контекста всех родительских классов с данными текущего класса. Чтобы сохранить такое поведение в пользовательских классах, в которых вы собираетесь изменять контекст, вы должны в начале вызвать метод get_context_data родительского класса. Если нет двух классов, которые пытаются определить одинаковый ключ, - вы получите желаемый результат. Однако, если есть некий класс, который пытается переопределить ключ, установленный родительскими классами(после вызова super), то любой потомок этого класса также должен явно установить такой ключ(после вызова super), если необходимо гарантировать полное переопределение данных родителей. Если у вас возникли проблемы, просмотрите mro(method resolution order) вашего представления.

Отображение подмножеств объектов
---------------------------------
Аргумент model, определяющий модель базы данных, с которой работает данное представление, доступен во всех общих представлениях-классах, которые предназначены для отображения единичного объекта или списка объектов. Тем не менее, аргумент model это не единственный способ, указать представлению с какими данными оно должно работать. Вы также можете указать необходимый список объектов используя аргумент queryset:

```
class AlbumDetail(ListView):

    context_object_name = 'album'
    queryset = Album.objects.all()
```
Запись model = Album это всего лишь сокращенный вариант записи queryset = Album.objects.all(). Однако, используя queryset вы можете в полной мере использовать механизмы выборки данных, фильтрации , предоставив вашему представлению более конкретный список объектов, с которым оно должно работать. 

Вот простой пример: нам необходимо упорядочить список по дате публикации:

```
class List(ListView):
    queryset = Album.objects.order_by('-publication_date')
    context_object_name = 'album_list'
```
Если мы хотим получить список определенного year='2015', мы можем использовать аналогичную технику:

```
class List(ListView):
    model = Album
    paginate_by = settings.PHOTOS_PER_PAGE
    queryset = Album.objects.filter(album__year='2015')
    template_name = 'photo/album_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Albums')
        return context
```

Обратите внимание, что вместе с созданием отфильтрованной выборки объектов с использованием queryset, мы также используем другое(пользовательское) имя шаблона. Если мы этого не сделаем, представление будет использовать тот же шаблон, что и для отображения “родного” списка объектов, что нас не устраивает.

views/album.py:
---------------
```
from django.conf import settings
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from apps.photo.models import Album

class List(ListView):
    model = Album
    paginate_by = settings.PHOTOS_PER_PAGE
    template_name = 'photo/album_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Albums')
        return context

list = List.as_view()
```
urls.py:
---------
```
from django.conf.urls import url
from . import views
from .views import album

urlpatterns = [
    url(r'^albums/$', album.list, name='albums'),
]

```
album_list.html:
-----------------
```
{% extends 'base.html' %}

{% load i18n %}

{% block title %}{{ page_title }}{% endblock %}
{% block header %}{{ page_title }}{% endblock %}

{% block content %}
    <ul class="albums">
        {% for album in album_list %}
            
            <li>
                <a href="{{ url }}">
                    {% include 'photo/_cover_photo.html' with object=album %}
                    <span class="name">{{ album.name|truncatechars:"45" }}</span>
                    {% with count=album.photo_set.count %}
                        {% include 'photo/_photo_count.html' %}
                    {% endwith %}
                </a>
            </li>
        {% endfor %}
    </ul>
{% endblock %}

```
_cover_photo.html:
------------------
```
{% if object.cover_photo %}
    <img src="{{ object.cover_photo.file_thumb.url|default:"" }}" alt="{{ object.name }}">
{% else %}
    <img src="{{ STATIC_URL }}/img/cover-blank.png">
{% endif %}
```
_photo_count.html:
------------------
```
{% load i18n %}
{% load humanize %}

<span class="count">
    {% blocktrans trimmed count counter=count with total=count|intcomma %}
        {{ total }} photo
    {% plural %}
        {{ total }} photos
    {% endblocktrans %}
</span>

```
views/photo.py:
---------------
```
class Detail(ListView):
    paginate_by = settings.PHOTOS_PER_PAGE

    template_name = 'photo/photo_list.html'

    def get_album(self):
        return get_object_or_404(Album, pk=self.kwargs['pk'])

    def get_queryset(self):
        self.album = self.get_album()
        return self.album.photo_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        back_link = reverse('photo:albums'), _('Albums')
        location = None
        if 'location_pk' in self.kwargs:
            location = get_object_or_404(Location, pk=self.kwargs.get('location_pk'))
            back_link = reverse('location', kwargs={'pk': location.pk}), location.name

        context['location'] = location
        context['back_link'] = back_link
        context['page_title'] = self.album.name
        context['album'] = self.album
        return context

detail = Detail.as_view()
```
urls.py:
-------
```
from django.conf.urls import url

from . import views

from .views import album, photo

urlpatterns = [
    
    url(r'^albums/$', album.list, name='albums'),
    url(r'^albums/(?P<pk>\d+)/$', album.detail, name='album'),

]

```

photo/photo_list.html:
----------------------

```
{% extends 'base.html' %}

{% load i18n %}

{% block title %}{{ page_title }}{% endblock %}
{% block header %}{{ page_title }}{% endblock %}

{% block content %}
    <ul class="photos">
        {% for photo in photo_list %}
                        
            {% if query %}
                {% url 'photo:photodetail' pk=photo.pk query=query as url %}
            {% else %}
                {% url 'photo:photodetail' pk=photo.pk as url %}
            {% endif %}
            <li><a href="{{ url }}"><img src="{{ photo.file_thumb.url }}" alt="{{ photo.name }}"></a></li>
        {% endfor %}
    </ul>
{% endblock %}

```
DetailView Просмотр информации об отдельном объекте
====================================================

DetailView - отвечает за просмотр отдельного объекта.
Чтобы получить единичный объект, нам необходимо его идентифицировать по какому-нибудь параметру. Обычно для этого используется так называемый уникальный первичный ключ (pk, id). Django также позволяет идентифицировать объект по полю slug, которое может быть любым уникальным словом. Разумеется для SEO иногда удобнее использовать именно slug, в случае если объектами выступают статьи или список пользователей. Однако в других случаях использовать для идентификации slug нет смысла (например просмотр комментария или личного сообщения). В таких случаях используется первичный ключ.

views/photo.py
--------------
```
import mimetypes

from django.utils.translation import ugettext as _

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, View

from apps.photo.models import Person, Photo, Location

from apps.photo.views import get_search_queryset

class Detail(DetailView):
    model = Photo
    template_name = 'photo/photo_detail.html'
    person = None
    location = None
    query = None

    def paginate(self, queryset, obj):
        """
        Figure out where this photo is located in the queryset (sorted by id). Queryset can be variable
        based on how the user accessed the photo. Return a simple paginator dictionary.
        """
        values_list = list(queryset.order_by('name').values_list('id', flat=True))
        index = values_list.index(obj.id)

        def build_url(pk):
            newkwargs = self.kwargs.copy()
            newkwargs['pk'] = pk
            return reverse('photo:photodetail', kwargs=newkwargs)

        next_url, prev_url = None, None
        if len(values_list) > 1:
            if obj.id != values_list[0]:
                prev_url = build_url(values_list[index - 1])
            if obj.id != values_list[-1]:
                next_url = build_url(values_list[index + 1])

        self.paginator = {
            'has_next': (next_url is not None),
            'next_url': next_url,
            'has_previous': (prev_url is not None),
            'previous_url': prev_url,
            'index': (index + 1),
            'count': len(values_list)
        }
        return obj

    def get_object(self, queryset=None):
        """
        Get the photo object, set the proper "back" link, and create the paginator object.
        """
        obj = get_object_or_404(Photo, pk=self.kwargs[self.pk_url_kwarg])

        if 'query' in self.kwargs:
            self.query = self.kwargs['query']
            self.back_link = reverse('results', kwargs={'query': self.kwargs['query']}), _('Results')
            self.paginate(get_search_queryset(self.kwargs['query']), obj)
            return obj

        if 'person_pk' in self.kwargs:
            self.person = get_object_or_404(Person, pk=self.kwargs['person_pk'])
            self.back_link = reverse('person', kwargs={'pk': self.person.pk}), self.person.name
            self.paginate(self.person.photo_set, obj)
            return obj

        if 'location_pk' in self.kwargs:
            self.location = get_object_or_404(Location, pk=self.kwargs.get('location_pk'))
            album = get_object_or_404(self.location.album_set, pk=self.kwargs.get('location_pk'))
            self.back_link = reverse('album', kwargs={'pk': album.pk, 'location_pk': self.location.pk}), album.name
            self.paginate(album.photo_set, obj)
            return obj

        self.back_link = reverse('photo:album', kwargs={'pk': obj.album.pk}), obj.album.name
        self.paginate(obj.album.photo_set, obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        context['person'] = self.person
        context['location'] = self.location
        context['back_link'] = self.back_link
        context['paginator'] = self.paginator
        return context

detail = Detail.as_view()

```
наш объект будет доступен с помощью метода get_object. Этот метод поочередно пытается найти в маршруте переменные pk и slug, в данном случае переменная с именем pk будет обладать большим приоритетом. С помощью метода get_slug_field мы можем переопределить имя поля slug нашей модели. По умолчанию данный метод возвращает значение атрибута slug_field. Наш объект хранится в атрибуте object.

В случаях, когда необходимо отобразить огромное число объектов, крайне нежелательно выводить их все одновременно. В этом случае требуется механизм для постраничного вывода данных (пагинация). Класс DetailView наследует примесь MultipleObjectMixin, которая реализует требуемый нам функционал. Для определения количества объектов на страницу используется метод get_paginate_by, который по умолчанию возвращает значение атрибута paginate_by. С помощью атрибута мы можем без особых хлопот указать количество выводимых на 1 страницу объектов.

Иногда возникает необходимость реализовать постраничный вывод своим способом, для этого мы можем передать наш класс пагинации атрибуту paginator_class. По умолчанию этот атрибут содержит ссылку на стандартный класс Paginator, который реализован в модуле django.core.paginator.

Атрибут allow_empty определяет как обработать ситуацию, когда нет ни одного объекта в списке. Если мы установим значение данного атрибута в True (по умолчанию), то будет возвращаться пустой список объектов. В случае значения False будет возвращаться ошибка 404. Значение данного атрибута возвращает метод get_allow_empty. Его же можно использовать, если требуется некоторая дополнительная проверка или изменение логики.


Атрибут object_list хранит список наших объектов. Необходимо помнить о том, что мы должны не забыть передать текущую страницу нашему отображению для корректной работы. Наиболее простой способ — использование именованных групп в нашем файле urls.py

После того, как мы выбрали способ идентификации объекта, мы должны сообщить Django о своем выборе, передав переменную с соответствующим именем с помощью маршрута файла urls.py.

urls.py
-------
```
from django.conf.urls import url

from . import views

from .views import album, photo

urlpatterns = [
    
    url(r'^albums/$', album.list, name='albums'),
    url(r'^albums/(?P<pk>\d+)/$', album.detail, name='album'),
    url(r'^photos/(?P<pk>\d+)/$', photo.detail, name='photodetail'),

]

```
В шаблоне наш список объектов будет доступен по имени, которое задано с помощью атрибута context_object_name - photo.name (или возвращается методом get_context_object_name). Объекты с текущей страницы находятся в переменной с именем object_list. Значение переменной is_paginated (булево значение) определяет разбит ли наш список объектов на страницы.

templates/photo/photo.html
--------------------------
```
{% extends 'base.html' %}

{% load i18n %}

{% block title %}{{ photo.album.name }}{% endblock %}
{% block header %}{{ photo.album.name }}{% endblock %}

{% block pagination %}
    <ul class="paginator">
        <li class="prev">
            {% if paginator.has_previous %}
                <a href="{{ paginator.previous_url }}" data-navigate="left">&larr;&nbsp;{% trans 'Prev' %}</a>
            {% else %}
                <span>&larr;&nbsp;{% trans 'Prev' %}</span>
            {% endif %}
        </li>
        <li class="count">{{ paginator.index }} {% trans 'of' %} {{ paginator.count }}</li>
        <li class="next">
            {% if paginator.has_next %}
                <a href="{{ paginator.next_url }}" data-navigate="right">{% trans 'Next' %}&nbsp;&rarr;</a>
            {% else %}
                <span>{% trans 'Next' %}&nbsp;&rarr;</span>
            {% endif %}
        </li>
    </ul>
{% endblock %}


{% block content %}
    <div class="photo">
        <img src="{{ photo.file_medium.url }}" alt="{{ photo.name }}">

        <div class="name">{{ photo.name }}</div>
    </div>
{% endblock %}

```