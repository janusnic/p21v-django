# p21v-django unit 08

### STATIC_ROOT
По умолчанию: None

Абсолютный путь к каталогу, в который collectstatic соберет все статические файлы.
```
Например: "/var/www/example.com/static/"
```
Если используется стандартное приложение staticfiles (по умолчанию), команда collectstatic соберет все статические файлы в указанном каталоге.

Это должен быть каталог(изначально пустой), куда будут скопированы все статические файлы для более простой настройки сервера; это не каталог, в котором вы создаете статические файлы при разработке. Вы должны создавать статические файлы в каталогах, которые будут найдены модулями поиска статических файлов. По умолчанию это подкаталоги 'static/' в приложениях и каталоги, указанные в STATICFILES_DIRS.

settings.py
```
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'statics'))

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

```
Шаблоны можно настроить с помощью настройки TEMPLATES. Это список, который содержит настройки для систем шаблонов. По умолчанию настройка пустая. settings.py, сгенерированный командой startproject, содержит более полезное значение:
settings.py
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
BACKEND путь для импорта Python к классу бэкенда шаблонов. Встроенные бэкенды это django.template.backends.django.DjangoTemplates и django.template.backends.jinja2.Jinja2.

Т.к. большинство систем шаблонов загружают шаблоны с файлов, настройки содержат:

- DIRS, которая содержим список каталогов с шаблонами. Бэкенд ищет в них шаблон в указанном порядке.

- APP_DIRS указывает бэкенду искать ли шаблоны в установленных приложениях. Каждый бэкенд определяет определенное название для каталога с шаблонами в приложении.

- OPTIONS содержит настройки специфические для бэкенда.


#### Модуль django.template.loader предоставляет две функции для загрузки шаблонов.
```
get_template(template_name[, dirs][, using])
```
Эта функция загружает шаблон с указанным названием и возвращает объект Template.

Возвращаемое значение зависит от используемого бэкенда т.к. каждый бэкенд использует свой класс Template.

get_template() пытается загрузить шаблон каждым из бэкендов, пока шаблон не будет загружен. Если шаблон не найден, будет вызвано исключение TemplateDoesNotExist. Если шаблон найден, но синтаксис не верен, будет вызвано TemplateSyntaxError.

Как шаблоны ищутся и загружаются, зависит от используемого бэкенда шаблонов и его настроек.

Если вы хотите использовать конкретный бэкенд, передайте его название из NAME в аргументе using.
#### select_template()
```
select_template(template_name_list[, dirs][, using])
```
select_template() как и get_template(), но принимает список названий шаблонов. Пытается загрузить по очереди каждый из шаблонов, возвращает первый загруженный.

Если не удалось загрузить шаблон, вызываются исключения, описанные в django.template:

- exception TemplateDoesNotExist
Это исключение вызывается, если шаблон не был найден.

- exception TemplateSyntaxError
Это исключение вызывается, если шаблон найден, но содержит ошибки.

Объекты Template, которые возвращают get_template() и select_template(), должны содержать метод render() со следующей сигнатурой:

### Template.render(context=None, request=None)
Рендерит шаблон с переданным контекстом.

Если context передан, это должен быть dict. Если не передан, используется пустой контекст.

Если передан request, это должен быть экземпляр HttpRequest. Шаблонизатор должен добавить его в шаблон, как и CSRF токен. Как это должно происходит определяет шаблонизатор.


## Initializr: HTML5 Boilerplate and Twitter Bootstrap
http://www.initializr.com/

- Переместить index.html, 404.html, humans.txt и robots.txt в /templates.
- Изменить имя index.html на base.html. 
- Переместить остальные файлв в /static
- Если есть собственный favicon.ico - заменить на свой.
- Удалить apple-touch-icon.png, browserconfig.xml, tile-wide.png и tile.png.

### Шаблоны

Шаблон это просто текстовый файл. Он позволяет создать любой текстовый формат (HTML, XML, CSV, и др.).

Шаблон содержит переменные, которые будут заменены значениями при выполнении шаблона, и теги, которые управляют логикой шаблона.

### block и extends
Определяет наследование шаблонов, эффективный способ использовать шаблоны.

base.html

```
<head>
    ...
    <title>{% block head_title %}{% endblock %}</title>
    ...
</head>
```

## Наследование шаблонов

Наследование шаблонов позволяет создать вам шаблон-“скелет”, который содержит базовые элементы вашего сайта и определяет блоки, которые могут быть переопределены дочерними шаблонами.

