# p21v-django unit_04

Pillow
------

        pip install Pillow


CKEditor 
========
https://github.com/django-ckeditor/django-ckeditor


        pip install django-ckeditor

CKEditorWidget
===============
settings.py
------------
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'ckeditor',
    'ckeditor_uploader',
    'blog',
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "public/static")

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'public/media')

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'


CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_IMAGE_BACKEND = "pillow"


CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YouCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'youcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YouCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join(
            [
                # you extra plugins here
                'div',
                'autolink',
                'autoembed',
                'embedsemantic',
                'autogrow',
                # 'devtools',
                'widget',
                'lineutils',
                'clipboard',
                'dialog',
                'dialogui',
                'elementspath'
            ]),
    }
}

```

urls.py
--------
```
urlpatterns += [
    url(r'^$', view_home.home, name='home'),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    
    url(r'^admin/', admin.site.urls),
]

```

admin.py
--------
```
from django.contrib import admin
from django import forms

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


from .models import Category, Tag, Article

class ArticleAdminForm(forms.ModelForm):
    
    content = forms.CharField(widget=CKEditorWidget())
    content = forms.CharField(widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Article
        fields = '__all__'

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status', 'was_published_recently')
    list_filter = ['publish_date']
    search_fields = ['title']

    ordering = ['publish_date']

    filter_horizontal = ('tags',)

    prepopulated_fields = {"slug": ("title",)}

    date_hierarchy = 'publish_date'
    readonly_fields = ('publish_date','created_date')
    fieldsets = [
        ('Item',             {'fields': [('title','slug'),'category','content']}),
        ('Date information', {'fields': [('publish_date','created_date')], 'classes': ['collapse']}),
        ('Related tags',     {'fields': ['tags']}),
        ('Metas',            {'fields': [('status')]}),
    ]

    actions = [make_published,'make_draft','make_expired']

    form = ArticleAdminForm

```

Install django-wysiwyg-redactor:
================================
https://github.com/douglasmiranda/django-wysiwyg-redactor

```
pip install django-wysiwyg-redactor

```
settings.py
-----------
```
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'redactor',

    'blog',
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'public/media')
MEDIA_URL = '/media/'

REDACTOR_OPTIONS = {'lang': 'en'}
REDACTOR_UPLOAD = MEDIA_ROOT
```
urls.py
```
urlpatterns = [

    url(r'^redactor/', include('redactor.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
]

```

admin.py
---------
```
class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'content': RedactorEditor(),
        }
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status', 'was_published_recently')
    list_filter = ['publish_date']
    search_fields = ['title']

    ordering = ['title']

    prepopulated_fields = {"slug": ("title",)}

    fieldsets = [
        ('Item',             {'fields': [('title','slug'),'category','content']}),
        ('Date information', {'fields': [('created_date','publish_date')], 'classes': ['collapse']}),
        ('Related tags',     {'fields': ['tags']}),
        ('Metas',            {'fields': [('status','views_count')]}),
        ('Comments',            {'fields': ['enable_comment','comment_count']}),
    ]
    actions = [make_published,'make_draft','make_expired']

    actions_on_top = True 
    actions_on_bottom = False 
    actions_selection_counter = True

    date_hierarchy = 'publish_date'

    filter_horizontal = ('tags',)

    form = ArticleAdminForm

```

tinymce
========
urls.py
-------
```
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),

    url(r'^tinymce/', include('tinymce.urls')),
]

```
models.py:
```
from django.db import models
from tinymce.models import HTMLField

class MyModel(models.Model):
    ...
    content = HTMLField()
```

settings.py
-----------
```
# tinymce
TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'plugins': "wordcount,preview,emotions,preview,spellchecker,",
    'height': "400px",
    'width': "700px",
    'theme_advanced_buttons3' : "fontselect,fontsizeselect,emotions,preview,",
    }
