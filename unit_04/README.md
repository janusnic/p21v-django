# p21v-django

## LiveServerTestCase
### class LiveServerTestCase

При работе LiveServerTestCase в фоне запускается встроенный сервер Django, который по завершению тестов выключается. Это позволяет использовать клиенты для автоматического тестирования вместо тестового клиента Django, такие как, например, клиент Selenium. С их помощью вы можете создавать функциональные тесты и симулировать реальное поведение пользователей.

По умолчанию адрес сервера 'localhost:8081' и полный URL в тесте можно получить из атрибута self.live_server_url. Если вы хотите поменять адрес (например порт 8081 уже занят), укажите его при запуске команды test, используя опцию --liveserver, например:
```
$ ./manage.py test --liveserver=localhost:8082
```
Еще один способ поменять адрес тестового сервера, установить переменную окружения DJANGO_LIVE_TEST_SERVER_ADDRESS (например в своем классе запуска тестов):
```
import os
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8082'
```
Если тесты выполняются в нескольких параллельных процессах (например, при сборке нескольких паралельных билдов), они будут пытаться запустить сервер на одном и том же порте, и могут завершаться с ошибкой “Address already in use”. Чтобы избежать такой проблемы, вы можете указать список портов, разделенных запятой, или диапазон портов (количество портов должно соответствовать количеству предполагаемых параллельных процессов). Например:
```
$ ./manage.py test --liveserver=localhost:8082,8090-8100,9000-9200,7041
```
Тогда, при запуске тестов сервер будет перебирать указанные порты, пока не будет найдет свободный.

Чтобы продемонстрировать возможности LiveServerTestCase, давайте напишем простой тест на Selenium. 

```
$ mkdir functional_tests
$ touch functional_tests/__init__.py

$ git mv functional_tests.py functional_tests/tests.py
$ git status # shows the rename to functional_tests/tests.py and __init__.py

```
Мыкет проекта

```
.
├── db.sqlite3
├── functional_tests
│   ├── __init__.py
│   └── tests.py
├── todo
│   ├── admin.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_item_text.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── __pycache__
│   ├── templates
│   │   └── home.html
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
./manage.py test functional_tests
```

Creating test database for alias 'default'...
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (tests.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_04/mysite/functional_tests/tests.py", line 51, in test_can_start_a_list_and_retrieve_it_later
    self.check_for_row_in_list_table('1: Купить бочку апельсинов')
  File "/home/janus/21_perspective/github/p21v-django/unit_04/mysite/functional_tests/tests.py", line 18, in check_for_row_in_list_table
    self.assertIn(row_text, [row.text for row in rows])
AssertionError: '1: Купить бочку апельсинов' not found in ['1: test', '2: test2', '3: Купить бочку апельсинов', '4: Грузить апельсины бочками', '5: Купить бочку апельсинов', '6: Сменить колеса Дрону налету']

----------------------------------------------------------------------
Ran 1 test in 16.780s

FAILED (failures=1)
Destroying test database for alias 'default'...

```

Редактируем functional_tests/tests.py и меняем NewVisitorTest class для использования LiveServerTestCase:

functional_tests/tests.py
```
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):

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
        # self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)

        [...]