index.html
```
{% extends "base.html" %}

{% load staticfiles %}

{% block head_title %}Janus Blog {% endblock %}
```

python manage.py startapp home

urls.py
```
from django.conf.urls import include, url
from django.contrib import admin
from home import views
from todo import urls as todo_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', views.home, name='home'),
    url(r'^todo/', include(todo_urls)),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
]
```

home/tests.py
```

# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
 
 
class TestHomePage(TestCase):
 
    def test_uses_index_template(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "home/index.html")
 
    def test_uses_base_template(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "base.html")

```

python manage.py test home.tests
```
Creating test database for alias 'default'...
..
----------------------------------------------------------------------
Ran 2 tests in 0.399s

OK
Destroying test database for alias 'default'...

```

Let’s prepare our base.html template to be more flexible. You can find the final version of these files here: base.html and index.html.

We will add two blocks at the end of the head tag in the base.html file:

```
{% block head_css %}{% endblock %}
{% block head_javascript %}{% endblock %}
```
### base.html
определяет HTML структуру документа, которую вы можете использовать для двух-колоночной страницы. Задача “дочернего” шаблона заполнить пустые блоки содержимым.

base.html
```
{% load staticfiles %}
<!doctype html>
<html class="no-js" lang="">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>{% block head_title %}{% endblock %}</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="apple-touch-icon" href="apple-touch-icon.png">

        <link rel="stylesheet" href="{% static "css/normalize.min.css" %}">
        <link rel="stylesheet" href="{% static "css/main.css" %}">

        <script src="{% static "js/vendor/modernizr-2.8.3.min.js" %}"></script>
        {% block head_css %}{% endblock %}
        {% block head_javascript %}{% endblock %}
    </head>
    <body>
        <!--[if lt IE 8]>
            <p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> to improve your experience.</p>
        <![endif]-->

        {% block navbar %}
            <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
    
            </nav>
        {% endblock %}
        
        {% block content %}{% endblock %}

        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
        <script>window.jQuery || document.write('<script src="js/vendor/jquery-1.11.2.min.js"><\/script>')</script>

        <script src="{% static "js/plugins.js" %}"></script>
        <script src="{% static "js/main.js" %}"></script>

        <!-- Google Analytics: change UA-XXXXX-X to be your site's ID. -->
        <script>
            (function(b,o,i,l,e,r){b.GoogleAnalyticsObject=l;b[l]||(b[l]=
            function(){(b[l].q=b[l].q||[]).push(arguments)});b[l].l=+new Date;
            e=o.createElement(i);r=o.getElementsByTagName(i)[0];
            e.src='//www.google-analytics.com/analytics.js';
            r.parentNode.insertBefore(e,r)}(window,document,'script','ga'));
            ga('create','UA-XXXXX-X','auto');ga('send','pageview');
        </script>
    </body>
</html>
```
#### Дочерний шаблон может выглядеть таким образом:
blog/index.html

```
{% extends "base.html" %}

{% load staticfiles %}

{% block head_title %}Janus Blog {% endblock %}

<link rel="stylesheet" type="text/css" href="{% static 'blog/css/style.css' %}" />

{% block content %}

    <div class="jumbotron">
        <h1>Janus Blog Latest publications</h1>
    </div>
    
    <div class="container">

            {% if latest_blog_list %}
                <ul>
                {% for item in latest_blog_list %}
                    <li><a href="{% url 'blog:detail' item.id %}">{{ item.title }}</a></li>
                {% endfor %}
                </ul>
            {% else %}
                <p>No items are available.</p>
            {% endif %}

    </div>

{% endblock %}

```

### footer

```
        {% block footer %}
            <footer> 

            </footer>
        {% endblock %}

```

Один из распространенных способов использовать наследование – это трехуровневый подход:

1. Создать шаблон base.html, который отображает основной вид вашего сайта.

2. Создать шаблон base_SECTIONNAME.html для каждого “раздела” вашего сайта. Например, base_news.html, base_sports.html. Все эти шаблоны наследуют base.html и включают стили и дизайн специфические для конкретного раздела.

3. Создание шаблона для каждого типа страницы, такие как новость или запись в блоге. Эти шаблоны наследуют соответствующий шаблон раздела.

Такой подход позволяет максимально использовать существующий код и легко добавлять элементы, такие как элементы навигации специфические для каждого раздела, в общие блоки шаблона.