```
autoescape
-----------
```
<p><strong>В этом примере к начальному QuerySet</strong>, который возвращает все объекты, добавляется фильтр, затем исключающий фильтр, и еще один фильтр. Полученный <em>QuerySet</em> содержит все объекты, у которых заголовок начинается с <em>QuerySet</em>, и которые были опубликованы между 3-го января 2016 и текущей датой.</p><p><img src="/home/janus/github/dj-21v/unit_06/mysite/public/media/loshadka.png"></p><p>Отфильтрованный QuerySet – уникален</p><hr><pre>После каждого изменения QuerySet, вы получаете новый QuerySet, который никак не связан с предыдущим QuerySet. Каждый раз создается отдельный QuerySet, который может быть сохранен и использован.</pre> 
```

autoescape off
--------------
```
            {% autoescape off %}
                <p> {{ item.content }} </p>
            {% endautoescape %}
```
Monthly archive
===============
blog/views.py
-------------
```
import time
from calendar import month_name

def monthly_archive_list():
    """Make a list of months to show archive links."""

    if not Article.objects.count(): return []

    # set up vars
    year, month = time.localtime()[:2]
    first = Article.objects.order_by("created_date")[0]
    fyear = first.created_date.year
    fmonth = first.created_date.month
    months = []

    # loop over years and months
    for y in range(year, fyear-1, -1):
        start, end = 12, 0
        if y == year: start = month
        if y == fyear: end = fmonth-1

        for m in range(start, end, -1):
            months.append((y, m, month_name[m]))
    return months

def monthly_archive(request, year, month):
    """Monthly archive."""

    posts = Article.objects.filter(created_date__year=year, created_date__month=month)

    return render(request,"blog/month_archive.html",dict(posts=posts, months=monthly_archive_list()))
```

blog/urls.py
------------
```
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^news/$', views.news, name='news'),
    url(r'^latest/$', views.latest),
    url(r"^archive/(\d+)/(\d+)/$", views.monthly_archive , name='archive'),
    url(r'^category/(?P<categoryslug>.*)/$', views.category, name='category' ),
    url(r'^(?P<postslug>.*)/$', views.detail, name='detail' ),
]
```
blog/month_archive.html
-----------------------
```
       <h3>Monthly Archive</h3>
          <div>
          {% for month in months %} 
            <a href="{% url 'blog:archive' month.0 month.1 %}">{{ month.2 }}</a> <br /> 
        {% endfor %} 
        </div>
```
blog/index.html
---------------
```
    <h3>Monthly Archive</h3>
          <div>
        {% for month in months %} 
            <a href="{% url 'blog:archive' month.0 month.1 %}">{{ month.2 }}</a> <br /> 
        {% endfor %}
          </div>
       </div>
```

blog/views.py
-------------
```
def index(request):
    blog_list = Article.objects.order_by('-publish_date')
    category_list = Category.objects.order_by('name')
    tags_name = Tag.objects.order_by('name')
    context = {'categories_list':category_list, 'blog_list': blog_list , 'tags_name':tags_name, 'months':monthly_archive_list()}
    return render(request, 'blog/index.html', context)
```
Постраничный вывод - Paginator
==============================

Django предоставляет несколько классов, которые помогают реализовать постраничный вывод данных, т.е. данных, распределённых на несколько страниц с ссылками «Предыдущая/Следующая». Эти классы располагаются в django/core/paginator.py.

вы можете передать классу Paginator список/кортеж, QuerySet Django или любой другой объект, который имеет методы count() или __len__(). Для определения количества объектов, содержащихся в переданном объекте, Paginator сначала попробует вызвать метод count(), затем, при его отсутствии, вызывает len(). Такой подход позволяет объектам, подобным QuerySet, более эффективно использовать метод count() при его наличии.
Использование Paginator в представлении
---------------------------------------
Функция представления может выглядеть так:
```
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def monthly_archive(request, year, month):
    """Monthly archive."""

    posts = Article.objects.filter(created_date__year=year, created_date__month=month)

    paginator = Paginator(posts, 2)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    return render(request,"blog/month_archive.html",dict(blog_list=posts, months=monthly_archive_list(), archive=True))
