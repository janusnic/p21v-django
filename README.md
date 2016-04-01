# p21v-django unit_02

./manage.py startapp home
--------------------------
```
mysite/
├── db.sqlite3
├── f_tests.py
├── home
│   ├── admin.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
└── mysite
    ├── __init__.py
    ├── __pycache__
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

Static Files Settings
=====================
Settings file (settings.py)
---------------------------
```
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    ...
    
    'django.contrib.staticfiles',
]
```

Static files (CSS, JavaScript, Images)
---------------------------------------
```
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
```

STATICFILES DIR
---------------
```
mkdir static
```

settings.py:
------------
```
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

STATICFILES_DIRS:
-----------------
```
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
```
Templates Settings
------------------
```
mkdir templates
```
Templates files
---------------
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                 django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Initializr: HTML5 Boilerplate and Twitter Bootstrap
---------------------------------------------------
http://www.initializr.com/

После загрузки и распаковки:
----------------------------
- Переместить index.html, 404.html, humans.txt и robots.txt в templates folder.
- Переименовать index.html в base.html. 
- Остальные файлы переместить в static
- Создайте свой favicon.ico.
- Можно удалить файлы apple-touch-icon.png, browserconfig.xml, tile-wide.png и tile.png.


# Django MVC, URLs, and View Functions

### Рабочий процесс в Django:

- HTTP-запрос приходит на определенной URL.
- Django использует некоторые правила и решает, какой метод контроллера должен откликнуться на запрос (это называется разрешением URL).
- Метод контроллера обрабатывает запрос и возвращает ответ HTTP.


## urls.py

mysite/urls.py. 
```
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

```
mysite/urls.py. 
```
from django.conf.urls import include, url
from django.contrib import admin

from home import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^admin/', include(admin.site.urls)),
]

```

home/views.py. 
--------------
```
from django.shortcuts import render

# Create your views here.
def home_page():
    pass
```
home/views.py. 

```
from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):

    return HttpResponse("<html><title>Welcome to Django. This is my cool Site!</title>")

```

urls.py
--------
```
rlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
]
```

home/views.py
-------------
```
 
def home(request):
    return render(request, "home/index.html", {})
```
templates/home
---------------
```
mkdir templates/home
touch templates/home/index.html
```
base.html
----------

    <title>{% block head_title %}{% endblock %}</title>


home/index.html
---------------
```
{% extends "base.html" %}
{% block head_title %}My Cook Django Site{% endblock %}
```

static/css/main.css
-------------------
```
.jumbotron h1 {
    color: rgba(200, 50, 255, 1);
}
```
base.html:
----------

        {% load staticfiles %}
        <!DOCTIPE html> 

static files
------------
Заменить

    <link rel="stylesheet" href="css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="css/main.css">

на

    <link rel="stylesheet" href="{% static 'css/bootstrap-theme.min.css' %}">
    <link rel="stylesheet" href="{% static 'css/main.css' %}">

Заменить

    <script src="js/vendor/modernizr-2.8.3-respond-1.4.2.min.js"></script>

на

    <script src="{% static 'js/vendor/modernizr-2.8.3-respond-1.4.2.min.js' %}">

Заменить

    <script src="js/main.js"></script>
    <script src="js/plugins.js"></script>

на

    <script src="{% static 'js/main.js' %}">
    <script src="{% static 'js/plugins.js' %}">

Заменить

    <script src="js/vendor/bootstrap.min.js"></script>

на

    <script src="{% static 'js/vendor/bootstrap.min.js' %}">

Но
--

    document.write('<script src="js/vendor/jquery-1.11.0.min.js"><\/script>')</script>

заменить на

    document.write('<script src="static/js/vendor/jquery-1.11.0.min.js"><\/script>')</script>


Объекты ответа и запроса
=========================

Django использует объекты ответа и запроса, чтобы передавать состояние в системе.

Когда запрашивает страница, Django создает объект HttpRequest, который содержит различные данные о запросе. Потом Django определяет и загружает необходимое представление и вызывает его передавая объект HttpRequest первым аргументом. Каждое представление должно вернуть объект HttpResponse.

urls.py
--------
```
from django.conf.urls import url
from home import views

urlpatterns = [
    url(r'^req/', views.req_test, name='req_test'),
]
```
views.py
---------
```
from django.http import HttpResponse

def req_test(request): 
    return HttpResponse("<html><title>Welcome to Django.</title><body><p>This is Request Test!</p></body></html>")

```

Объект class HttpRequest
-------------------------
Атрибуты
--------
Все атрибуты должны рассматриваться как неизменяемые, пока об обратном не будет сказано явно. Атрибут session является исключением из правила.

HttpRequest.scheme
------------------
Строка, указывающая схему запроса (обычно http или https).

HttpRequest.body
----------------
Тело запроса HTTP в байтовой строке. Он полезен для обработки данных различными способами, а не только традиционной HTML формой: передача изображений, загрузка XML и др. Для обработки данных обычной формы, используйте HttpRequest.POST.

HttpRequest.path
-----------------
Содержит полный путь к запрашиваемой странице, не включая домен.

HttpRequest.path_info
---------------------
часть URL-а после названия домена содержит префикс скрипта и “полезную” часть пути(path info portion). Атрибут path_info всегда содержит часть URL-а, которую использует Django, независимо от сервера. Использование этого атрибута вместо path сделает ваш код более надежным и независимым от настроек сервера.

Например
--------
```
def req_test(request): 
    output = "<html><title>Welcome to Django.</title><body><p>This is Request Test!</p>"
    mess = request.scheme
    output += 'scheme = '+ mess + '<br>'
    mess = request.path
    output += 'path = '+ mess + '<br>'
    mess = request.path_info
    output += 'path_info = '+ mess + '<br>'
   
    return HttpResponse(output)
```

HttpRequest.method
-------------------
Строка отображающая метод HTTP запроса. Значение всегда будет в верхнем регистре. 
Например:
---------
```
if request.method == 'GET':
        mess = 'Method = '+'GET' + '<br>'
    elif request.method == 'POST':
        mess = 'Method = '+'POST' + '<br>'
    output += mess
    output += "</body></html>"
```

HttpRequest.encoding
---------------------
Кодировка, которая используется для декодирования данных формы (или None, что означает использовать значение настройки DEFAULT_CHARSET). Вы можете изменить значение этого атрибута. При последующих доступах к атрибутам (например, чтение с GET или POST) будет использоваться новое значение encoding. Полезен, если вы знаете, что данные формы не используют кодировку указанную DEFAULT_CHARSET.

DEFAULT_CHARSET
---------------
По умолчанию: 'utf-8'

Кодировка, которая используется по умолчанию для объектов HttpResponse если MIME-тип не указан явно. Используется вместе с DEFAULT_CONTENT_TYPE при установке заголовка Content-Type.

DEFAULT_CONTENT_TYPE
--------------------
По умолчанию: 'text/html'

Тип содержимого(content type), который используется по умолчанию для объектов HttpResponse если MIME-тип не указан явно. Используется вместе с DEFAULT_CHARSET при установке заголовка Content-Type.

```
    request.encoding = 'utf-8'
    mess = settings.DEFAULT_CHARSET
    output += 'DEFAULT_CHARSET = '+ mess + '<br>'
    mess = str(request.encoding)
    output += 'encoding = '+ mess + '<br>'
```

HttpRequest.GET
---------------
Объект с интерфейсом словаря, который содержит HTTP GET параметры.

HttpRequest.POST
----------------
Объект-словарь содержащий все POST параметры, переданные формой. Если вам необходимо получить необработанные данные или данные переданные не через форму, используйте атрибут HttpRequest.body.

Запрос может использовать метод POST, но содержать пустой словарь POST – например, форма была передана через POST HTTP метод, но не содержала никаких данных. Поэтому, вы не должны использовать if request.POST для проверки был ли использован метод POST; вместо этого используйте if request.method == "POST".

POST не содержит информацию о загруженных файлах.
-------------------------------------------------

HttpRequest.COOKIES
--------------------
Словарь Python содержащий все “cookie”. Ключи и значения являются строками.

HttpRequest.FILES
-----------------
Объект с интерфейсом словаря, который содержит все загруженные файлы. Каждый ключ в FILES это name из input type="file" name="". Каждое значение в FILES это объект UploadedFile.

FILES содержит данные только, если метод запроса POST и form содержал enctype="multipart/form-data". В другом случае FILES будет содержать пустой словарь.

HttpRequest.META
----------------
Словарь Python содержащий все доступные HTTP заголовки запроса. Доступные заголовки зависят от сервера и клиента. Вот список возможных:

- CONTENT_LENGTH – размер содержимого запроса (содержимое учитывается как строка).

- CONTENT_TYPE – MIME-тип содержимого запроса.

- HTTP_ACCEPT_ENCODING – принимаемые кодировки ответа.

- HTTP_ACCEPT_LANGUAGE – принимаемые языки ответа.

- HTTP_HOST – заголовок HTTP Host отсылаемый клиентом.

- HTTP_REFERER – Ссылающаяся страница, если определена.

- HTTP_USER_AGENT – Строка “user-agent” клиента.

- QUERY_STRING – Строка запроса, не обработанная.

- REMOTE_ADDR – IP-адрес клиента.

- REMOTE_HOST – имя хоста клиента.

- REMOTE_USER – пользователь аутентифицированный Web-сервером, если определен.

- REQUEST_METHOD – Метод запроса. Строка, например, "GET" или "POST".

- SERVER_NAME – имя хоста сервера.

- SERVER_PORT – Порт сервера(строка).
```
    mess = request.META['HTTP_ACCEPT_ENCODING']
    output += 'HTTP_ACCEPT_ENCODING = '+ mess + '<br>'
```
За исключением CONTENT_LENGTH и CONTENT_TYPE, любый HTTP заголовок запроса преобразуется в ключ атрибута META конвертированием всех символов в верхний регистр, заменой дефисов нижним подчеркиванием и добавлением префикса HTTP_ к названию. Например, заголовок X-Bender будет добавлен в META с ключом HTTP_X_BENDER.

HttpRequest.user
----------------
Содержит объект AUTH_USER_MODEL представляющий текущего “залогиненного” пользователя. Если пользователь не авторизирован, атрибут user будет содержать django.contrib.auth.models.AnonymousUser. Вы можете различить их используя is_authenticated():

```
    if request.user.is_authenticated():
        mess = 'Hi User'
    else:
        mess = 'Hi Anonimouse!'

    output += 'User = '+ mess + '<br>'
```
Атрибут user доступен только если проект использует AuthenticationMiddleware. 

HttpRequest.session
-------------------
Объект с интерфейсом словаря, который доступен для чтения и изменений, представляет текущую сессию. Доступен только, если настроена поддержка сессии.

HttpRequest.urlconf
-------------------
Не определяется Django, но будет использован если другой код (например, собственный функциональный слой(middleware)) установит его. Если определен, значение будет использоваться как URLconf текущего запроса вместо значения настройки ROOT_URLCONF.

HttpRequest.resolver_match
--------------------------
Экземпляр ResolverMatch представляющий запрошенный URL. Атрибут устанавливается при поиске подходящего URL-шаблона, это значит что middleware он не доступен т.к. они вызывается до обработки URL-а (в таком случае вместо process_request можно использовать process_view).

Методы
======
HttpRequest.get_host()
-----------------------
Возвращает оригинальное имя хоста используя информацию из HTTP_X_FORWARDED_HOST (если включена настройка USE_X_FORWARDED_HOST) и HTTP_HOST заголовков, в соответствующем порядке. Если эти значения не определенны, метод использует комбинацию SERVER_NAME и SERVER_PORT как описано в PEP 3333.

Например: 
```
output += 'Host = '+ request.get_host() + '<br>'
```
HttpRequest.get_full_path()
---------------------------
Возвращает path, со строкой запроса, если она присутствует.

HttpRequest.build_absolute_uri(location)
----------------------------------------
Возвращает абсолютный URI для аргумента location. Если location не указан, будет использовано значение request.get_full_path().

Если location уже является абсолютным URI, значение останется не измененным. В другом случае абсолютный URI будет создан с использованием данных запроса.

Например:
```
output += 'Path = '+ request.get_full_path() + '<br>'
```

Объект HttpResponse
===================
class HttpResponse
------------------
В отличии от объекта HttpRequest, который создается Django, объект HttpResponse создаете вы. Каждое представление должно создать и вернуть объект HttpResponse.

Класс HttpResponse находится в модуле django.http.

Передача строки
----------------
Типичное использование заключается в передаче содержимого страницы в виде строки в конструктор HttpResponse:
```
from django.http import HttpResponse
response = HttpResponse("Here's the text of the Web page.")
response = HttpResponse("Text only, please.", content_type="text/plain")
```
Но если вам необходимо добавлять содержимое постепенно, вы можете использовать объект response как объект файла:

```
response = HttpResponse()
response.write("<p>Here's the text of the Web page.</p>")
response.write("<p>Here's another paragraph.</p>")
```

Передача итератора
------------------
Вы можете передать итератор в конструктор HttpResponse вместо строк. HttpResponse сразу выполнит итератор и сохранит результат как строку.

Если необходимо отдавать данные из итератора в потоке, используйте экземпляр StreamingHttpResponse.

Установка заголовков
--------------------
При установке или удалении заголовка в объекте ответа, рассматривайте его как словарь:
```
response = HttpResponse()
response['Age'] = 120
del response['Age']
```
в отличии от словаря, del не вызовет исключение KeyError если заголовок не определен.

Для установки заголовков Cache-Control и Vary, лучше использовать функции patch_cache_control() и patch_vary_headers() из модуля django.utils.cache, так как эти поля могут содержать несколько значений, разделенных запятыми. Эти функции добавят новые значение не удаляя существующие.

HTTP заголовки не могут содержать перенос строки. При попытке добавить заголовок содержащий символ переноса строки (CR или LF) будет вызвано исключение BadHeaderError

Указываем браузеру воспринимать ответ как вложенный файл
---------------------------------------------------------
Для этого используйте аргумент content_type и установите заголовок Content-Disposition. Например, вот так вы можете вернуть таблицу Microsoft Excel:
```
response = HttpResponse(output, content_type='application/vnd.ms-excel')
response['Content-Disposition'] = 'attachment; filename="foo.xls"'
```
HttpResponse.content
--------------------
Байтовое представление содержимого, закодированное с объекта Unicode при необходимости.

HttpResponse.charset
---------------------
Кодировка, в которую будет закодирован ответ. Если не указана во время создания объекта HttpResponse, будет проверятся content_type, и если не будет найдена, будет использоваться значение настройки DEFAULT_CHARSET.
```
 print(response.charset)
```
HttpResponse.status_code
------------------------
Код HTTP состояния ответа.
```
print(response.status_code) # 200
```
HttpResponse.reason_phrase
--------------------------
Описание HTTP ответа(HTTP reason phrase).
```
    print(response.reason_phrase) # OK
```
HttpResponse.streaming
-----------------------
Всегда False.
Указывает middleware, что этот ответ потоковый и его нужно обрабатывать не так, как обычные запросы.

HttpResponse.closed
--------------------
True, если ответ был закрыт.

Методы
-------
HttpResponse.__init__(content='', content_type=None, status=200, reason=None, charset=None)
--------------------------------------------------------------------------------------------
Создает экземпляр HttpResponse с переданным содержимым и MIME-типом.

- content должен быть строкой или итератором. Если это итератор, он должен возвращать строки, которые будут объединены для формирования содержимого ответа. Если это не итератор и не строка, значение будет конвертировано в строковое представление.

- content_type - MIME-тип, возможно с кодировкой, используется в HTTP заголовке Content-Type. Если не указан, используются настройки DEFAULT_CONTENT_TYPE и DEFAULT_CHARSET, по умолчанию: “text/html; charset=utf-8”.

