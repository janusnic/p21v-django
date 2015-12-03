## p21v-django unit 16

Размещение Django app на PythonAnywhere
=======================================

www.pythonanywhere.com

1. Создание PythonAnywhere Account
--------------------------------------
Зарегистрировать, создать бесплатный аккаунт уровня "Beginner" на PythonAnywhere - https://www.pythonanywhere.com/pricing/.
После слздания вашего account, доменное имя вашего проекта будет - http://username.pythonanywhere.com, где username - ваш PythonAnywhere username. 

2. PythonAnywhere Web Interface
-----------------------------------
PythonAnywhere web interface сожержит dashboard со следующим функцилналом:

- вкладка consoles, позволяет запускать Python и Bash скрипты;
- вкладка files, управление вашими файлами;
- вкладка web, позволяет конфигурировать ваши установки для хлстинга web application;
- вкладка schedule, позволяет запускать ваши задачи;
- вкладка databases, для конфигурации базы данных MySQL.

PythonAnywhere wiki - https://www.pythonanywhere.com/wiki/.

3. Создание Virtual Environment
---------------------------------

1. Зарегистрипутесь на PythonAnywhere и создайте новое Web app:
2. Перейти в "Web" tab.
3. Выберите "Add a new web app" слева. Нажмите "Next"
4. Выбрать "Manual configuration". Нажмите "Next" - дождитесь создания приложения.
5. Адрес вашего web app -- yourusername.pythonanywhere.com.

Создадим собственное virtualenv и изменим Virtualenv path option.

Создание virtualenv и установка django
----------------------------------------
1. Перейти в "Consoles" tab м запустить Bash console
```
~ $ mkvirtualenv django18
```
- Если хотите использовать Python 3 в virtualenv, используйте mkvirtualenv --python=/usr/bin/python3.4 django18

- Если возникла ошибка mkvirtualenv: command not found, установите VirtualenvWrapper.

```
echo '' >> ~/.bashrc && echo 'source virtualenvwrapper.sh' >> .bashrc

source virtualenvwrapper.sh
```

Проверим pip:

```
(django18) ~ $ which pip
/home/myusername/.virtualenvs/django18/bin/pip

```

Если pip не найден, активируйте virtualenv:
-------------------------------------------
```
workon django18
```

Установить Django:
-------------------
```
(django18) ~ $ pip install django==1.8.7
```
Проверить:
```
(django18) ~ $ which django-admin.py
/home/myusername/.virtualenvs/django18/bin/django-admin.py

(django18) ~ $ django-admin.py --version
1.8.7
```
Создать новый django project:
-----------------------------
(django18) ~ $ django-admin.py startproject mysite

Проверить:
----------------
```
(django18) ~ $ tree mysite
mysite
├── manage.py
└── mysite
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

Использование virtualenv в вашем web app
----------------------------------------
Перейти в Web tab и отредактировать WSGI file:
```
# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys

# assuming your django settings file is at '/home/myusername/mysite/mysite/settings.py'
path = '/home/myusername/mysite'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

```
- Затем отредактировать ауть к вашему virtualenv в секции Virtualenv. Необходимо указать полный путь, /home/myusername/.virtualenvs/django18, или короткое имя virtualenv, _django18.
- Сохранить изменения, нпжать кнопку Reload для вашего домена.

Проверить.
----------
Перейти на сайт -- должны увидеть "it worked!" page.

Extra packages
--------------
Для установки MySQL:
```
(django18) ~/mysite $ pip install mysql-python
```
Static files
--------------

- Перейти в "Web" tab, выбрать domain, выбрать "Static files" table:
- Нажать "Enter URL" и ввести /static/admin/.
- Нажать "Enter path" и ввести /home/myusername/.virtualenvs/django18/lib/python2.7/site-packages/django/contrib/admin/static/admin.
- Нажать кнопку Reload.

Работа с вашим virtualenv
-------------------------------

Если нудно установить новый пакет, нужно запустить:
```
(django18) ~ $ source virtualenvwrapper.sh
```
и
```
(django18) ~ $ workon django18
```

из GitHub на PythonAnywhere
---------------------------
загрузим наш код из GitHub на PythonAnywhere, создав "клон" репозитория. 
Ввести следующую команду в консоли на PythonAnywhere (заменить your-github-username на свою учётку GitHub):

```
$ git clone https://github.com/your-github-username/myblog.git
```
Эта команда загрузит копию кода на PythonAnywhere. 

Проверить
```
tree myblog
```
Сбор статических файлов.
------------------------

whitenoise - Это утилита для работы с статическими файлами. 

нужно запускать дополнительную команду collectstatic, на сервере. Это даст Django знать, что он должен собрать все статические файлы, которые потребуются серверу.

```
(django18) $ python manage.py collectstatic