```

В шаблоне month_archive.html подключен блок навигации по страницам:
```
 <!-- Next/Prev page links  --> 
      {% if blog_list.object_list and blog_list.paginator.num_pages > 1 %} 
        <div class="pagination" style="margin-top: 20px; margin-left: -20px; "> 
            <span class="step-links"> 
                {% if blog_list.has_previous %} 
                    <a href= "?page={{ blog_list.previous_page_number }}">newer entries &lt;&lt; </a> 
                {% endif %} 

                <span class="current"> 
                    &nbsp;Page {{ blog_list.number }} of {{ blog_list.paginator.num_pages }} 
                </span> 

                {% if blog_list.has_next %} 
                    <a href="?page={{ blog_list.next_page_number }}"> &gt;&gt; older entries</a> 
                {% endif %} 
            </span> 
        </div> 
       {% endif %}

```

Объекты Paginator
------------------
У класса Paginator есть конструктор:
```
class Paginator(object_list, per_page, orphans=0, allow_empty_first_page=True)
```
Обязательные аргументы
----------------------
- object_list
Список, кортеж, Django QuerySet, или другой контейнер, у которого есть метод count() или``__len__()``.

- per_page
Максимальное количество элементов на странице, без учёта остатка.

Необязательные аргументы
------------------------
- orphans
Минимальное количество элементов на последней странице, по умолчанию, ноль. Используйте, когда нежелательно отображать последнюю страницу почти пустой. Если последняя страница будет содержать количество элементов меньше или равно orphans, то эти элементы будут добавлены к предыдущей странице (которая станет последней). Например, для 23 элементов, per_page=10``и ``orphans=3, будет выдано две страницы; первая страница будет содержать 10 элементов, а вторая (и последняя) — 13.

- allow_empty_first_page
Позволять или нет первой странице быть пустой. Если указан False и object_list пустой, то будет вызвано исключение EmptyPage.

Методы
-------
- Paginator.page(number)
Возвращает объект Page по переданному индексу (начинается с единицы). Вызывает исключение InvalidPage, если указанная страница не существует.

Атрибуты
---------
- Paginator.count
Общее количество объектов, распределенных по всем страницам.

При определении количества объектов, содержащихся в object_list, Paginator сначала пробует вызвать object_list.count(). Если у object_list нет метода count(), то Paginator попробует вызвать len(object_list). Такой подход позволяет объектам, подобным QuerySet Django, более эффективно использовать метод count() при его наличии.

- Paginator.num_pages
Общее количество страниц.

- Paginator.page_range
Диапазон номеров страниц, начинающийся с единицы, т.е., [1, 2, 3, 4].

InvalidPage исключения
----------------------
- exception InvalidPage
Базовый класс для исключений, которые вызываются когда происходит запрос страницы по несуществующему номеру.

Метод Paginator.page() вызывает исключение, если номер запрошенной страницы является неправильным (например, не представлен целым числом) или не содержит объектов. В общем случае, достаточно обрабатывать исключение InvalidPage

- exception PageNotAnInteger
Вызывается, если page() получает значение, которое не является целым числом.

- exception EmptyPage
Вызывается, если page() получает правильное значение, но для указанной страницы нет объектов.

Эти исключения являются потомками класса InvalidPage, таким образом, вы можете обрабатывать их с помощью простого except InvalidPage.

Объекты Page
--------------
Обычно создавать объекты Page вручную не требуется, так как вы получаете их с помощью метода Paginator.page().
```
class Page(object_list, number, paginator)
```
Страница работает как срез Page.object_list при использовании len() или итерации по ней.

Методы
------
- Page.has_next()
Возвращает True, если следующая страница существует.

- Page.has_previous()
Возвращает True, если предыдущая страница существует.

- Page.has_other_pages()
Возвращает True, если существует следующая или предыдущая страница.

- Page.next_page_number()
Возвращает номер следующей страницы. Вызывает InvalidPage если следующая страница не существует.

- Page.previous_page_number()
Возвращает номер предыдущей страницы. Вызывает InvalidPage если предыдущая страница не существует.

- Page.start_index()
Возвращает индекс (начинается с единицы) первого объекта на странице относительно списка всех объектов. Например, для списка из пяти объектов при отображении двух объектов на странице, то для второй страницы метод start_index() вернёт 3.

- Page.end_index()
Возвращает индекс (начинается с единицы) последнего объекта на странице относительно списка всех объектов. Например, для списка из пяти объектов при отображении двух объектов на странице, то для второй страницы метод end_index() вернёт 4.

Атрибуты
---------
- Page.object_list
Список объектов текущей страницы.

- Page.number
Номер (начинается с единицы) текущей страницы.

- Page.paginator
Соответствующий объект Paginator.

blog/views.py
-------------
```
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse

def monthly_archive(request, year, month):
    """Monthly archive."""

    posts = Article.objects.filter(created_date__year=year, created_date__month=month)

    paginator = Paginator(posts, 2)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    return render(request,"blog/month_archive.html",dict(blog_list=posts, months=monthly_archive_list(), archive=True))

```
blog/month_archive.html
-----------------------
```
    <!-- Next/Prev page links  --> 
      {% if blog_list.object_list and blog_list.paginator.num_pages > 1 %} 
        <div class="pagination" style="margin-top: 20px; margin-left: -20px; "> 
            <span class="step-links"> 
                {% if blog_list.has_previous %} 
                    <a href= "?page={{ blog_list.previous_page_number }}">newer entries &lt;&lt; </a> 
                {% endif %} 

                <span class="current"> 
                    &nbsp;Page {{ blog_list.number }} of {{ blog_list.paginator.num_pages }} 
                </span> 

                {% if blog_list.has_next %} 
                    <a href="?page={{ blog_list.next_page_number }}"> &gt;&gt; older entries</a> 
                {% endif %} 
            </span> 
        </div> 
       {% endif %}
```

Собственные шаблонные теги и фильтры
====================================
Шаблонизатор Django содержит большое количество встроенных тегов и фильтров. Тем не менее, вам может понадобиться добавить собственный функционал к шаблонам. Вы можете сделать это добавив собственную библиотеку тегов и фильтров используя Python, затем добавить ее в шаблон с помощью тега {% load %}.

Добавление собственной библиотеки
---------------------------------
Собственные теги и фильтры шаблонов должны определяться в приложении Django. Если они логически связаны с каким-то приложением, есть смысл добавить их в это приложение, иначе создайте новое приложение.

Приложение должно содержать каталог templatetags на том же уровне что и models.py, views.py и др. Если он не существует, создайте его. Не забудьте создать файл __init__.py чтобы каталог мог использоваться как пакет Python. После добавления этого модуля, необходимо перезапустить сервер, перед тем как использовать теги или фильтры в шаблонах.

templatetags
------------
теги и фильтры будут находиться в модуле пакета templatetags. Название модуля будет использоваться при загрузке библиотеки в шаблоне, так что убедитесь что оно не совпадает с названиями библиотек других приложений.

Например, если теги/фильтры находятся в файле latest_posts.py, ваше приложение может выглядеть следующим образом:
```
blog/
    __init__.py
    models.py
    templatetags/
        __init__.py
        latest_posts.py
    views.py
```
в шаблоне:
----------
```
{% load latest_posts %}
```
Приложение содержащее собственные теги и фильтры должно быть добавлено в INSTALLED_APPS, чтобы тег {% load %} мог загрузить его. Это сделано в целях безопасности.

Не имеет значение сколько модулей добавлено в пакет templatetags. тег {% load %} использует название модуля, а не название приложения.

Библиотека тегов должна содержать переменную register равную экземпляру template.Library, в которой регистрируются все определенные теги и фильтры. 

```

# -*- coding: UTF-8 -*-
from django import template
from blog.models import Article

register=template.Library()