Вот несколько советов по работе с наследованием:

- Если вы используете {% extends %}, он должен быть первым тегом в шаблоне. Иначе наследование не будет работать.

- Чем больше тегов {% block %} в вашем шаблоне, тем лучше. Помните, дочерний шаблон не обязан определять все блоки родительского, вы можете указать значение по умолчанию для всех блоков, а затем определить в дочернем шаблоне только те, которые необходимы. Лучше иметь больше “hooks”, чем меньше “hooks”.

- Если вы дублируете содержимое в нескольких шаблонах, возможно вы должны перенести его в тег {% block %} родительского шаблона.

- Если вам необходимо содержимое блока родительского шаблона, используйте переменную {{ block.super }}. Эта полезно, если вам необходимо дополнить содержимое родительского блока, а не полностью переопределить его. Содержимое {{ block.super }} не будет автоматически экранировано, так как оно уже было экранировано, при необходимости, в родительском шаблоне.

blog/index.html
```
{% block head_title %} {{ block.super }} Janus Blog {% endblock %}

```

Для ясности, вы можете добавить название вашему тегу {% endblock %}. Например:
```
{% block content %}
...
{% endblock content %}
```
В больших шаблонах такой подход поможет вам увидеть какой тег {% block %} был закрыт.

Вы не можете определить несколько тегов block с одним названием в одном шаблоне. Такое ограничение существует потому, что тег block работает в “оба” направления. block не просто предоставляет “полость” в шаблоне – он определяет содержимое, которое заполняет “полость” в родительском шаблоне. Если бы было несколько тегов block с одним названием, родительский шаблон не знал содержимое какого блока использовать.

### Автоматическое экранирование HTML

Создавая HTML используя шаблон, есть риск, что переменная может содержать символы, которые повлияют на структуру полученного HTML. Например, рассмотрим такой фрагмент:
```
Hello, {{ name }}
```
На первый взгляд это кажется безобидным способом отображения имени пользователя, но давайте посмотрим, что произойдет, если пользователь выбрал такое имя::
```
<script>alert('hello')</script>
```
С таким именем шаблон вернет:
```
Hello, <script>alert('hello')</script>
```
...что приведет к отображению alert-окна JavaScript!

Аналогично, что если имя содержит символ 
```
<b>username
```
Шаблон вернет такое содержимое:
```
Hello, <b>username
```
...в результате оставшееся содержимое страницы будет выделено полужирным!

Такой тип уязвимости называется Cross Site Scripting (XSS) атакой.

Чтобы избежать этой проблемы, у вас есть два варианта:

- Первый, вы можете применять ко всем сомнительным переменным фильтр escape, который преобразует потенциально опасные HTML символы в безопасные. Такое решение было принятым в первых версиях Django, но проблема в том, что оно возлагает бремя ответственности за безопасность на вас, разработчика / автора шаблона. Легко забыть экранировать переменную.

- Второй, вы можете позволить Django автоматически экранировать HTML. 

По-умолчанию в Django, каждый шаблон экранирует все переменные. В частности выполняются такие замены:
```
< заменяется на &lt;

> заменяется на &gt;

' (одинарная кавычка) заменяется на &#39;

" (двойная кавычка) заменяется на &quot;

& заменяется на &amp;
```
такое поведение используется по умолчанию. Если вы используете систему шаблонов Django, вы в безопасности.

### Как это отключить
Если вы не хотите, чтобы данные автоматически экранировались, на уровне сайта, шаблона или одной переменной, вы можете отключить это несколькими способами.

#### Для отдельных переменных
Для отключения авто-экранирования для отдельных переменных, используйте фильтр safe:
```
This will be escaped: {{ data }}
This will not be escaped: {{ data|safe }}
```
Думайте о safe как сокращение “обезопасить от последующего экранирования” или “может быть смело интерпретировано как HTML”. 
```
This will be escaped: &lt;b&gt;
This will not be escaped: <b>
```
#### Для блоков шаблона
Для контроля авто-экранирования в шаблоне, “оберните” шаблон (или часть шаблона) тегом autoescape, например:
```
{% autoescape off %}
    Hello {{ name }}
{% endautoescape %}
```
Тег autoescape в качестве аргумента принимает on или off. В некоторых случаях, вы захотите включить экранирование в шаблоне, в котором оно было отключено. Например:
```
Auto-escaping is on by default. Hello {{ name }}

{% autoescape off %}
    This will not be auto-escaped: {{ data }}.

    Nor this: {{ other_data }}
    {% autoescape on %}
        Auto-escaping applies again: {{ name }}
    {% endautoescape %}
{% endautoescape %}
```
Тег autoescape распространяет свой эффект на шаблоны, которые наследуют текущий, и на включенные тегом include шаблоны, как и другие блочные теги. Например:

base.html
````

{% autoescape off %}
<h1>{% block title %}{% endblock %}</h1>
{% block content %}
{% endblock %}
{% endautoescape %}

```

child.html
```
{% extends "base.html" %}
{% block title %}This &amp; that{% endblock %}
{% block content %}{{ greeting }}{% endblock %}
````
Так как авто-экранирование отключено в базовом шаблоне, оно будет отключено и в дочернем шаблоне.

#### Robots.txt 
```
/robots.txt
```
#### humans.txt
```
/humans.txt
```

functional_tests/test_all_users.py
```
# -*- coding: utf-8 -*-

# test_all_users.py

from selenium import webdriver
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import LiveServerTestCase  
 
 
class HomeNewVisitorTest(LiveServerTestCase): 
 
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
 
    def tearDown(self):
        self.browser.quit()
 
    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)
 
    def test_home_title(self):
        self.browser.get(self.get_full_url("home"))
        self.assertIn("Janus HOME PAGE", self.browser.title)
 
    def test_h1_css(self):
        self.browser.get(self.get_full_url("home"))
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.value_of_css_property("color"),"rgba(34, 34, 34, 1)")

def test_home_files(self):
    self.browser.get(self.live_server_url + "/robots.txt")
    self.assertNotIn("Not Found", self.browser.title)
    self.browser.get(self.live_server_url + "/humans.txt")
    self.assertNotIn("Not Found", self.browser.title)
```

urls.py:

```

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', views.home, name='home'),
    url(r'^(?P<filename>(robots.txt)|(humans.txt))$',
        views.home_files, name='home-files'),
    url(r'^todo/', include(todo_urls)),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
]
```

home_files view:
```
def home_files(request, filename):
    return render(request, filename, {}, content_type="text/plain")
```

python manage.py test functional_tests
```
Creating test database for alias 'default'...
..
----------------------------------------------------------------------
Ran 2 tests in 9.624s

OK
Destroying test database for alias 'default'...
```

robots.txt file:

```
User-agent: *
Disallow: /
```
humans.txt
````

# humanstxt.org/
# The humans responsible & technology colophon
 
# TEAM
    Janus Nic -- Developer -- @janusnic
 
# THANKS
    Thanks to all my Blog readers, who encouraged me to write the
    Janus Django Blog
 
# TECHNOLOGY COLOPHON
    Django
    HTML5 Boilerplate
    Twitter Bootstrap
```


## favicon.ico image
```
/static/favicon.ico
```
base.html 

```
<link rel="shortcut icon" href="{% static 'favicon.ico' %}" type="image/x-icon">
```

### Testing Coverage

```
$ pip install coverage
````

#### $ coverage run --source='.' manage.py test
```
coverage run --source='.' manage.py test
Creating test database for alias 'default'...
...F..........
======================================================================
FAIL: test_root_url_resolves_to_home_page_view (todo.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_08/mysite/todo/tests.py", line 14, in test_root_url_resolves_to_home_page_view
    self.assertEqual(found.func, index)
AssertionError: <function home at 0x7f33353c2f28> != <function index at 0x7f3335711d08>

----------------------------------------------------------------------
Ran 14 tests in 14.718s

FAILED (failures=1)

```

### $ coverage report

