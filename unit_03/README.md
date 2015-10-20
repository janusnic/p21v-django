# p21v-django

# Шаблоны
Django позволяет динамически генерировать HTML. Самый распространенный подход - использование шаблонов. Шаблоны содержат статический HTML и динамические данные, рендеринг которых описан специальным синтаксисом. 

Проект Django может использовать один или несколько механизмов создания шаблонов (или ни одного, если вы не используете шаблоны). Django предоставляет бэкенд для собственной системы шаблонов, которая называется - язык шаблонов Django (Django template language, DTL), и популярного альтернативного шаблонизатора Jinja2. Сторонние приложения могут предоставлять бэкенд и для других систем шаблонов.

Django предоставляет стандартный API для загрузки и рендеринга шаблонов, незавимисо от используемого бэкенда. Загрузка включает в себя поиск шаблона по названию и предварительную обработку, обычно выполняется загрузка шаблона в память. Рендеринг означает передачу данных контекста в шаблон и возвращение строки с результатом.

Язык шаблонов Django – собственная система шаблонов Django. До Django 1.8 – это была единственная альтернатива. Встроенные шаблоны Django, которые содержат шаблоны, например django.contrib.admin, используют систему шаблонов Django.

По историческим причинам поддержка шаблонов и встроенная система шаблонов Django находятся в одном пакете django.template.

# Поддержка систем шаблонов TEMPLATES.

## Настройки
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
BACKEND путь для импорта Python к классу бэкенда шаблонов. Встроенные бэкенды это django.template.backends.django.DjangoTemplates и django.template.backends.jinja2.Jinja2.

Т.к. большинство систем шаблонов загружают шаблоны с файлов, настройки содержат:

- DIRS, которая содержим список каталогов с шаблонами. Бэкенд ищет в них шаблон в указанном порядке.

- APP_DIRS указывает бэкенду искать ли шаблоны в установленных приложениях. Каждый бэкенд определяет определенное название для каталога с шаблонами в приложении.

templates/home.html

```
<html>
    <head>
        <title>Сделай сам To-Do lists</title>
    </head>
    <body>
        <h1>Сделай сам - Your To-Do list</h1>
        <input id="id_new_item" placeholder="Добавить в список дел" />
        <table id="id_list_table">
        </table>
    </body>
</html>

```
urls.py
```
from django.conf.urls import include, url
from django.contrib import admin
from todo import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home_page, name='home'),
]

```

views.py
```
from django.shortcuts import render

def home_page(request):
    return render(request, 'home.html')
```

tests.py
```
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from todo.views import home_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

```

./manage.py test
```
Creating test database for alias 'default'...
E.
======================================================================
ERROR: test_home_page_returns_correct_html (todo.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_03/mysite/todo/tests.py", line 17, in test_home_page_returns_correct_html
    response = home_page(request)
  File "/home/janus/21_perspective/github/p21v-django/unit_03/mysite/todo/views.py", line 4, in home_page
    return render(request, 'home.html')
  File "/home/janus/Envs/env2/lib/python3.4/site-packages/django/shortcuts.py", line 67, in render
    template_name, context, request=request, using=using)
  File "/home/janus/Envs/env2/lib/python3.4/site-packages/django/template/loader.py", line 98, in render_to_string
    template = get_template(template_name, using=using)
  File "/home/janus/Envs/env2/lib/python3.4/site-packages/django/template/loader.py", line 46, in get_template
    raise TemplateDoesNotExist(template_name)
django.template.base.TemplateDoesNotExist: home.html

----------------------------------------------------------------------
Ran 2 tests in 0.003s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

settings.py
```
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todo',
)
```
./manage.py test

```
Creating test database for alias 'default'...
..
----------------------------------------------------------------------
Ran 2 tests in 0.004s

OK
Destroying test database for alias 'default'...
```

functional_tests.py
```
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Посетим нашу главную страницу 
        self.browser.get('http://localhost:8000')

        # Проверим, содержит ли заголовок h1 страницы фразу 'Сделай сам - Your To-Do list'
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Сделай сам To-Do', header_text)

        # Содержит ли поле ввода приглашение 'Добавить в список дел'?
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Добавить в список дел'
        )

        # Напечатаем "Купить бочку апельсинов" в поле ввода
        inputbox.send_keys('Купить бочку апельсинов')

        # При нажатии клавиши enter страница изменится и появится пункт 
        # "1: Купить бочку апельсинов" в табличном списке 
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Купить бочку апельсинов' for row in rows),
            "New to-do item did not appear in table"
        )

        # Поле ввода снова содержит приглашение - Добавить в список дел
        
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')