```
Включающие теги
================
django.template.Library.inclusion_tag()
---------------------------------------
это теги, которые выполняют другой шаблон и показывают результат. Например, интерфейс администратора Django использует включающий тег для отображения кнопок под формой на страницах добавления/редактирования объектов. Эти кнопки выглядят всегда одинаково, но ссылки зависят от текущего объекта – небольшой шаблон, который выполняется с данными из текущего объекта, удобно использовать в данном случае. (В приложении администратора это тег submit_row.)

Такие теги называются “включающие теги”.
-----------------------------------------
создадим тег, который выводит список 6-и последних публикаций для объекта модели Article

создадим функцию, которая возвращает словарь с данными. 

```
def latest_posts():
    posts = Article.objects.order_by('-publish_date').filter(status='P')[:6]
    return locals()
```

Using { } 
--------------
```
def latest_posts():
    return {
            'posts': Article.objects.order_by('-publish_date').filter(status='P')[:6],
           }
```
locals():
----------
```
def latest_posts():
    posts = Article.objects.order_by('-publish_date').filter(status='P')[:6]
    return locals()
```

создадим шаблон, который будет использоваться для генерации результата. Этот шаблон полностью относится к тегу: создатель тега определяет его, не создатель шаблонов(template designer).

blog/_latest_posts.html
------------------------
```
<!-- _latest_posts.html -->
<ul>
  {% for p in posts %}
    <li><a href="{% url 'blog:detail' p.slug %}">{{ p.title }}</a>
  {% endfor %}
</ul>
```

создадим и зарегистрируем тег, используя метод inclusion_tag() объекта Library. 
```
# -*- coding: UTF-8 -*-
from django import template
from blog.models import Article

register=template.Library()
 
@register.inclusion_tag('blog/_latest_posts.html') # регистрируем тег и подключаем шаблон _latest_posts

def latest_posts():
    posts = Article.objects.order_by('-publish_date').filter(status='P')[:6]
    return locals()

```

blog/index.html
---------------
```
{% extends "base.html" %}
{% load latest_posts %}

    <h2>Latest Posts</h2>
      <div>
          {% latest_posts %}
      </div>
