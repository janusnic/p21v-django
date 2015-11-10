# p21v-django unit 09

## Install PostgreSQL

Установить PostgreSQL. Инсталятор включает PostgreSQL, pgAdmin и StackBuilder.

При установке необходимо установить password для database superuser account (Postgres).

Выполнить
```
$ pg_config
```
или:

```
$ sudo find / -name pg_config
```
Добавить $PATH variable в .bash_profile:

```
export PATH=/Library/PostgreSQL/9.3/bin:$PATH
```
Перезапустить сервер

## Create PostgreSQL Database

Выполнить

```
$ which psql
```
Выполнить:

```
$ psql -h localhost
```
или:

```
$sudo -u postgres psql
```
Выполнить:

```
$ createdb
$ psql -h localhost
(или $ sudo -u postgres psql)
```
Выйти из шела

```
\q
```
Получить справку
```
 \?
```
Список баз
```
\list
```
Список пользователей
```
 \du
```

### Создать базу:

```
$ createdb mysite_db
(or $ sudo -u postgres createdb mysite_db)
$ psql
(или $ sudo -u postgres psql)
CREATE ROLE myusername WITH LOGIN PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE taskbuster_db TO myusername;
ALTER USER myusername CREATEDB;

```

Установить PostgreSQL Django adapter, psycopg2

```
$ pip install psycopg2
```

## Конфигурация Django Database Settings

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DATABASE_NAME'),
        'USER': get_env_variable('DATABASE_USER'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
        'HOST': '',
        'PORT': '',
    }
}
```
settings.py:

```
from django.core.exceptions import ImproperlyConfigured
 
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)
```
Редактировать postactivate file для environment:

```
$ vi $VIRTUAL_ENV/bin/postactivate

```
Database settings:
```

export DATABASE_NAME='mysite_db'
export DATABASE_USER='myusername'
export DATABASE_PASSWORD='mypassword'
```
Редактировать predeactivate file для enviroment:

```
unset DATABASE_NAME
unset DATABASE_USER
unset DATABASE_PASSWORD
```
Миграция database:

```
$ python manage.py check
$ python manage.py migrate
```

Создать суперпользователя:

```
$ python manage.py createsuperuser
```

Запусить тест

```
$ python manage.py test
```

## Install MySQL

Добавить $PATH 

```
~/.bash_profile:
export PATH=$PATH:/usr/local/mysql/bin
```

start mysql:

```
$ sudo /usr/local/mysql/support-files/mysql.server start
```
Создать username и password:

```
$ mysqladmin -u root&nbsp;password yourpassword
```
Изменить password:

```
$ mysqladmin -u root -p'oldpassword' password newpassword
```

### Создать MySQL Database


```
$ mysql -u root -p
Enter password:
```
create  database, user и grant all privileges для user:

```
CREATE DATABASE mysite_db;
CREATE USER 'username'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON mysite_db.* TO 'username'@'localhost';
FLUSH PRIVILEGES;
quit
```
Проверка:

```
show grants for 'username'@'localhost';
```
Установить MySQL Django adapter, mysqlclient

```
$ pip install mysqlclient
```

Конфигурация Django Database Settings

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env_variable('DATABASE_NAME'),
        'USER': get_env_variable('DATABASE_USER'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
        'HOST': '',
        'PORT': '',
    }
}
```
settings.py:

```
from django.core.exceptions import ImproperlyConfigured
 
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)
```
Изменить postactivate file для environment:

```
$ vi $VIRTUAL_ENV/bin/postactivate
```
Добавить Database settings:

```
export DATABASE_NAME='mysite_db'
export DATABASE_USER='myusername'
export DATABASE_PASSWORD='mypassword'
```
Изменить predeactivate file для enviroment:

```
unset DATABASE_NAME
unset DATABASE_USER
unset DATABASE_PASSWORD
```
 
Миграции.

```
$ python manage.py check
$ python manage.py migrate
```
Создать суперпользователя:

```
$ python manage.py createsuperuser
```
Тестируем

```
$ python manage.py test
```

### MySQL Workbench

Установить http://dev.mysql.com/downloads/workbench/.

## django-allauth

Создаем functional_tests/test_allauth.py:

```

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
 
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.translation import activate
 
 
class TestGoogleLogin(StaticLiveServerTestCase):
 
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.wait = WebDriverWait(self.browser, 10)
        activate('en')
 
    def tearDown(self):
        self.browser.quit()
 
    def get_element_by_id(self, element_id):
        return self.browser.wait.until(EC.presence_of_element_located(
                (By.ID, element_id)))
 
    def get_button_by_id(self, element_id):
        return self.browser.wait.until(EC.element_to_be_clickable(
                (By.ID, element_id)))
 
    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)
 
    def test_google_login(self):
        self.browser.get(self.get_full_url("home"))
        google_login = self.get_element_by_id("google_login")
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("logout")
        self.assertEqual(
            google_login.get_attribute("href"),
            self.live_server_url + "/accounts/google/login")
        google_login.click()
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("google_login")
        google_logout = self.get_element_by_id("logout")
        google_logout.click()
        google_login = self.get_element_by_id("google_login")

```