```
python functional_tests.py 
```
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 42, in test_can_start_a_list_and_retrieve_it_later
    "New to-do item did not appear in table"
AssertionError: False is not true : New to-do item did not appear in table

----------------------------------------------------------------------
Ran 1 test in 8.421s

FAILED (failures=1)

```

## Form to Send a POST Request

```
<input> element name= attribute
<form> tag method="POST".
```
urls.py
```
from django.conf.urls import include, url
from django.contrib import admin
from todo import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', views.home_page, name='home'),
    url(r'^$', views.index1, name='home'),
]

```
views.py
```
def index1(request):
    return render(request, 'index1.html')
```
todo/templates/index1.html
```
<html>
    <head>
        <title>Сделай сам To-Do lists</title>
    </head>
    <body>
        <h1>Сделай сам - Your To-Do list</h1>
        <form method="POST">
        <input name="item_text" id="id_new_item" placeholder="Добавить в список дел" />
        </form>
        <table id="id_list_table">
        </table>
    </body>
</html>
```
python functional_tests.py 
```
E
======================================================================
ERROR: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 38, in test_can_start_a_list_and_retrieve_it_later
    table = self.browser.find_element_by_id('id_list_table')
  File "/home/janus/Envs/env2/lib/python3.4/site-packages/selenium/webdriver/remote/webdriver.py", line 234, in find_element_by_id
    return self.find_element(by=By.ID, value=id_)
  File "/home/janus/Envs/env2/lib/python3.4/site-packages/selenium/webdriver/remote/webdriver.py", line 712, in find_element
    {'using': by, 'value': value})['value']
  File "/home/janus/Envs/env2/lib/python3.4/site-packages/selenium/webdriver/remote/webdriver.py", line 201, in execute
    self.error_handler.check_response(response)
  File "/home/janus/Envs/env2/lib/python3.4/site-packages/selenium/webdriver/remote/errorhandler.py", line 181, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate element: {"method":"id","selector":"id_list_table"}
