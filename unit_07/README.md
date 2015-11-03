# p21v-django

# Заполнение моделей начальными данными
Работать с “пустой” базой данных неудобно. Поэтому, при настройке и отладке приложения часто возникает необходимость в “начальных” данных для проекта. Django предлагает нам ряд возможностей для автоматического создания таких данных: с помощью файлов предварительной настройки (fixtures), либо с помощью SQL запросов.

В общем, подход с использованием файлов с данными является более “чистым”, поскольку он учитывает специфику конкретной базы данных, но использование SQL запросов дает немного больше гибкости.

## Создание начальных данных с помощью файлов(fixtures)

Файлы предварительной настройки (fixtures) содержат набор данных, которые Django может импортировать в базу данных. Самый простой путь создания таких файлов (при условии что ваша база данных уже содержит некоторую нужную информацию) это использование команды manage.py dumpdata. Вы также может создать данные “вручную” используя синтаксис XML, YAML(при установленном PyYAML http://www.pyyaml.org/) или JSON и сохранив результат в соответствующем формате. 
```
./manage.py dumpdata [app_name] > [app_name]/fixtures/initial_data.json

./manage.py dumpdata blog > blog/fixtures/initial_data.json
```
Н-р, ниже представлено содержимое такого файла в формате JSON для простой модели Category:
```
[

    {
        "model": "blog.category", 
        "pk": 1, 
        "fields": {
            "name": "django", 
            "slug": "django", 
            "description": "Django framework", 
            "views_count": 0
        }
    }, 
    {
        "model": "blog.category", 
        "pk": 2, 
        "fields": {
            "name": "python", 
            "slug": "python", 
            "description": "Python language", 
            "views_count": 0
        }
    }

]
```
А вот те же данные в формате YAML:
```
- model: blog.category
  pk: 1
  fields:
    name: django
    slug: django
    description: Django framework
    views_count: 0
- model: blog.category
  pk: 2
  fields:
    name: python
    slug: python
    description: Python language
    views_count: 0
```
Что-бы данные “заработали”, создайте папку fixtures в папке приложения и сохраните в ней файлы с данными. ( имя fixtures предопределено в Django, и в случае опечатки в названии - данные не будут найдены!)

Загрузить данные просто: выполните команду manage.py loaddata fixturename, где fixturename это имя созданного вами файла с данными. Каждый раз при запуске loaddata, данные будут считываться из файлов и записываться в базу данных. Обратите внимание, вы можете изменить загруженные начальные данные в процессе работы, но при следующем вызове loaddata все изменения будут утеряны.

### Где Django ищет файлы предустановки
По умолчанию Django ищет и “просматривает” папки fixtures внутри папки с приложением. Вы можете немного изменить это поведение, указав в настройках проекта FIXTURE_DIRS список дополнительных директорий для поиска.

При запуске manage.py loaddata, вы можете указать абсолютный путь к файлу с данными, “отменив” тем самым механизм поиска по умолчанию.

# django-autofixture
https://github.com/gregmuellegger/django-autofixture
```
pip install django-autofixture
```
Создание начальных данных
```
python manage.py loadtestdata blog.Category:10 blog.Tag:20 blog.Article:100 
```
python manage.py help loadtestdata
```
Usage: manage.py loadtestdata [options] app.Model:# [app.Model:# ...]

Create random model instances for testing purposes.

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -v VERBOSITY, --verbosity=VERBOSITY
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings=SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath=PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions
  --no-color            Don't colorize the command output.
  -d, --overwrite-defaults
                        Generate values for fields with default values.
                        Default is to use default values.
  --no-follow-fk        Ignore foreignkeys while creating model instances.
  --generate-fk=GENERATE_FK
                        Do not use already existing instances for ForeignKey
                        relations. Create new instances instead. You can
                        specify a comma sperated list of field names or ALL to
                        indicate that all foreignkeys should be generated
                        automatically.
  --no-follow-m2m       Ignore many to many fields while creating model
                        instances.
  --follow-m2m=FOLLOW_M2M
                        Specify minimum and maximum number of instances that
                        are assigned to a m2m relation. Use two, colon
                        separated numbers in the form of: min,max. Default is
                        1,5. You can limit following of many to many relations
                        to specific fields using the following format:
                        field1:min:max,field2:min:max ...
  --generate-m2m=GENERATE_M2M
                        Specify minimum and maximum number of instances that
                        are newly created and assigned to a m2m relation. Use
                        two, colon separated numbers in the form of: min:max.
                        Default is to not generate many to many related models
                        automatically. You can select specific of many to many
                        fields which are automatically generated. Use the
                        following format: field1:min:max,field2:min:max ...
  -u USE, --use=USE     Specify a autofixture subclass that is used to create
                        the test data. E.g. myapp.autofixtures.MyAutoFixture
```
# Представление

Представление – это “тип” страниц вашего приложения, которое является функцией для обработки запроса и использует шаблон для генерации страницы. Например, блог может состоять из следующих представлений:

- Главная страница – показывает несколько последних записей блога.
- Страница записи – страница отображения одной записи блога.
- Страница-архив записей по годам – показывает все месяца года и записи блога, сгруппированные по этим месяцам.
- Страница-архив записей по месяцам – показывает все дни месяца и записи блога, сгруппированные по этим дням.
- Страница-архив записей по дням – показывает все записи за указанный день.
- Форма комментариев – предоставляет возможность добавить комментарий к записи блога.

В нашем приложении blog реализуем следующие представления:

- Главная страница вопросов – показывает несколько последних записей блога.
- Страница записи – страница отображения одной записи блога.

В Django страницы и остальной контент отдается представлениями. Представление - это просто функция Python(или метод представления-класса). Django выбирает представление, анализируя запрошенный URL(точнее часть URL-а после домена).

URL-шаблон - это общая форма URL-а. 

Чтобы из URL-а получить представление, Django используется так называемый ‘URLconf’. URLconf определяет соответствие URL-шаблонов(являются регулярными выражениями) и представлений.


## Создадим представление

Откройте файл blog/views.py и добавьте следующий код:

blog/views.py
```
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

Это самое простое из возможных представлений в Django. Необходимо прикрепить это представление к какому-то URL-у -для этого воспользуемся URLconf.

Создайте файл urls.py в каталоге приложения blog. 

blog/urls.py
```
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
```

Теперь в главном URLconf подключим модуль blog.urls. 

mysite/urls.py
```
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
```

Вы привязали представление index к URL-у используя URLconf. Откройте http://localhost:8000/blog/ в браузере, вы должны увидеть текст “Hello, world. You’re at the blog index.”, который вы указали в представлении index.

Функция url() принимает четыре аргумента, два обязательных: regex и view, и два необязательных: kwargs и name. 

### url() argument: regex
Django проверяет соответствие запрошенного URL-а с регулярным выражением(первый элемент кортежа), начиная с первого и далее по списку, пока не будет найдено подходящее.

Обратите внимание, что регулярные выражения не обрабатывают GET и POST параметры или название домена. Например, при запросе к http://www.example.com/myapp/, URLconf будет обрабатывать myapp/. При запросе к http://www.example.com/myapp/?page=3, URLconf также получит myapp/.

регулярные выражения компилируются при первой загрузке модуля URLconf. 

### url() argument: view
При нахождении подходящего регулярного выражения, Django вызывает функцию Python передавая: первым аргументом объект HttpRequest, а потом все “распознанные” значения как позиционные или именованные аргументы. 

### url() argument: kwargs
Любое количество именованных аргументов может быть передано в представление через словарь.

### url() argument: name
Название URL-а позволяет однозначно указать на него в любом месте в Django, особенно полезно это в шаблонах. Это позволяет глобально изменять шаблоны URL-ов в одном месте.

Теперь создадим еще пару представлений в blog/views.py. 

blog/views.py
```
def detail(request, blog_id):
    return HttpResponse("You're looking at article %s." % blog_id)

def results(request, blog_id):
    response = "You're looking at the results of article %s."
    return HttpResponse(response % blog_id)

def vote(request, blog_id):
    return HttpResponse("You're voting on article %s." % blog_id)

```

blog/urls.py
```
from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /blog/
    url(r'^$', views.index, name='index'),
    # ex: /blog/5/
    url(r'^(?P<blog_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /blog/5/results/
    url(r'^(?P<blog_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /blog/5/vote/
    url(r'^(?P<blog_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
```

Откройте страницу “/blog/34/”. Будет выполнена функция detail() и показан ID, который вы указали в URL. Откройте “/blog/34/results/” и “/blog/34/vote/” – вы увидите наши будущие страницы результатов и голосования.

При запросе страницы – например, “/blog/34/”, Django загружает модуль mysite.urls т.к. он указан в ROOT_URLCONF. Находит переменную urlpatterns и перебирает все регулярные выражения по порядку. include() просто ссылается на другой URLconf. Заметим, что регулярное выражение не содержит $ (признак конца строки) но содержит завершающий слэш. Когда Django встречает include(), он отрезает распознанную часть URL, все, что осталось, передает в указанный URLconf для дальнейшей обработки.

Идея использования include() и разделения URLconf состоит в том, чтобы легко подключать и изменять конфигурацию URL-ов. Теперь, когда приложение blog содержит собственный URLconf(blog/urls.py), вы можете подключить его в “/blog/”, или “/fun_blog/”, или в “/content/blog/”, или другой путь и приложение будет работать.

Вот что произойдет при запросе к “/blog/34/”:

1. Django найдет '^blog/'

2. Затем Django обрежет распознанную часть ("blog/") и передаст остаток – "34/" – в ‘blog.urls’ для дальнейшей обработки, который будет распознан '''r'^(?P<blog_id>[0-9]+)/$' ''' и будет вызвана функция detail():
```
detail(request=<HttpRequest object>, blog_id='34')
```
Аргумент blog_id='34' получен из 
```
(?P<blog_id>[0-9]+). 
```
Использование скобок вокруг “captures” позволяет передать значения распознанные регулярным выражением в представление, 
```
?P<question_id> 
```
определяет название переменной при передаче и регулярное выражение [0-9]+, которое распознает цифры.

Так как URL-шаблоны – это регулярные выражения, вы можете распознать какой угодно URL. 
```
url(r'^blog/latest\.html$', views.index),
```
Но не делайте так. Это глупо.

### Добавим функционал в представления

Каждое представление должно выполнить одно из двух действий: вернуть экземпляр HttpResponse с содержимым страницы, или вызвать исключения такое как Http404.

Все что нужно Django – это HttpResponse. Или исключение.

Мы будем использовать API Django для работы с базой данных. Изменим index() так, чтобы оно отображало последние 5 article.title разделенные запятой от самого нового к самому старому:

blog/views.py
```
from django.http import HttpResponse

from .models import Article


def index(request):
    latest_blog_list = Article.objects.order_by('-publish_date')[:5]
    output = ', '.join([p.title for p in latest_blog_list])
    return HttpResponse(output)
```

внешний вид страницы определяется в представлении. Если вы захотите изменить дизайн страницы, вам придется менять код. 

Давайте воспользуемся системой шаблонов Django, чтобы отделить представление от кода.

Для начала создайте каталог templates в каталоге приложения polls. Django будет искать шаблоны в этом каталоге.

Настройка TEMPLATES указывает Django как загружать и выполнять шаблоны. По умолчанию используется бэкенд DjangoTemplates, с опцией APP_DIRS равной True. В этом случае бэкенд проверяет подкаталог “templates” в приложениях, указанных в INSTALLED_APPS - таким образом Django сможет найти наши шаблоны даже если мы не меняем DIRS.

## Организация шаблонов
Мы можем содержать все шаблоны в одном каталоге и это будет отлично работать. 
В только что созданном каталоге templates, создайте каталог blog, и в нем создайте файл index.html. Учитывая как работает загрузчик шаблонов app_directories , вы сможете обращаться к шаблону как blog/index.html.

#### Пространства имен для шаблонов
Django будет использовать первый найденный шаблон, и если существует шаблон с аналогичным названием в другом приложении, Django не сможет различить их. Чтобы этого избежать, мы будем использовать пространство имен. Точнее, просто добавим их в еще один подкаталог с названием, аналогичным названию приложения.

blog/templates/blog/index.html
```
{% if latest_blog_list %}
    <ul>
    {% for item in latest_blog_list %}
        <li><a href="/blog/{{ item.id }}/">{{ item.title }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No items are available.</p>
{% endif %}


```
Теперь изменим наше представление index в blog/views.py, чтобы использовать шаблон:

blog/views.py
```
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Article

def index(request):
    latest_blog_list = Article.objects.order_by('-publish_date')[:5]
    template = loader.get_template('blog/index.html')
    context = RequestContext(request, {
        'latest_blog_list': latest_blog_list,
    })
    return HttpResponse(template.render(context))

```
Этот код загружает шаблон blog/index.html и передает ему контекст. Контекст - это словарь, содержащий название переменных шаблона и соответствующие им значения.

#### Функция render()
Процесс загрузки шаблона, добавления контекста и возврат объекта HttpResponse, вполне тривиальный. Django предоставляет функцию для всех этих операций. Вот как будет выглядеть наш index():

blog/views.py
```
from django.shortcuts import render

from .models import Article


def index(request):
    latest_blog_list = Article.objects.order_by('-publish_date')[:5]
    context = {'latest_blog_list': latest_blog_list}
    return render(request, 'blog/index.html', context)

```

Так как мы используем такой подход во всех наших представлениях, нет необходимости импортировать loader, RequestContext и HttpResponse (HttpResponse еще нужен, если остались старые detail, results и vote).

Функция render() первым аргументом принимает объект запроса, также название шаблона и необязательный словарь значений контекста. Возвращает объект HttpResponse содержащий выполненный шаблон с указанным контекстом.

#### Вызов 404 исключения
```
blog/views.py
from django.http import Http404
from django.shortcuts import render

from .models import Article
# ...
def detail(request, blog_id):
    try:
        item = Article.objects.get(pk=blog_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    return render(request, 'blog/detail.html', {'item': item})
```

Представление вызывает исключение Http404, если item с указанным ID не существует.

Содержимое шаблона blog/detail.html:

blog/templates/blog/detail.html
```
{{ item }}
```

### Функция get_object_or_404()
Вызов get() и Http404 при отсутствии объекта – обыденные операции. Django предоставляет функцию, которая выполняет эти действия. Вот как будет выглядеть наше представление detail():

blog/views.py
```
from django.shortcuts import get_object_or_404, render

from .models import Article
# ...
def detail(request, blog_id):
    item = get_object_or_404(Article, pk=blog_id)
    return render(request, 'blog/detail.html', {'item': item})
```
Функция get_object_or_404() первым аргументом принимает Django модель и произвольное количество именованных аргументов, которые передаются в метод get() менеджера модели. Если объект не найден, вызывается исключение Http404.

Зачем мы используем функцию get_object_or_404() вместо того, чтобы автоматически перехватывать исключения ObjectDoesNotExist уровнем выше, или вызывать на уровне API моделей исключение Http404 вместо ObjectDoesNotExist?

Потому что это связывает уровень моделей с уровнем представления. Один из главных принципов проектирования Django – слабая связанность. Некоторая связанная функциональность находится в модуле django.shortcuts.
Существует также функция get_list_or_404(), которая работает аналогично get_object_or_404(), но использует filter() вместо get(). Вызывает Http404, если получен пустой список.

### Использование системы шаблонов

Вот как может выглядеть наш шаблон blog/detail.html, использующий контекстную переменную item:

blog/templates/blog/detail.html
```
<h1>{{ item.title }}</h1>
<div>{{ item.content }}</div>

```
Система шаблонов использует точку для доступа к атрибутам переменной. Например, для {{ item.title }} Django сначала пытается обратиться к item как к словарю. При неудаче ищется атрибут переменной, в данном случае он и используется. Если атрибут не найден, будет искаться индекс в списке.

### Избавляемся от “хардкода” URL-ов в шаблонах

index.html:
```
{% if latest_blog_list %}
    <ul>
    {% for item in latest_blog_list %}
        <li><a href="/blog/{{ item.id }}/">{{ item.title }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No items are available.</p>
{% endif %}

```

Проблема в том, что нам будет очень сложно поменять URL-ы в проекте с большим количеством шаблонов. Однако, так как мы указали названия при вызове url() в модуле blog.urls, мы можем ссылаться на шаблоны URL-ов используя шаблонный тег {% url %}:
```
<h1>Janus Blog Latest publications</h1>
{% if latest_blog_list %}
    <ul>
    {% for item in latest_blog_list %}
        <li><a href="{% url 'detail' item.id %}">{{ item.title }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No items are available.</p>
{% endif %}

```
Определение URL-а будет найдено в модуле blog.urls. Вот где определен наш URL с названием ‘detail’:
```
...
# the 'name' value as called by the {% url %} template tag
url(r'^(?P<blog_id>[0-9]+)/$', views.detail, name='detail'),
...
```
Теперь, если вы захотите поменять URL, например на blog/specifics/12/, вам не придется менять все шаблоны, вы можете сделать это в blog/urls.py:
```
...
# added the word 'specifics'
url(r'^specifics/(?P<blog_id>[0-9]+)/$', views.detail, name='detail'),
...
```
### Пространства имен в названиях URL-ов

Изменим mysite/urls.py и добавим использование пространства имен:

mysite/urls.py
```
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^admin/', include(admin.site.urls)),
]
```
Теперь поменяем в шаблоне blog/index.html:

```
<li><a href="{% url 'detail' item.id %}">{{ item.title }}</a></li>
```
чтобы использовать пространство имен URL-ов:

```

<li><a href="{% url 'blog:detail' item.id %}">{{ item.title }}</a></li>

```

## Настройка вида приложения

В отличие от HTML, генерируемого сервером, веб приложения обычно нуждаются в обработке дополнительных файлов, таких как изображения, JavaScript или CSS, которые нужны для отображения полной веб страницы. В Django мы называем такие файлы “статикой”.

Именно для решения этой задачи существует django.contrib.staticfiles. Он собирает статичные файлы из каждого вашего приложения (и из других мест, которые вы укажете) в единое место, которое может легко применяться на боевом сервере.

Сначала создайте каталог static в каталоге blog. Django будет искать статичные файлы в нём, аналогично тому как Django ищет шаблоны внутри blog/templates/.

Параметр конфигурации STATICFILES_FINDERS содержит список модулей, которые знают как получать статичные файлы из различных источников. Одним из стандартных является AppDirectoriesFinder, который ищет каталоги “static” в каждом зарегистрированном приложении, например, созданный нами каталог в blog. Интерфейс администратора использует аналогичную структуру каталогов для своих статичных файлов.

Внутри созданного каталога static создайте ещё один каталог с именем blog/css и внутри него создайте файл style.css. Из-за особенностей работы AppDirectoriesFinder вы можете обращаться из шаблона к этому статичному файлу как blog/css/style.css, аналогично работе с шаблонами.

### Пространство имен для статических файлов
Аналогично шаблонам, мы можем просто размещать наши статичные файлы прямо в каталоге blog/static (не создавая ещё один каталог blog внутри), но это будет плохой идеей. Django выбирает первый найденный статичный файл с указанным именем и если другое приложение имеет статичный файл с таким же именем, Django не сможет понять какой именно был вам нужен. Нам надо явно указать Django нужный, а вложенный каталог даёт нам именованное пространство для этого. Следовательно, просто размещайте статичные файлы приложения внутри другого каталога с именем, как у приложения.

style.css

```
li a {
    color: green;
}
```
Затем добавьте следующие строки в начало blog/templates/blog/index.html:

```
{% load staticfiles %}

<link rel="stylesheet" type="text/css" href="{% static 'blog/css/style.css' %}" />
```
Тэг {% load staticfiles %} загружает шаблонный тег {% static %} из шаблонной библиотеки staticfiles. Шаблонные тег {% static %} создаёт абсолютный URL на статичный файл.

Это всё, что вам требуется сделать. Перегрузите страницу http://localhost:8000/blog/ и вы должны увидеть, что ссылки опроса стали зелёными (стиль Django!). Это означает, что ваш файл стилей загрузился нормально.

#### Добавление фонового изображения

Теперь надо создать каталог для изображений. Создайте каталог images в каталоге blog/static/blog/. Внутри созданного каталога разместите изображение с именем bg.jpg. 

Затем добавьте следующие строки в файл стилей (blog/static/blog/css/style.css):

```
body {
    background: white url("../images/bg.jpg") no-repeat right bottom;
}
```
Перегрузите страницу http://localhost:8000/blog/ и вы должны увидеть, что фоновое изображение появилось в нижнем правом углу экрана.

Естественно, что шаблонный тег {% static %} не доступен для использования в статичных файлах, таких как ваш файл стилей, так как эти файлы не создаются с помощью Django. Вы должны всегда использовать относительные пути для связывания ваших статичных файлов друг с другом, так как вы можете изменить параметр конфигурации STATIC_URL (используемый шаблонным тегом static для генерации своих URL) без необходимости менять кучу путей в ваших статичных файлах.


## Работа со статическими файлами (CSS, изображения)
Веб-приложения обычно требуют различные дополнительные файлы для своей работы (изображения, CSS, Javascript и др.). В Django их принято называть “статическими файлами”( ли “статика”). Django предоставляет приложение django.contrib.staticfiles для работы с ними.

### Настройка статики

Убедитесь что django.contrib.staticfiles добавлено INSTALLED_APPS.

В настройках укажите STATIC_URL, например:
```
STATIC_URL = '/static/'
```
В шаблоне или “захардкодьте” URL /static/my_app/myexample.jpg, или лучше использовать тег static для генерация URL-а по указанному относительному пути с использованием бэкенда, указанного в STATICFILES_STORAGE (это позволяет легко перенести статические файлы на CDN).
```
{% load staticfiles %}
<img src="{% static "my_app/myexample.jpg" %}" alt="My image"/>
```
Сохраните статические файлы в каталоге static вашего приложения. Например my_app/static/my_app/myimage.jpg.

### Раздача файлов
Кроме конфигурации, необходимо настроить раздачу статических файлов.

При разработке, если вы используете django.contrib.staticfiles, это все происходит автоматически через runserver, при DEBUG равной True.

Ваш проект, возможно, будет содержать статические файлы, которые не относятся ни к одному из приложений. Настройка STATICFILES_DIRS указывает каталоги, которые проверяются на наличие статических файлов. По умолчанию эта настройка пустая. Например:
```
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    '/var/www/static/',
)
```

### Пространства имен для статических файлов
Django использует первый найденный по имени файл и, если у вас есть файлы с одинаковым названием в разных приложениях, Django не сможет использовать оба. Необходимо как-то указать, какой файл использовать, и самый простой способ – это пространство имен. Просто положите их в каталог с названием приложения(my_app/static/my_app).

### Раздача статических файлов при разработке.

Если вы используете django.contrib.staticfiles, runserver все сделает автоматически, если DEBUG равна True. Если django.contrib.staticfiles не добавлено в INSTALLED_APPS, вы можете раздавать статические файлы используя представление django.contrib.staticfiles.views.serve().

Не используйте его на боевом сервере! 

Например, если STATIC_URL равна /static/, вы можете добавить следующий код в urls.py:
```
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```
Это представление работает только при включенной отладке и для локальных префиксов (например /static/), а не полных URL-ов (e.g. http://static.example.com/).

Также эта функция раздает файлы из каталога STATIC_ROOT не выполняя поиск всех статических файлов, как это делает django.contrib.staticfiles.

### Раздача файлов, загруженных пользователем, при разработке

При разработке медиа файлы из MEDIA_ROOT можно раздавать используя представление django.contrib.staticfiles.views.serve().

Не используйте его на боевом сервере!

Например, если MEDIA_URL равна /media/, вы можете добавить следующий код в urls.py:
```
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
Это представление работает только при включенной отладке и для локальных префиксов (например /media/), а не полных URL-ов (e.g. http://media.example.com/).
### Тестирование

При выполнении тестов, которые отправляют действительные HTTP запросы вместо встроенного тестового клиента (то есть при использовании LiveServerTestCase), статические файлы должны быть доступны как и остальная часть контента, чтобы тестовое окружение было максимально близким к настоящему. Но LiveServerTestCase предоставляет минимальную поддержку раздачи статических файлов: не поддерживает различные возможности поиска файлов, которые предоставляет приложение staticfiles, и предполагает, что все статические файлы уже собраны в STATIC_ROOT.

Поэтому staticfiles предоставляет django.contrib.staticfiles.testing.StaticLiveServerTestCase, который работает с файлами аналогично серверу разработки при DEBUG = True, то есть не требуя выполнения команды collectstatic.

#### Развертывание

django.contrib.staticfiles предоставляет команду, чтобы собрать все статические файлы в одном каталоге.

Укажите в STATIC_ROOT каталог, из которого будут раздаваться статические файлы, например:
```
STATIC_ROOT = "/var/www/example.com/static/"
```
Выполните команду collectstatic:
```
$ python manage.py collectstatic
```
Она скопирует все статические файлы в каталог STATIC_ROOT.