```
Создаем базу данных на PythonAnywhere
---------------------------------------

Нам нужно инициализировать базу данных на сервере с помощью команд migrate и createsuperuser:
```
(django18) ~ $ python manage.py migrate

(django18) ~ $ python manage.py createsuperuser
```

Хостинг на Heroku - Размещение Django app на Heroku
====================================================

Heroku была одной из первых платформ, предоставляющих услуги PaaS. В начале, она предлагала услуги размещения только Ruby приложений, но позднее была включена поддержка многих других языков таких как Java, Node.js и нашего фаворита, Python.

для развертывания приложения на Heroku требуется лишь загрузить приложение при помощи git. Heroku ищет файл Procfile в корневой папке приложения для получения инструкций как приложение должно выполняться. Для Python проектов Heroku также ожидает увидеть файл requirements.txt, содержащий список необходимых сторонних пакетов.

После загрузки приложения Heroku применит свою магию и приложение будет доступно онлайн через считанные секунды. 

Установка клиента Heroku
------------------------
Heroku предлагает утилиту «Heroku клиент», которой мы будем пользоваться для создания и управления нашим приложением. Эта утилита может быть запущена под управлением Windows, Mac OS X и Linux. 

Установка Heroku
----------------
- Создать Heroku user account http://heroku.com/
- Установить Heroku Toolbelt https://toolbelt.heroku.com/
- Доступ к Heroku осуществояется с помощью command-line client https://devcenter.heroku.com/categories/command-line

Для входа на Heroku:
--------------------
```
$ heroku login
```
Heroku запросит у вас email и пароль от вашего аккаунта. При первой авторизации, клиент отправит ваш ssh ключ на сервера Heroku.

Последующие команды можно будет выполнять без авторизации.

Создание базы данных Heroku PostgreSQL
--------------------------------------

Для создания базы данных мы используем клиент Heroku:
heroku addons:add heroku-postgresql:dev

После установки django-toolbelt будут установлены слудующие packages:

– django
– psycopg2
– gunicorn (WSGI server)
– dj-database-url (a Django configuration helper)
– dj-static (a Django static file server)


Из вашего virtual environment active:
-------------------------------------
```
$ pip install django-toolbelt
```
Веб сервер
----------
Heroku не предоставляет свой веб сервер. Вместо этого, ожидает что приложение запустит свой собственный сервер на порту, номер которого получит из переменной окружения $PORT.

Procfile
---------
https://devcenter.heroku.com/articles/procfile

Последнее требование состоит в том, чтобы сообщить Heroku как запустить приложение. Для этого Heroku требуется файл Procfile в корневой папке приложения.

Этот файл весьма прост, он просто определяет имена процессов и команды ассоциированные с ними (файл Procfile):

```
web: gunicorn myapp.wsgi
```
Для использования локальной версии Procfile и Foreman:
```
$ foreman start
```
Dependencies Файл requirements.txt
----------------------------------

На нашем локальном ПК, мы управляли зависимостями при помощи виртуального окружения, устанавливая в него модули при помощи pip.

Heroku поступает похожим образом. Если файл requirements.txt обнаруживается в корневой папке приложения, то Heroku устанавливает все модули перечисленные в нем при помощи pip.

Для создания файла requirements.txt мы должны использовать опцию freeze при вызове pip

```
$ pip freeze > requirements.txt
```
В список необходимо добавить сервер gunicorn, а также драйвер psycopg2, который необходим SQLAlchemy для подключения к базе данных PostgreSQL. 

Django settings
----------------
Изменмить settings.py:

1. Изменить:
```
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ALLOWED_HOSTS = [‘yourappname.herokuapp.com’]
```

2. После DATABASES declaration:
```
import dj_database_url

DATABASES = {'default': dj_database_url.config()}

```
3. В конце файла:
```
SECURE_PROXY_SSL_HEADER = (‘HTTP_X_FORWARDED_PROTO’, ‘https’)
```
4. В settings.py следует указать значение для STATIC_ROOT:
```
STATIC_URL = ‘/static/’
STATIC_ROOT = ‘staticfiles’
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, ‘static’),
)
```
wsgi.py
----------
Изменить в wsgi.py:

```
application = get_wsgi_application()
```
на
```
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())

```
Настройка Git
---------------
git представляет собой основу разворачивания приложений на Heroku, поэтому он также должен быть установлен. Если вы установили набор инструментов Heroku, то git у вас уже установлен.

Для разворачивания приложения на Heroku, оно должно присутствовать в локальном репозитарии

Git и Heroku
---------------
```
$ touch .gitignore
```
Отредактировать:
```
myenv

*.pyc