Stacktrace:
    at FirefoxDriver.prototype.findElementInternal_ (file:///tmp/tmpkxexvol3/extensions/fxdriver@googlecode.com/components/driver-component.js:10659)
    at fxdriver.Timer.prototype.setTimeout/<.notify (file:///tmp/tmpkxexvol3/extensions/fxdriver@googlecode.com/components/driver-component.js:621)

----------------------------------------------------------------------
Ran 1 test in 9.474s

FAILED (errors=1)
```
functional_tests.py 
```
        inputbox.send_keys(Keys.ENTER)

        import time
        time.sleep(10)
        
        table = self.browser.find_element_by_id('id_list_table')
```

Forbidden (403)

CSRF verification failed. Request aborted.

You are seeing this message because this site requires a CSRF cookie when submitting forms. This cookie is required for security reasons, to ensure that your browser is not being hijacked by third parties.

If you have configured your browser to disable cookies, please re-enable them, at least for this site, or for 'same-origin' requests.
Help

Reason given for failure:

    CSRF cookie not set.
    

In general, this can occur when there is a genuine Cross Site Request Forgery, or when Django's CSRF mechanism has not been used correctly. For POST forms, you need to ensure:

    Your browser is accepting cookies.
    The view function passes a request to the template's render method.
    In the template, there is a {% csrf_token %} template tag inside each POST form that targets an internal URL.
    If you are not using CsrfViewMiddleware, then you must use csrf_protect on any views that use the csrf_token template tag, as well as those that accept the POST data.

You're seeing the help section of this page because you have DEBUG = True in your Django settings file. Change that to False, and only the initial error message will be displayed.

You can customize this page using the CSRF_FAILURE_VIEW setting.

# Подделка межсайтового запроса (CSRF)
Промежуточный слой CSRF и шаблонный тег предоставляют легкую-в-использовании защиту против Межсайтовой подделки запроса. Этот тип атак случается, когда злонамеренный Web сайт содержит ссылку, кнопку формы или некоторый javascript, который предназначен для выполнения некоторых действий на вашем Web сайте, используя учетные данные авторизованного пользователя, который посещал злонамеренный сайт в своем браузере. Сюда также входит связанный тип атак, ‘login CSRF’, где атакуемый сайт обманывает браузер пользователя, авторизируясь на сайте с чужими учетными данными.

Первая защита против CSRF атак - это гарантирование того, что GET запросы (и другие ‘безопасные’ методы, определенные в 9.1.1 Safe Methods, HTTP 1.1, RFC 2616) свободны от побочных эффектов. Запросы через ‘небезопасные’ методы, такие как POST, PUT и DELETE могут быть защищены при помощи шагов, описанных ниже.

Для того чтобы включить CSRF защиту для ваших представлений, выполните следующие шаги:

Промежуточный слой CSRF активирован по умолчанию и находится в настройке MIDDLEWARE_CLASSES. Если вы переопределяете эту настройку, помните, что ``‘django.middleware.csrf.CsrfViewMiddleware’``должен следовать перед промежуточными слоями, которые предполагают, что запрос уже проверен на CSRF атаку.
```
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

```
Если вы отключили защиту, что не рекомендуется, вы можете использовать декоратор csrf_protect() в части представлений, которые вы хотите защитить.

В любом шаблоне, который использует POST форму, используйте тег csrf_token внутри элемента form если форма для внутреннего URL, т. е.:
```
<form action="." method="post">{% csrf_token %}
```
Это не должно делаться для POST форм, которые ссылаются на внешние URL’ы, поскольку это может вызвать утечку CSRF токена, что приводит к уязвимости.

В соответствующих функциях представления, убедитесь, что 'django.template.context_processors.csrf' контекстный процессор используется. Обычно, это может быть сделано в один из двух способов:

Использовать RequestContext, который всегда использует 'django.template.context_processors.csrf' (не зависимо от параметра TEMPLATES ). Если вы используете общие представления или contrib приложения, вы уже застрахованы, так как эти приложения используют RequestContext повсюду.

Вручную импортировать и использовать процессор для генерации CSRF токена и добавить в шаблон контекста. т.е.:
```
from django.shortcuts import render_to_response
from django.template.context_processors import csrf

def my_view(request):
    c = {}
    c.update(csrf(request))
    # ... view code here
    return render_to_response("a_template.html", c)
```

## AJAX
Хотя вышеописанный метод может быть использован для AJAX POST запросов, он имеет некоторые неудобства: вы должны не забывать передавать CSRF токен в POST данных с каждым POST запросом. По этой причине есть альтернативный метод: для каждого XMLHttpRequest можно устанавливать кастомный заголовок X-CSRFToken в значение CSRF токена. Это проще, потому что многие javascript фреймворки предоставляют хуки, которые позволяют устанавливать заголовки для каждого запроса.

В качестве первого шага, вы должны получить CSRF токен самостоятельно. Рекомендованный источник для токен - это кука csrftoken , которая будет установлена, если вы включили CSRF защиту для ваших представлений.

Кука CSRF токена называется csrftoken по умолчанию, но вы можете управлять именем куки при помощи параметра CSRF_COOKIE_NAME.

Получение токена является простым:
```
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
```
Вышеприведенный код может быть упрощен при помощи плагина jQuery для замены getCookie:
```
var csrftoken = $.cookie('csrftoken');
```

CSRF токен также представлен в DOM, но только если он явно включен, используя csrf_token в шаблоне. Кука содержит канонический токен; CsrfViewMiddleware будет предпочитать этот куки куке из DOM. Не смотря на это, вы гарантировано имеете куки, если токен представлен в DOM, так что вы должны использовать куки.

Если ваше представление не рендерит шаблон, содержащий шаблонный тег csrf_token, Django может не установить куки с CSRF токеном.
В конце концов, вы должны фактически установить заголовок в вашем AJAX запросе, одновременно защищая CSRF токен от отправки на другие домены, используя settings.crossDomain в jQuery 1.5.1 и выше:
```
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
```

## Встроенные шаблонные теги и фильтры

### csrf_token
Этот тег используется для организации CSRF защиты.

```
<form method="POST">
    <input name="item_text" id="id_new_item" placeholder="Добавить в список дел" />
    {% csrf_token %}
</form>

```

## Язык шаблонов Django

### Синтаксис

Шаблон Django – это просто текстовый файл, или строка Python, которые следуют языку шаблонов Django. Определенные конструкции распознаются и интерпретируются шаблонизатором. Основные – это переменные и теги.

Шаблон рендерится с контекстом. Рендеринг заменяет переменные на их значения, которые ищутся в контексте, и выполняет теги. Все остальное выводится как есть.

Синтаксис языка шаблонов Django использует четыре конструкции.

### Переменные
Переменные выводят значения из контекста, который является словарем.

Переменные выделяются {{ и }}, например:
```
My first name is {{ first_name }}. My last name is {{ last_name }}.
```
Для контекста {'first_name': 'John', 'last_name': 'Doe'} шаблон отрендерит:

My first name is John. My last name is Doe.
Обращение к ключам словаря, атрибутам объектов и элементам списка выполняется через точку:
```
{{ my_dict.key }}
{{ my_object.attribute }}
{{ my_list.0 }}
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

## Фильтры
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

## Комментарии
Комментарии могут выглядеть таким образом:
```
{# this won't be rendered #}
```
Тег {% comment %} позволяет добавлять многострочные комментарии.

todo/tests.py
```
# -*- coding:utf-8 -*-
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from todo.views import home_page, index1

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/home')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'Грузить апельсины бочками'

        response = index1(request)

        self.assertIn('Грузить апельсины бочками', response.content.decode())

```

./manage.py test
```
Creating test database for alias 'default'...
F..
======================================================================
FAIL: test_home_page_can_save_a_POST_request (todo.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_03/mysite/todo/tests.py", line 29, in test_home_page_can_save_a_POST_request
    self.assertIn('Гркзить фпельсины бочками', response.content.decode())
AssertionError: 'Гркзить фпельсины бочками' not found in '<html>\n    <head>\n        <title>Сделай сам To-Do lists</title>\n    </head>\n    <body>\n        <h1>Сделай сам - Your To-Do list</h1>\n        <form method="POST">\n        <input name="item_text" id="id_new_item" placeholder="Добавить в список дел" />\n        </form>\n        <table id="id_list_table">\n        </table>\n    </body>\n</html>'

----------------------------------------------------------------------
Ran 3 tests in 0.028s

FAILED (failures=1)
Destroying test database for alias 'default'...
```
Изменим представление

```
from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    return render(request, 'home.html')

def index1(request):
    if request.method == 'POST':
        return HttpResponse(request.POST['item_text'])
    return render(request, 'index1.html')

```
./manage.py test
```
Creating test database for alias 'default'...
...
----------------------------------------------------------------------
Ran 3 tests in 0.004s

OK
Destroying test database for alias 'default'...

```

## Passing Python Variables to Be Rendered in the Template

index1.html
```
<html>
    <head>
        <title>Сделай сам To-Do lists</title>
    </head>
    <body>
        <h1>Сделай сам - Your To-Do list</h1>
        <form method="POST">{% csrf_token %}
        <input name="item_text" id="id_new_item" placeholder="Добавить в список дел" />
        </form>
        <table id="id_list_table">
            <tr><td>{{ new_item_text }}</td></tr>
        </table>
    </body>
</html>
```
Изменим tests.py
```

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'Грузить апельсины бочками'

        response = index1(request)

        # self.assertIn('Грузить апельсины бочками', response.content.decode())
        self.assertIn('Грузить апельсины бочками', response.content.decode())

        expected_html = render_to_string(
            'index1.html',
            {'new_item_text':  'Грузить апельсины бочками'}
        )
        self.assertEqual(response.content.decode(), expected_html)

```

./manage.py test
```
Creating test database for alias 'default'...
F..
======================================================================
FAIL: test_home_page_can_save_a_POST_request (todo.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_03/mysite/todo/tests.py", line 36, in test_home_page_can_save_a_POST_request
    self.assertEqual(response.content.decode(), expected_html)
AssertionError: 'Грузить апельсины бочками' != '<html>\n    <head>\n        <title>Сделай[240 chars]tml>'

----------------------------------------------------------------------
Ran 3 tests in 0.005s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

views.py

```
def index1(request):
    return render(request, 'index1.html', {
        'new_item_text': request.POST['item_text'],
    })
    

```
views.py
```
def index1(request):
    
    return render(request, 'index1.html', {
        'new_item_text': request.POST.get('item_text', ''),
    })

```
./manage.py test
```
Creating test database for alias 'default'...
...
----------------------------------------------------------------------
Ran 3 tests in 0.006s

OK
Destroying test database for alias 'default'...
```
functional_tests1.py 
```

        import time
        time.sleep(10)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Купить бочку апельсинов' for row in rows),
            # "New to-do item did not appear in table"
            "New to-do item did not appear in table -- its text was:\n%s" % (
            table.text,
            )
        )

```
python functional_tests1.py 
```
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests1.py", line 47, in test_can_start_a_list_and_retrieve_it_later
    table.text,
AssertionError: False is not true : New to-do item did not appear in table -- its text was:
Купить бочку апельсинов

----------------------------------------------------------------------
Ran 1 test in 22.459s

FAILED (failures=1)
```
functional_tests2.py 
```
# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Посетим нашу главную страницу 
        self.browser.get('http://localhost:8000')

        # Проверим, содержит ли заголовок страницы фразу 'Сделай сам - Your To-Do list'
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Сделай сам - Your To-Do list', header_text)

        # Содержит ли поле ввода приглашение 'Добавить в список дел'?
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Добавить в список дел'
        )

        # Напечатаем "Купить бочку апельсинов" в поле ввода
        inputbox.send_keys('Купить бочку апельсинов')

        # При нажатии клавиши enter страница изменится и появится пункт 
        # "1: Купить бочку апельсинов" в табличном списке 
        inputbox.send_keys(Keys.ENTER)

        import time
        time.sleep(10)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Купить бочку апельсинов', [row.text for row in rows])
        
        # Поле ввода снова содержит приглашение Добавить в список дел
        
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