- status – это Код HTTP состояния ответа.

- reason – это описание HTTP ответа. Если не указано, будет использоваться стандартное значение.

- charset - кодировка, в которую будет закодирован ответ. Если не указана во время создания объекта HttpResponse, будет проверятся content_type, и если не будет найдена, будет использоваться значение настройки DEFAULT_CHARSET.

HttpResponse.__setitem__(header, value)
---------------------------------------
Устанавливает заголовок ответа. header и value должны быть строками.

HttpResponse.__delitem__(header)
--------------------------------
Удаляет заголовок ответа. Не вызывает исключения, если заголовок не существует. Регистронезависимый.

HttpResponse.__getitem__(header)
----------------------------------
Возвращает значение заголовка. Регистрозависимый.

HttpResponse.has_header(header)
-------------------------------
Возвращает True или False в результате регистронезависимого поиска заголовка по указанному названию.

HttpResponse.setdefault(header, value)
--------------------------------------
Устанавливает заголовок, если он еще не был установлен.

HttpResponse.write(content)
----------------------------
Метод для соблюдения интерфейса объекта файла.

HttpResponse.flush()
--------------------
Метод для соблюдения интерфейса объекта файла.

HttpResponse.tell()
--------------------
Метод для соблюдения интерфейса объекта файла.

HttpResponse.getvalue()
-----------------------
Возвращает значение HttpResponse.content. Этот метод позволяет использовать HttpResponse как объект-файл.
```
print(response.content)
print(response.getvalue())

```
HttpResponse.writable()
-----------------------
Всегда True. Этот метод позволяет использовать HttpResponse как объект-файл.

HttpResponse.writelines(lines)
------------------------------
Записывает список строк в ответ. Разделители строк не добавляются. Этот метод позволяет использовать HttpResponse как объект-файл.

Шаблоны
========
Django позволяет динамически генерировать HTML. Самый распространенный подход - использование шаблонов. Шаблоны содержат статический HTML и динамические данные, рендеринг которых описан специальным синтаксисом. 

Проект Django может использовать один или несколько механизмов создания шаблонов (или ни одного, если вы не используете шаблоны). Django предоставляет бэкенд для собственной системы шаблонов, которая называется - язык шаблонов Django (Django template language, DTL), и популярного альтернативного шаблонизатора Jinja2. Сторонние приложения могут предоставлять бэкенд и для других систем шаблонов.

Django предоставляет стандартный API для загрузки и рендеринга шаблонов, незавимисо от используемого бэкенда. Загрузка включает в себя поиск шаблона по названию и предварительную обработку, обычно выполняется загрузка шаблона в память. Рендеринг означает передачу данных контекста в шаблон и возвращение строки с результатом.

Язык шаблонов Django – собственная система шаблонов Django. До Django 1.8 – это была единственная альтернатива. Встроенные шаблоны Django, которые содержат шаблоны, например django.contrib.admin, используют систему шаблонов Django.

По историческим причинам поддержка шаблонов и встроенная система шаблонов Django находятся в одном пакете django.template.

Поддержка систем шаблонов TEMPLATES.
====================================
Настройки
---------
Шаблоны можно настроить с помощью настройки TEMPLATES. Это список, который содержит настройки для систем шаблонов. По умолчанию настройка пустая. settings.py, сгенерированный командой startproject, содержит значение:
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            # ... some options here ...
        },
    },
]
```
BACKEND - путь для импорта Python к классу бэкенда шаблонов. Встроенные бэкенды это django.template.backends.django.DjangoTemplates и django.template.backends.jinja2.Jinja2.

Т.к. большинство систем шаблонов загружают шаблоны с файлов, настройки содержат:

- DIRS, которая содержим список каталогов с шаблонами. Бэкенд ищет в них шаблон в указанном порядке.

- APP_DIRS указывает бэкенду искать ли шаблоны в установленных приложениях. Каждый бэкенд определяет определенное название для каталога с шаблонами в приложении.

Загрузка шаблонов
=================
Обычно при разработке проекта шаблоны хранятся в файлах. Сохраняйте их в каталоге, который называют templates.

Django ищет каталоги с шаблонами в соответствии с настройками загрузки шаблонов. Самый простой способ – указать каталоги с шаблонами в опции DIRS.

Опция DIRS
----------
По умолчанию использует значение настройки TEMPLATE_DIRS.

Настройка должна содержать список или кортеж полных путей к каталогам. Например:
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            '/home/html/templates/lawrence.com',
            '/home/html/templates/default',
        ],
    },
]
```
Шаблоны могут находиться где угодно, главное, чтобы у Web-сервера были права на чтение. Расширение файла может быть любым, .html или .txt, или вообще без расширения.

пути должны быть Unix-стиле, даже для Windows (то есть использовать /).

Типы загрузчиков
-----------------
По умолчанию Django использует загрузчик шаблонов с файловой системы, но Django предоставляет и другие загрузчики шаблонов, которые позволяют загружать шаблоны с других источников.

Некоторые из них выключены по умолчанию, но вы можете активировать их изменив опцию 'loaders' бэкенда DjangoTemplates в настройке TEMPLATES, или передав аргумент loaders в Engine. Опция loaders содержит кортеж строк, каждая из которых представляет класс загрузчика шаблонов. Вот список загрузчиков, которые предоставляет Django:
```
django.template.loaders.filesystem.Loader
```
class filesystem.Loader
-----------------------
Загружает шаблоны с файловой системы в соответствии с настройкой DIRS.

Этот загрузчик включен по умолчанию. Однако, он не найдет ни один шаблон, пока вы не укажите список каталогов в DIRS:
```
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
}]
django.template.loaders.app_directories.Loader
```
class app_directories.Loader
----------------------------
Загружает шаблоны из каталога приложения Django. Для каждого приложения в INSTALLED_APPS загрузчик ищет под-каталог templates. Если под-каталог найден, Django ищет в нем шаблон.

Это означает, что вы можете хранить шаблоны вместе с приложением. Таким образом легко распространять приложение Django с шаблонами по умолчанию.

Например для следующих настроек:
```
INSTALLED_APPS = ('myproject.polls', 'myproject.music')
```
... get_template('foo.html') будет искать foo.html в таких каталогах в указанном порядке:
```
/path/to/myproject/polls/templates/
/path/to/myproject/music/templates/
```
... и будет использовать первый найденный.

Порядок INSTALLED_APPS – важен! Например, вы хотите переопределить шаблон админки Django, например admin/base_site.html из django.contrib.admin, заменив на admin/base_site.html из myproject.polls. Вы должны указать myproject.polls перед django.contrib.admin в INSTALLED_APPS, иначе шаблон из django.contrib.admin будет загружен первым, а ваш проигнорирован.

Обратите внимание, загрузчик выполняет некоторую оптимизацию при первом импорте: он кеширует список приложений из INSTALLED_APPS, которые содержат под-каталог templates.

Вы можете включить этот загрузчик, указав True в APP_DIRS:
```
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
}]
django.template.loaders.eggs.Loader
```
class eggs.Loader
------------------
Аналогичен app_directories, но загружает шаблоны из Python eggs, а не файловой системы.

Загрузчик выключен по умолчанию.

django.template.loaders.cached.Loader
-------------------------------------
class cached.Loader
-------------------
По умолчанию система шаблонов читает и компилирует ваш шаблон при каждом рендеринге шаблона. Хотя система шаблонов Django работает достаточно быстро, но общие накладные расходы на чтение и компилирование шаблонов могут быть существенны.

Кеширующий загрузчик шаблонов принимает список загрузчиков Он будет использовать их для поиска неизвестных шаблонов, которые загружаются первый раз. Затем скомпилированные Template сохраняются в памяти. Закешированный объект Template возвращается при повторном поиске уже загруженного шаблона.

Например, чтобы включить кеширование с загрузчиками filesystem и app_directories, используйте следующие настройки:
```
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'OPTIONS': {
        'loaders': [
            ('django.template.loaders.cached.Loader', [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]),
        ],
    },
}]
```

Все встроенные теги Django можно использовать с кеширующим загрузчиком, но теги сторонних приложений, или ваши собственные, должны использовать потокобезопасный код при использовании класса Node.
Загрузчик выключен по умолчанию.

django.template.loaders.locmem.Loader
-------------------------------------

class locmem.Loader
--------------------
Загружает шаблоны из словаря Python. Удобен при тестировании.

Этот загрузчик принимает словарь каталогов первым аргументом:
```
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'OPTIONS': {
        'loaders': [
            ('django.template.loaders.locmem.Loader', {
                'index.html': 'content here',
            }),
        ],
    },
}]
```
Загрузчик выключен по умолчанию.

Django использует загрузчики шаблонов в порядке, указанном в опции 'loaders'. Загрузчики используются пока один из них не найдет шаблон.

urls.py
--------
```
from django.conf.urls import include, url
from django.contrib import admin
from home import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home_page, name='home_page'),
]

```

Вспомогательные функции
========================
Пакет django.shortcuts содержит вспомогательные функции и классы влияющие на несколько уровней MVC. эти функции упрощают разработку и код.

render
-------
```
render(request, template_name[, context][, context_instance][, content_type][, status][, current_app][, dirs][, using])

```
Выполняет указанный шаблон с переданным словарем контекста и возвращает HttpResponse с полученным содержимым.

Функция render() аналогична вызову функции render_to_response() с аргументом context_instance, который указывает использовать RequestContext.

Django не предоставляет функции для создания TemplateResponse т.к. конструктор TemplateResponse принимает аргументы аналогичные аргументам render().

Обязательные аргументы
----------------------
request
--------
Объект обрабатываемого запроса

template_name
-------------
Полное название шаблона, который должен использоваться, или список названий шаблонов. Если передать список, будет использован первый существующий шаблон.

Необязательные аргументы
------------------------
context
-------
Словарь переменных для контекста шаблона. По умолчанию, этот словарь пустой. Если значение ключа словаря это функция, она будет вызвана перед выполнением шаблона.

content_type
-------------
MIME-тип результата. По умолчанию используется значение настройки DEFAULT_CONTENT_TYPE.

status
------
Код HTTP статуса ответа. По умолчанию 200.

using
-----
Параметр конфигурации NAME используется шаблонным движком для загрузки шаблона.

views.py
--------
```
from django.shortcuts import render

def home_page(request):
    return render(request, 'home/home.html', {})
```
Этот method аналогичен:
-----------------------
```
from django.http import HttpResponse
from django.template import RequestContext, loader

def home_page(request):
    t = loader.get_template('home/home.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))
```

tests.py
--------
```
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from home.views import home_page, home

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home/home.html')
        self.assertEqual(response.content.decode(), expected_html)

```
./manage.py test
-----------------
```
ERROR: test_home_page_returns_correct_html (home.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/dj-21v/unit_03/mysite/home/tests.py", line 20, in test_home_page_returns_correct_html
    response = home_page(request)
  File "/home/janus/github/dj-21v/unit_03/mysite/home/views.py", line 60, in home_page
    return render(request, 'home/home.html')
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/shortcuts.py", line 67, in render
    template_name, context, request=request, using=using)
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/template/loader.py", line 96, in render_to_string
    template = get_template(template_name, using=using)
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/template/loader.py", line 43, in get_template
    raise TemplateDoesNotExist(template_name, chain=chain)
django.template.exceptions.TemplateDoesNotExist: home/home.html

```
templates/home/home.html
------------------------
```
<html>
    <head>
        <title>Home Page</title>
    </head>
    <body>
        <h1>Home Page</h1>
        
    </body>
</html>
```
./manage.py test
----------------
```
Creating test database for alias 'default'...
...
----------------------------------------------------------------------
Ran 3 tests in 0.062s

OK
Destroying test database for alias 'default'...

```
Язык шаблонов Django
====================
Шаблон Django – это просто текстовый файл, или строка Python, которые следуют языку шаблонов Django. Определенные конструкции распознаются и интерпретируются шаблонизатором. Основные – это переменные и теги.

Шаблон рендерится с контекстом. Рендеринг заменяет переменные на их значения, которые ищутся в контексте, и выполняет теги. Все остальное выводится как есть.

Синтаксис языка шаблонов Django использует четыре конструкции.
--------------------------------------------------------------
### Переменные
Переменные выводят значения из контекста, который является словарем.

Переменные выделяются {{ и }}, например:
views.py
--------
```
from django.shortcuts import render

def home_page(request):
    return render(request, 'home/home.html', {'first_name': 'Billi', 'last_name': 'Bons'})
```
home.html
---------
```
My first name is {{ first_name }}. My last name is {{ last_name }}.
```
Обращение к ключам словаря, атрибутам объектов и элементам списка выполняется через точку:

views.py
--------
```
from django.shortcuts import render

def home_page(request):
    my_dict = {'key':'My dikt Key'}

    return render(request, 'home/home.html', {'first_name': 'Billi', 'last_name': 'Bons', 'my_dict':my_dict})

```
home.html
---------
```
My first name is {{ first_name }}. My last name is {{ last_name }}.
{{ my_dict.key }}
```
views.html
----------
```
def home_page(request):
    my_dict = {'key':'My dikt Key'}
    my_list = [1,2,3,4]
    return render(request, 'home/home.html', {'first_name': 'Billi', 'last_name': 'Bons', 'my_dict':my_dict,'my_list':my_list})

```
home.html
---------
```
My first name is {{ first_name }}. My last name is {{ last_name }}.
        {{ my_dict.key }}
        {{ my_list.1 }}
```

views.html
----------
```
class Myobject:
    attribute = 'my_object.attribute'

def home_page(request):
    my_dict = {'key':'My dikt Key'}

    my_object = Myobject()
    my_list = [1,2,3,4]

    return render(request, 'home/home.html', {'first_name': 'Billi', 'last_name': 'Bons', 'my_dict':my_dict,'my_list':my_list,'my_object':my_object})
 
```
home.html
---------
```
{{ my_object.attribute }}

```
Если значение переменной является вызываемый объект, шаблонизатор вызовет его без аргументов и подставит результат.

### Теги
Теги позволяют добавлять произвольную логику в шаблон.

Например, теги могут выводить текст, добавлять логические операторы, такие как “if” или “for”, получать содержимое из базы данных, или предоставлять доступ к другим тегам.

Теги выделяются {% и %}, например:
```
{% csrf_token %}
```
Большинство тегов принимают аргументы:
```
{% cycle 'odd' 'even' %}
```
Некоторые теги требуют закрывающий тег:
```
{% if user.is_authenticated %}Hello, {{ user.username }}.{% endif %}
```
autoescape
----------
Контролирует авто-экранирование. Этот тег принимает on или off аргумент, указывающий должно ли использоваться автоматическое экранирование внутри блока. Блок закрывается закрывающим тегом endautoescape.

Если экранирование включено, ко всем переменным будет применяется HTML-экранирование перед выводом (но после применения всех фильтров). Это эквивалентно использованию фильтра escape для каждой переменной.

Не будут экранированы переменные помеченные как безопасные( “safe”), или кодом определяющим переменную, или после применения фильтров safe или escape.

Пример 
-------
views.py
--------
```
def home_page(request):
    my_dict = {'key':'My dikt Key'}
    my_object = Myobject()
    my_list = [1,2,3,4]
    return render(request, 'home/home.html', {'first_name': 'Billi', 'last_name': 'Bons', 'my_dict':my_dict,'my_list':my_list,'my_object':my_object, 'name':'<script>alert("XSS");</script>'})

```
home.html:
----------
```
        {% autoescape on %}
        <h2>autoescape on</h2>
        {{ name }}
        {% endautoescape %}
        
        {% autoescape off %}
        <h3>autoescape off</h3>
        {{ name }}
        {% endautoescape %}
```
Комментарии
------------
Комментарии могут выглядеть таким образом:
```
{# this won't be rendered #}
```
Тег {% comment %} позволяет добавлять многострочные комментарии.