```
blog/models.py
---------------
```
@python_2_unicode_compatible
class Article(models.Model):
    ARTICLE_STATUS = (
        ('D', 'Not Reviewed'),
        ('P', 'Published'),
        ('E', 'Expired'),
    )
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
    status = models.IntegerField(default=0)
    content = models.TextField()
    status = models.CharField(max_length=1, choices=ARTICLE_STATUS, default='D')
    category = models.ForeignKey(Category, verbose_name="the related category")
    tags = models.ManyToManyField(Tag, verbose_name="the related tags", related_name="keyword_set", blank=True)
        
    views = models.IntegerField(default=0)
    publish_date = models.DateTimeField(auto_now=True, editable=False, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
```

views.py
----------
```
def detail(request, postslug):
    result = get_object_or_404(Article, slug=postslug)

    try:
        result.views = result.views + 1
        result.save()
    except:
        pass

    category_list = Category.objects.order_by('name')
    tags_name = Tag.objects.order_by('name')
        
    return render(request, 'blog/detail.html', {'categories_list':category_list, 'item': result, 'tags_name':tags_name})
```
blog/detail.html
----------------
```
         <h2>{{ item.title }}</h2>
             {% autoescape off %}
                <p> {{ item.content }} </p>
             {% endautoescape %}

          <p> {{ item.publish_date }} | <a href ="{% url 'blog:category' item.category.slug %}">{{ item.category }}</a> | {% for tag in item.tags.all %}
                <span> {{ tag.name }} </span> {% endfor %}
                {% if item.views > 1 %}
                    ({{ item.views }} views)
                {% elif item.views == 1 %}
                    ({{ item.views }} view)
                {% endif %}
          </p>
```

popular_posts
=============

```
# -*- coding: UTF-8 -*-
from django import template
from blog.models import Article

register=template.Library()
 
@register.inclusion_tag('blog/_popular_posts.html') # регистрируем тег и подключаем шаблон _popular_posts

def popular_posts():
    posts = Article.objects.filter(views__gte=5).filter(status='P')[:6]
    return locals()

```

blog/_popular_posts.html
------------------------
```
<ul>
  {% for p in posts %}
    <li><a href="{% url 'blog:detail' p.slug %}">{{ p.title }}</a>
  {% endfor %}
</ul>
```
index.html
----------
```
{% extends "base.html" %}
{% load latest_posts popular_posts %}

        <h2>Popular Posts</h2>
          <div>
          {% popular_posts %}
          </div>
```
Templates
==========
layout.html
-----------
```
{% extends "base.html" %}
{% load latest_posts popular_posts %}
{% block head_title %}My Cool Django Blog  {% endblock %}

      <!-- row of columns -->
      {% block content %}       

            {% block main %} 
            {% endblock main %} 
        
            {% block aside %} 
                   <h2>Categorits</h2>
                  {% if categories_list %}       
                    <ul>
                        {% for category in categories_list %}
                        <li><a href ="{% url 'blog:category' category.slug %}">{{ category.name }}</a></li>
                        {% endfor %}
                    </ul>

                    {% else %}
                    <strong>There are no categories present.</strong>
                  {% endif %}

                  <h2>Tags</h2>
                  {% if tags_name %}       
                    <ul>
                        {% for tag in tags_name %}
                        <li><a href ="">{{ tag.name }}</a></li>
                        {% endfor %}
                    </ul>
                    {% else %}
                        <strong>There are no tags present.</strong>
                    {% endif %}


                  <h2>Latest Posts</h2>
                  <div>
                      {% latest_posts %}
                  </div>

                  <h2>Popular Posts</h2>
                  <div>
                      {% popular_posts %}
                  </div>

                  <h3>Monthly Archive</h3>
                  <div>
                      {% for month in months %} 
                           <a href="{% url 'blog:archive' month.0 month.1 %}">{{ month.2 }}</a> <br /> 
                      {% endfor %}
                  </div>
            {% endblock aside %} 
        {% endblock content %} 
```

index.html
----------
```
{% extends "blog/layout.html" %}
{% block head_title %} {{ block.super }} - All Blog Publications{% endblock %}

        {% block content %} 
        
        <div class="row">
          <div class="col-md-8">
          {% block main %} 
            <h2>Publications</h2>
              {% if blog_list %}
                {% for item in blog_list %}
                  <h3><a href ="{% url 'blog:detail' item.slug %}">{{ item.title }}</a></h3>
                    <p><a class="btn btn-default" href="{% url 'blog:detail' item.slug %}" role="button">View details &raquo;</a></p>
                {% endfor %}
              {% else %}
                <li>Sorry, no items in this list.</li>
             {% endif %}
          {% endblock main %} 
          </div>
        
           <div class="col-md-4">   
             {% block aside %} 
                {{ block.super }}         
             {% endblock aside %}
           </div>    
         
         </div>
        {% endblock content %}
```
detail.html
------------
```
{% extends "blog/layout.html" %}
{% block head_title %} {{ block.super }} - Blog Topik{% endblock %}

        {% block content %} 
        
        <div class="row">
          <div class="col-md-8">
          {% block main %} 
          <h2>{{ item.title }}</h2>
          {% autoescape off %}
                <p> {{ item.content }} </p>
                {% endautoescape %}
          
          <p> {{ item.publish_date|date:"D d M Y" }} | <a href ="{% url 'blog:category' item.category.slug %}">{{ item.category }}</a> | {% for tag in item.tags.all %}
                <span> {{ tag.name }} </span> {% endfor %}
                {% if item.views > 1 %}
                    ({{ item.views }} views)
                {% elif item.views == 1 %}
                    ({{ item.views }} view)
                {% endif %}
          </p>

          <p><a class="btn btn-default" href="{% url 'blog:index' %}" role="button">All publications &raquo;</a></p>
          {% endblock main %} 
          
          </div>
        
           <div class="col-md-4">   
             {% block aside %} 
                {{ block.super }}         
             {% endblock aside %}
           </div>    
         
         </div>
        {% endblock content %}

```