```

python functional_tests2.py 
```
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests2.py", line 43, in test_can_start_a_list_and_retrieve_it_later
    self.assertIn('1: Купить бочку апельсинов', [row.text for row in rows])
AssertionError: '1: Купить бочку апельсинов' not found in ['Купить бочку апельсинов']

----------------------------------------------------------------------
Ran 1 test in 15.203s

FAILED (failures=1)
```
functional_tests2.py 

```
# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Посетим нашу главную страницу 
        self.browser.get('http://localhost:8000')

        # Проверим, содержит ли заголовок страницы фразу 'Сделай сам - Your To-Do list'
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Сделай сам - Your To-Do list', header_text)

        # Содержит ли поле ввода приглашение 'Добавить в список дел'?
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Сменить колеса Дрону налету')
        inputbox.send_keys(Keys.ENTER)

        import time
        time.sleep(10)

        # При нажатии клавиши enter страница изменится и появятся пункты 
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Купить бочку апельсинов', [row.text for row in rows])
        self.assertIn(
            '2: Сменить колеса Дрону налету' ,
             [row.text for row in rows]
        )

        # Поле ввода снова содержит приглашение Добавить в список дел
        
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

```

python functional_tests2.py 
```
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests2.py", line 35, in test_can_start_a_list_and_retrieve_it_later
    self.assertIn('1: Купить бочку апельсинов', [row.text for row in rows])