```


./manage.py test functional_tests
```
Creating test database for alias 'default'...
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (functional_tests.tests.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_04/mysite/functional_tests/tests.py", line 59, in test_can_start_a_list_and_retrieve_it_later
    self.fail('Finish the test!')
AssertionError: Finish the test!

----------------------------------------------------------------------
Ran 1 test in 15.693s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

./manage.py test 
```
Creating test database for alias 'default'...
........F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (functional_tests.tests.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_04/mysite/functional_tests/tests.py", line 59, in test_can_start_a_list_and_retrieve_it_later
    self.fail('Finish the test!')
AssertionError: Finish the test!

----------------------------------------------------------------------
Ran 9 tests in 15.795s

FAILED (failures=1)
Destroying test database for alias 'default'...
```
$ ./manage.py test todo
```
Creating test database for alias 'default'...
........
----------------------------------------------------------------------
Ran 8 tests in 0.014s

OK
Destroying test database for alias 'default'...

```

# YAGNI!

Принцип «YAGNI» (англ. You Ain't Gonna Need It — «Вам это не понадобится» ronounced yag-knee) — процесс и принцип проектирования ПО, при котором в качестве основной цели и/или ценности декларируется отказ от избыточной функциональности, — т. е. отказ добавления функциональности, в которой нет непосредственной надобности.

Согласно адептам принципа YAGNI, желание писать код, который не нужен прямо сейчас, но может понадобиться в будущем, приводит к следующим нежелательным последствиям:
- Тратится время, которое было бы затрачено на добавление, тестирование и улучшение необходимой функциональности.
- Новые функции должны быть отлажены, документированы и сопровождаться.
- Новая функциональность ограничивает то, что может быть сделано в будущем, — ненужные новые функции могут впоследствии помешать добавить новые нужные.
- Пока новые функции действительно не нужны, трудно полностью предугадать, что они должны делать, и протестировать их. Если новые функции тщательно не протестированы, они могут неправильно работать, когда впоследствии понадобятся.
- Это приводит к тому, что программное обеспечение становится более сложным (подчас чрезмерно сложным).
- Если вся функциональность не документирована, она может так и остаться неизвестной пользователям, но может создать для безопасности пользовательской системы различные риски.
- Добавление новой функциональности может привести к желанию ещё более новой функциональности, приводя к эффекту «снежного кома».


# REST

REST (Representational State Transfer — «передача репрезентативного состояния») — метод взаимодействия компонентов распределённого приложения в сети Интернет, при котором вызов удаленной процедуры представляет собой обычный HTTP-запрос (обычно GET или POST; такой запрос называют REST-запрос), а необходимые данные передаются в качестве параметров запроса. Этот способ является альтернативой более сложным методам, таким как SOAP, CORBA и RPC.
В широком смысле REST поддерживает концепцию построения распределённого приложения, при которой компоненты взаимодействуют наподобие взаимодействия клиентов и серверов во Всемирной паутине.
Хотя данная концепция лежит в самой основе Всемирной паутины, термин REST был введён Роем Филдингом (Roy Fielding), одним из создателей протокола HTTP, лишь в 2000 году. В своей диссертации в Калифорнийском университете в Ирвайне он подвёл теоретическую основу под метод взаимодействия клиентов и серверов во Всемирной паутине, абстрагировав его и назвав «передачей репрезентативного состояния». Филдинг описал концепцию построения распределённого приложения, при которой каждый запрос (REST-запрос) клиента к серверу содержит в себе исчерпывающую информацию о желаемом ответе сервера (желаемом репрезентативном состоянии), и сервер не обязан сохранять информацию о состоянии клиента («клиентской сессии»).

В качестве необходимых условий для построения распределённых REST-приложений Филдинг перечислил следующие:
- Клиент-серверная архитектура.
- Сервер не обязан сохранять информацию о состоянии клиента.
- В каждом запросе клиента должно явно содержаться указание о возможности кэширования ответа и получения ответа из существующего кэша.
- Клиент может взаимодействовать не напрямую с сервером, а с произвольным количеством промежуточных узлов. При этом клиент может не знать о существовании промежуточных узлов, за исключением случаев передачи конфиденциальной информации.
- Унифицированный программный интерфейс сервера. Филдинг приводил URI в качестве примера формата запросов к серверу, а в качестве примера ответа сервера форматы HTML, XML и JSON, различаемые с использованием идентификаторов MIME.

Филдинг указывал, что приложения, не соответствующие приведённым условиям, не могут называться REST-приложениями. Если же все условия соблюдены, то, по его мнению, приложение получит следующие преимущества:
- надёжность (за счёт отсутствия необходимости сохранять информацию о состоянии клиента, которая может быть утеряна);
- производительность (за счёт использования кэша);
- масштабируемость;
- прозрачность системы взаимодействия (особенно необходимая для приложений обслуживания сети);
- простота интерфейсов;
- портативность компонентов;
- лёгкость внесения изменений;
- способность эволюционировать, приспосабливаясь к новым требованиям (на примере Всемирной паутины).

Маршруты

```
    /todo/<list identifier>/

    /lists/new

    /lists/<list identifier>/add_item
```

functional_tests/tests.py. 
```
        inputbox.send_keys('Купить бочку апельсинов')

        # При нажатии клавиши enter на странице появится новый URL и новый 
        # пункт '1: Купить бочку апельсинов' списка дел
        
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/todo/.+')
        self.check_for_row_in_list_table('1: Купить бочку апельсинов')
    [...]


```
Страница снова обновляется
```
# Страница снова обновляется и мы видим новые элементы списка дел
self.check_for_row_in_list_table('1: Купить бочку апельсинов')
self.check_for_row_in_list_table('2: Сменить колеса Дрону налету')
```

``` 
    # Пришел новый пользователь на страницу

    ## Мы используем новую сессию для пользователя 
    # чтобы он работал только со своим списком дел
    self.browser.quit()
    self.browser = webdriver.Firefox()

    # Новый пользователь зашел на страницу. 
    # На странице находится список дел, которые ему не принадлежат
    self.browser.get(self.live_server_url)
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Купить бочку апельсинов', page_text)
    self.assertNotIn('Сменить колеса Дрону налету', page_text)

    # Пользователь Chatlanyn решил добавить новый пукт в список дел 
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Купить гравицапу')
    inputbox.send_keys(Keys.ENTER)

    # Он получает собственный уникальный URL
    chatl_list_url = self.browser.current_url
    self.assertRegex(chatl_list_url, '/todo/.+')
    self.assertNotEqual(chatl_list_url, edith_list_url)

    # Чужой список ему недоступен
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Купить бочку апельсинов', page_text)
    self.assertIn('Купить гравицапу', page_text)

    # Усталые, но довольные мы отправляемся отдыхать

```

./manage.py test
```
Creating test database for alias 'default'...
........F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (functional_tests.tests.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_04/mysite/functional_tests/tests.py", line 46, in test_can_start_a_list_and_retrieve_it_later
    self.assertRegex(edith_list_url, '/todo/.+')
AssertionError: Regex didn't match: '/todo/.+' not found in 'http://localhost:8081/'

----------------------------------------------------------------------
Ran 9 tests in 8.219s

FAILED (failures=1)
```

todo/tests.py
```
self.assertEqual(response.status_code, 302)
self.assertEqual(response['location'], '/todo/the-only-todo-in-the-world/')
```

./manage.py test todo
```
Creating test database for alias 'default'...
.....F..
======================================================================
FAIL: test_home_page_can_save_a_POST_request (todo.tests.ItemModelTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_04/mysite/todo/tests.py", line 88, in test_home_page_can_save_a_POST_request
    self.assertEqual(response['location'], '/todo/the-only-todo-in-the-world/')
AssertionError: '/' != '/todo/the-only-todo-in-the-world/'
- /
+ /todo/the-only-todo-in-the-world/


----------------------------------------------------------------------
Ran 8 tests in 0.015s

FAILED (failures=1)
```
views.py. 
```
def index(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/todo/the-only-todo-in-the-world/')

    items = Item.objects.all()
    return render(request, 'index.html', {'items': items})
```

Добавьте тест
```
class ListViewTest(TestCase):

    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/todo/the-only-todo-in-the-world/') #1

        self.assertContains(response, 'itemey 1') #2
        self.assertContains(response, 'itemey 2') #3

```
./manage.py test todo
```
AssertionError: 404 != 200 : Couldn't retrieve content: Response code was 404 (expected 200)
```
urls.py
```
url(r'^todo/the-only-todo-in-the-world/$', views.view_todo, name='view_todo'),

```
./manage.py test todo
```
AttributeError: 'module' object has no attribute 'view_todo'
```

views.py
```
def view_todo(request):
    pass
```
./manage.py test todo
```
AssertionError: 404 != 200 : Couldn't retrieve content: Response code was 404 (expected 200)
```
views.py
```
def view_todo(request):
    items = Item.objects.all()
    return render(request, 'index.html', {'items': items})
```
./manage.py test todo
```
Creating test database for alias 'default'...
.........
----------------------------------------------------------------------
Ran 9 tests in 0.021s

OK
```

Добавьте тест check that it’s using a different template:

todo/tests.py. 
```
class ListViewTest(TestCase):

    def test_uses_todo_template(self):
        response = self.client.get('/todo/the-only-todo-in-the-world/')
        self.assertTemplateUsed(response, 'todo.html')

    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/todo/the-only-todo-in-the-world/') #1

        self.assertContains(response, 'itemey 1') #2
        self.assertContains(response, 'itemey 2') #3
```

views.py

```
def view_todo(request):
    items = Item.objects.all()
    return render(request, 'todo.html', {'items': items})
```

touch todo/templates/todo.html


./manage.py test todo
```
Creating test database for alias 'default'...
..........
----------------------------------------------------------------------
Ran 10 tests in 0.023s

OK

```
index.html
```
<html>
    <head>
        <title>Сделай сам To-Do lists</title>
    </head>
    <body>
        <h1>Сделай сам - Your To-Do list</h1>
        <form method="POST"  action="/todo/new">{% csrf_token %}
        <input name="item_text" id="id_new_item" placeholder="Добавить в список дел" />
        </form>
        
    </body>
</html>

```

views.py. 
```
def index(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/todo/the-only-todo-in-the-world/')
    return render(request, 'index.html')
```

./manage.py test todo
```
AssertionError: 'itemey 1' not found in '<html>\n    <head>\n        <title>Сделай сам To-Do lists</title>\n    </head>\n    <body>\n        <h1>Сделай сам - Your To-Do list</h1>\n        <form method="POST">\n        <input name="item_text" id="id_new_item" placeholder="Добавить в список дел" />\n        </form>\n        \n    </body>\n</html>'

```

todo.html
```
<html>
    <head>
        <title>Сделай сам To-Do lists</title>
    </head>
    <body>
        <h1>Сделай сам - Your To-Do list</h1>
        <form method="POST" action="/todo/{{ list.id }}/add_item">{% csrf_token %}
        <input name="item_text" id="id_new_item" placeholder="Добавить в список дел" />
        </form>
        <table id="id_list_table">

           
            {% for item in list.item_set.all %}
           
                <tr><td>{{ forloop.counter }}: {{ item.text }}</td></tr>
            {% endfor %}
        
        </table>
    </body>
</html>


```

views.py

```

def index(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/todo/the-only-todo-in-the-world/')
    return render(request, 'index.html')

def view_todo(request):
    items = Item.objects.all()
    return render(request, 'todo.html', {'items': items})
```

./manage.py test todo
```
Creating test database for alias 'default'...
..........
----------------------------------------------------------------------
Ran 10 tests in 0.022s

OK
Destroying test database for alias 'default'...
```

Добавьте тест Class  New List Creation
```
class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/todo/new',
            data={'item_text': 'A new todo item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new todo item')


    def test_redirects_after_POST(self):
        response = self.client.post(
            '/todo/new',
            data={'item_text': 'A new todo item'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/todo/the-only-todo-in-the-world/')
```


urls.py
```
url(r'^todo/new$', views.new_todo, name='new_todo'),
```
views.py

```
def new_todo(request):
    return redirect('/todo/the-only-todo-in-the-world/')


def new_todo(request):
    Item.objects.create(text=request.POST['item_text'])
    
    return redirect('/todo/the-only-todo-in-the-world/')
```

todo/tests.py
```
def test_redirects_after_POST(self):
        response = self.client.post(
            '/todo/new',
            data={'item_text': 'A new todo item'}
        )
        
        self.assertRedirects(response, '/todo/the-only-todo-in-the-world/')

```

todo.html
```
<html>
    <head>
        <title>Сделай сам To-Do lists</title>
    </head>
    <body>
        <h1>Сделай сам - Your To-Do list</h1>
        <form method="POST" action="/todo/new">{% csrf_token %}
        <input name="item_text" id="id_new_item" placeholder="Добавить в список дел" />
        </form>
        <table id="id_list_table">

           
            {% for item in items %}
           
                <tr><td>{{ forloop.counter }}: {{ item.text }}</td></tr>
            {% endfor %}
        
        </table>
    </body>
</html>
```

./manage.py test todo
```
Creating test database for alias 'default'...
............
----------------------------------------------------------------------
Ran 12 tests in 0.029s

OK
Destroying test database for alias 'default'...
```

models.py
```
from django.db import models

class List(models.Model):
    pass

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)
```
 ./manage.py makemigrations
```
Migrations for 'todo':
  0003_auto_20151022_1134.py:
    - Create model List
    - Alter field text on item
    - Add field list to item

```

```    
class ListViewTest(TestCase):

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

```    

```    
from todo.models import Item, List

def new_todo(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    
    return redirect('/todo/the-only-todo-in-the-world/')
```
urls.py

```
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home', views.home_page, name='home'),
    url(r'^$', views.index, name='index'),
    url(r'^todo/the-only-todo-in-the-world/$', views.view_todo, name='view_todo'),
    url(r'^todo/new$', views.new_todo, name='new_todo'),
    url(r'^todo/(.+)/$', views.view_todo, name='view_todo'),
]

```


```
def view_todo(request, list_id):
    items = Item.objects.all()
    return render(request, 'todo.html', {'items': items})


def view_todo(request, list_id):
    
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'todo.html', {'items': items})
```


```    
    def test_redirects_after_POST(self):
        response = self.client.post(
            '/todo/new',
            data={'item_text': 'A new todo item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/todo/%d/' % (new_list.id,))
```

```
def new_todo(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    
    return redirect('/todo/%d/' % (list_.id,))
```


```
# -*- coding:utf-8 -*-
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from todo.views import index
from todo.models import Item, List

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        expected_html = render_to_string('index.html')
        self.assertEqual(response.content.decode(), expected_html)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/todo/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'todo.html')


    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/todo/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)


    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/todo/%d/' % (correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/todo/new',
            data={'item_text': 'A new todo item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new todo item')
   
    def test_redirects_after_POST(self):
        response = self.client.post(
            '/todo/new',
            data={'item_text': 'A new todo item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/todo/%d/' % (new_list.id,))

class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/todo/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)


    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/todo/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/todo/%d/' % (correct_list.id,))

```


```
class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/todo/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'todo.html')


    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/todo/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)


    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/todo/%d/' % (correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)
```


# Как Django обрабатывает запрос

При запросе к странице вашего Django-сайта, используется такой алгоритм для определения какой код выполнить:

- Django определяет какой корневой модуль URLconf использовать. Обычно, это значение настройки ROOT_URLCONF, но, если объект запроса HttpRequest содержит атрибут urlconf (установленный request middleware), его значение будет использоваться вместо ROOT_URLCONF.

- Django загружает модуль конфигурации URL и ищет переменную urlpatterns. Это должен быть список экземпляров django.conf.urls.url().

- Django перебирает каждый URL-шаблон по порядку, и останавливается при первом совпадении с запрошенным URL-ом.

- Если одно из регулярных выражений соответствует URL-у, Django импортирует и вызывает соответствующее представление, которое является просто функцией Python(или представление-класс). При вызове передаются следующие аргументы:

## Объект HttpRequest.

Если в результате применения регулярного выражения получили именованные совпадения, они будут переданы как позиционные аргументы.

Именованные аргументы создаются из именованных совпадений. Они могут быть перезаписаны значениями из аргумента kwargs, переданного в django.conf.urls.url().

Если ни одно регулярное выражение не соответствует, или возникла ошибка на любом из этапов, Django вызывает соответствующий обработчик ошибок. 


Вот пример простого URLconf:
```
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^articles/2003/$', views.special_case_2003),
    url(r'^articles/([0-9]{4})/$', views.year_archive),
    url(r'^articles/([0-9]{4})/([0-9]{2})/$', views.month_archive),
    url(r'^articles/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),
]
```

Не нужно добавлять косую черту в начале, потому что каждый URL содержит его. Например, используйте ^articles, вместо ^/articles.

Символ 'r' перед каждым регулярным выражением не обязателен, но рекомендуется. Он указывает Python что строка “сырая(raw)” и ничего в строке не должно быть экранировано. 


- Запрос к``/articles/2005/03/`` будет обработан третьим элементом списка. Django вызовет функцию views.month_archive(request, '2005', '03').

- /articles/2005/3/ не соответствует ни одному URL-шаблону, потому что третья запись требует две цифры в номере месяца.

- /articles/2003/ соответствует первому выражению, не второму, потому что шаблоны проверяются по порядку. Не стесняйтесь использовать порядок для обработки различных ситуаций, таких как эта.

- /articles/2003 не соответствует ни одному регулярному выражению, потому что каждое ожидает, что URL оканчивается на косую черту.

- /articles/2003/03/03/ соответствует последнему выражению. Django вызовет функцию views.article_detail(request, '2003', '03', '03').

# Именованные группы

Для регулярных выражений в Python синтаксис для именованных совпадений выглядит таким образом (?P<name>pattern), где name это название группы, а pattern – шаблон.

```
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^articles/2003/$', views.special_case_2003),
    url(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    url(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    url(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.article_detail),
]

```

полученные значения передаются в представление как именованные аргументы, а не позиционные. 

- Запрос к /articles/2005/03/ вызовет функцию views.month_archive(request, year='2005', month='03'), вместо views.month_archive(request, '2005', '03').

- Запрос к /articles/2003/03/03/ вызовет views.article_detail(request, year='2003', month='03', day='03').

# Алгоритм соответствия/группировки

- Если существует именованный аргумент, он будет использован вместо позиционного аргумента.

- Иначе все неименованные параметры будут переданы как позиционные аргументы.

- В любом случае дополнительные именованные аргументы будут переданы как именованные. 

### Что использует URLconf при поиске нужного шаблона URL

- URLconf использует запрашиваемый URL как обычную строку Python. Он не учитывает параметры GET, POST и имя домена.

Например, при запросе к http://www.example.com/myapp/, URLconf возьмет myapp/.

- При запросе к http://www.example.com/myapp/?page=3 – myapp/.

URLconf не учитывает тип запроса. POST, GET, HEAD, и др. – будут обработаны одним представлением при одинаковом URL.

## Найденные аргументы – всегда строки

Каждый найденный аргумент передается в представление как строка, независимо от того, какое “совпадение” определено в регулярном выражении. Например, URLconf содержит такую строку:
```
url(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
```
...аргумент year для views.year_archive() будет строкой, несмотря на то, что [0-9]{4} отлавливает только числа.

## Значения по умолчанию для аргументов представления

Принято указывать значения по-умолчанию для аргументов представления. Пример URLconf и представления:
```
# URLconf
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^blog/$', views.page),
    url(r'^blog/page(?P<num>[0-9]+)/$', views.page),
]
```
# View (in blog/views.py)
```
def page(request, num="1"):
    # Output the appropriate page of blog entries, according to num.
    ...
```
оба URL-шаблона указывают на одно представление – views.page – но первый шаблон не принимает аргументы в URL. Если первый шаблон будет выбран, функция page() будет использовать значение по-умолчанию аргумента num равное "1". Если будет выбран другой шаблон, page() будет использовать значение num из URL, которое найдет регулярное выражение.

Каждое регулярное выражение в urlpatterns будет скомпилировано при первом использовании.

## Синтаксис переменной urlpatterns

urlpatterns должен быть списком экземпляров url().

## Обработчики ошибок

Если Django не может найти подходящий шаблон URL, или было вызвано исключение в процессе обработки запроса, Django вызовет соответствующее представление обрабатывающее ошибку.

Эти представления определены в четырёх переменных. Их значения по-умолчанию должны подойти для большинства проектов, но вы можете их поменять при необходимости.

Эти значения должны быть определены в главном URLconf.

Значение это функции, или полный путь для импорта, которая будет вызвана, если не был найден подходящий URL-шаблон.

Есть следующие переменные:

- handler404 – Смотрите django.conf.urls.handler404.

- handler500 – Смотрите django.conf.urls.handler500.

- handler403 – Смотрите django.conf.urls.handler403.

- handler400 – Смотрите django.conf.urls.handler400.

# Комбинирование URLconfs

В любой момент, ваш urlpatterns может “включать” другие модули URLconf.

Вот пример URLconf для сайта Django. Он включает множество других конфигураций URL:
```
from django.conf.urls import include, url

urlpatterns = [
    # ... snip ...
    url(r'^community/', include('django_website.aggregator.urls')),
    url(r'^contact/', include('django_website.contact.urls')),
    # ... snip ...
]
```
Заметим, что регулярные выражения не содержат $ (определитель конца строки), но содержит косую черту в конце. Каждый раз, когда Django встречает include() (django.conf.urls.include()), из URL обрезается уже совпавшая часть, остальное передается во включенный URLconf для дальнейшей обработки.


urls.py
```
from django.conf.urls import include, url
from django.contrib import admin
from todo import views
from todo import urls as todo_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home', views.home_page, name='home'),
    url(r'^$', views.index, name='index'),
    url(r'^todo/', include(todo_urls)),
]

```

todo/urls.py

```
from django.conf.urls import url

from todo import views

urlpatterns = [
    url(r'^new$', views.new_todo, name='new_todo'),
    url(r'^(\d+)/$', views.view_todo, name='view_todo'),
    url(r'^(\d+)/add_item$', views.add_item, name='add_item'),
]


```
models.py
```
from django.db import models
from django.core.urlresolvers import reverse


class List(models.Model):

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)


```


Blog
```
    
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    description = models.TextField(max_length=4096)
        
    views_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    views_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
        
    status = models.IntegerField(default=0)
    enable_comment = models.BooleanField(default=True)
    content = models.TextField()

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
        
    publish_date = models.DateTimeField(auto_now=True)

    created_date = models.DateTimeField(auto_now_add=True)
        
    views_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title    


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('status', models.IntegerField(default=0)),
                ('enable_comment', models.BooleanField(default=True)),
                ('content', models.TextField()),
                ('publish_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('views_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=4096)),
                ('views_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('views_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(to='blog.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.Tag'),
        ),
    ]
```