## Install django-allauth

```
$ pip install django-allauth
```

### Settings File

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
                # Required by allauth template tags
                "django.core.context_processors.request",
                # allauth specific context processors
                для версии меньше 0.23
                "allauth.account.context_processors.account",
                "allauth.socialaccount.context_processors.socialaccount",
            ],
        },
    },
]
```

Включаем Authentication Backend:

```

AUTHENTICATION_BACKENDS = (
    # Default backend -- used to login by username in Django admin
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)
```
Добавим:

```

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'redactor',
    'todo',
    'blog',
    'autofixture',
    # The Django sites framework is required
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Login via Google
    'allauth.socialaccount.providers.google',

)
```
Добавим 
```
SITE_ID = 1
```

Кофигурация аутентификации:

```
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_QUERY_EMAIL = True
LOGIN_REDIRECT_URL = "/"
```

## Urls

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
    url(r'^accounts/', include('allauth.urls')),
]
```
### Database migrations

```
$ python manage.py check
$ python manage.py migrate

Operations to perform:
  Synchronize unmigrated apps: tinymce, google, staticfiles, messages, autofixture, allauth, redactor
  Apply all migrations: contenttypes, auth, blog, socialaccount, todo, sessions, sites, account, admin
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
  Installing custom SQL...
Running migrations:
  Rendering model states... DONE
  Applying account.0001_initial... OK
  Applying account.0002_email_max_length... OK
  Applying sites.0001_initial... OK
  Applying socialaccount.0001_initial... OK
  Applying socialaccount.0002_token_max_lengths... OK

```

### Конфигурация Sites
```
$ python manage.py runserver
```
Переходим в admin interface http://127.0.0.1:8000/admin/sites/site и создаем Site для localhost, 127.0.0.1:8000. 

## Goolge App Registration

Создадим Google App и получим key и secret. Переходим на Google Developers Console https://console.developers.google.com/project и кликаем Create Project. Указываем name для project и ID.
```
Project: janus-my
ID: janus-my (#1111189205155)
```
Слева в menu выбираем 
```
APIs & auth –> Credentials 
```
и открываем вкладку Consent. Заполняем Name и Email.

Выбираем Credentials и вызываем Create new Client ID. 

```
Create client ID
Application type
Web application
Android Learn more
Chrome App Learn more
iOS Learn more
PlayStation 4
Other Name
```
Выбираем Web Application:

заполняем
```
## Authorized JavaScript origins
Enter JavaScript origins here or redirect URIs below (or both)  
Cannot contain a wildcard (http://*.example.com) or a path (http://example.com/subdir).

http://127.0.0.1:8000  
Authorized redirect URIs
Must have a protocol. Cannot contain URL fragments or relative paths. Cannot be a public IP address.

http://127.0.0.1:8000/accounts/google/login/callback/

This app will work in our development and testing environment. You should create another Client/secret pair for production, and change http://127.0.0.1:8000/ by your website domain.

Here is your client ID
111111205155-p1o8vj1j6joce71f5gdvgldo13k6dorv.apps.googleusercontent.com

Here is your client secret
uuPPPuuuuUkKiAbMOWxReb7U4Ow
```
### Allauth Django Configuration

Создаем Social Application for Google http://127.0.0.1:8000/admin/socialaccount/socialapp:
```
Provider: Google
Name: Google (or something similar)
Client ID: your application Client ID (obtained in the Developers Console at APIs & auth –> Credentials).
Secret Key: your application Client Secret
Key: not needed (leave blank).
Select the corresponding site.
Finally, just save the instance.
```
Тестируем
```
$ python manage.py test functional_tests.test_allauth
```
Изменим templates/base.html:
```

<div class="navbar-collapse collapse">
  <div class="navbar-form navbar-right">
    {% if user.is_authenticated %}
      <a id="logout" href="/accounts/logout" class="btn btn-success">Logout</a>
    {% else %} 
      <a id="google_login" href="/accounts/google/login" class="btn btn-success">
        Sign in with Google
      </a>
    {% endif %}
  </div>
</div><!--/.navbar-collapse -->
```