AssertionError: '1: Купить бочку апельсинов' not found in ['Сменить колеса Дрону налету']

----------------------------------------------------------------------
Ran 1 test in 15.200s

FAILED (failures=1)
```
functional_tests3.py 
```
# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Посетим нашу главную страницу 
        self.browser.get('http://localhost:8000')

        # Проверим, содержит ли заголовок страницы фразу 'Сделай сам - Your To-Do list'
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Сделай сам - Your To-Do list', header_text)

        # Содержит ли поле ввода приглашение 'Добавить в список дел'?
        
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Добавить в список дел'
        )
       
        inputbox.send_keys('Купить бочку апельсинов')

        inputbox.send_keys(Keys.ENTER)
        # self.check_for_row_in_list_table('1: Купить бочку апельсинов')

        import time
        time.sleep(10)

        # При нажатии клавиши enter страница изменится и появятся пункты
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Сменить колеса Дрону налету')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Купить бочку апельсинов')
        self.check_for_row_in_list_table('2: Сменить колеса Дрону налету')


        # Поле ввода снова содержит приглашение Добавить в список дел
        
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

```
python functional_tests3.py 
```
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests3.py", line 51, in test_can_start_a_list_and_retrieve_it_later
    self.check_for_row_in_list_table('1: Купить бочку апельсинов')
  File "functional_tests3.py", line 18, in check_for_row_in_list_table
    self.assertIn(row_text, [row.text for row in rows])