myproject/ignore_directory
```
Инициировать новый Git repository:
-----------------------------------
```
$ git init

$ git add .

$ git commit -m “First commit of my django app”
```
Создать приложение Heroku:
---------------------------
```
heroku create janusnic
Creating janusnic... done, stack is cedar-14
https://janusnic.herokuapp.com/ | https://git.heroku.com/janusnic.git
Git remote heroku added

```
В дополнение к установкам URL, эта команда добавляет нашему репозитарию удаленный репозитарий (git remote), который используем для загрузки кода приложения в облако.

Развертывание приложения:
------------------------
```
$ git push heroku master
```
Метка heroku, которую мы используем в нашей команде git push, была автоматически зарегистрирована в нашем репозитарии git когда мы создавали наше приложение при помощи heroku create. Чтобы посмотреть, как настроен этот удаленный репозитарий, вы можете запустить git remote -v в папке приложения.

Если возникла ошибка Permission denied (publickey)
```
$ heroku keys:add ~/.ssh/id_rsa.pub
```
если ключ у вас есть
```
$ heroku keys:add
```
если хотите ключ создать.

Открыть ваше приложение
```
$ heroku open
```
Убедитесь, что у вас есть dyno
```
$ heroku ps:scale web=1
```
Изменить имя вашего приложения.
------------------------------

```
$ git remote rm heroku

$ git remote add heroku git@heroku.com:yourappname.git
```
Обновите ваши установки
```````````````````````
```
ALLOWED_HOSTS.
```

При каждом изменении в проекте:
```
$ git add .
```
Удалить последнюю команду:
```
$ git reset
```
Закоммитить:
```
$ git commit -m “Describe your changes”

$ git push heroku master
```

Можно проверить состояние нод с помощью команды ps: 
--------------------------------------------------
```
$ heroku ps
=== web: `gunicorn projectname.wsgi`
web.1: up for 10s
```
Лог можно посмотреть с помощью команды log: 
-------------------------------------------
```
$ heroku logs
$ heroku logs -n 200  # показать 200 последних строк
$ heroku logs --tail  # не возвращать управление, выводить новые сообщения
$ heroku help logs    # вывести справку по команде logs
```
Запускать команды Django можно с помощью команды run: 
-----------------------------------------------------
```
$ heroku run python manage.py syncdb
$ heroku run python manage.py shell
```

PostgreSQL Database – Heroku
----------------------------
Проверка:
```
$ heroku addons | grep POSTGRES
```
Создать новую free postgres database (dev option):
--------------------------------------------------
```
heroku addons:create heroku-postgresql:dev
 !    That add-on plan is only available to select users.

```

HEROKU_POSTGRESQL_COLOR_URL 
```
$ heroku config | grep HEROKU_POSTGRESQL
```
DATABASE_URL:
```
$ heroku pg:promote HEROKU_POSTGRESQL_YELLOW_URL
```
PostgreSQL databases
```
$ heroku pg:info
```
To establish a psql session
```
$ heroku pg:psql
```

Добавить изменения:
```
$ git add .

$ git commit -m “PostgreSQL set”

$ git push heroku master
```

Миграции Django models
----------------------
https://devcenter.heroku.com/articles/one-off-dynos

```
$ heroku run python manage.py migrate
```
Можно и с помощью Django shell:
```
$ heroku run python manage.py shell
```

Языковая поддержка
------------------
settings.py
```
$ mkdir locale
```
Редактировать settings.py:
```
ugettext = lambda s : s
LANGUAGES = (
    (‘en’, ugettext(‘English’)),
    (‘ca’, ugettext(‘Catalan’)),
)
LOCALE_PATHS = os.path.join(BASE_DIR, ‘locale’)
```
And finally, add the locale middleware in the correct position:
```
MIDDLEWARE_CLASSES = (
    …
    ‘django.contrib.sessions.middleware.SessionMiddleware’,
    ‘django.middleware.locale.LocaleMiddleware’,
    ‘django.middleware.common.CommonMiddleware’,
    …
)
```

Time zone
-------------
```
TIME_ZONE = ‘Europe/Madrid’
```

Удалить базу
-------------
```
$ drop mylocaldb
```
pull database:
--------------
```
$ heroku pg:pull myapponheroku::YELLOW mylocaldb
```
Установка user и password для local database:
---------------------------------------------
```
$ PGUSER=user PGPASSWORD=password heroku pg:pull myapponheroku::YELLOW mylocaldb
```

push database в Heroku:
-----------------------
```
$ heroku pg:push mylocaldb HEROKU_POSTGRESQL_YELLOW –app myapponheroku
```
Если удаленная database не пустая, очистить ее
```
$ heroku pg:reset HEROKU_POSTGRESQL_YELLOW
```
