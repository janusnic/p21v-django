# p21v-django unit 02

# Selenium

http://docs.seleniumhq.org/

Selenium – это проект, в рамках которого разрабатывается серия программных продуктов с открытым исходным кодом (open source):

- Selenium WebDriver,
- Selenium RC,
- Selenium Server,
- Selenium Grid,
- Selenium IDE.

Называть просто словом Selenium любой из этих пяти продуктов, вообще говоря, неправильно, хотя так часто делают, если из контекста понятно, о каком именно из продуктов идёт речь, или если речь идёт о нескольких продуктах одновременно, или обо всех сразу.

## Selenium RC

Selenium RC – это предыдущая версия библиотеки для управления браузерами. Аббревиатура RC в названии этого продукта расшифровывается как Remote Control, то есть это средство для «удалённого» управления браузером.

## Selenium Server

Selenium Server – это сервер, который позволяет управлять браузером с удалённой машины, по сети. 

## Selenium Grid

Selenium Grid – это кластер, состоящий из нескольких Selenium-серверов. 

## Selenium IDE

Selenium IDE – плагин к браузеру Firefox, который может записывать действия пользователя, воспроизводить их, а также генерировать код для WebDriver или Selenium RC, в котором выполняются те же самые действия.


# Selenium WebDriver

http://selenium-python.readthedocs.org/en/latest/api.html

Selenium WebDriver – это программная библиотека для управления браузерами. WebDriver представляет собой драйверы для различных браузеров и клиентские библиотеки на разных языках программирования, предназначенные для управления этими драйверами.

Часто употребляется также более короткое название WebDriver.

использование такого веб-драйвера сводится к созданию бота, выполняющего всю ручную работу с браузером автоматизированно.