AssertionError: '1: Купить бочку апельсинов' not found in ['Сменить колеса Дрону налету']

----------------------------------------------------------------------
Ran 1 test in 15.222s

FAILED (failures=1)
```
#  Django ORM and Our First Model

tests.py

```
from todo.models import Item

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'Купить бочку апельсинов'
        first_item.save()

        second_item = Item()
        second_item.text = 'Грузить апельсины бочками'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Купить бочку апельсинов')
        self.assertEqual(second_saved_item.text, 'Грузить апельсины бочками')

```
./manage.py test
```
Creating test database for alias 'default'...
E
======================================================================
ERROR: todo.tests (unittest.loader.ModuleImportFailure)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/lib/python3.4/unittest/case.py", line 57, in testPartExecutor
    yield
  File "/usr/lib/python3.4/unittest/case.py", line 574, in run
    testMethod()
  File "/usr/lib/python3.4/unittest/loader.py", line 32, in testFailure
    raise exception
ImportError: Failed to import test module: todo.tests
Traceback (most recent call last):
  File "/usr/lib/python3.4/unittest/loader.py", line 312, in _find_tests
    module = self._get_module_from_name(name)
  File "/usr/lib/python3.4/unittest/loader.py", line 290, in _get_module_from_name
    __import__(name)
  File "/home/janus/21_perspective/github/p21v-django/unit_03/mysite/todo/tests.py", line 8, in <module>
    from todo.models import Item
ImportError: cannot import name 'Item'


----------------------------------------------------------------------
Ran 1 test in 0.020s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

models.py
```
from django.db import models

class Item(object):
    pass
```
 ./manage.py test
```
Creating test database for alias 'default'...
...E
======================================================================
ERROR: test_saving_and_retrieving_items (todo.tests.ItemModelTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_03/mysite/todo/tests.py", line 45, in test_saving_and_retrieving_items
    first_item.save()
AttributeError: 'Item' object has no attribute 'save'

----------------------------------------------------------------------
Ran 4 tests in 0.118s

FAILED (errors=1)
Destroying test database for alias 'default'...
```
models.py
```
from django.db import models

# Create your models here.
# class Item(object):
class Item(models.Model):
    pass

```
 ./manage.py test
```
django.db.utils.OperationalError: no such table: todo_item

```

# Database Migration

./manage.py makemigrations
```
Migrations for 'todo':
  0001_initial.py:
    - Create model Item

```
 ./manage.py test
```
Creating test database for alias 'default'...
...E
======================================================================
ERROR: test_saving_and_retrieving_items (todo.tests.ItemModelTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_03/mysite/todo/tests.py", line 56, in test_saving_and_retrieving_items
    self.assertEqual(first_saved_item.text, 'Купить бочку апельсинов')
AttributeError: 'Item' object has no attribute 'text'

----------------------------------------------------------------------
Ran 4 tests in 0.007s

FAILED (errors=1)
Destroying test database for alias 'default'...
```
models.py
```
from django.db import models

# Create your models here.
# class Item(object):
class Item(models.Model):
    # pass
    text = models.TextField()
```
./manage.py makemigrations
```
You are trying to add a non-nullable field 'text' to item without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows)
 2) Quit, and let me add a default in models.py
Select an option: 1
Please enter the default value now, as valid Python
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now()
>>> ''
Migrations for 'todo':
  0002_item_text.py:
    - Add field text to item
```

./manage.py test
```
Creating test database for alias 'default'...
....
----------------------------------------------------------------------
Ran 4 tests in 0.007s

OK

```
2) Quit, and let me add a default in models.py
models.py
```
class Item(models.Model):
    text = models.TextField(default='')
```
# Saving the POST to the Database
tests.py
```
    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'Купить бочку апельсинов'

        response = index1(request)

        self.assertEqual(Item.objects.count(), 1)  #We check that one new Item has been saved to the database.  objects.count() is a shorthand for objects.all().count().
        new_item = Item.objects.first()  #objects.first() is the same as doing objects.all()[0].
        self.assertEqual(new_item.text, 'Купить бочку апельсинов')  #We check that the item’s text is correct

        self.assertIn('Купить бочку апельсинов', response.content.decode())
        expected_html = render_to_string(
            'index1.html',
            {'new_item_text':  'Купить бочку апельсинов'}
        )
        self.assertEqual(response.content.decode(), expected_html)


```
 ./manage.py test