```
coverage report
Name                                         Stmts   Miss  Cover
----------------------------------------------------------------
blog/__init__.py                                 1      0   100%
blog/admin.py                                   57     14    75%
blog/apps.py                                     4      0   100%
blog/migrations/0001_initial.py                  5      0   100%
blog/migrations/0002_auto_20151029_0925.py       5      0   100%
blog/migrations/__init__.py                      0      0   100%
blog/models.py                                  39      4    90%
blog/tests.py                                    1      0   100%
blog/urls.py                                     3      0   100%
blog/views.py                                   16      8    50%
functional_tests/__init__.py                     0      0   100%
functional_tests/test_all_users.py              23      4    83%
home/__init__.py                                 0      0   100%
home/admin.py                                    1      1     0%
home/migrations/__init__.py                      0      0   100%
home/models.py                                   1      1     0%
home/tests.py                                    9      0   100%
home/views.py                                    5      1    80%
manage.py                                        6      0   100%
mysite/__init__.py                               0      0   100%
mysite/apps.py                                   3      3     0%
mysite/settings.py                              29      0   100%
mysite/urls.py                                   5      0   100%
mysite/wsgi.py                                   4      4     0%
todo/__init__.py                                 0      0   100%
todo/admin.py                                    1      0   100%
todo/migrations/0001_initial.py                  5      0   100%
todo/migrations/__init__.py                      0      0   100%
todo/models.py                                   8      1    88%
todo/tests.py                                  105     18    83%
todo/urls.py                                     3      0   100%
todo/views.py                                   18      1    94%
----------------------------------------------------------------
TOTAL                                          357     60    83%

```

### $ coverage html

```
$ echo ".coverage" >> .gitignore
$ echo "htmlcov" >> .gitignore
```

base.html
```

        {% block navbar %}
            <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
    
            </nav>
        {% endblock %}
        
        
        {% block page %} 
            <div class="container">
                {% block content %} 
                
                {% endblock %} 

                {% block sidebar %}
                
   
                    {% block recent %}
                
                    {% endblock %}
        
                {% endblock %}

            </div>
        {% endblock %} 

        {% block footer %}
            <footer> 
                {% block copyright %} 
                {% endblock %} 
            </footer>
        {% endblock %}

```

### Добавление собственной библиотеки

Приложение должно содержать каталог templatetags на том же уровне что и models.py, views.py и др. Если он не существует, создайте его. Не забудьте создать файл __init__.py чтобы каталог мог использоваться как пакет Python. После добавления этого модуля, необходимо перезапустить сервер, перед тем как использовать теги или фильтры в шаблонах.

теги и фильтры будут находиться в модуле пакета templatetags. Название модуля будет использоваться при загрузке библиотеки в шаблоне, так что убедитесь что оно не совпадает с названиями библиотек других приложений.

Например, если теги/фильтры находятся в файле listlastnews.py, ваше приложение может выглядеть следующим образом:
```
blog/
    __init__.py
    models.py
    templatetags/
        __init__.py
        listlastnews.py
    views.py
```
И в шаблоне вы будете использовать:
```
{% load listlastnews %}
```
Приложение содержащее собственные теги и фильтры должно быть добавлено в INSTALLED_APPS, чтобы тег {% load %} мог загрузить его. Это сделано в целях безопасности.

Не имеет значение сколько модулей добавлено в пакет templatetags. Помните что тег {% load %} использует название модуля, а не название приложения.

Библиотека тегов должна содержать переменную register равную экземпляру template.Library, в которой регистрируются все определенные теги и фильтры. Так что в начале вашего модуля укажите следующие строки:
```
from django import template

register = template.Library()
```
templatetags/listlastnews.py
```
# -*- coding: UTF-8 -*-
from django import template
from blog.models import Article
register=template.Library()
 
@register.inclusion_tag('blog/lastnews.html') # регистрируем тег и подключаем шаблон lastnews
def lastnews():
    return {
        'last5news': Article.objects.filter(status='P')[:5],
    }
    
```
blog/lastnews.html
```
<div id = "news">
<h4>Последние статьи</h4>
<ul class="links">
    {% for item in last5news %}
       
       <li><a href="{% url 'blog:detail' item.id %}">{{ item.title }}</a></li>
    {% endfor %}
    
</ul>
</div>
```
blog/index.html
```
{% extends "base.html" %}

{% load staticfiles %}
{% load listlastnews %} <!-- загрузить listlastnews тег -->

{% block sidebar %} 
    <style type="text/css"> 
        #sidebar { float: right; border: 1px dotted #ccc; padding: 4px; } 
    </style> 

    <div id="sidebar"> 
     {% lastnews %}

    </div> 
{% endblock %}

{% block content %}
    <div class="jumbotron">
        <h1>Janus Blog Latest publications</h1>
    </div>

            {% if latest_blog_list %}
                <ul>
                {% for item in latest_blog_list %}
                    <li><a href="{% url 'blog:detail' item.id %}">{{ item.title }}</a></li>
                {% endfor %}
                </ul>
            {% else %}
                <p>No items are available.</p>
            {% endif %}


{% endblock %}
```