Создаем fixutres:
```

$ mkdir home/fixtures

$ python manage.py dumpdata --indent 2 --natural-foreign -e contenttypes -e auth.Permission > home/fixtures/allauth_fixture.json
```
Изменяем .gitignore

```
# .gitignore
...
home/fixtures
```
В settings.py
```

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'home/fixtures'),
    )

```
Меняем test class
```

class TestGoogleLogin(StaticLiveServerTestCase):
 
    fixtures = ['allauth_fixture']
 
    def setUp(self):
        ...
```
Запускаем tests.

```
$ python manage.py test functional_tests.test_allauth
```
Срздаем home/fixtures/google_user.json
```

{"Email": "example@gmail.com", "Passwd": "example_psw"}
```
Редактируем:
```

class TestGoogleLogin(StaticLiveServerTestCase):
    ...
    def user_login(self):
        import json
        with open("home/fixtures/google_user.json") as f:
            credentials = json.loads(f.read())
        self.get_element_by_id("Email").send_keys(credentials["Email"])
        self.get_button_by_id("next").click()
        self.get_element_by_id("Passwd").send_keys(credentials["Passwd"])
        for btn in ["signIn", "submit_approve_access"]:
            self.get_button_by_id(btn).click()
        return
    def test_google_login(self):
        ...
        google_login.click()
        self.user_login()
        ...
```

urls.py 

Перед allauth.urls вставим:
```
url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
```

## TestTwitter

Добавим в funcitonal_tests/test_allauth.py:

```
class TestTwitterLogin(StaticLiveServerTestCase):
 
    fixtures = ['allauth_fixture']
 
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.wait = WebDriverWait(self.browser, 10)
        activate('en')
 
    def tearDown(self):
        self.browser.quit()
 
    def get_element_by_id(self, element_id):
        return self.browser.wait.until(EC.presence_of_element_located(
                (By.ID, element_id)))
 
    def get_button_by_id(self, element_id):
        return self.browser.wait.until(EC.element_to_be_clickable(
                (By.ID, element_id)))
 
    def user_login(self):
        import json
        with open("home/fixtures/twitter_user.json") as f:
            credentials = json.loads(f.read())
        for key, value in credentials.items():
            self.get_element_by_id(key).send_keys(value)
        for btn in ["allow"]:
            self.get_button_by_id(btn).click()
        return
 
    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)
 
    def test_twitter_login(self):
        self.browser.get(self.get_full_url("home"))
        twitter_login = self.get_element_by_id("twitter_login")
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("logout")
        self.assertEqual(
            twitter_login.get_attribute("href"),
            self.live_server_url + "/accounts/twitter/login")
        twitter_login.click()
        self.user_login()
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("twitter_login")
        logout = self.get_element_by_id("logout")
        logout.click()
        twitter_login = self.get_element_by_id("twitter_login")
```

Выполним тест
```
$ python manage.py test functional_tests.test_allauth.TestTwitterLogin
```

### Кофигурация Allauth

Добавим в settings.py:
```

INSTALLED_APPS = (
    ...
    'allauth.socialaccount.providers.twitter',
    ...
)
```
Если нужна миграция:
```
$ python manage.py check
$ python manage.py makemigrations
$ python manage.py migrate
```
Редактируем base.html template:
```

<div class="navbar-collapse collapse">
  <div class="navbar-form navbar-right">
    {% if user.is_authenticated %}
      <a id="logout" href="/accounts/logout" class="btn btn-success">Logout</a>
    {% else %} 
      <a id="google_login" href="/accounts/google/login" class="btn btn-success">Sign in with Google</a>
      <a id="twitter_login" href="/accounts/twitter/login" class="btn btn-success">Sign in with Twitter</a>
    {% endif %}
  </div>
</div><!--/.navbar-collapse -->
```

## Создаем Twitter Application

Переходим на https://apps.twitter.com/app/new with:
```

Website: http://127.0.0.1:8000 (twitter не поддерживаеи имя localhost как url)
Callback Url: http://127.0.0.1:8000/accounts/twitter/login/callback/
```
Создаем Allauth social application в http://127.0.0.1:8000/admin/socialaccount/socialapp/add/ 
```
Provider: Twitter
Name: Twitter (or something similar)
Client ID: Your Twitter app Consumer Key (API Key)
Secret Key: Your Twitter app Consumer Secret (API Secret)
Sites: Select the corresponding site
```

Создаем fixtures. 
```
$ python manage.py dumpdata --indent 2 --natural-foreign -e contenttypes -e auth.Permission > home/fixtures/allauth_fixture.json
```
Создаем fixtures/twitter_user.json:

```
{"username_or_email": "user@email.com", "password": "userpassword"}
```
Тестируем
```
$ python manage.py test functional_tests.test_allauth
```