```
Creating test database for alias 'default'...
...F.
======================================================================
FAIL: test_home_page_can_save_a_POST_request (todo.tests.ItemModelTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_03/mysite/todo/tests.py", line 66, in test_home_page_can_save_a_POST_request
    self.assertEqual(Item.objects.count(), 1)  #We check that one new Item has been saved to the database.  objects.count() is a shorthand for objects.all().count().
AssertionError: 0 != 1

----------------------------------------------------------------------
Ran 5 tests in 0.009s

FAILED (failures=1)
Destroying test database for alias 'default'...
```
views.py

```
from django.shortcuts import render
from django.http import HttpResponse
from todo.models import Item

def home_page(request):
    return render(request, 'home.html')

def index1(request):
    item = Item()
    item.text = request.POST.get('item_text', '')
    item.save()

    return render(request, 'index1.html', {
        'new_item_text': request.POST.get('item_text', ''),
    })
    

def index1(request):
    item = Item()
    item.text = request.POST.get('item_text', '')
    item.save()
    
    return render(request, 'index1.html',{'new_item_text': item.text})
```

test.py
```

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/home')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'Грузить апельсины бочками'

        response = index1(request)

        # self.assertIn('Грузить апельсины бочками', response.content.decode())
        self.assertIn('Грузить апельсины бочками', response.content.decode())

        expected_html = render_to_string(
            'index1.html',
            {'new_item_text':  'Грузить апельсины бочками'}
        )
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        index1(request)
        self.assertEqual(Item.objects.count(), 0)


```    
views.py
```
def index1(request):
    if request.method == 'POST':
        new_item_text = request.POST['item_text']  #1
        Item.objects.create(text=new_item_text)  #2
    else:
        new_item_text = ''  #3

    return render(request, 'index1.html', {
        'new_item_text': new_item_text,  #4
    })
```
./manage.py test
```
Creating test database for alias 'default'...
......
----------------------------------------------------------------------
Ran 6 tests in 0.011s

OK
Destroying test database for alias 'default'...
```
# Redirect After a POST

## redirect
```
redirect(to, [permanent=False, ]*args, **kwargs)
```
Возвращает перенаправление(HttpResponseRedirect) на URL указанный через аргументы.

В аргументах можно передать:

- Экземпляр модели: как URL будет использоваться результат вызова метода get_absolute_url().

- Название представления, возможно с аргументами: для вычисления URL-а будет использоваться функция urlresolvers.reverse.

- Абсолютный или относительный URL, который будет использован для перенаправления на указанный адрес.

- По умолчанию использует временное перенаправление, используйте аргумент permanent=True для постоянного перенаправления.

Функцию redirect() можно использовать несколькими способами.

Передавая объект; в качестве URL-а для перенаправления будет использоваться результат вызова метода get_absolute_url():
```
from django.shortcuts import redirect

def my_view(request):
    ...
    object = MyModel.objects.get(...)
    return redirect(object)
```
Передавая название представления и необходимые позиционные или именованные аргументы; URL будет вычислен с помощью функции reverse():
```
def my_view(request):
    ...
    return redirect('some-view-name', foo='bar')
```
Передавая непосредственно URL:
```
def my_view(request):
    ...
    return redirect('/some/url/')
```
Работает также с полным URL-ом:
```
def my_view(request):
    ...
    return redirect('http://example.com/')
```
По умолчанию, redirect() возвращает временное перенаправление. Все варианты выше принимают аргумент permanent; если передать True будет использоваться постоянное перенаправление:
```
def my_view(request):
    ...
    object = MyModel.objects.get(...)
    return redirect(object, permanent=True)
```
tests.py