comment
-------
Игнорирует содержимое между {% comment %} и {% endcomment %}. Можно добавить заметку в первый тег. Например, добавить комментарий, описывающий почему код был закомментирован.

Пример:
-------
```
<p>Rendered text with {{ pub_date|date:"c" }}</p>
{% comment "Optional note" %}
    <p>Commented out text with {{ create_date|date:"c" }}</p>
{% endcomment %}
```

Тег comment не может быть вложенным.
------------------------------------
csrf_token
-----------
Этот тег используется для организации CSRF защиты.

Циклы
======
# Цикл for
Цикл по каждому элементу массива, добавляя их в контекст блока:

views.py
--------
```
def home_page(request):
    my_dict = {'key':'My dikt Key'}
    my_object = Myobject()
    my_list = [1,2,3,4]

    categories = [{'id':0,'name':'Python'},{'id':1,'name':'Django'},{'id':2,'name':'Web'},{'id':4,'name':'Javascript'}]

    return render(request, 'home/home.html', {'first_name': 'Billi', 'last_name': 'Bons', 'my_dict':my_dict,'my_list':my_list,'my_object':my_object, 'name':'<script>alert("XSS");</script>','rowclass1':'border: red solid 7px;', 'rowclass2':'border: green solid 3px;','categories':categories})
 
```
home.html
----------
```
<h2>Категории</h2>
<ul>
{% for cat in categories %}
    <li>{{ cat.name }}</li>
{% endfor %}
</ul>
```
Категории
---------
```
        <ul>
            <li>Python</li>
            <li>Django</li>
            <li>Web</li>
            <li>Javascript</li>
        </ul>
```
Можно использовать цикл по списку в обратном порядке {% for obj in list reversed %}.
```
    <h2>Категории reversed</h2>
        <ul>
        {% for cat in categories reversed %}
            <li>{{ cat.name }}</li>
        {% endfor %}
        </ul>
```
Если нужен цикл по списку списков, можно распаковать значения под-списка на отдельные переменные. 

Например, если контекст содержит список (x,y) координат points, можно использовать следующий код для их вывода:

```
{% for x, y in points %}
    There is a point at {{ x }},{{ y }}
{% endfor %}

```
Аналогично можно использовать словарь. Например, если контекст содержит словарь data, следующий код выведет ключи и значения словаря:
```
        <ul>
        {% for data in categories %}
        {% for key, value in data.items %}
            <li>{{ key }}: {{ value }}</li>
        {% endfor %}
        {% endfor %}
        </ul>
```

Внутри цикла доступные некоторые дополнительные переменные:
-----------------------------------------------------------
- forloop.counter 
Номер текущей итерации цикла начиная с 1

home.html
---------
```
    <h2>Категории</h2>
        <ul>
        {% for cat in categories %}
            <li>{{ forloop.counter }} {{ cat.name }}</li>
        {% endfor %}
        </ul>
```

- forloop.counter0    
Номер текущей итерации цикла начиная с 0

- forloop.revcounter  
Номер текущей итерации цикла начиная с конца с 1

- forloop.revcounter0 
Номер текущей итерации цикла начиная с конца с 0

- forloop.first   
True, если это первая итерация

- forloop.last    
True, если это последняя итерация

- forloop.parentloop  
Для вложенных циклов, это “внешний” цикл.

- for ... empty
Тег for содержит необязательную часть {% empty %}, которая будет отображена, если список пуст или не найден:
```
<ul>
{% for cat in categories %}
    <li>{{ cat.name }}</li>
{% empty %}
    <li>Sorry, no categore in this list.</li>
{% endfor %}
</ul>
```
Это эквивалентно, но короче, читабельней и возможно быстрее, такому коду:
```
<ul>
  {% if categories %}
    {% for cat in categories %}
      <li>{{ cat.name }}</li>
    {% endfor %}
  {% else %}
    <li>Sorry, no categories in this list.</li>
  {% endif %}
</ul>
```

cycle
------
Возвращает один из аргументов при вызове. Первый аргумент при первом вызове, второй - при втором, и т.д. Когда аргументы кончаются, тег начинает с начала списка аргументов.

Этот тег полезен в циклах:
--------------------------
```
<table>
        <caption><h2>Test Table</h2></caption>
        {% for o in my_list %}
            <tr class="{% cycle 'row1' 'row2' %}">
                <td><img src='static/img/star.png'></td><td><img src='static/img/star.png'></td>
            </tr>
        {% endfor %}
        </table>
```
Первый вызов сгенерирует HTML используя класс row1, второй - row2, третий - снова row1, и так далее для каждой итерации цикла.
```
        <table>
            <caption><h2>Test Table</h2></caption>
            <tr class="row1">
                <td><img src='static/img/star.png'></td><td><img src='static/img/star.png'></td>
            </tr>
            <tr class="row2">
                <td><img src='static/img/star.png'></td><td><img src='static/img/star.png'></td>
            </tr>
            <tr class="row1">
                <td><img src='static/img/star.png'></td><td><img src='static/img/star.png'></td>
            </tr>
            <tr class="row2">
                <td><img src='static/img/star.png'></td><td><img src='static/img/star.png'></td>
            </tr>
        </table>
```

Вы можете также использовать переменные. Например, если у вас есть две переменных в шаблоне, rowclass1 и rowclass2, вы можете переключаться между их значениями:
```
def home_page(request):
    my_dict = {'key':'My dikt Key'}
    my_object = Myobject()
    my_list = [1,2,3,4]

    return render(request, 'home/home.html', {'first_name': 'Billi', 'last_name': 'Bons', 'my_dict':my_dict,'my_list':my_list,'my_object':my_object, 'name':'<script>alert("XSS");</script>','rowclass1':'border: red solid 7px;', 'rowclass2':'border: green solid 3px;'})
```

Переданные значения будут экранированы. Автоматическое экранирование можно выключить:

```
        <table>
        <caption><h2>Border Table</h2></caption>
        {% for o in my_list %}
            <tr>
                <td style="{% autoescape off %}{% cycle rowclass1 rowclass2  %}{% endautoescape %}"><img src='static/img/star.png'></td><td><img src='static/img/star.png'></td>
            </tr>
        {% endfor %}
        </table>
```
В можете использовать переменные и строки вместе:
```
{% for o in some_list %}
    <tr class="{% cycle 'row1' rowclass2 'row2' %}">
        ...
    </tr>
{% endfor %}
```
В некоторых случаях вам может понадобиться обратиться к значению не в цикле. Для этого просто передайте в тег {% cycle %} название, используя “as”, например:
```
{% cycle 'row1' 'row2' as rowcolors %}
```
Теперь вы можете использовать текущее значение цикла в любом месте шаблона используя переданное название как переменную контекста. Если вам необходимо следующее значение, используйте тег снова, используя название переменной. 