Библиотеки WebDriver доступны на языках Java, .Net (C#), Python, Ruby, JavaScript, драйверы реализованы для браузеров Firefox, InternetExplorer, Safari, Andriod, iOS (а также Chrome и Opera).

Чаще всего Selenium WebDriver используется для тестирования функционала веб-сайтов/веб-ориентированных приложений. Автоматизированное тестирование удобно, потому что позволяет многократно запускать повторяющиеся тесты. Регрессионное тестирование, то есть, проверка, что старый код не перестал работать правильно после внесения новых изменений, является типичным примером, когда необходима автоматизация. WebDriver предоставляет все необходимые методы, обеспечивает высокую скорость теста и гарантирует корректность проверки (поскольку человеский фактор исключен). В официальной документации Selenium приводятся следующие плюсы автоматизированного тестирования веб-приложений:

- возможность проводить чаще регрессионное тестирование;
- быстрое предоставление разработчикам отчета о состоянии продукта;
- получение потенциально бесконечного числа прогонов тестов;
- обеспечение поддержки Agile и экстремальным методам разработки;
- сохранение строгой документации тестов;
- обнаружение ошибок, которые были пропущены на стадии ручного тестирования.

Привязка Python-Selenium предоставляет удобный API для доступа к таким веб-драйверам Selenium как Firefox, Ie, Chrome, Remote и других. На данный момент поддерживаются версии Python 2.7, 3.2, 3.3 и 3.4.

# Загрузка Selenium для Python
```
pip install selenium
```

## В виртуальное окружение ставим Selenium
```
$ workon env2

(env2)$ pip install django==1.8.5 
(env2)$ pip install selenium
(env2)$ pip install mock
(env2)$ pip install unittest2 # (only if using Python 2.6)
```

# Подробная инструкция для пользователей Windows

1. Установите Python 3.4 через файл MSI, доступный на странице загрузок сайта python.org.
2. Запустите командную строку через программу cmd.exe и запустите команду pip установки selenium.
```
C:\Python34\Scripts\pip.exe install selenium
```
Теперь вы можете запускать свои тестовые скрипты, используя Python:
```
C:\Python34\python.exe C:\my_selenium_script.py
```

pip list

```
Django (1.8.5)
mock (1.3.0)
pbr (1.8.1)
pip (7.1.2)
pytz (2015.2)
selenium (2.48.0)
setuptools (15.0)
six (1.10.0)

```
## Проверка работы selenium
test.py
```
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # начиная с версии 2.4.0
from selenium.webdriver.support import expected_conditions as EC # начиная с версии 2.26.0

# Создаем новый instance от Firefox driver
driver = webdriver.Firefox()

# идем на страницу google
# Метод driver.get перенаправляет к странице URL. 
# WebDriver будет ждать пока страница не загрузится полностью (то есть, событие “onload” игнорируется), прежде чем передать контроль вашему тесту или скрипту. Стоит отметить, что если страница использует много AJAX-кода при загрузке, то WebDriver может не распознать, загрузилась ли она полностью:
driver.get("http://www.google.com")

# страница динамическая, поэтому title найдем здесь:
print (driver.title)

# Google

assert "Google" in driver.title

# это утверждение (assertion), что заголовок содержит слово “Google” [assert позволяет проверять предположения о значениях произвольных данных в произвольном месте программы. По своей сути assert напоминает констатацию факта, расположенную посреди кода программы. В случаях, когда произнесенное утверждение не верно, assert возбуждает исключение. Такое поведение позволяет контролировать выполнение программы в строго определенном русле. Отличие assert от условий заключается в том, что программа с assert не приемлет иного хода событий, считая дальнейшее выполнение программы или функции бессмысленным.]

# WebDriver предоставляет ряд способов получения элементов с помощью методов find_element_by_*. Для примера, элемент ввода текста input может быть найден по его атрибуту name методом find_element_by_name. 

# найдем элемент с атрибутом name = q (google search box)
inputElement = driver.find_element_by_name("q")

# После этого мы посылаем нажатия клавиш (аналогично введению клавиш с клавиатуры). Специальные команды могут быть переданы с помощью класса Keys импортированного из selenium.webdriver.common.keys
# inputElement.send_keys(Keys.RETURN)

# набираем строку поиска
inputElement.send_keys("cheese!")

# сабмитим форму (обычно google автоматически выполняет поиск без submitting)
inputElement.submit()

# После ответа страницы, вы получите результат, если таковой ожидается. Чтобы удостовериться, что мы получили какой-либо результат, добавим утверждение:

# assert "No results found." not in driver.page_source

try:
    # ждем обновления страницы, ждем обновления title
    WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))

    # Должны увидеть "cheese! - Поиск в Google"
    print (driver.title)

# В завершение, окно браузера закрывается. Вы можете также вызывать метод quit вместо close. Метод quit закроет браузер полностью, в то время как close закроет одну вкладку. Однако, в случае, когда открыта только одна вкладка, по умолчанию большинство браузеров закрывается полностью:
finally:
    driver.quit()
```

python test.py 

```
Google
cheese! - Поиск в Google
```
## Selenium для написания тестов
Selenium чаще всего используется для написания тестовых ситуаций. Сам пакет selenium не предоставляет никаких тестовых утилит или инструментов разработки. Вы можете писать тесты с помощью модуля Python unittest. Другим вашим выбором в качестве тестовых утилит/инструментов разработки могут стать py.test и nose.

### тесты с помощью модуля Python unittest
Данный скрипт тестирует функциональность поиска на сайте www.google.com:

test_search.py
```
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Сначала были импортированы все основные необходимые модули. Модуль unittest встроен в Python и реализован на Java’s JUnit. Этот модуль предоставляет собой утилиту для организации тестов.

# Класс теста унаследован от unittest.TestCase. Наследование класса TestCase является способом сообщения модулю unittest, что это тест:

class PythonOrgSearch(unittest.TestCase):

# setUp — это часть инициализации, этот метод будет вызываться перед каждым методом теста, который вы собираетесь написать внутри класса теста. Здесь мы создаем элемент класса Firefox WebDriver.

    def setUp(self):
        self.driver = webdriver.Firefox()

# Метод теста всегда должен начинаться с фразы test. Первая строка метода создает локальную ссылку на объект драйвера, созданный методом setUp.

    def test_search_in_python_org(self):
        driver = self.driver

        # Метод driver.get перенаправляет к странице URL в параметре. WebDriver будет ждать пока страница не загрузится полностью (то есть, событие “onload” игнорируется), прежде чем передать контроль вашему тесту или скрипту. 

        driver.get("http://www.google.com")

        # утверждение, что заголовок содержит слово “Google”:

        self.assertIn("Google", driver.title)
        
        # WebDriver предоставляет ряд способов получения элементов с помощью методов find_element_by_*. Для примера, элемент ввода текста input может быть найден по его атрибуту name методом find_element_by_name. 

        elem = driver.find_element_by_name("q")

        # После этого мы посылаем нажатия клавиш (аналогично введению клавиш с клавиатуры). Специальные команды могут быть переданы с помощью класса Keys импортированного из selenium.webdriver.common.keys:

        elem.send_keys("django")

        # После ответа страницы, вы получите результат, если таковой ожидается. Чтобы удостовериться, что мы получили какой-либо результат, добавим утверждение:

        assert "No results found." not in driver.page_source
        elem.send_keys(Keys.RETURN)

    # Метод tearDown будет вызван после каждого метода теста. Это метод для действий чистки. В текущем методе реализовано закрытие окна браузера. Вы можете также вызывать метод quit вместо close. Метод quit закроет браузер полностью, в то время как close закроет одну вкладку. Однако, в случае, когда открыта только одна вкладка, по умолчанию большинство браузеров закрывается полностью.:

    def tearDown(self):
        self.driver.close()

# Завершающий код — это стандартная вставка кода для запуска набора тестов [Сравнение __name__ с "__main__" означает, что модуль (файл программы) запущен как отдельная программа («main» — «основная», «главная») (а не импортирован из другого модуля). Если вы импортируете модуль, атрибут модуля __name__ будет равен имени файла без каталога и расширения.]:

if __name__ == "__main__":
    unittest.main()
```

запустить тест python test_search.py 

```
.
----------------------------------------------------------------------
Ran 1 test in 22.895s

OK

```
тест завершился успешно



django-admin startproject mysite

```
-- mysite
    |-- manage.py
    `-- mysite
        |-- __init__.py
        |-- settings.py
        |-- urls.py
        `-- wsgi.py
```

cd mysite

python manage.py runserver

```
./manage.py runserver

Performing system checks...

System check identified no issues (0 silenced).

You have unapplied migrations; your app may not work properly until they are applied.
Run 'python manage.py migrate' to apply them.

October 14, 2015 - 11:13:40
Django version 1.8.5, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

```

## Наш первый functional test для нашего сайта: 

test0.py

```
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title

```
test1.py

```
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title

print (browser.title)

try:
    
    WebDriverWait(browser, 10).until(EC.title_contains("Welcome"))

    # You should see "Welcome to Django This is my cool Site!"
    print (browser.title,' This is my cool Site!')

finally:
    browser.quit()
```


python test1.py 

```
Welcome to Django
Welcome to Django  This is my cool Site!
```

# Functional Test == Acceptance Test == End-to-End Test

test_hello.py
```
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'This is my cool Site!' in browser.title

print (browser.title)

try:
    
    WebDriverWait(browser, 10).until(EC.title_contains("Site"))

 
    print (browser.title)

finally:
    browser.quit()

```
python test_hello.py 
```
Traceback (most recent call last):
  File "test_hello.py", line 9, in <module>
    assert 'This is my cool Site!' in browser.title
AssertionError
```
test_welcome.py 
```
# Сначала были импортированы все основные необходимые модули. Модуль unittest встроен в Python и реализован на Java’s JUnit. Этот модуль предоставляет собой утилиту для организации тестов.

from selenium import webdriver
import unittest

# Класс теста унаследован от unittest.TestCase. Наследование класса TestCase является способом сообщения модулю unittest, что это тест:

class NewVisitorTest(unittest.TestCase):  

    # setUp — это часть инициализации, этот метод будет вызываться перед каждым методом теста, который вы собираетесь написать внутри класса теста. Здесь мы создаем элемент класса Firefox WebDriver.

    def setUp(self):  
        self.browser = webdriver.Firefox()

    # Метод tearDown будет вызван после каждого метода теста. Это метод для действий чистки. В текущем методе реализовано закрытие окна браузера. Вы можете также вызывать метод quit вместо close. Метод quit закроет браузер полностью, в то время как close закроет одну вкладку. Однако, в случае, когда открыта только одна вкладка, по умолчанию большинство браузеров закрывается полностью.:

    def tearDown(self):  
        self.browser.quit()

    # Метод теста всегда должен начинаться с фразы test. Первая строка метода создает локальную ссылку на объект драйвера, созданный методом setUp.
    
    def test_can_start_a_list_and_retrieve_it_later(self):  
        
        # Метод driver.get перенаправляет к странице URL в параметре. WebDriver будет ждать пока страница не загрузится полностью (то есть, событие “onload” игнорируется), прежде чем передать контроль вашему тесту или скрипту. 

        self.browser.get('http://localhost:8000')
        
        # утверждение, что заголовок содержит слово “This is my cool Site!”:
        self.assertIn('This is my cool Site!', self.browser.title)  
        
        # self.fail ничего не получилось, генерирует сообщение об ошибке. Используется в качестве напоминания, чтобы закончить тест.

        self.fail('Finish the test!')  
            
# Завершающий код — это стандартная вставка кода для запуска набора тестов [Сравнение __name__ с "__main__" означает, что модуль (файл программы) запущен как отдельная программа («main» — «основная», «главная») (а не импортирован из другого модуля). Если вы импортируете модуль, атрибут модуля __name__ будет равен имени файла без каталога и расширения.]:

if __name__ == '__main__':  
    unittest.main(warnings='ignore')  
```
warnings='ignore' подавляет избыточные предупреждения ResourceWarning,  которые генерируются в момент выполнения. 


python test_welcome.py 
```
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_welcome.py", line 18, in test_can_start_a_list_and_retrieve_it_later
    self.assertIn('This is my cool Site!', self.browser.title)
AssertionError: 'This is my cool Site!' not found in 'Welcome to Django'

----------------------------------------------------------------------
Ran 1 test in 13.133s

FAILED (failures=1)

```
# Implicit waits - Неявные ожидания
добавить implicitly_wait в настройки setUp:

```
    def setUp(self):  
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

```
git status
```
$ git diff
$ git commit -a
```

# Django admin site

./manage.py syncdb
```
/home/janus/Envs/env2/lib/python3.4/site-packages/django/core/management/commands/syncdb.py:24: RemovedInDjango19Warning: The syncdb command will be removed in Django 1.9
  warnings.warn("The syncdb command will be removed in Django 1.9", RemovedInDjango19Warning)

Operations to perform:
  Synchronize unmigrated apps: messages, staticfiles
  Apply all migrations: auth, admin, sessions, contenttypes
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
  Installing custom SQL...
Running migrations:
  Rendering model states... DONE
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying sessions.0001_initial... OK

You have installed Django's auth system, and don't have any superusers defined.
Would you like to create one now? (yes/no): yes
Username (leave blank to use 'janus'): 
Email address: janus@ex.ua
Password: 
Password (again): 
Superuser created successfully.
```
git commit

```
$ echo "db.sqlite3" >> .gitignore

$ git add .
$ git status
$ git add .gitignore
$ git commit
```


./manage.py startapp todo

```
mysite/
├── db.sqlite3
├── functional_tests.py
├── todo
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

## Unit Tests

Основное различие между юнит-тестами и функциональными тестами является то, что функциональные тесты используются для тестирования приложения с точки зрения пользователя. Модульные тесты используются для тестирования приложения с точки зрения программиста.

TDD подход будет выглядеть как-нибудь так:

- Начнем с написания функциональных тестов, описывая новые возможности с точки зрения пользователя.
- После того, как у нас есть функциональный тест, который не удается, мы начинаем думать о том, как написать код, который может заставить его пройти (или по крайней мере пройти его нынешнем недостаточности). Сейчас мы используем один или несколько юнит-тестов, чтобы определить, как должен вести себя наш код.
- После того, как у нас есть модульный тест и он не проходит, мы пишем некоторое количество кода приложения, достаточное чтобы пройти модульный тест. Мы можем повторять шаги 2 и 3 несколько раз, пока не получим желаемое.
Теперь мы можем повторно вызвать наши функциональные тесты и посмотреть, проходят ли они. 

# Unit Testing in Django

todo/test.py

```
from django.test import TestCase

# Create your tests here.
```

todo/test.py
```
from django.test import TestCase

# Create your tests here.
class EqualTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 3)
```
./manage.py test      
```
======================================================================
FAIL: test_bad_maths (todo.tests.EqualTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_02/mysite/todo/tests.py", line 7, in test_bad_maths
    self.assertEqual(1 + 1, 3)
AssertionError: 2 != 3

```

# Django MVC, URLs, and View Functions

### Рабочий процесс в Django:

- HTTP-запрос приходит на определенной URL.
- Django использует некоторые правила и решает, какой метод контроллера должен откликнуться на запрос (это называется разрешением URL).
- Метод контроллера обрабатывает запрос и возвращает ответ HTTP.

Проверим две идеи:

- Можем ли мы разрешить URL для корня сайта ("/") и в каком методе это сделать?
- Может ли метод вернуть некоторый HTML, который получит функциональный тест?

todo/tests.py. 

```
from django.core.urlresolvers import resolve
from django.test import TestCase
from todo.views import home_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')  
        self.assertEqual(found.func, home_page)  

```

При вызове "/"(корень сайта), Django находит метод с именем home_page.

Что это за метод? Этот метод мы напишем позже. Мы планируем сохранить его в todo/tests.py.

todo/views.py. 
```
from django.shortcuts import render

# Create your views here.
home_page = None

```

./manage.py test
```
Creating test database for alias 'default'...
FEEF
======================================================================
ERROR: test_root_url_resolves_to_home_page_view (todo.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_02/mysite/todo/tests.py", line 8, in test_root_url_resolves_to_home_page_view
    found = resolve('/')
  File "/home/janus/Envs/env2/lib/python3.4/site-packages/django/core/urlresolvers.py", line 521, in resolve
    return get_resolver(urlconf).resolve(path)
  File "/home/janus/Envs/env2/lib/python3.4/site-packages/django/core/urlresolvers.py", line 387, in resolve
    raise Resolver404({'tried': tried, 'path': new_path})
django.core.urlresolvers.Resolver404: {'tried': [[<RegexURLResolver <RegexURLPattern list> (admin:admin) ^admin/>]], 'path': ''}

```

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

from todo import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^admin/', include(admin.site.urls)),
]
```
./manage.py test
```
Creating test database for alias 'default'...
FEEEEF
======================================================================
ERROR: test_root_url_resolves_to_home_page_view (todo.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_02/mysite/todo/tests.py", line 8, in test_root_url_resolves_to_home_page_view
    found = resolve('/')
  File "/home/janus/Envs/env2/lib/python3.4/site-packages/django/core/urlresolvers.py", line 521, in resolve
    return get_resolver(urlconf).resolve(path)
  File "/home/janus/Envs/env2/lib/python3.4/site-packages/django/core/urlresolvers.py", line 367, in resolve
    sub_match = pattern.resolve(new_path)
  File "/home/janus/Envs/env2/lib/python3.4/site-packages/django/core/urlresolvers.py", line 239, in resolve
    return ResolverMatch(self.callback, args, kwargs, self.name)
  File "/home/janus/Envs/env2/lib/python3.4/site-packages/django/core/urlresolvers.py", line 246, in callback
    self._callback = get_callable(self._callback_str)
  File "/home/janus/Envs/env2/lib/python3.4/functools.py", line 428, in wrapper
    result = user_function(*args, **kwds)
  File "/home/janus/Envs/env2/lib/python3.4/site-packages/django/core/urlresolvers.py", line 95, in get_callable
    mod_name, func_name = get_mod_func(lookup_view)
  File "/home/janus/Envs/env2/lib/python3.4/site-packages/django/core/urlresolvers.py", line 158, in get_mod_func
    dot = callback.rindex('.')
AttributeError: 'NoneType' object has no attribute 'rindex'
```

todo/views.py. 
```
from django.shortcuts import render

# Create your views here.
def home_page():
    pass
```

./manage.py test
```
Creating test database for alias 'default'...
..
----------------------------------------------------------------------
Ran 2 tests in 0.002s

OK
Destroying test database for alias 'default'...
```


## Unit Test методов

todo/tests.py. 
```
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from todo.views import home_page 

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/') 
        self.assertEqual(found.func, home_page) 

    def test_home_page_returns_correct_html(self):

        # создали HttpRequest object, который использует Django когда пользователь запрашивает страницу.

        request = HttpRequest()  
        
        # перенаправляем запрос на метод home_page view, который формирует response - экземпляр класса HttpResponse. Далее проверяем является ли .content в response HTML-текстом который мы отдаем пользователю.

        response = home_page(request)  
        
        # HTML-текст должен начинаться с html тега, который должен закрываться вконце. response.content является сырым литералом (raw bytes), а не Python-строкой, поэтому мы используем b'' синтаксис.

        self.assertTrue(response.content.startswith(b'<html>'))  
        
        # Мы хотим поместить тег title, содержащий наш заголовок.

        self.assertIn(b'<title>Welcome to Django. This is my cool Site!</title>', response.content)  
        self.assertTrue(response.content.endswith(b'</html>'))  


class EqualTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 2)
```

./manage.py test

```
Creating test database for alias 'default'...
...E.
======================================================================
ERROR: test_home_page_returns_correct_html (todo.tests_home.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_02/mysite/todo/tests_home.py", line 15, in test_home_page_returns_correct_html
    response = home_page(request)
TypeError: home_page() takes 0 positional arguments but 1 was given

----------------------------------------------------------------------
Ran 5 tests in 0.003s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

todo/views.py. 
```
def home_page(request):
    pass
```
./manage.py test
```
Creating test database for alias 'default'...
...E.
======================================================================
ERROR: test_home_page_returns_correct_html (todo.tests_home.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_02/mysite/todo/tests_home.py", line 16, in test_home_page_returns_correct_html
    self.assertTrue(response.content.startswith(b'<html>'))
AttributeError: 'NoneType' object has no attribute 'content'

----------------------------------------------------------------------
Ran 5 tests in 0.003s

FAILED (errors=1)
Destroying test database for alias 'default'...
```
todo/views.py. 
```
from django.http import HttpResponse

# Create your views here.

def home_page(request):
    return HttpResponse()
```

./manage.py test
```
Creating test database for alias 'default'...
...F.
======================================================================
FAIL: test_home_page_returns_correct_html (todo.tests_home.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_02/mysite/todo/tests_home.py", line 16, in test_home_page_returns_correct_html
    self.assertTrue(response.content.startswith(b'<html>'))
AssertionError: False is not true

----------------------------------------------------------------------
Ran 5 tests in 0.003s

FAILED (failures=1)
Destroying test database for alias 'default'...

```

todo/views.py. 

```
from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):

    return HttpResponse("<html><title>Welcome to Django. This is my cool Site!</title>")

```

./manage.py test
```
Creating test database for alias 'default'...
...F.
======================================================================
FAIL: test_home_page_returns_correct_html (todo.tests_home.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/21_perspective/github/p21v-django/unit_02/mysite/todo/tests_home.py", line 18, in test_home_page_returns_correct_html
    self.assertTrue(response.content.endswith(b'</html>'))
AssertionError: False is not true

----------------------------------------------------------------------
Ran 5 tests in 0.003s

FAILED (failures=1)
Destroying test database for alias 'default'...

```

todo/views.py. 

```
from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):

    return HttpResponse("<html><title>Welcome to Django. This is my cool Site!</title></html>")

```
./manage.py test
```
Creating test database for alias 'default'...
.....
----------------------------------------------------------------------
Ran 5 tests in 0.003s

OK
Destroying test database for alias 'default'...
```

python test_welcome.py 
```
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_welcome.py", line 19, in test_can_start_a_list_and_retrieve_it_later
    self.fail('Finish the test!')
AssertionError: Finish the test!

----------------------------------------------------------------------
Ran 1 test in 4.182s

FAILED (failures=1)
```

$ git log --oneline