```
    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'Купить бочку апельсинов'

        response = index1(request)
        
        self.assertEqual(Item.objects.count(),1) 
        new_item = Item.objects.first()  
        self.assertEqual(new_item.text, 'Купить бочку апельсинов')  

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

        self.assertIn('Купить бочку апельсинов', response.content.decode())
        expected_html = render_to_string(
            'index1.html',
            {'new_item_text':  'Купить бочку апельсинов'}
        )
        self.assertEqual(response.content.decode(), expected_html)
```
./manage.py test
```
Creating test database for alias 'default'...
....F.
======================================================================
FAIL: test_home_page_can_save_a_POST_request (todo.tests.ItemModelTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_03/mysite/todo/tests.py", line 75, in test_home_page_can_save_a_POST_request
    self.assertEqual(response.status_code, 302)
AssertionError: 200 != 302

----------------------------------------------------------------------
Ran 6 tests in 0.011s

FAILED (failures=1)
Destroying test database for alias 'default'...

```
views.py
```
def index1(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    return render(request, 'index1.html')

```
./manage.py test
```
Creating test database for alias 'default'...
......
----------------------------------------------------------------------
Ran 6 tests in 0.010s

OK
Destroying test database for alias 'default'...
```

# Each Test Should Test One Thing
tests.py
```
    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'Купить бочку апельсинов'

        response = index1(request)
        
        self.assertEqual(Item.objects.count(),1) 
        new_item = Item.objects.first()  
        self.assertEqual(new_item.text, 'Купить бочку апельсинов')  



    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = index1(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
```


./manage.py test
```
Creating test database for alias 'default'...
.......
----------------------------------------------------------------------
Ran 7 tests in 0.011s

OK
Destroying test database for alias 'default'...
```
# Rendering Items in the Template

tests.py

```
   def test_home_page_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        request = HttpRequest()
        response = index1(request)

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

```
./manage.py test
```
AssertionError: 'itemey 1' not found in '<html>\

```

# Цикл for
Цикл по каждому элементу массива, добавляя их в контекст блока. Например, выведем список спортсменов из athlete_list:
```
<ul>
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% endfor %}
</ul>
```
Вы можете использовать цикл по списку в обратном порядке {% for obj in list reversed %}.

Если вам нужен цикл по списку списков, вы можете распаковать значения под-списка на отдельные переменные. Например, если ваш контекст содержит список (x,y) координат points, вы можете использовать следующий код для их вывода:
```
{% for x, y in points %}
    There is a point at {{ x }},{{ y }}
{% endfor %}
```
Аналогично можно использовать словарь. Например, если ваш контекст содержит словарь data, следующий код выведет ключи и значения словаря:
```
{% for key, value in data.items %}
    {{ key }}: {{ value }}
{% endfor %}
```

index1.html
```
<html>
    <head>
        <title>Сделай сам To-Do lists</title>
    </head>
    <body>
        <h1>Сделай сам - Your To-Do list</h1>
        <form method="POST">{% csrf_token %}
        <input name="item_text" id="id_new_item" placeholder="Добавить в список дел" />
        </form>
        <table id="id_list_table">

            <!-- tr><td>{# {{ new_item_text }} #}</td></tr-->
            {% for item in items %}
                <tr><td>1: {{ item.text }}</td></tr>
            {% endfor %}
        
        </table>
    </body>
</html>
```

views.py
```
def index1(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'index1.html', {'items': items})
```

http://127.0.0.1:8000/

settings.py. 
```
[...]
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


```

./manage.py migrate
```
Operations to perform:
  Synchronize unmigrated apps: staticfiles, messages
  Apply all migrations: admin, sessions, auth, todo, contenttypes
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
  Installing custom SQL...
Running migrations:
  Rendering model states... DONE
  Applying todo.0001_initial... OK
  Applying todo.0002_item_text... OK
```

# forloop.counter 
Внутри цикла доступные некоторые дополнительные переменные:

- forloop.counter 
Номер текущей итерации цикла начиная с 1

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


index1.html
```
<html>
    <head>
        <title>Сделай сам To-Do lists</title>
    </head>
    <body>
        <h1>Сделай сам - Your To-Do list</h1>
        <form method="POST">{% csrf_token %}
        <input name="item_text" id="id_new_item" placeholder="Добавить в список дел" />
        </form>
        <table id="id_list_table">

            <!-- tr><td>{# {{ new_item_text }} #}</td></tr-->
            {% for item in items %}
                <!--tr><td>1:{# {{ item.text }}#}</td></tr-->
                <tr><td>{{ forloop.counter }}: {{ item.text }}</td></tr>
            {% endfor %}
        
        </table>
    </body>
</html>
```