Следующий шаблон:
```
        <table>
        <caption><h2>Background Table</h2></caption>
        <tr>
            <td class="{% cycle 'row1' 'row2' as rowcolors %}">Background Table</td>
            <td class="{{ rowcolors }}">Background Table</td>
        </tr>
        <tr>
            <td class="{% cycle rowcolors %}">Background Table</td>
            <td class="{{ rowcolors }}">Background Table</td>
        </tr>
        </table>
```
выведет:
```
        <table>
        <caption><h2>Background Table</h2></caption>
        <tr>
            <td class="row1">Background Table</td>
            <td class="row1">Background Table</td>
        </tr>
        <tr>
            <td class="row2">Background Table</td>
            <td class="row2">Background Table</td>
        </tr>
        </table>
```
Вы можете использовать любое количество значений в теге cycle, разделенных пробелами. Значения в одинарных (') или двойных кавычках (") рассматриваются как строки, в то время как, значения без кавычек, интерпретируются как переменные.

По умолчанию, использование тега {% cycle %} с аргументом as выведет первое значение цикла. Это может быть проблемой, если вы хотите использовать значение во вложенном теге или в включенном теге. Если вы хотите просто определить цикл, но не выводить первое значение, используйте аргумент silent в конце тега. 

ifchanged
---------
Проверяет было ли изменено значение предыдущей итерации цикла.

Блочный тег {% ifchanged %} используется внутри цикла. 

Существует два способа использовать тег.

1. Проверять содержимое тега, и если оно было изменено с последней итерации, отображать его. Например, этот код отображает список дней и отображает месяц только при его изменении:
```
<h1>Archive for {{ year }}</h1>

{% for date in days %}
    {% ifchanged %}<h3>{{ date|date:"F" }}</h3>{% endifchanged %}
    <a href="{{ date|date:"M/d"|lower }}/">{{ date|date:"j" }}</a>
{% endfor %}
```
2. Если передано одна или более переменных, проверяет была ли изменена одна из переменных. Например, следующий код отображает дату при каждом изменении, в то же время отображает час, если час или дата были изменены:
```
{% for date in days %}
    {% ifchanged date.date %} {{ date.date }} {% endifchanged %}
    {% ifchanged date.hour date.date %}
        {{ date.hour }}
    {% endifchanged %}
{% endfor %}
```
Тег ifchanged может содержать необязательный блок {% else %}, который будет отображаться, если значение не изменилось:
```
{% for match in matches %}
    <div style="background-color:
        {% ifchanged match.ballot_id %}
            {% cycle "red" "blue" %}
        {% else %}
            gray
        {% endifchanged %}
    ">{{ match }}</div>
{% endfor %}
```

debug
-----
Выводит всю отладочную информацию, в том числе текущей контекст и импортированные модули.


firstof
-------
Выводит первую из переданных переменных, которая не равна False. Ничего не выводит, если все переменные равны False.

Пример:
```
{% firstof var1 var2 var3 %}
```
Это равносильно:
```
{% if var1 %}
    {{ var1 }}
{% elif var2 %}
    {{ var2 }}
{% elif var3 %}
    {{ var3 }}
{% endif %}
```
Вы можете использовать строку как значение по-умолчанию на случай, если все переменные равны False:
```
{% firstof var1 var2 var3 "fallback value" %}
```
Этот тэг экранирует переменные. Автоматическое экранирование можно выключить:
```
{% autoescape off %}
    {% firstof var1 var2 var3 "<strong>fallback value</strong>" %}
{% endautoescape %}
```
Если только некоторые переменные должны быть экранированы, используйте:
```
{% firstof var1 var2|safe var3 "<strong>fallback value</strong>"|safe %}
```

if
---
Тег {% if %} вычисляет переменную и если она равна “true” (то есть существует, не пустая и не равна “false”) выводит содержимое блока:
```
{% if categories %}
    Number of categories: {{ categories|length }}
{% elif subcategories %}
    This is categories
{% else %}
    No categories.
{% endif %}
```
тег if может содержать один или несколько блоков `` {% elif %}``, так же как и блок {% else %}, который будет выведен, если все предыдущие условия не верны. Все эти блоки необязательны.

Булевы операторы
----------------
Тег if может использовать and, or или not:
```
{% if categories and subcategories %}
    Both categories and subcategories are available.
{% endif %}

{% if not categories %}
    There are no categories.
{% endif %}

{% if categories or subcategories %}
    There are some categories or some subcategories.
{% endif %}

{% if not categories or subcategories %}
    There are no categories or there are some subcategories.
{% endif %}

{% if categories and not subcategories %}
    There are some categories and absolutely no subcategories.
{% endif %}
```
Можно использовать and и or вместе, операция and имеет больший приоритет чем or, например:
```
{% if categories and subcategories or tag_list %}
```
будет интерпретировано как:
```
if (categories and subcategories) or tag_list
```
Использовать скобки в теге if нельзя. Если вам нужно указать приоритет, используйте вложенные теги if.

Тег if может использовать операторы ==, !=, <, >, <=, >= и in которые работают таким образом:

Оператор ==
------------
Равенство. Например:
```
{% if somevar == "x" %}
  This appears if variable somevar equals the string "x"
{% endif %}
```
Оператор !=
------------
Неравенство. Например:
```
{% if somevar != "x" %}
  This appears if variable somevar does not equal the string "x",
  or if somevar is not found in the context
{% endif %}
```
Оператор <
-----------
Меньше чем. Например:
```
{% if somevar < 100 %}
  This appears if variable somevar is less than 100.
{% endif %}
```
Оператор >
------------
Больше чем. Например:
```
{% if somevar > 0 %}
  This appears if variable somevar is greater than 0.
{% endif %}
```
Оператор <=
-------------
Меньше чем или равно. Например:
```
{% if somevar <= 100 %}
  This appears if variable somevar is less than 100 or equal to 100.
{% endif %}
```
Оператор >=
------------
Больше чем или равно. Например:
```
{% if somevar >= 1 %}
  This appears if variable somevar is greater than 1 or equal to 1.
{% endif %}
```
Оператор in
------------
Вхождение в. Этот оператор поддерживается большинством контейнеров Python, чтобы проверит входит ли значение в контейнер. 
```
{% if "bc" in "abcdef" %}
  This appears since "bc" is a substring of "abcdef"
{% endif %}

{% if "hello" in greetings %}
  If greetings is a list or set, one element of which is the string
  "hello", this will appear.
{% endif %}

{% if user in users %}
  If users is a QuerySet, this will appear if user is an
  instance that belongs to the QuerySet.
{% endif %}
```
Оператор not in
----------------
Не вхождение в. Оператор обратный оператору in.

Операторы сравнения не могут использовать вместе как в Python или математике. Например, вместо использования:
```
{% if a > b > c %}  (WRONG)
```
вы должны использовать:
```
{% if a > b and b > c %}
```
Фильтры
========
Вы можете использовать фильтры в выражении if. Например:
```
{% if messages|length >= 100 %}
   You have lots of messages today!
{% endif %}
```
Сложные выражения
------------------
Приоритет операторов, от низшего к высшему, выглядит следующим образом:

1. or
2. and
3. not
4. in
5. ==, !=, <, >, <=, >=

тег if:
-------
```
{% if a == b or c == d and e %}
```
...будет интерпретирован как:
```
(a == b) or ((c == d) and e)
```
Если вам нужен другой приоритет, используйте вложенные теги if.

ifequal
--------
Выводит содержимое блока, если два аргумента равны

Например:
```
{% ifequal user.pk comment.user_id %}
    ...
{% endifequal %}
```
Как и в теге if, можно использовать необязательный блок {% else %}.

Аргументом может быть строка:
```
{% ifequal user.username "adrian" %}
    ...
{% endifequal %}
```
Альтернативой использованию тега ifequal является применение if и оператора ==.

ifnotequal
----------
Аналогичен тегу ifequal, но проверяет аргументы на неравенство.

Альтернативой тегу ifnotequal является использование тега if и оператора !=.

lorem
------
Выводит случайный “lorem ipsum” текст. Полезен для генерации примера данных в шаблоне.

Использование:
```
{% lorem [count] [method] [random] %}
```
Тег {% lorem %} принимает несколько аргументов:
- count   
Количество параграфов или слов в сгенерированном тесте (по умолчанию 1).

- method  
Принимает w для слов, p – для HTML параграфов, или b – для текстовых параграфов (по умолчанию b).

- random 
Если передать слово random, не будет использоваться стандартный текст (“Lorem ipsum dolor sit amet...”) при генерации текста.

Примеры:
```
{% lorem %} выведет обычный параграф “lorem ipsum”.

{% lorem 3 p %} выведет обычный параграф “lorem ipsum” и два случайных параграфа, обернутые в HTML тег <p>.

{% lorem 2 w random %} выведет два случайных слова на латыни.
```
now
----
Отображает текущую дату и/или время, используя формат соответственно переданной строке. Эта строка может содержать символы форматирования описанные в разделе о фильтре date.

Например:
```
It is {% now "jS F Y H:i" %}
```
Вы можете экранировать символ форматирования с помощью слэша и использовать его как строку. В этом примере, “o” и “f” экранированы, т.к. иначе они будут использованы как строки форматирования, отображающие год и время:
```
It is the {% now "jS \o\f F" %}
```
Этот пример выведет “It is the 4th of September”.

Переданный формат может быть одним из предопределенных DATE_FORMAT, DATETIME_FORMAT, SHORT_DATE_FORMAT или SHORT_DATETIME_FORMAT. Предопределенные форматы зависят от текущего языка и настройки Формат локализации, например:
```
It is {% now "SHORT_DATETIME_FORMAT" %}
```
Вы можете использовать синтаксис {% now "Y" as current_year %}, чтобы сохранить результат в переменной. Это может быть полезно при использовании {% now %} в теге blocktrans:
```
{% now "Y" as current_year %}
{% blocktrans %}Copyright {{ current_year }}{% endblocktrans %}
```
regroup
-------
Группирует объекты по общему атрибуту.

пример: 

cities является списком городов, представленным словарями с ключами "name", "population" и "country":
```
def home_page(request):
    my_dict = {'key':'My dikt Key'}
    my_object = Myobject()
    my_list = [1,2,3,4]
    categories = [{'id':0,'name':'Python'},{'id':1,'name':'Django'},{'id':2,'name':'Web'},{'id':4,'name':'Javascript'}]
    
    cities = [
    {'name': 'Mumbai', 'population': '19,000,000', 'country': 'India'},
    {'name': 'Calcutta', 'population': '15,000,000', 'country': 'India'},
    {'name': 'New York', 'population': '20,000,000', 'country': 'USA'},
    {'name': 'Chicago', 'population': '7,000,000', 'country': 'USA'},
    {'name': 'Tokyo', 'population': '33,000,000', 'country': 'Japan'},
    ]

    return render(request, 'home/home.html', {'first_name': 'Billi', 'last_name': 'Bons', 'my_dict':my_dict,'my_list':my_list,'my_object':my_object, 'name':'<script>alert("XSS");</script>','rowclass1':'border: red solid 7px;', 'rowclass2':'border: green solid 3px;','categories':categories,'cities':cities})

```
нужно отобразить список, отсортированный по стране:
```
India
Mumbai: 19,000,000
Calcutta: 15,000,000

USA
New York: 20,000,000
Chicago: 7,000,000

Japan
Tokyo: 33,000,000
```
использовать тег {% regroup %}, чтобы сгруппировать список городов по странам. 
------------------------------------------------------------------------------
```
{% regroup cities by country as country_list %}

<ul>
{% for country in country_list %}
    <li>{{ country.grouper }}
    <ul>
        {% for item in country.list %}
          <li>{{ item.name }}: {{ item.population }}</li>
        {% endfor %}
    </ul>
    </li>
{% endfor %}
</ul>
```
- {% regroup %} принимает три аргумента: список, который вы хотите перегруппировать; атрибут, по которому нужно сгруппировать, и название переменной с результатами. 

- {% regroup %} создает список (country_list) из групп объектов. Каждый объект группы содержит два атрибута:

1. grouper – значение, по которому происходила группировка (например, строка “Индия” или “Япония”).
2. list – список объектов в группе (например, список всех городов с country='India').

- {% regroup %} не сортирует переданный список! Если элементы списка cities не были бы отсортированы по country, перегруппировка отобразила бы несколько групп для одной страны. Например, список cities был таким (заметьте, что страны не сгруппированы вместе):
```
cities = [
    {'name': 'Mumbai', 'population': '19,000,000', 'country': 'India'},
    {'name': 'New York', 'population': '20,000,000', 'country': 'USA'},
    {'name': 'Calcutta', 'population': '15,000,000', 'country': 'India'},
    {'name': 'Chicago', 'population': '7,000,000', 'country': 'USA'},
    {'name': 'Tokyo', 'population': '33,000,000', 'country': 'Japan'},
]
```
В результате применения тега {% regroup %} для списка выше получим такой результат:
```
Индия
Мамбай: 19,000,000

США
Нью Йорк: 20,000,000

Индия
Калькутта: 15,000,000

США
Чикаго: 7,000,000

Япония
Токио: 33,000,000
```
способ отсортировать в шаблоне, используя фильтр dictsort:

```
{% regroup cities|dictsort:"country" by country as country_list %}
```
Группировка по другим свойствам
--------------------------------
Можно группировать объекты по методу, атрибуту, ключу словаря и списку объектов. Например, если “country” является внешним ключом на модель с атрибутом “description” :
```
{% regroup cities by country.description as country_list %}
```
spaceless
----------
Убирает пробелы между HTML тегами, включая символы табуляции и перенос строки.

Пример использования:
```
{% spaceless %}
    <p>
        <a href="foo/">Foo</a>
    </p>
{% endspaceless %}
```
Этот пример вернет такой HTML:
```
<p><a href="foo/">Foo</a></p>
```
Будут удалены пробелы только между тегами, и оставит между тегами и текстом. В этом примере пробелы вокруг Hello не будут удалены:
```
{% spaceless %}
    <strong>
        Hello
    </strong>
{% endspaceless %}
```
templatetag
-----------
Выводит один из символов, которые используются для определения тегов.

Так как система шаблонов не поддерживает “экранирование”, для отображения элементов синтаксиса необходимо использовать тег {% templatetag %}.

- openblock   {%
- closeblock  %}
- openvariable    {{
- closevariable   }}
- openbrace   {
- closebrace  }
- opencomment {#
- closecomment    #}

Примеры использования:
```
{% templatetag openblock %} url 'entry_list' {% templatetag closeblock %}
```
url
---
Возвращает абсолютную ссылку (URL без имени домена) соответствующую указанному представлению с необязательными аргументами. Любые спецсимволы будут экранированы с помощью функции iri_to_uri().

urls.py
-------
```
urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^req/', views.req_test, name='req_test'),

    url(r'^exampl1/', views.exampl1, name='some-url-name'),

    url(r'^admin/', admin.site.urls),
]

```
views.py
---------
```
def exampl1(request):
    return render(request, "home/exampl1.html", {})

```
home.html
----------
```
        <h2>url</h2>

        <a href="{% url 'some-url-name' %}">Example 1 </a>

```
Позиционные аргументы.
----------------------
Этот способ выводить ссылки без “хардкодинга” в шаблоне, чтобы не нарушать принцип DRY:
```
{% url 'some-url-name' v1 v2 %}
```
Первый аргумент – это путь к функции представления в формате package.package.module.function. Он может быть строкой в кавычках или любой другой контекстной переменной. Дополнительные аргументы необязательны. Это значения, разделенные пробелами, которые будут использоваться как аргументы при формировании URL.  

Также можно использовать именованные аргументы:
-----------------------------------------------
```
{% url 'some-url-name' arg1=v1 arg2=v2 %}
```
Нельзя использовать и позиционные и именованные аргументы в одном теге. Все обязательные аргументы URLconf должны быть указаны.

Например, мы имеем представление, views.article, чей URLconf принимает ID клиента (article() это метод в файле views.py). 
views.py
--------
```
def article(request,id):
    item = {'title':1,'content':id}    
    return render(request, "home/article.html", {'item':item})
```

urls.py:
--------
```
url(r'^article/([0-9]+)/$', views.article, name='app-views-article'),
```
example1.html
-------------
```
        <h3>Article</h3>
      
        <a href="{% url 'app-views-article' 1 %}">Article 1 </a>
```


Фильтры
========
Фильтры преобразуют переменные и аргументы тегов.

Могут выглядеть таким образом:
```
{{ django|title }}
```
Для контекста {'django': 'the web framework for perfectionists with deadlines'} этот шаблон выведет:

The Web Framework For Perfectionists With Deadlines

Некоторые фильтры принимают аргументы:
```
{{ my_date|date:"Y-m-d" }}
```

add
----
Суммирует аргумент и значение.
```
{{ value|add:"2" }}
```
Если value равно 4, будет выведено 6.

Фильтр попытается преобразовать оба значения в целое число. Если это не удастся, он будет пытаться добавить значения в любом случае. Это работает для некоторых типов (строки, списки и др.) и не работает с другими. Если ничего не получится, будет выведена пустая строка.

Например, у нас есть:
```
{{ first|add:second }}
```
и first равно [1, 2, 3] и second равно [4, 5, 6], тогда результат будет [1, 2, 3, 4, 5, 6].

Строки, которые могут быть преобразованы в числа, будут суммированы, а не объединены.
addslashes
----------
Добавляет слэш перед кавычкой. Удобно при экранировании строк в CSV, например.
```
{{ value|addslashes }}
```
Если value равно "I'm using Django", результат будет "I\'m using Django".

capfirst
--------
Первый символ аргумента возводит в верхний регистр. Если первый символ не буква, фильтр ничего не будет делать.
```
{{ value|capfirst }}
```
Если value равно "django", результат будет "Django".

center
--------
Центрирует значение в поле заданной ширины.
```
"{{ value|center:"15" }}"
```
Если value равно "django", результат будет "     Django    ".

cut
---
Удаляет значение аргумента из строки, к которой применяется фильтр.
```
{{ value|cut:" " }}
```
Если value равно "String with spaces", результат будет "Stringwithspaces".

date
-----
Форматирует дату в соответствии с указанным форматом.

Использует формат функции date() в PHP (http://php.net/date) с небольшими отличиями.

Доступное форматирование:
-------------------------
- a - 'a.m.' или 'p.m.' 
```
'a.m.'
```
- A   
'AM' или 'PM'.
```
'AM'
```
- b   
Название месяца, 3-х буквенное, в нижнем регистре.
```
'jan'
```
- c   
ISO 8601 формат. (в отличии от других форматов, таких как “Z”, “O” или “r”, формат “c” не добавит временную зону для относительного времени).
```
2008-01-02T10:30:00.000123+02:00, или 2008-01-02T10:30:00.000123 если время относительное
```
- d   
День месяца, 2 цифры с ведущим нулем.
```
От '01' до '31'
```
- D   
День недели, 3-х буквенное текстовое название.
```
'Fri'
```
- e   
Название временной зоны. Может быть в любом формате, или вернуть пустую строку в зависимости от объекта даты.
```
'', 'GMT', '-500', 'US/Eastern' и др.
```
- E   
Название месяца, зависит от текущего языка. Используется для отображения полного называния даты.
```
'listopada' (для польского языка, не 'Listopad')
```
- f   
Время, час в 12-часовом формате и минуты, минуты не отображаются если равны нулю. Собственное расширение.
```
'1', '1:30'
```
- F   
Название месяца, текстовое, длинное.
```
'January'
```
- g   
Час, 12-часовом формате без ведущих нулей.
```
От '1' до '12'
```
- G   
Час, 24-часовой формат
```
От '0' до '23'
```
- h   
Час, 12-часовой формат.
```
От '01' до '12'
```
- H   
Час, 24-часовой формат.
```
От '00' до '23'
```
- i   
Минуты.
```
От '00' до '59'
```
- I   
Летнее время (DST), не важно, используется оно или нет.
```
От '1' до '0'
```
- j   
День месяца без ведущего нуля.
```
От '1' до '31'
```
- l   
Название дня недели, текстовое, длинное.
```
'Friday'
```
- L   
Булево значение указывающее високосный ли год.
```
True или False
```
- m   
Месяц, 2-цифирный с ведущими нулями.
```
От '01' до '12'
```
- M   
Название месяца, текстовое, 3-х буквенное.
```
'Jan'
```
- n   
Номер месяца без ведущего нуля.
```
От '1' до '12'
```
- N   
Аббревиатура названия месяца в формате Associated Press.
```
'Jan.', 'Feb.', 'March', 'May'
```
- o   
week-numbering год в соответствии с ISO-8601
```
'1999'
```
- O   
Разница с временем по Гринвичу
```
'+0200'
```
- P   
Время, в 12-часовом формате, минуты и ‘a.m.’/’p.m.’, минуты упускаются если равны нулю, значения ‘midnight’ и ‘noon’ используются по возможности.
```
'1 a.m.', '1:30 p.m.', 'midnight', 'noon', '12:30 p.m.'
```
- r   
Дата в формате RFC 2822.
```
'Thu, 21 Dec 2000 16:01:07 +0200'
```
- s   
Секунды, 2-цифирный формат без ведущих нулей.
```
От '00' до '59'
```
- S   
Английский суффикс для дня месяца, 2 символа.
```
'st', 'nd', 'rd' или 'th'
```
- t   
Количество дней в месяце.
```
От 28 до 31
```
- T   
Часовой пояс сервера.
```
'EST', 'MDT'
```
- u   
микросекунды
```
От 000000 до 999999
```
- U   
Секунды с начала эпохи Unix (1 января 1970 00:00:00 UTC).
- w  
Номер дня недели, без ведущих нулей.
```
от '0' (воскресение) до '6' (суббота)
```
- W   
Норме недели в году в соответствии с ISO-8601, первая неделя начинается с понедельника.
```
1, 53
```
- y   
Год, 2 цифры.
```
'99'
```
- Y   
Год, 4 цифры.
```
'1999'
```
- z   
Номер дня в году.
```
От 0 до 365
```
- Z   
Смещения часового пояса в секундах. Для часового пояса западнее UTC значение будет отрицательным, для тех, что восточнее UTC – положительным.
```
От -43200 до 43200
```
Например:
```
{{ value|date:"D d M Y" }}
```
Если value равно объекту datetime (например, результат выполнения datetime.datetime.now()), будет выведено значение 'Wed 09 Jan 2008'.

Переданный формат может быть одним из предопределенных(DATE_FORMAT, DATETIME_FORMAT, SHORT_DATE_FORMAT или SHORT_DATETIME_FORMAT) или любой другой сформированный из символов форматирования из таблицы выше. Предопределенные форматы зависят от текущего языка и настройки Формат локализации, например:

Предположим что USE_L10N равно True и LANGUAGE_CODE равно "es", тогда:
```
{{ value|date:"SHORT_DATE_FORMAT" }}
```
результат вывода будет "09/01/2008" (формат "SHORT_DATE_FORMAT" для языка es указан в Django как "d/m/Y").

Если форматирование не указано:
```
{{ value|date }}
```
будет использовано значение из настройки DATE_FORMAT без учета текущего языка.

Вы можете использовать date с фильтром time, чтобы получить полное представление значения datetime. Например:
```
{{ value|date:"D d M Y" }} {{ value|time:"H:i" }}
```
default
--------
Если значение равно False, будет использовано значение по-умолчанию. В противном случае используется значение.

Например:
```
{{ value|default:"nothing" }}
```
Если value равно "" (пустая строка), будет выведено nothing.

default_if_none
---------------
Если (и только в этом случае) значение равно None, будет использовано значение по-умолчанию. В противном случае используется значение.

Например:
```
{{ value|default_if_none:"nothing" }}
```
Если value равно None, будет выведено "nothing".

dictsort
--------
Принимает список словарей и возвращает список, отсортированный по указанному ключу.

Например:
```
{{ value|dictsort:"name" }}
```
Если value равно:
```
[
    {'name': 'zed', 'age': 19},
    {'name': 'amy', 'age': 22},
    {'name': 'joe', 'age': 31},
]
```
будет возвращено:
```
[
    {'name': 'amy', 'age': 22},
    {'name': 'joe', 'age': 31},
    {'name': 'zed', 'age': 19},
]
```
Вы также можете делать более сложные вещи:
```
{% for book in books|dictsort:"author.age" %}
    * {{ book.title }} ({{ book.author.name }})
{% endfor %}
```
Если books равно:
```
[
    {'title': '1984', 'author': {'name': 'George', 'age': 45}},
    {'title': 'Timequake', 'author': {'name': 'Kurt', 'age': 75}},
    {'title': 'Alice', 'author': {'name': 'Lewis', 'age': 33}},
]
```
будет возвращено:
```
* Alice (Lewis)
* 1984 (George)
* Timequake (Kurt)
```
dictsortreversed
-----------------
Принимает список словарей и возвращает список отсортированный по указанному ключу в обратном порядке. 

divisibleby
-----------
Возвращает True, если значение делится на аргумент.

Например:
```
{{ value|divisibleby:"3" }}
```
Если value равно 21, будет возвращено True.

escape
------
Экранирует HTML. В частности выполняются такие замены:
```
< заменяется на &lt;

> заменяется на &gt;

' (одинарная кавычка) заменяется на &#39;

" (двойная кавычка) заменяется на &quot;

& заменяется на &amp;
```
Экранирование применяется к выводимой строке, и нет разницы где в цепочке фильтров будет добавлен escape: он всегда будет применяться так, как будто это последний фильтр. Если экранирование необходимо сразу применить, используйте фильтр force_escape.

Применение escape к переменной, которая уже была экранирована с помощью авто-экранирования, безопасно. Будет применено только одно экранирование. Так что безопасно использовать его с авто-экранированием. Если вам нужно применить экранирование несколько раз, используйте force_escape.

Например, escape можно использовать для экранирования, если autoescape выключен:
```
{% autoescape off %}
    {{ title|escape }}
{% endautoescape %}
```
escapejs
--------
Экранирует символы в строке, используемой в JavaScript. Это не делает строку безопасной для использования в HTML, но защищает от синтаксических ошибок при генерации JavaScript/JSON.

Например:
```
{{ value|escapejs }}
```
Если value равно 
```
"testing\r\njavascript \'string" <b>escaping</b>", 
```
будет выведено 
```
"testing\\u000D\\u000Ajavascript \\u0027string\\u0022 \\u003Cb\\u003Eescaping\\u003C/b\\u003E".
```
filesizeformat
--------------
Форматирует размер файла в читабельном формате (например, '13 KB', '4.1 MB', '102 bytes' и др.).

Например:
```
{{ value|filesizeformat }}
```
Если value равно 123456789, будет выведено 117.7 MB.

Размер файла и Международная система единиц
-------------------------------------------
filesizeformat не соответствует Международной системе единиц, которая рекомендует использовать кибибайт, мебибайт, гибибайт, и т.д. когда размеры байта вычислены в степени 1024 (данный случай). Вместо этого Django использует традиционные имена для единиц измерений (Кбайт, Мбайт, Гбайт, и т.д.) соответствующие именам, которые используются обычно.
first
------
Возвращает первый элемент списка.

Например:
```
{{ value|first }}
```
Если value равно ['a', 'b', 'c'], будет возвращено 'a'.

floatformat
------------
При использовании без аргументов, округляет число с плавающей запятой до одной десятой. Дробная часть отображается только, если существует. Например:
```
34.23234    {{ value|floatformat }} 34.2
34.00000    {{ value|floatformat }} 34
34.26000    {{ value|floatformat }} 34.3
```
Если используется целочисленный аргумент, floatformat округляет до указанного количества знаков после запятой. Например:

```
34.23234    {{ value|floatformat:3 }}   34.232
34.00000    {{ value|floatformat:3 }}   34.000
34.26000    {{ value|floatformat:3 }}   34.260
```
Особенно полезный передавать 0 (нуль) как параметр, который будет округлять значение с плавающей точкой к ближайшему целому.

```
34.23234    {{ value|floatformat:"0" }} 34
34.00000    {{ value|floatformat:"0" }} 34
39.56000    {{ value|floatformat:"0" }} 40
```
Если аргумент отрицательный, floatformat округляет до указанного количества знаков после запятой – но дробная часть отображается только если существует. Например:

```
34.23234    {{ value|floatformat:"-3" }}    34.232
34.00000    {{ value|floatformat:"-3" }}    34
34.26000    {{ value|floatformat:"-3" }}    34.260
```
Использование floatformat без аргументов эквивалентно floatformat с -1.

force_escape
------------
Применяет экранирование HTML к строке. Это фильтр применяется сразу и возвращает новую экранированную строку. Это полезно в редких случаях, если вам необходимо применить экранирование несколько раз, или если необходимо применить другие фильтры в экранированной строке.

например, если вы хотите экранировать тег p созданный фильтром linebreaks:
```
{% autoescape off %}
    {{ body|linebreaks|force_escape }}
{% endautoescape %}
```
get_digit
----------
Принимает число и возвращает запрашиваемую цифру, где 1 самая правая цифра, 2 - вторая справа, и тд. Возвращает оригинальное значение, если оно не верно (не число или меньше 1). В противном случае, всегда выводится целое число.

Например:
```
{{ value|get_digit:"2" }}
```
Если value равно 123456789, будет выведено 8.

iriencode
---------
Конвертирует IRI (Internationalized Resource Identifier) в строку, которая может быть использована в URL. Это необходимо, если вы хотите использовать не ASCII символы в URL.

Можно использовать этот фильтр после использования фильтра urlencode.

Например:
```
{{ value|iriencode }}
```
Если value равно "?test=1&me=2", вывод будет "?test=1&amp;me=2".

join
-----
Объединяет список, используя указанную строку, аналог str.join(list) в Python

Например:
```
{{ value|join:" // " }}
```
Если value равно списку ['a', 'b', 'c'], вывод будет "a // b // c".

last
-----
Возвращает последний элемент списка.

Например:
```
{{ value|last }}
```
Если value равно ['a', 'b', 'c', 'd'], выведет "d".

length
-------
Возвращает размер значения. Работает для строк и списков.

Например:
```
{{ value|length }}
```
Если value равно ['a', 'b', 'c', 'd'] или "abcd", выведет 4.

length_is
----------
Возвращает True, если размер значения равен аргументу, и False в противном случае.

Например:
```
{{ value|length_is:"4" }}
```
Если value равно ['a', 'b', 'c', 'd'] или "abcd", вернет True.

linebreaks
-----------
Заменяет переносы строки аналогами из HTML; один перенос строки будет заменен на br, новая строка с предыдущей пустой строкой оборачиваются в тег p.

Например:
```
{{ value|linebreaks }}
```
Если value равно Joel\nis a slug, вывод будет 
```
<p>Joel<br />is a slug</p>.
```
linebreaksbr
------------
Заменяет все переносы строки на br.

Например:
```
{{ value|linebreaksbr }}
```
Если value равно Joel\nis a slug, вывод будет 
```
Joel<br />is a slug.
```
linenumbers
------------
Отображает текст с номерами строк.

Например:
```
{{ value|linenumbers }}
```
Если value равно:
```
one
two
three
```
вернет:
```
1. one
2. two
3. three
```
ljust
------
Выравнивает значение влево в поле указанной ширины.

Аргумент: размер поля

Например:
```
"{{ value|ljust:"10" }}"
```
Если value равно Django, выведет "Django    ".

lower
------
Конвертирует строку в нижний регистр.

Например:
```
{{ value|lower }}
```
Если value равно Still MAD At Yoko, выведет still mad at yoko.

make_list
----------
Превращает значение в список. Для строк это будет список символов. Число сначала конвертируется в unicode, а потом в список.

Например:
```
{{ value|make_list }}
```
Если value равно строке "Joel", будет возвращен список ['J', 'o', 'e', 'l']. Если value равно 123, вернет список ['1', '2', '3'].

phone2numeric
--------------
Преобразует телефонный номер (возможно, содержащий буквы) в его числовой эквивалент.

Значение не должно быть правильным телефонным номером, будет преобразована любая строка.

Например:
```
{{ value|phone2numeric }}
```
Если value равно 800-COLLECT, выведет 800-2655328.

pluralize
---------
Возвращает суффикс множественного числа, если значение не 1. По умолчанию использует суффикс 's'.

Например:
```
You have {{ num_messages }} message{{ num_messages|pluralize }}.
```
Если num_messages равно 1, выведет You have 1 message. Если num_messages равно 2 выведет You have 2 messages.

Для слов, которые используют суффикс отличный от 's', вы можете указать его как аргумент.

Например:
```
You have {{ num_walruses }} walrus{{ num_walruses|pluralize:"es" }}.
```
Для слов, которые не преобразуются в множественную форму добавлением суффикса, вы можете указать как одинарный так и множественный суффиксы, разделенные запятыми.

Например:
```
You have {{ num_cherries }} cherr{{ num_cherries|pluralize:"y,ies" }}.
```
Используйте blocktrans для переводимых строк.
pprint
-------
“Обёртка” для pprint.pprint() – используется для отладки.

random
-------
Возвращает случайный элемент из списка.

Например:
```
{{ value|random }}
```
Если value равно ['a', 'b', 'c', 'd'], вернет "b".

rjust
-----
Выравнивает значение вправо в поле указанной ширины.

Аргумент: размер поля

Например:
```
"{{ value|rjust:"10" }}"
```
Если value равно Django, вернет "    Django".

safe
-----
Помечает строку, как не требующую последующего HTML экранирования. Если авто-экранирование отключено, этот фильтр ничего не изменит.

Если вы используете цепочку фильтров, фильтр примененный после safe может снова сделать переменную не безопасной. Например, следующий код выведет переменную без экранирования:
```
{{ var|safe|escape }}
```
safeseq
-------
Применяет фильтр safe к каждому элементу последовательности. Полезно применять с другими тегами, работающими с последовательностями, такими как join. Например:
```
{{ some_list|safeseq|join:", " }}
```
Вы не можете использовать фильтр safe в таком случае, так как он сначала преобразует значение в строку.

slice
------
Возвращает срез списка.

Используйте синтаксис срезов Python. Смотрите http://www.diveintopython3.net/native-datatypes.html#slicinglists.

Например:
```
{{ some_list|slice:":2" }}
```
Если some_list равно ['a', 'b', 'c'], вернет ['a', 'b'].

slugify
-------
Конвертирует в ASCII. Преобразует пробелы в дефисы. Удаляет нетекстовые символы (все кроме букв, цифр, дефиса и символа подчеркивания). Удаляет пробелы в начале и в конце строки.

Например:
```
{{ value|slugify }}
```
Если value равно "Joel is a slug", вернет "joel-is-a-slug".

stringformat
------------
Форматирует значение в соответствии с аргументом, который является спецификатором форматирования строк. Спецификатор использует синтаксис форматирования строк Python, с той лишь разницей, что ведущий символ “%” опущен.

Например:
```
{{ value|stringformat:"E" }}
```
Если value равно 10, будет выведено 1.000000E+01.

striptags
----------
Пытается удалить все [X]HTML теги.

Например:
```
{{ value|striptags }}
```
Если value равно 
```
"<b>Joel</b> <button>is</button>
 a 
 <span>slug</span>"
```
выведет "Joel is a slug".

time
----
Форматирует время в соответствии с указанным форматом.

Можно использовать предопределенный TIME_FORMAT, или собственный формат аналогичный формату описанному в date. Заметим, что предопределенный формат зависит от текущего языка.

Например:
```
{{ value|time:"H:i" }}
```
Если value равно datetime.datetime.now(), может вернуть "01:23".

Другой пример:

Предположим USE_L10N равно True и LANGUAGE_CODE равно "de", тогда:
```
{{ value|time:"TIME_FORMAT" }}
```
будет возвращена строка "01:23:00" (формат "TIME_FORMAT" для языка de определен в Django как "H:i:s").

Фильтр time принимает только строку формата, который относится к времени, а не дате (по понятным причинам). Если вам нужно отформатировать дату, используйте фильтр date (или вместе с time, если необходимо вывести полное значение datetime).

Есть одно исключение: если передано значение datetime с указанным часовым поясом (time-zone-aware datetime объект) фильтр time принимает параметры форматирования для часового пояса, такие как 'e', 'O' , 'T' и 'Z'.

Если форматирование не указано:
```
{{ value|time }}
```
будет использовано значение из настройки TIME_FORMAT без учета текущего языка.

timesince
---------
Форматирует дату как время прошедшее с момента другой даты (например, “4 days, 6 hours”).

Принимает необязательный аргумент – дату, используемую как точку отсчета (без аргументов используется текущее время). Например, если blog_date это дата, равная полночи 1 июня 2006, и comment_date равен 08:00, 1 июня 2006, тогда следующий код вернет “8 часов”:
```
{{ blog_date|timesince:comment_date }}
```
Сравнение абсолютной(с временной зоной) и относительной(без временной зоны) дат вернет пустую строку.

Минута - самая малая единица измерения, и для дат из будущего, относительно точки сравнения, возвращается “0 минут” .

timeuntil
---------
Аналогичен timesince, только определяет время от текущей даты до указанной. Например, если сегодня 1 июня 2006 и conference_date это дата 29 июня 2006, тогда {{ conference_date|timeuntil }} вернет “4 недели”.

Принимает необязательный аргумент – дату, используемую как точку отсчета (вместо текущего времени). Если from_date содержит 22 июня 2006, тогда следующий код вернёт “1 неделя”:
```
{{ conference_date|timeuntil:from_date }}
```
Сравнение абсолютной(с временной зоной) и относительной(без временной зоны) дат вернет пустую строку.

Минута - самая малая единица измерения, и для дат из прошлого, относительно точки сравнения, возвращается “0 минут” .

title
------
Преобразует первый символ слов в верхний регистр, остальные в нижний.
```
{{ value|title }}
```
Если value равно "my FIRST post", вернет "My First Post".

truncatechars
--------------
Обрезает строку до указанной длины. Обрезанная строка будет оканчиваться троеточием(”...”).

Аргумент: длина строки в символах

```
{{ value|truncatechars:9 }}
```
Если value равно "Joel is a slug", вернет "Joel i...".

truncatechars_html
-------------------
Аналогичен truncatechars, но учитывает наличие HTML-тегов. Теги, которые остались открыты в строке после обрезания, будут немедленно закрыты.

```
{{ value|truncatechars_html:9 }}
```
Если value равно 
```
"<p>Joel is a slug</p>"
```
вернет 
```
"<p>Joel i...</p>".
```
Символы новой строки в содержимом будут сохранены.

truncatewords
--------------
Обрезает строку после указанного количества слов.

Аргумент: количество слов в строке

```
{{ value|truncatewords:2 }}
```
Если value равно "Joel is a slug", вернет "Joel is ...".

Переносы строки будут удалены.

truncatewords_html
-------------------
Аналогичен truncatewords, но учитывает наличие HTML-тегов. Теги, которые остались открыты в строке после обрезания, будут немедленно закрыты.

Этот фильтр менее эффективен, чем truncatewords, используйте его только с HTML-текстом.

```
{{ value|truncatewords_html:2 }}
```
Если value равно 
```
"<p>Joel is a slug</p>"
```
вернет 
```
"<p>Joel is ...</p>".
```
Символы новой строки в содержимом будут сохранены.

upper
------
Конвертирует строку в верхний регистр

```
{{ value|upper }}
```
Если value равно "Joel is a slug", будет возвращено "JOEL IS A SLUG".

urlencode
----------
Экранирует значение для безопасного использования в URL.

```
{{ value|urlencode }}
```
Если value равно "http://www.example.org/foo?a=b&c=d", будет возвращено "http%3A//www.example.org/foo%3Fa%3Db%26c%3Dd".

Используй необязательный аргумент, можно указать символы, который не должны быть экранированы.

Если аргумент не указан, символ ‘/’ предполагается как безопасный символ. Если необходимо экранировать все символы, передайте пустую строку. Например:
```
{{ value|urlencode:"" }}
```
Если value равно "http://www.example.org/", будет возвращено "http%3A%2F%2Fwww.example.org%2F".

urlize
------
Конвертирует URL-ы и email-ы в тексте в “кликабельные” ссылки.

Этот тег конвертирует ссылки с префиксами http://, https://, или www.. Например, http://goo.gl/aia1t будет конвертирован, goo.gl/aia1t – нет.

Поддерживаются ссылки состоящие только из домена и заканчивающиеся на один из первоначальных доменов первого уровня (.com, .edu, .gov, .int, .mil, .net, and .org). Например, djangoproject.com будет преобразован.

Ссылки могут быть с завершающей пунктуацией (точка, запятая, закрывающая скобка) и предшествующей пунктуацией (открывающая скобка), urlize все корректно преобразует.

Ссылки, созданные urlize содержат атрибут rel="nofollow".

Например:
```
{{ value|urlize }}
```
Если value равно "Check out www.djangoproject.com", будет выведено 
```
"Check out <a href="http://www.djangoproject.com" rel="nofollow">www.djangoproject.com</a>".
```
В дополнение к обычным ссылкам, urlize также преобразует email-ы в ссылки с mailto:. 
Если value содержит "Send questions to foo@example.com", результат будет 
```
"Send questions to <a href="mailto:foo@example.com">foo@example.com</a>".
```
Фильтр urlize принимает необязательный аргумент autoescape. Если autoescape равен True, текст ссылки и URL будут экранированы с помощью фильтра escape. Значение по-умолчанию для autoescape равно True.

urlizetrunc
------------
Преобразует URL-ы в ссылки как и urlize, но обрезает название ссылок длиннее указанного предела.

Аргумент: Максимальное количество символов в названии ссылки, включая многоточие, добавленное при обрезании текста.

Например:
```
{{ value|urlizetrunc:15 }}
```
Если value равно "Check out www.djangoproject.com", вернет 
```
'Check out <a href="http://www.djangoproject.com" rel="nofollow">www.djangopr...</a>'.
```
Как и urlize, фильтр следует применять к обычному тексту.

wordcount
-----------
Возвращает количество слов.

Например:
```
{{ value|wordcount }}
```
Если value равно "Joel is a slug", вернет 4.

wordwrap
---------
“Оборачивает” слова до указанной длины строки.

Аргумент: количество символов в строке

Например:
```
{{ value|wordwrap:5 }}
```
Если value равно Joel is a slug, вернет:
```
Joel
is a
slug
```
yesno
------
Для true, false и (опционально) None выводит строки “yes”, “no”, “maybe”, или другие, переданные как список значений, разделенный запятыми:

Например:
```
{{ value|yesno:"yeah,no,maybe" }}
```
```
True        yes
True    "yeah,no,maybe" yeah
False   "yeah,no,maybe" no
None    "yeah,no,maybe" maybe
None    "yeah,no"   
"no" (конвертирует None в False, если значение для None не указано)
```

тег filter
----------
Содержимое тега будет обработано указанными фильтрами. Можно указать цепочку фильтров, а также их аргументы, как и при выводе переменной в шаблоне.

Содержимое тега включает весь текст между filter и endfilter.

Пример:
```
{% filter force_escape|lower %}
    This text will be HTML-escaped, and will appear in all lowercase.
{% endfilter %}
```
Нельзя передавать фильтры escape и safe. Вместо этого используйте тег autoescape.

Шаблон
=======
include
--------
Загружает шаблон и выводит его с текущим контекстом. Это способ “включить” один шаблон в другой.

Названия шаблона можно указать переменной или строкой в одинарных или двойных кавычках.

Это пример включает содержимое шаблона "foo/bar.html":
```
{% include "foo/bar.html" %}
```
Этот пример включает содержимое шаблона, чье имя содержится в переменной template_name:
```
{% include template_name %}
```
Можно передать любой объект с методом render(), который принимает контекст. Это позволяет указать скомпилированные объекты Template из контекста.

Включенный шаблон выполняется с контекстом шаблона, который его включает. Этот пример выводит "Hello, John":

Контекст: переменная person равна "john".

Шаблон:
```
{% include "name_snippet.html" %}
```
Шаблон name_snippet.html:
```
{{ greeting }}, {{ person|default:"friend" }}!
```
Вы можете передать дополнительные переменные контекста в шаблон используя именованные аргументы:
```
{% include "name_snippet.html" with person="Jane" greeting="Hello" %}
```
Если вы хотите выполнить шаблон используя только указанные переменные в контексте (или не используя переменные совсем), добавите параметр only. Другие переменные не будут доступны в включаемом шаблоне:
```
{% include "name_snippet.html" with greeting="Hi" only %}
```
Тег include должен восприниматься как “выполним этот под-шаблон и включим полученный HTML”, а не “парсим этот под-шаблон и включаем его как часть родительского”. Это означает, что нет никакого общего состояния между включенными шаблонами – каждое включение это полностью независимый процесс.

Блоки выполняются перед включение шаблона. Это означает, что шаблон включает уже выполненные и отрендеренные блоки - вы не можете переопределить эти блоки, как это делается при наследовании шаблонов.

Наследование шаблонов
======================
Наследование шаблонов позволяет создать шаблон-“скелет”, который содержит базовые элементы  сайта и определяет блоки, которые могут быть переопределены дочерними шаблонами.

block
------
Определяет блок, который может быть переопределен в дочернем шаблоне. 

пример base.html:
-----------------
```
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css" />
    <title>{% block title %}My amazing site{% endblock %}</title>
</head>

<body>
    <div id="sidebar">
        {% block sidebar %}
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        {% endblock %}
    </div>

    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```
Этот шаблон определяет HTML структуру документа, которую вы можете использовать для двух-колоночной страницы. Задача “дочернего” шаблона заполнить пустые блоки содержимым.

В этом примере, тег block определяет три блока, которые может переопределить дочерний шаблон. Все что делает тег block – указывает механизму шаблонов, какая часть шаблона может быть переопределена в дочернем шаблоне.

extends
-------
Указывает что данный шаблон наследуется от родительского.

Может использоваться двумя способами:

1. {% extends "base.html" %} (с кавычками) использует буквальное значение "base.html" в качестве названия родительского шаблона.

2. {% extends variable %} использует значение variable. Если значение строка, Django использует ее как название родительского шаблона. Если значение переменной объект Template, Django использует этот объект как родительский шаблон.

Дочерний шаблон может выглядеть таким образом:
```
{% extends "base.html" %}

{% block title %}My amazing blog{% endblock %}

{% block content %}
{% for entry in blog_entries %}
    <h2>{{ entry.title }}</h2>
    <p>{{ entry.body }}</p>
{% endfor %}
{% endblock %}
```
тег extends говорит механизму шаблонов, что этот шаблон “наследует” другой шаблон. Когда механизм шаблонов выполняет этот шаблон, первым делом находится родительский шаблон – “base.html”.

Далее механизм шаблонов находит три тега block в base.html и заменяет их содержимым дочернего шаблона. В зависимости от значения blog_entries, результат может выглядеть таким образом:
```
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css" />
    <title>My amazing blog</title>
</head>

<body>
    <div id="sidebar">
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
    </div>

    <div id="content">
        <h2>Entry one</h2>
        <p>This is my first entry.</p>

        <h2>Entry two</h2>
        <p>This is my second entry.</p>
    </div>
</body>
</html>
```
Так как дочерний шаблон не определяет блок sidebar, будет использовано значение из родительского шаблона. Содержимое тега {% block %} родительского шаблона всегда используется как значение по умолчанию.

Один из распространенных способов использовать наследование – это трехуровневый подход:

1. Создать шаблон base.html, который отображает основной вид вашего сайта.

2. Создать шаблон base_SECTIONNAME.html для каждого “раздела” вашего сайта. Например, base_news.html, base_sports.html. Все эти шаблоны наследуют base.html и включают стили и дизайн специфические для конкретного раздела.

3. Создание шаблона для каждого типа страницы, такие как новость или запись в блоге. Эти шаблоны наследуют соответствующий шаблон раздела.

Такой подход позволяет максимально использовать существующий код и легко добавлять элементы, такие как элементы навигации специфические для каждого раздела, в общие блоки шаблона.

- Если вы используете {% extends %}, он должен быть первым тегом в шаблоне. Иначе наследование не будет работать.

- Чем больше тегов {% block %} в вашем шаблоне, тем лучше. Помните, дочерний шаблон не обязан определять все блоки родительского, вы можете указать значение по умолчанию для всех блоков, а затем определить в дочернем шаблоне только те, которые необходимы. Лучше иметь больше “hooks”, чем меньше “hooks”.

- Если вы дублируете содержимое в нескольких шаблонах, возможно вы должны перенести его в тег {% block %} родительского шаблона.

- Если вам необходимо содержимое блока родительского шаблона, используйте переменную {{ block.super }}. Эта полезно, если вам необходимо дополнить содержимое родительского блока, а не полностью переопределить его. Содержимое {{ block.super }} не будет автоматически экранировано, так как оно уже было экранировано, при необходимости, в родительском шаблоне.

Для ясности, вы можете добавить название вашему тегу {% endblock %}. Например:
```
{% block content %}
...
{% endblock content %}
```
В больших шаблонах такой подход поможет вам увидеть какой тег {% block %} был закрыт.

Вы не можете определить несколько тегов block с одним названием в одном шаблоне. Такое ограничение существует потому, что тег block работает в “оба” направления. block не просто предоставляет “полость” в шаблоне – он определяет содержимое, которое заполняет “полость” в родительском шаблоне. Если бы было несколько тегов block с одним названием, родительский шаблон не знал содержимое какого блока использовать.

Автоматическое экранирование HTML
----------------------------------
Создавая HTML используя шаблон, есть риск, что переменная может содержать символы, которые повлияют на структуру полученного HTML. Например, рассмотрим такой фрагмент:
```
Hello, {{ name }}
```
что произойдет, если пользователь выбрал такое имя:
```
<script>alert('hello')</script>
```
С таким именем шаблон вернет:
```
Hello, <script>alert('hello')</script>
```
что приведет к отображению alert-окна JavaScript!

Аналогично, что если имя содержит символ '<'?
```
<b>username
```
Шаблон вернет такое содержимое:
```
Hello, <b>username
```
в результате оставшееся содержимое страницы будет выделено полужирным!

Очевидно, пользовательским данными нельзя слепо доверять и вставлять непосредственно в содержимое страницы, так как злоумышленники могут использовать это с плохими намерениями. Такой тип уязвимости называется Cross Site Scripting (XSS) атакой.

Чтобы избежать этой проблемы, у вас есть два варианта:

1. Первый, вы можете применять ко всем сомнительным переменным фильтр escape, который преобразует потенциально опасные HTML символы в безопасные. 

2. Второй, вы можете позволить Django автоматически экранировать HTML. 

По-умолчанию в Django, каждый шаблон экранирует все переменные. В частности выполняются такие замены:
```
< заменяется на &lt;

> заменяется на &gt;

' (одинарная кавычка) заменяется на &#39;

" (двойная кавычка) заменяется на &quot;

& заменяется на &amp;
```
такое поведение используется по умолчанию. 
------------------------------------------

Если вы не хотите, чтобы данные автоматически экранировались, на уровне сайта, шаблона или одной переменной, вы можете отключить это несколькими способами.

Зачем вам отключить экранирование? Потому что в некоторых ситуациях, вы намеренно добавляете HTML в переменную, и хотите, чтобы он выводился без экранирования. Например, вы можете хранить HTML в базе данных и хотите непосредственно вставить его в содержимое страницы. Или шаблоны Django используются для создания текста, который не является HTML – например email.

Для отдельных переменных
-------------------------
Для отключения авто-экранирования для отдельных переменных, используйте фильтр safe:
```
This will be escaped: {{ data }}
This will not be escaped: {{ data|safe }}
```

если data содержит 'b', будет выведено:
```
This will be escaped: &lt;b&gt;
This will not be escaped: <b>
```
Для блоков шаблона
------------------
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
```
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
```
Так как авто-экранирование отключено в базовом шаблоне, оно будет отключено и в дочернем шаблоне. 
Если переменная greeting равна 
```
<b>Hello!</b>
```
будет выведено:
```
<h1>This &amp; that</h1>
<b>Hello!</b>
```
Если вы создаете шаблон, который может использовать как с включенным авто-экранированием так и без него, добавляйте фильтр escape для каждой переменной, которую нужно экранировать. При включенном авто-экранировании фильтр escape не выполнит замену символов повторно.

Строки и автоматическое экранирование
--------------------------------------
аргументом фильтра может быть строка:
```
{{ data|default:"This is a string literal." }}
```
Все строки в шаблоне вставляются без автоматического экранирования – они обрабатываются как строки, к которым применили фильтр safe. Причина этого состоит в том, что автор шаблона контролирует содержимое этих строк и самостоятельно может убедиться при создании шаблона, что они не содержат не безопасных символов.

Это означает, чтобы вы должны писать:
```
{{ data|default:"3 &lt; 2" }}
```
вместо:
```
{{ data|default:"3 < 2" }}  {# Bad! Don't do this. #}
```
Это правило не распространяется на переменные, которые используются в качестве аргументов, так как автор шаблоне не может контролировать содержимое этих переменных.

Blog
====
```
./manage.py startapp blog
```
Настройка базы данных
======================
mysite/settings.py. 
-------------------
```
# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

```
По умолчанию используется SQLite. SQLite включен в Python, так что вам не нужно устанавливать что либо еще. 

Модели
=======
Модели отображают информацию о данных, с которыми вы работаете. Они содержат поля и поведение ваших данных. Обычно одна модель представляет одну таблицу в базе данных.

Каждая модель это класс унаследованный от django.db.models.Model.
```
from django.db import models
```
Атрибут модели представляет поле в базе данных.

```
class Category(models.Model):
    name = models.CharField('categories name', max_length=100)
    
    description = models.TextField(max_length=4096)
        
    views_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name
```

name,description,views_count - поля модели. Каждое поле определено как атрибут класса (представлено экземпляром класса Field), и каждый атрибут соответствует полю таблицы в базе данных.

CharField для текстовых полей и DateTimeField для полей даты и времени. Это указывает Django какие типы данных хранят эти поля.

Названия каждого экземпляра Field - это название поля, в “машинном”(machine-friendly) формате. Вы будете использовать эти названия в коде, а база данных будет использовать их как названия колонок.

Вы можете использовать первый необязательный аргумент конструктора класса Field, чтобы определить отображаемое, удобное для восприятия, название поля. Оно используется в некоторых компонентах Django, и полезно для документирования. Если это название не указано, Django будет использовать “машинное” название. В этом примере, мы указали отображаемое название только для поля name - 'categories name'. Для всех других полей будет использоваться “машинное” название.

Некоторые классы, унаследованные от Field, имеют обязательные аргументы. Например, CharField требует, чтобы вы передали ему max_length. Это используется не только в схеме базы данных, но и при валидации.

Field может принимать различные необязательные аргументы; в нашем примере мы указали default значение для views_count равное 0.

Активация моделей
=================
- Создать структуру базы данных (CREATE TABLE) для приложения.

- Создать Python API для доступа к данным объектов Category.

Но первым делом мы должны указать нашему проекту, что приложение blog установлено.

Приложения Django “подключаемые”: вы можете использовать приложение в нескольких проектах и вы можете распространять приложение, так как они не связаны с конкретным проектом Django.

Отредактируйте файл mysite/settings.py и измените настройку INSTALLED_APPS добавив строку 'blog':

mysite/settings.py
-------------------
```
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'blog',
)
```
Теперь Django знает, что необходимо использовать приложение blog. 

INSTALLED_APPS
--------------
По умолчанию: () (Пустой кортеж)

Кортеж строк, который указывают все приложения Django, используемые в проекте. Каждая строка должна быть полным Python путем к:

- классу настройки приложения, или
- пакету с приложением.

INSTALLED_APPS теперь поддерживает конфигурации приложений.

- Названия приложения и метки(labels) должны быть уникальны в INSTALLED_APPS
- Названия приложений — Python путь к пакету приложения — должны быть уникальны. Нельзя подключить одно приложение дважды, разве что продублировав код с другим названием.

Короткие названия приложения — по умолчанию последняя часть названия приложения — должны быть так же уникальны. Например, можно использовать вместе django.contrib.auth и myproject.auth. Однако, необходимо указать label.

Эти правила распространяются на все приложения в INSTALLED_APPS, как на классы настройки приложений, так и на пакеты приложений.
Если несколько приложений содержат разные версии одних и тех же ресурсов (шаблоны, статические файлы, команды, файлы перевода), будут использоваться ресурсы из приложения, которое указано выше в INSTALLED_APPS.

Поля
====
Самая важная часть модели – и единственная обязательная – это список полей таблицы базы данных которые она представляет. Поля определены атрибутами класса. Нельзя использовать имена конфликтующие с API моделей, такие как clean, save или delete.

```
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=4096)

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    status = models.IntegerField(default=0)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
```

Типы полей
===========
Каждое поле в модели должно быть экземпляром соответствующего Field класса. Django использует классы полей для определения такой информации:

- Типа колонки в базе данных (например: INTEGER, VARCHAR).

- Виджет используемый при создании поля формы (например: input type="text", select).

- Минимальные правила проверки данных, используемые в интерфейсе администратора и для автоматического создания формы.

Настройка полей
===============
Для каждого поля есть набор предопределенных аргументов. Например, CharField (и унаследованные от него) имеют обязательный аргумент max_length, который определяет размер поля VARCHAR для хранения данных этого поля.

Также есть список стандартных аргументов для всех полей. Все они не обязательны.

null
-----
Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.

blank
------
Если True, поле не обязательно и может быть пустым. По умолчанию - False.

Это не то же что и null. null относится к базе данных, blank - к проверке данных. Если поле содержит blank=True, форма позволит передать пустое значение. При blank=False - поле обязательно.

# help_text
Поля моделей в Django принимают атрибут help_text, который используется в Django формах/админке для вывода назначения полей  — это служит отличной возможностью для документации ваших моделей. Если в дальнейшем вы пригласите нового разработчика в проект, то help_text позволит сохранить бесчисленное количество часов на объяснения структуры моделей.

Подсказка, отображаемая в поле формы. 
при отображении в форме, HTML-символы не экранируются. Это позволяет использовать HTML в help_text если вам необходимо. Например:
```
help_text="Please use the following format: <em>YYYY-MM-DD</em>."
```
Также вы можете использовать обычный текст и django.utils.html.escape(), чтобы экранировать HTML. Убедитесь, что вы экранируете все подсказки, которые могут определять непроверенные пользователи, чтобы избежать XSS атак.

# primary_key

При True поле будет первичным ключом.

Если primary_key=True не указан ни для одного поля, Django самостоятельно добавит поле типа IntegerField для хранения первичного ключа, поэтому вам не обязательно указывать primary_key=True для каждой модели. 

Поле первичного ключа доступно только для чтения. Если вы поменяете значение первичного ключа для существующего объекта, а затем сохраните его, будет создан новый объект рядом с существующим. 
Например:
```
from django.db import models

class Fruit(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
>>> fruit = Fruit.objects.create(name='Apple')
>>> fruit.name = 'Pear'
>>> fruit.save()
>>> Fruit.objects.values_list('name', flat=True)
['Apple', 'Pear']
unique
```
При True поле будет уникальным.

# краткое описание самых используемых аргументов.

## Первичный ключ по умолчанию
По умолчанию Django для каждой модели добавляет такое поле:
```
id = models.AutoField(primary_key=True)
```
Это автоинкрементный первичный ключ.

Для его переопределения просто укажите primary_key=True для одного из полей. При этом Django не добавит поле id.

Каждая модель должна иметь хотя бы одно поле с primary_key=True (явно указанное или созданное автоматически).

primary_key=True подразумевает null=False и unique=True. Модель может содержать только один первичный ключ.

# verbose_name
Field.verbose_name

## Читабельное имя поля
Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField, первым аргументом принимает необязательное читабельное название. Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
```
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    description = models.TextField(max_length=4096)
```
# default
Field.default
Значение по умолчанию для поля. Это может быть значение или вызываемый(callable) объект. Если это вызываемый объект, он будет вызван при создании нового объекта.

Значение по умолчанию не может быть изменяемым значением (экземпляр модели, список, множество и т.д.), т.к. все объекты модели будут ссылаться на этот объект и использовать его как значение по умолчанию. Вместо этого укажите функцию, которая возвращает нужное значение. Например, если у вас есть собственное поле JSONField и вы хотите указать словарь как значение по умолчанию, используйте следующую функцию:
```
def contact_default():
    return {"email": "to1@example.com"}

contact_info = JSONField("ContactInfo", default=contact_default)
```
Обратите внимание, lambda нельзя использовать в качестве значения для default т.к. она не может быть сериализована для миграций.

Значение по умолчанию используется, если был создан экземпляр модели, а значение для поля не было указано. Если поле является первичным ключом, значение по умолчанию также использует и при указании None.


# unique
Field.unique
При True значение поля должно быть уникальным.

Этот параметр учитывается при сохранении в базу данных и при проверке данных в модели. Если вы попытаетесь сохранить повторное значение в поле с unique, будет вызвана ошибка django.db.IntegrityError методом save().

Этот параметр можно использовать для любого типа поля кроме ManyToManyField, OneToOneField и FileField.

Заметим что, при unique равном True, не нужно указывать db_index, т.к. unique создает индекс.

# Типы полей

## AutoField
class AutoField(**options)
Автоинкрементное поле IntegerField. Используется для хранения ID. Скорее всего вам не придется использовать это поле, первичный ключ будет автоматически добавлен к модели.

## BigIntegerField
class BigIntegerField([**options])
64-битное целочисленное, аналогично IntegerField но позволяет хранить числа от -9223372036854775808 до 9223372036854775807. Форма будет использовать TextInput для отображения.

## BooleanField
class BooleanField(**options)
Поле хранящее значение true/false.

Виджет по умолчанию для этого поля CheckboxInput.

Если вам нужен параметр null, используйте поле NullBooleanField.

по умолчанию для BooleanField None, если Field.default не указан.

## CharField
class CharField(max_length=None[, **options])
Строковое поле для хранения коротких или длинных строк.

Для большого количества текстовой информации используйте TextField.

Виджет по умолчанию для этого поля TextInput.

CharField принимает один дополнительный аргумент:

### CharField.max_length
Максимальная длинна(в символах) этого поля. max_length используется для проверки данных на уровне базы данных и форм Django.

Если вы создаете независимое приложение, которое должно работать на различных базах данных, помните что существуют некоторые ограничения использования max_length для некоторых типов баз данных. 
#### Пользователям MySQL
Если вы используете это поле с MySQLdb 1.2.2 и utf8_bin “collation” (которое не является значением по умолчанию), могут быть некоторые проблемы.

## DateField
class DateField([auto_now=False, auto_now_add=False, **options])
Дата, представленная в виде объекта datetime.date Python. Принимает несколько дополнительных параметров:

### DateField.auto_now
Значение поля будет автоматически установлено в текущую дату при каждом сохранении объекта. Полезно для хранения времени последнего изменения. текущее время будет использовано всегда; 

### DateField.auto_now_add
Значение поля будет автоматически установлено в текущую дату при создании(первом сохранении) объекта. Полезно для хранения времени создания. 

В форме поле будет представлено как :class:`~django.forms.TextInput с JavaScript календарем, и кнопкой “Сегодня”. Содержит дополнительную ошибку invalid_date.

Опции auto_now_add, auto_now и default взаимоисключающие. Использование их вместе вызовет ошибку.

При использовании auto_now или auto_now_add со значением True будут установлены параметры editable=False и blank=True.

Опции``auto_now`` и auto_now_add всегда используют дату в часовом поясе по умолчанию в момент создания или изменения объекта. Если такое поведение вам не подходит, вы можете указать свою функцию как значение по умолчанию, или переопределить метод save(), вместо использования auto_now или auto_now_add. Или использовать DateTimeField вместо DateField и выполнять преобразование в дату при выводе значения.

## DateTimeField
class DateTimeField([auto_now=False, auto_now_add=False, **options])
Дата и время, представленные объектом datetime.datetime Python. Принимает аналогичные параметры что и DateField.

Виджет по умолчанию в форме для этого поля - TextInput. Интерфейс администратора использует два виджета TextInput и JavaScript.

## IntegerField
class IntegerField([**options])
Число. Значение от -2147483648 до 2147483647 для всех поддерживаемых баз данных Django. Форма использует виджет TextInput.


## SmallIntegerField
class SmallIntegerField([**options])
Как и поле IntegerField, но принимает значения в определенном диапазоне(зависит от типа базы данных). Для баз данных поддерживаемых Django можно использовать значения от -32768 до 32767.

## TextField
class TextField([**options])
Большое текстовое поле. Форма использует виджет Textarea.

Если указать атрибут max_length, это повлияет на поле, создаваемое виджетом Textarea. Но не учитывается на уровне модели или базы данных. Для этого используйте CharField.

#### Пользователям MySQL
Если вы используете это поле с MySQLdb 1.2.1p2 и utf8_bin “collation” (которое не является значением по умолчанию), могут быть некоторые проблемы. 

## TimeField¶
class TimeField([auto_now=False, auto_now_add=False, **options])
Время, представленное объектом datetime.time Python. Принимает те же аргументы, что и DateField.

Форма использует виджет TextInput. Интерфейс администратора также использует немного JavaScript.

Миграции
=========

Выполняя makemigrations, вы говорите Django, что внесли некоторые изменения в ваши модели и хотели бы сохранить их в миграции.
```
./manage.py makemigrations blog
App 'blog' could not be found. Is it in INSTALLED_APPS?

```
INSTALLED_APPS
--------------
'blog'
```
./manage.py makemigrations blog
Migrations for 'blog':
  0001_initial.py:
    - Create model Article
    - Create model Category
    - Create model Tag

```
Миграции используются Django для сохранения изменений ваших моделей (и структуры базы данных) - это просто файлы на диске. Вы можете изучить миграцию для создания ваших моделей, она находится в файле blog/migrations/0001_initial.py. 

Команда sqlmigrate получает название миграции и возвращает SQL:

```
./manage.py sqlmigrate blog 0001
```
Вы увидите приблизительно такое:

```
BEGIN;
--
-- Create model Article
--
CREATE TABLE "blog_article" 
    (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "title" varchar(100) NOT NULL UNIQUE, 
    "status" integer NOT NULL, 
    "content" text NOT NULL, 
    "publish_date" datetime NOT NULL, 
    "created_date" datetime NOT NULL
    );
--
-- Create model Category
--
CREATE TABLE "blog_category" 
    (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "name" varchar(100) NOT NULL, 
    "description" text NOT NULL
    );
--
-- Create model Tag
--
CREATE TABLE "blog_tag" 
    (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "name" varchar(100) NOT NULL UNIQUE)
    ;

COMMIT;

```
Полученные запросы зависят от базы данных, которую вы используете. 

Названия таблиц созданы автоматически из названия приложения(blog) и названия модели в нижнем регистре – category, tag и article. (Вы можете переопределить это.)

Первичные ключи (ID) добавлены автоматически. (Вы можете переопределить и это.)

Django добавляет "_id" к названию внешнего ключа. (вы можете переопределить это.)

Учитываются особенности базы данных, которую вы используете. Специфические типы данных такие как auto_increment (MySQL), serial (PostgreSQL), или integer primary key (SQLite) будут использоваться автоматически. Тоже касается и экранирование названий, что позволяет использовать в названии кавычки – например, использование одинарных или двойных кавычек.

Команда sqlmigrate не применяет миграцию к базе данных - она просто выводит запросы на экран, чтобы вы могли увидеть какой SQL создает Django. Это полезно, если вы хотите проверить что выполнит Django, или чтобы предоставить вашему администратору базы данных SQL скрипт.

Если необходимо, можете выполнить python manage.py check. Эта команда ищет проблемы в вашем проекте не применяя миграции и не изменяя базу данных.

В Django есть команда, которая выполняет миграции и автоматически обновляет базу данных - она называется migrate. 

выполните команду migrate, чтобы создать таблицы для этих моделей в базе данных:
```
$ python manage.py migrate
```
Команда migrate выполняет все миграции, которые ещё не выполнялись, (Django следит за всеми миграциями, используя таблицу в базе данных django_migrations) и применяет изменения к базе данных, синхронизируя структуру базы данных со структурой ваших моделей.

Миграции - очень мощная штука. Они позволяют изменять ваши модели в процессе развития проекта без необходимости пересоздавать таблицы в базе данных. Их задача изменять базу данных без потери данных. 

1. Внесите изменения в модели (в models.py).
2. Выполните python manage.py makemigrations чтобы создать миграцию для ваших изменений
3. Выполните python manage.py migrate чтобы применить изменения к базе данных.
```
./manage.py migrate
Operations to perform:
  Apply all migrations: sessions, auth, contenttypes, blog, admin
Running migrations:
  Rendering model states... DONE
  Applying blog.0001_initial... OK

```
Две команды необходимы для того, чтобы хранить миграции в системе контроля версий. Они не только помогают вам, но и могут использоваться другими программистами вашего проекта.

Мыкет проекта
==============
```
.
├── db.sqlite3
├── f_tests
│   ├── __init__.py
│   └── tests.py
├── static
│   ├── favicon.ico
│   ├── css
│   │   ├── main.css
│   │   ├── bootstrap.css
│   │   ├── bootstrap-theme.css
│   │   └── bootstrap.css.map
│   ├── js
│   │   ├── main.js
│   │   ├── plugins.js
│   │   └── vendor
│   ├── img
│   │   └── star.png
│   └── fonts
│       ├── glyphicons-halflings-regular.eot
│       ├── glyphicons-halflings-regular.svg
│       ├── glyphicons-halflings-regular.ttf
│       └── glyphicons-halflings-regular.woff
├── templates
│   ├── base.html
│   ├── 404.html
│   ├── home
│   │   └── index.html
│   └── blog
│       └── index.html
├── blog
│   ├── admin.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── __pycache__
│   ├── tests.py
│   └── views.py
├── home
│   ├── admin.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── __pycache__
│   ├── tests.py
│   └── views.py
├── manage.py
└── mysite
    ├── __init__.py
    ├── __pycache__
    ├── settings.py
    ├── urls.py
    └── wsgi.py

```
admin.py
--------
```
from django.contrib import admin

from .models import Category, Tag, Article

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)

```

base.html
---------
```
    </nav>
        {% block jumbotron %} 

        {% endblock jumbotron %}
        
        <div class="container">
        {% block content %} 

        {% endblock content %}
          <hr>

          <footer>
            <p>&copy; Company 2016</p>
          </footer>
        </div> <!-- /container -->     
```
home/index.html
----------------
```
{% extends "base.html" %}
{% block head_title %}My Cool Django Site{% endblock %}
<!-- Main jumbotron for a primary marketing message or call to action -->
    {% block jumbotron %} 

    
    <div class="jumbotron">
      <div class="container">
        <h1>Hello, world!</h1>
        <p>This is a template for a simple marketing or informational website. It includes a large callout called a jumbotron and three supporting pieces of content. Use it as a starting point to create something more unique.</p>
        <p><a class="btn btn-primary btn-lg" href="#" role="button">Learn more &raquo;</a></p>
      </div>
    </div>
{% endblock jumbotron %}

{% block content %} 
      <!-- Example row of columns -->
      <div class="row">
        <div class="col-md-4">
          <h2>Heading</h2>
          <p>Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p>
          <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-4">
          <h2>Heading</h2>
          <p>Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p>
          <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
       </div>
        <div class="col-md-4">
          <h2>Heading</h2>
          <p>Donec sed odio dui. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Vestibulum id ligula porta felis euismod semper. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.</p>
          <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
        </div>
      </div>

{% endblock content %}
```

blog/index.html
----------------
```
{% extends "base.html" %}
{% block head_title %}My Cool Django Blog{% endblock %}

{% block content %} 
      <!-- Example row of columns -->
      <div class="row">
        <div class="col-md-8">
          <h2>Heading</h2>
          <p>Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p>
          <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-4">
          <h2>Heading</h2>
          <p>Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p>
          <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
       </div>
        
      </div>

{% endblock content %}
```
includes/header.html
--------------------
```
{% load staticfiles %}
<!doctype html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang=""> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8" lang=""> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9" lang=""> <![endif]-->
<!--[if gt IE 8]><!--> 
<html class="no-js" lang=""> 
<!--<![endif]-->
    <head>
        <title>{% block head_title %}{% endblock %}</title>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="apple-touch-icon" href="apple-touch-icon.png">
        <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
        <style>
            body {
                padding-top: 50px;
                padding-bottom: 20px;
            }
        </style>
        <link rel="stylesheet" href="{% static 'css/bootstrap-theme.min.css' %}">
        <link rel="stylesheet" href="{% static 'css/main.css' %}">
        
        <script src="{% static 'js/vendor/modernizr-2.8.3-respond-1.4.2.min.js' %}"></script>
    </head>
    <body>        

```

includes/footer.html
--------------------
```
{% load staticfiles %}
      <hr>

      <footer>
        <p>&copy; Company 2016</p>
      </footer>
    </div> <!-- /container -->        

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="static/js/vendor/jquery-1.11.0.min.js"><\/script>')</script>

        <script src="{% static 'js/vendor/bootstrap.min.js' %}">
        
        <script src="{% static 'js/plugins.js' %}">
        <script src="{% static 'js/main.js' %}">
        

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
includes/mainmenu.html
----------------------
```
    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/">Project name</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">

          <ul class="nav navbar-nav">
            <li class="active"><a href="/">Home <span class="sr-only">(current)</span></a></li>
            <li><a href="/blog">Blog</a></li>
          </ul>

          <form class="navbar-form navbar-right" role="form">
            <div class="form-group">
              <input type="text" placeholder="Email" class="form-control">
            </div>
            <div class="form-group">
              <input type="password" placeholder="Password" class="form-control">
            </div>
            <button type="submit" class="btn btn-success">Sign in</button>
          </form>
        </div><!--/.navbar-collapse -->
      </div>
    </nav>
```
base.html
----------
```
{% include 'includes/header.html'%}
{% include 'includes/mainmenu.html'%}

    {% block jumbotron %} 

    {% endblock jumbotron %}
    
    <div class="container">
    {% block content %} 

    {% endblock content %}

{% include 'includes/footer.html'%}

```

Как Django обрабатывает запрос
===============================
При запросе к странице Django-сайта, используется такой алгоритм для определения какой код выполнить:

- Django определяет какой корневой модуль URLconf использовать. Обычно, это значение настройки ROOT_URLCONF, но, если объект запроса HttpRequest содержит атрибут urlconf (установленный request middleware), его значение будет использоваться вместо ROOT_URLCONF.
settings.py:
------------
```
ROOT_URLCONF = 'mysite.urls'
```
- Django загружает модуль конфигурации URL и ищет переменную urlpatterns. Это должен быть список экземпляров django.conf.urls.url().
```
def url(regex, view, kwargs=None, name=None, prefix=''):
    if isinstance(view, (list, tuple)):
        # For include(...) processing.
        urlconf_module, app_name, namespace = view
        return RegexURLResolver(regex, urlconf_module, kwargs, app_name=app_name, namespace=namespace)
    else:
        if isinstance(view, six.string_types):
            warnings.warn(
                'Support for string view arguments to url() is deprecated and '
                'will be removed in Django 1.10 (got %s). Pass the callable '
                'instead.' % view,
                RemovedInDjango110Warning, stacklevel=2
            )
            if not view:
                raise ImproperlyConfigured('Empty URL pattern view name not permitted (for pattern %r)' % regex)
            if prefix:
                view = prefix + '.' + view
        return RegexURLPattern(regex, view, kwargs, name)

```
- Django перебирает каждый URL-шаблон по порядку, и останавливается при первом совпадении с запрошенным URL-ом.

- Если одно из регулярных выражений соответствует URL-у, Django импортирует и вызывает соответствующее представление, которое является просто функцией Python(или представление-класс). 

При вызове передаются следующие аргументы:
------------------------------------------
Объект HttpRequest.
-------------------
Если в результате применения регулярного выражения получили именованные совпадения, они будут переданы как позиционные аргументы.

Именованные аргументы создаются из именованных совпадений. Они могут быть перезаписаны значениями из аргумента kwargs, переданного в django.conf.urls.url().

Если ни одно регулярное выражение не соответствует, или возникла ошибка на любом из этапов, Django вызывает соответствующий обработчик ошибок. 

пример простого URLconf:
------------------------
```
from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^blog/2016/$', views.special_case_2016),
    url(r'^blog/([0-9]{4})/$', views.year_archive),
    url(r'^blog/([0-9]{4})/([0-9]{2})/$', views.month_archive),
    url(r'^blog/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),
]
```
views.py
--------
```
def special_case_2016(request):
    item = {'title':'Special Case 2016','topics':10}    
    return render(request, "home/special_case_2016.html", {'item':item})

def year_archive(request,yy):
    item = {'title':'Year Archive','content':yy}    
    return render(request, "home/year_archive.html", {'item':item})

def month_archive(request,yy,mm):
    item = {'title':'Month Archive','content':yy}    
    return render(request, "home/month_archive.html", {'item':item})

def article_detail(request,yy,mm,id):
    item = {'title':'Article Detail','content':id}    
    return render(request, "home/article_detail.html", {'item':item})
```
Не нужно добавлять косую черту в начале, потому что каждый URL содержит его. Например, используйте ^blog, вместо ^/blog.

Символ 'r' перед каждым регулярным выражением не обязателен, но рекомендуется. Он указывает Python что строка “сырая(raw)” и ничего в строке не должно быть экранировано. 

- Запрос к``/blog/2016/03/`` будет обработан третьим элементом списка. Django вызовет функцию views.month_archive(request, '2016', '03').

- /blog/2016/3/ не соответствует ни одному URL-шаблону, потому что третья запись требует две цифры в номере месяца.

- /blog/2016/ соответствует первому выражению, не второму, потому что шаблоны проверяются по порядку. 

- /blog/2016 не соответствует ни одному регулярному выражению, потому что каждое ожидает, что URL оканчивается на косую черту.

- /blog/2016/03/03/ соответствует последнему выражению. Django вызовет функцию views.article_detail(request, '2016', '03', '03').

blog/views.py
-------------
```
from django.shortcuts import render
from .models import Article

def special_case_2016(request):
    item = {'title':'Special Case 2016','topics':10}    
    return render(request, "blog/special_case_2016.html", {'item':item})

def year_archive(request,yy):
    item = {'title':'Year Archive','content':yy}    
    return render(request, "blog/year_archive.html", {'item':item})

def month_archive(request,yy,mm):
    item = {'title':'Month Archive','content':yy}    
    return render(request, "blog/month_archive.html", {'item':item})

def article_detail(request,yy,mm,id):
    item = {'title':'Article Detail','content':id}    
    return render(request, "blog/article_detail.html", {'item':item})
```

QuerySet API
============

Когда вычисляется QuerySets
----------------------------
QuerySet может быть создан, отфильтрован, ограничен и использован фактически без выполнения запросов к базе данных. База данных не будет затронута, пока вы не спровоцируете выполнение QuerySet.

QuerySet будет вычислен при таких действиях:
--------------------------------------------
Итерация. QuerySet – это итератор, и при первом выполнении итерации будет произведен запрос к базе данных. Например, этот код выводит заголовки статей из базы данных:
```
for e in Article.objects.all():
    print(e.title)
```
не используйте такой подход, если необходимо всего лишь узнать содержит ли результат запроса хотя бы один объект, и вам не нужен сам результат. Эффективнее использовать метод exists().

Ограничение выборки. 
--------------------
выборка QuerySet может быть ограничена, используя синтаксис срезов в Python. Срез не вычисленного QuerySet обычно возвращает новый не вычисленный QuerySet, но Django выполнит запрос, если будет указан шаг среза и вернет список. Срез QuerySet, который был вычислен (частично или полностью), также вернет список.

если нужно узнать только количество записей в выборке, эффективнее использовать подсчет на уровне базы данных, используя оператор SQL SELECT COUNT(*), и Django предоставляет метод count() для этого.

order_by order_by(*fields)
---------------------------
По-умолчанию, результат возвращаемый QuerySet, отсортирован по полям указанным в аргументе ordering класса Meta модели. Вы можете переопределить сортировку используя метод order_by.

Например:
```
blog_list = Article.objects.order_by('-publish_date', 'title')
```
Результат выше будет отсортирован в обратном порядке по полю publish_date, далее по полю title. Знак “минус” в "-publish_date" указывает на “нисходящую” сортировку. Сортировка по возрастанию подразумевается по-умолчанию. Чтобы отсортировать случайно используйте "?", например:
```
Article.objects.order_by('?')
```
запрос с order_by('?') может быть медленным и сильно нагружать базу данных, зависит от типа базы данных, которую вы используете.

Вы можете также сортировать по выражению, вызвав asc() или desc() для выражения:
--------------------------------------------------------------------------------
```
Article.objects.order_by('-publish_date', 'title').desc())
```

отсортировать по полю преобразовав значение в нижний регистр, используя Lower:
------------------------------------------------------------------------------
```
Article.objects.order_by(Lower('title').desc())
```

Если вы не хотите использовать сортировку, даже указанную по-умолчанию, выполните метод order_by() без аргументов.

Вы можете определить используется сортировка или нет проверив атрибут QuerySet.ordered, который будет равен True, если сортировка была применена для QuerySet каким-либо образом.

Каждый последующий вызов order_by() сбросит предыдущую сортировку. 
------------------------------------------------------------------
Например, следующий запрос будет отсортирован по publish_date, а не title:
```
Article.objects.order_by('title').order_by('publish_date')
```
Сортировка не бесплатная операция. Каждое поле влияет на скорость выполнения запроса. Каждый внешний ключ добавит сортировку по умолчанию связанной модели.

views.py
---------
```
def index(request):
    blog_list = Article.objects.order_by('-publish_date')
    context = {'blog_list': blog_list}
    return render(request, 'blog/index.html', context)

```
blog/index.html
---------------
```
<div class="col-md-8">
          <h2>Publications</h2>
          
          <ul>
              {% if blog_list %}
                {% for item in blog_list %}
                  <li>{{ item.title }}</li>
                {% endfor %}
              {% else %}
                <li>Sorry, no items in this list.</li>
              {% endif %}
          </ul>
```

Метод get не возвращает QuerySets
---------------------------------
get метод выполняет QuerySet и возвращает не QuerySet.
метод не использует кэш и выполняет запрос к базе данных при каждом вызове.

get get(**kwargs)
-----------------
Возвращает объект соответствующий параметрам поиска

get() вызывает исключение MultipleObjectsReturned, если найдено более одно объекта. MultipleObjectsReturned – атрибут класса модели.

get() вызывает исключение DoesNotExist, ни один объект не был найден. Это исключение также атрибут класса модели. Например:
```
item = Article.objects.get(pk=blog_id) # raises Entry.DoesNotExist
```
Исключение DoesNotExist унаследовано от django.core.exceptions.ObjectDoesNotExist,таким образом можно обработать несколько исключений DoesNotExist. Например:
```
from django.core.exceptions import ObjectDoesNotExist
def detail(request, blog_id):
    try:
        item = Article.objects.get(pk=blog_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    return render(request, 'blog/detail.html', {'item': item})
```
url
---
Возвращает абсолютную ссылку (URL без имени домена) соответствующую указанному представлению с необязательными аргументами. Любые спецсимволы будут экранированы с помощью функции iri_to_uri().

urls.py
-------
```
urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^req/', views.req_test, name='req_test'),

    url(r'^exampl1/', views.exampl1, name='some-url-name'),

    url(r'^admin/', admin.site.urls),
]

```
views.py
---------
```
def exampl1(request):
    return render(request, "home/exampl1.html", {})

```
home.html
----------
```
        <h2>url</h2>

        <a href="{% url 'some-url-name' %}">Example 1 </a>

```
Позиционные аргументы.
----------------------
Этот способ выводить ссылки без “хардкодинга” в шаблоне, чтобы не нарушать принцип DRY:
```
{% url 'some-url-name' v1 v2 %}
```
Первый аргумент – это путь к функции представления в формате package.package.module.function. Он может быть строкой в кавычках или любой другой контекстной переменной. Дополнительные аргументы необязательны. Это значения, разделенные пробелами, которые будут использоваться как аргументы при формировании URL.  

Также можно использовать именованные аргументы:
-----------------------------------------------
```
{% url 'some-url-name' arg1=v1 arg2=v2 %}
```
Нельзя использовать и позиционные и именованные аргументы в одном теге. Все обязательные аргументы URLconf должны быть указаны.

Например, мы имеем представление, views.article, чей URLconf принимает ID клиента (article() это метод в файле views.py). 
views.py
--------
```
def article(request,id):
    item = {'title':1,'content':id}    
    return render(request, "home/article.html", {'item':item})
```

urls.py:
--------
```
url(r'^article/([0-9]+)/$', views.article, name='app-views-article'),
```
example1.html
-------------
```
        <h3>Article</h3>
      
        <a href="{% url 'app-views-article' 1 %}">Article 1 </a>
```



blog/index.html
----------------
```
            {% if blog_list %}
                {% for item in blog_list %}
                  <h3><a href ="{% url 'blog:detail' item.id %}">{{ item.title }}</a></h3>
                    <p><a class="btn btn-default" href="{% url 'blog:detail' item.id %}" role="button">View details &raquo;</a></p>
                {% endfor %}
              {% else %}
                <li>Sorry, no items in this list.</li>
              {% endif %}
```

blog/detail.html
```
{% extends "base.html" %}
{% block head_title %}My Cool Django Blog{% endblock %}

{% block content %} 
      <!-- Example row of columns -->
      <div class="row">
        <div class="col-md-8">
          <h2>{{ item.title }}</h2>
         
          <p> {{ item.content }} </p>
          <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-4">
          <h2>Heading</h2>
          
       </div>
        
      </div>

{% endblock content %}
```

blog/urls.py
------------
```
from django.conf.urls import url

from . import views

urlpatterns = [
    
    # ex: /blog/
    url(r'^$', views.index, name='index'),
    # ex: /blog/5/
    url(r'^(?P<blog_id>[0-9]+)/$', views.detail, name='detail'),
    
]

```
mysite/url.py
--------------
```
from django.conf.urls import include, url
from django.contrib import admin

from home import views as view_home
from blog import views

urlpatterns = [
    url(r'^$', view_home.home, name='home'),
    
    
    url(r'^blog/2016/$', views.special_case_2016),
    url(r'^blog/([0-9]{4})/$', views.year_archive),
    url(r'^blog/([0-9]{4})/([0-9]{2})/$', views.month_archive),
    url(r'^blog/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),

    url(r'^blog/', include('blog.urls', namespace="blog")),

    url(r'^blog/(?P<year>[0-9]{4})/$', views.year_archive),
    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.article_detail),
    
    url(r'^admin/', admin.site.urls),
]

```
