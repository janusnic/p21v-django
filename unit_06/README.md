# p21v-django

# Приложения

Django содержит реестр установленных приложений, который содержит текущие настройки и предоставляет интроспекцию. Также предоставляет список доступных моделей.

Этот реестр называется просто apps и находится в модуле django.apps:
```
>>> from django.apps import apps
>>> apps.get_app_config('admin').verbose_name
'Admin'
```
# Проекты и приложения

Django исторически использует термин проект для установленной версии Django. Проект в первую очередь определяется наличием модуля настроек.

Термин application используется для пакета Python, который предоставляет определенный функционал. Приложения могут повторно использоваться в различных проектах.

Приложения содержат набор моделей, представлений, шаблонов, шаблонных тегов, статических файлов, URL-ов, мидлваров, и прочее. Они добавляются в проект через настройку INSTALLED_APPS, подключение в URLconfs, настройку MIDDLEWARE_CLASSES, или наследование шаблонов.

Важно помнить, что приложение Django - это просто код, который работает с различными частями фреймверка. Не существует такой вещи, как объект Application. Однако, существуют ситуации, когда Django необходимо работать с установленными приложениями, в основном для конфигурации и интроспекции. Для этого реестр приложений содержит метаданные в объекте AppConfig для каждого экземпляра приложения.

# Настройка приложений

Для настройки приложения создайте класс наследник AppConfig и укажите путь для его импорта в INSTALLED_APPS.

Если INSTALLED_APPS содержит путь просто к модулю приложения, Django проверяет переменную default_app_config в модуле.

Если она определена, она должна содержать путь для импорта класса наследника AppConfig для этого приложения.

Если default_app_config не существует, Django будет использовать базовый класс AppConfig.

# Для разработчика приложений
Если вы разрабатываете приложение, которое называется “Blog”, вот как вы можете указать правильное название для админки:
```
# blog/apps.py

from django.apps import AppConfig

class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = "Janus Nicon Blog"

```
Вы можете указать Django использовать этот класс по умолчанию следующим образом:
```
# blog/__init__.py

default_app_config = 'blog.apps.BlogConfig'
```
Теперь BlogConfig будет использоваться, если в INSTALLED_APPS просто указать 'blog'. Теперь пользователи приложения могут использовать настройки из AppConfig без изменения настройки INSTALLED_APPS.

Конечно вы можете попросить пользователей использовать 'blog.apps.BlogConfig' в INSTALLED_APPS. Вы даже можете предоставить несколько классов наследников AppConfig с различными настройками и позволить пользователям добавить необходимый в INSTALLED_APPS.

Принято все классы настроек добавлять в под-модуль apps приложения. Но Django не заставляет соблюдать это правило.

Необходимо указывать атрибут name, чтобы Django мог определить к какому приложению относится класс конфигурации. 

Если ваш код импортирует реестр приложений в __init__.py приложения, название apps будет пересекаться с под-модулем apps. Можно вынести этот код в под-модуль приложения и импортировать его в __init__.py. Другой вариант - импортировать реестр под другим названием:
```
from django.apps import apps as django_apps
```

# Конфигурация приложения

## class AppConfig
Объект конфигурации приложения содержит метаданные о приложении. Некоторые атрибуты можно указать в классе наследнике AppConfig. Некоторые определены Django и доступны только для чтения.

### Настраиваемые атрибуты
#### AppConfig.name
Полный Python путь для импорта приложения, например 'django.contrib.admin'.

Этот атрибут указывает к какому приложению относится класс настроек. Должен указываться во всех классах наследниках AppConfig.

Должен быть уникальным для проекта.

### AppConfig.label
Короткое название(метка) приложения, например 'admin'

Этот атрибут позволяет поменять метку приложения, если два приложения используют по умолчанию одинаковые метки. По умолчанию метка равна последней части значения name. Метка должна быть правильным идентификатором Python.

Должен быть уникальным для проекта.

### AppConfig.verbose_name
Читабельное название приложения, например “Administration”.

По умолчанию равен label.title().

### AppConfig.path
Путь в файловой системе к каталогу с приложением, например '/usr/lib/python3.4/dist-packages/django/contrib/admin'.

В большинстве случае Django может автоматически определить и установить это значение, но вы можете переопределить его в классе наследнике AppConfig. Это может понадобиться в некоторых случаях, например, если пакет приложения является namespace-пакетом и расположен в нескольких каталогах.

## Неизменяемые атрибуты
### AppConfig.module
Корневой модуль приложения, например 
```
<module 'django.contrib.admin' from 'django/contrib/admin/__init__.pyc'>.
```
### AppConfig.models_module
Модуль, который содержит модели, например 
```
<module 'django.contrib.admin.models' from 'django/contrib/admin/models.pyc'>.
```
Может быть None, если приложение не содержит модуль models. Обратите внимание, сигналы, связанные с базой данных, такие как pre_migrate и post_migrate, вызываются только для приложений, которые содержат модуль models.

## Методы
### AppConfig.get_models()
Возвращает итератор по классам Model.

### AppConfig.get_model(model_name)
Возвращает Model для переданного model_name. Вызывает LookupError, если модель не существует. model_name регистро-независимое значение.

### AppConfig.ready()
Класс наследник может переопределить этот метод, чтобы выполнить инициализацию приложения, например зарегистрировать сигналы. Вызывает, когда реестр приложений будет полностью инициализирован и все приложения будут добавлены.

Вы не можете импортировать модели в модуле, который содержит классы настроек, но вы можете использовать метод get_model(), чтобы получить модель по названию:
```
def ready(self):
    MyModel = self.get_model('MyModel')
```
Хотя вы и можете получить доступ к моделям, как в примере выше, избегайте работы с базой данных в методе ready(). Это включает методы, которые выполняют запросы к базе данных (save(), delete(), методы менеджера и т.д.) и SQL запросы через django.db.connection. Метод ready() будет вызываться при каждом запуске команды Django. Например, хотя настройка тестовой базы данных отделена от рабочих настроек проекта, manage.py test выполнила бы запросы на рабочей базе данных!

При обычном процессе инициализации метод ready вызывается Django только один раз. Но в некоторых случаях, в частности при выполнении тестов, ready может вызываться несколько раз. Вам следует писать идемпотентный код(который можно безопасно вызывать несколько раз), или добавить флаг в класс AppConfig и проверять его, чтобы код выполнялся только один раз.
Namespace-пакеты приложений (Python 3.3+)
Python версии 3.3 и выше поддерживает Python пакеты без файла __init__.py. Эти пакеты называют “namespace-пакетами” и могут находится в нескольких каталогах в sys.path (смотрите PEP 420).

Django приложениям необходим один основной путь в файловой системе, где Django (в зависимости от настроек) будет искать шаблоны, статические файлы, и прочее. Таким образом, namespace-пакеты могут быть приложениями Django только при следующих условиях:

Namespace-пакет содержит один каталог (то есть не разделен на несколько каталогов)

Используется класс AppConfig, указывающий в path один абсолютный путь к каталогу, который Django будет использовать как каталог приложения.

Если ни одно из этих условий не соблюдено, Django вызовет исключение ImproperlyConfigured.

# Реестр приложений

## apps
Реестр приложений предоставляет следующий публичный API. Методы, которые не описаны здесь, являются приватными и могут изменяться в будущем без предупреждений.

## apps.ready
Булев атрибут, который устанавливается в True, когда реестр полностью проинициализирован.

## apps.get_app_configs()
Возвращает итератор по объектам AppConfig.

## apps.get_app_config(app_label)
Возвращает AppConfig приложения для app_label. Вызывает LookupError, если приложение не найдено.

## apps.is_installed(app_name)
Проверяет добавлено ли приложение с таким названием в реестр. app_name - полное название приложения, например 'django.contrib.admin'.

## apps.get_model(app_label, model_name)
Возвращает Model для app_label и model_name. Для удобства принимает аргумент вида app_label.model_name. model_name - регистро-независимое значение.

Вызывает LookupError, если приложение или модель не найдена. Вызывает ValueError, если передан один аргумент неправильного формата.

# Процесс инициализации

## Как загружаются приложения
Функция django.setup() отвечает за заполнение реестра приложений при запуске Django.

## setup()
Настраивает Django, выполняя следующие действия:

- Загрузка настроек.
- Настройка логирования.
- Инициализация реестра приложений.

Эта функция вызывается автоматически:

- При запуске HTTP сервера с Django через WSGI.
- При выполнении команды Django.

Этот метод необходимо вызывать явно в некоторых случаях, например в Python скрипте.

Реестр приложений инициализируется в три этапа. На каждом этапе Django обрабатывает приложения в порядке, указанном в INSTALLED_APPS.

Первым делом Django импортирует каждый элемент INSTALLED_APPS.

Если это класс настроек приложения, Django импортирует главный пакет приложения, указанный в атрибуте name. Если это пакет Python, Django создает настройки по умолчанию для приложения.

На этом этапе ваш код не должен импортировать модели!

Другими словами, ваш главный пакет и модули, которые содержат классы настроек, не должны импортировать модели, в том числе и неявно.

После выполнения этого этапа, можно использовать API, который работает с настройками приложения, например get_app_config().

Затем Django пытается импортировать модуль models каждого приложения, если такой существует.

Вы должны определить или импортировать все модели в models.py или models/__init__.py приложения. Иначе, реестр приложений будет не полностью заполнен, что может привести к неправильной работе ORM.

После выполнения этого этапа, можно использовать API, который работает с моделями, например get_model().

В конце Django вызывает метод ready() для каждого приложения.


# Интерфейс администратора Django
Одна из сильных сторон Django – это автоматический интерфейс администратора. Он использует мета-данные модели чтобы предоставить многофункциональный, готовый к использованию интерфейс для работы с содержимым сайта.

Интерфейс администратора по умолчанию включен, если вы создавали проект командой startproject.

## Объект ModelAdmin

### class ModelAdmin
Класс ModelAdmin – это отображение модели в интерфейсе администратора. Его код добавляют обычно в файл admin.py вашего приложения.
```
from django.contrib import admin
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    pass
admin.site.register(Article, ArticleAdmin)
```

### Декоратор для регистрации
```
register(*models[, site=django.admin.sites.site])
```
Существует также декоратор для регистрации ваших классов ModelAdmin:
```
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass
```
Можно указать несколько классов модели для регистрации с ModelAdmin. Также принимается необязательный аргумент site, если вы не используете стандартный AdminSite:

```
from django.contrib import admin
from .models import Article, Reader, Editor
from myproject.admin_site import custom_admin_site

@admin.register(Article, Reader, Editor, site=custom_admin_site)
class PersonAdmin(admin.ModelAdmin):
    pass
```

# файлы админки
При добавлении 'django.contrib.admin' в INSTALLED_APPS setting, Django автоматически ищет модуль admin в каждом приложении и импортирует его.

## class apps.AdminConfig

Стандартный класс AppConfig для админки. Вызывает autodiscover() при запуске Django.

## class apps.SimpleAdminConfig

Аналогичен AdminConfig, но не вызывает autodiscover().

## autodiscover()
Эта функция пытается импортировать модуль admin каждого установленного приложения. Предполагается, что в этом модуле выполняется регистрация моделей в админке.

Если вы используете собственный AdminSite, вам необходимо импортировать все подклассы ModelAdmin и зарегистрировать их в вашем AdminSite. В этом случае, чтобы отключить их добавление в стандартную админку, используйте 'django.contrib.admin.apps.SimpleAdminConfig' вместо 'django.contrib.admin' в INSTALLED_APPS.


# Человеко читабельные urls в Django

## SlugField. 

Slug – газетный термин. “Slug” – это короткое название-метка, которое содержит только буквы, числа, подчеркивание или дефис. 

Как и для CharField, можно указать max_length. Если max_length не указан, Django будет использовать значение 50.

Устанавливает Field.db_index в True, если аргумент явно не указан.

При True, django-admin sqlindexes добавит CREATE INDEX для этого поля.

Вставляем в нашу модель поле:
slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')

```
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
    
    description = models.TextField(max_length=4096)
        
    views_count = models.IntegerField(default=0, verbose_name='views count')

    def __str__(self):
        return self.name
```
Параметр unique=True отвечает за то, чтоб название было уникальным.

## Подключение к админке. 

### ModelAdmin.prepopulated_fields

Обычно значение SlugField создается на основе какого-то другого значения(например, название статьи). Это может работать автоматически в интерфейсе администрации благодаря параметру prepopulated_fields.

prepopulated_fields позволяет определить поля, которые получают значение основываясь на значениях других полей:
```
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
```
Указанные поля будут использовать код JavaScript для заполнения поля значением на основе значений полей-источников. Основное применение - это генерировать значение для полей SlugField из значений другого поля или полей. Процесс генерирования состоит в объединении значений полей-источников и преобразованию результата в правильный “slug” (например, заменой пробелов на дефисы).

prepopulated_fields не принимает поля DateTimeField, ForeignKey или ManyToManyField.

admin.py:
```
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category,CategoryAdmin)
```

Не забудьте сделать миграцию. 


# Настройки ModelAdmin
ModelAdmin очень гибкий. Он содержит ряд параметров для настройки интерфейса администратора. Все настройки определяются в подклассе ModelAdmin:
```
from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'publish_date'
```
## ModelAdmin.actions
Список действий, которые будут включены на странице списка объектов. 

Повседневный алгоритм работы с административным интерфейсом Django выглядит как “выделить объект, затем изменить его.” Он подходит для большинства случаев. Тем не менее, когда потребуется выполнить одно и то же действие над множеством объектов, то такое поведение интерфейса начинает напрягать.

В таких случаях административный интерфейс Django позволяет вам создать и зарегистрировать “действия” – простые функции, которые вызываются для выполнения неких действий над списком объектов, выделенных на странице интерфейса.

Если вы взгляните на любой список изменений на интерфейсе администратора, вы увидите эту возможность в действии. Django поставляется с действием “удалить выделенные объекты”, которое доступно для всех моделей. 


# Создание действий

Общим способом использования действий в интерфейсе администратора является пакетное изменение модели. 

Приложение для работы с новостями, которое обладает моделью Article:
```
class Article(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    EXPIRED ='E'
    ARTICLE_STATUS = (
        (DRAFT, 'Not Reviewed'),
        (PUBLISHED, 'Published'),
        (EXPIRED, 'Expired'),
    )
    def was_published_recently(self):
        return self.publish_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'publish_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
        
    status = models.CharField(max_length=1, choices=ARTICLE_STATUS, default=DRAFT)
    enable_comment = models.BooleanField(default=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.title
```

Стандартной задачей, которую мы возможно будем выполнять с подобной моделью, будет изменение состояний статьи с “черновик” на “опубликовано”. Мы легко сможем выполнить это действие в интерфейсе администратора для одной статьи за раз, но если потребуется выполнить массовую публикацию группы статей, то вы столкнётесь с нудной работой. Таким образом, следует написать действие, которое позволит нам изменять состояние статьи на “опубликовано.”

## Создание функций для действий
Сначала нам потребуется написать функцию, которая вызывается при выполнении действия в интерфейсе администратора. Функции действий - это обычные функции, которые принимают три аргумента:

- Экземпляр класса ModelAdmin,
- Экземпляр класса HttpRequest, представляющий текущий запрос,
- Экземпляр класса QuerySet, содержащий набор объектов, которые выделил пользователь.

Наша функция “опубликовать-эти-статьи” не нуждается в экземпляре ModelAdmin или в объекте реквеста, но использует выборку:
```
def make_published(modeladmin, request, queryset):
    queryset.update(status=PUBLISHED)

```
В целях улучшения производительности, мы используем метод выборки update method. Другие типы действий могут обрабатывать каждый объект индивидуально. В таких случаях мы просто выполняем итерацию по выборке:
```
for obj in queryset:
    do_something_with(obj)
```

Обеспечим действие “красивым” заголовком, который будет отображаться в интерфейсе администратора. По умолчанию, это действие будет отображено в списке действий как “Make published”, т.е. по имени функции, где символы подчёркивания будут заменены пробелами. 

make_published атрибут short_description:
```
def make_published(modeladmin, request, queryset):
    queryset.update(status=PUBLISHED)
make_published.short_description = "Mark selected stories as published"


```

### Добавление действий в класс ModelAdmin
Затем мы должны проинформировать наш класс ModelAdmin о новом действии. Это действие аналогично применению любой другой опции конфигурации. Таким образом, полный пример admin.py с определением действия и его регистрации будет выглядеть так:

```
def make_published(modeladmin, request, queryset):
    queryset.update(status=PUBLISHED)
make_published.short_description = "Mark selected stories as published"

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status', 'was_published_recently')
    list_filter = ['publish_date']
    search_fields = ['title']

    ordering = ['title']

    prepopulated_fields = {"slug": ("title",)}

    fieldsets = [
        ('Item',             {'fields': ['title','category','content']}),
        ('Date information', {'fields': ['created_date','publish_date'], 'classes': ['collapse']}),
        ('Related tags',     {'fields': ['tags']}),
        ('Metas',            {'fields': ['status','views_count']}),
        ('Comments',            {'fields': ['enable_comment','comment_count']}),
    ]
    actions = [make_published,]


admin.site.register(Article, ArticleAdmin)
```

### Обработка ошибок в действиях
При наличии предполагаемых условий возникновения ошибки, которая может возникнуть во время работы вашего действия, вы должны аккуратно проинформировать пользователя о проблеме. Это подразумевает обработку исключений и использование метода django.contrib.admin.ModelAdmin.message_user() для отображения описания проблемы в отклике.

### Действия как методы ModelAdmin
Вышеприведённый пример показывает действие make_published, определённое в виде обычной функции. Это нормальный подход, но к нему есть претензии с точки зрения дизайна кода: так как действия связано с объектом Article, то правильнее будет внедрить это действие в сам объект ArticleAdmin.

Это достаточно просто сделать:
```
class ArticleAdmin(admin.ModelAdmin):
    ...

    actions = [make_published, 'make_draft']

    def make_draft(self, request, queryset):
        queryset.update(status=DRAFT)
    make_draft.short_description = "Mark selected stories as draft"
```
Всё это указывает классу ModelAdmin искать действие среди своих методов.

Определение действий в виде методов предоставляет действиям более прямолинейный, идеоматический доступ к самому объекту ModelAdmin, позволяя вызывать любой метод, предоставляемый интерфейсом администратора.

Например, мы можем использовать self для вывода сообщения для пользователя в целях его информирования об успешном завершении действия:
```
class ArticleAdmin(admin.ModelAdmin):
    ...

    def make_expired(self, request, queryset):
        rows_updated = queryset.update(status=EXPIRED)
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as expired." % message_bit)
    make_expired.short_description = "Mark selected stories as expired"

```
Это обеспечивает действие функционалом, аналогичным встроенным возможностям интерфейса администратора


## Отключение действий
Иногда требуется отключать определённые действия, особенно зарегистрированные глобально, для определённых объектов. Существует несколько способов для этого:

### Отключение глобального действия
#### AdminSite.disable_action(name)
Если требуется отключить глобальное действие, вы можете вызвать метод AdminSite.disable_action().

Например, вы можете использовать данный метод для удаления встроенного действия “delete selected objects”:
```
admin.site.disable_action('delete_selected')
```
После этого действие больше не будет доступно глобально.

Тем не менее, если вам потребуется вернуть глобально отключенное действия для одной конкретной модели, просто укажите это действия явно в списке ModelAdmin.actions:

```
# Globally disable delete selected
admin.site.disable_action('delete_selected')

# This ModelAdmin will not have delete_selected available
class SomeModelAdmin(admin.ModelAdmin):
    actions = ['some_other_action']
    ...

# This one will
class AnotherModelAdmin(admin.ModelAdmin):
    actions = ['delete_selected', 'a_third_action']
    ...
```
## Отключение всех действия для определённого экземпляра ModelAdmin
Если вам требуется запретить пакетные действия для определённого экземпляра ModelAdmin, просто установите атрибут ModelAdmin.actions в None:
```
class MyModelAdmin(admin.ModelAdmin):
    actions = None
```
Это укажет экземпляру ModelAdmin не показывать и не позволять выполнения никаких действий, включая зарегистрированные глобально.

## Условное включение и отключение действий
### ModelAdmin.get_actions(request)
Наконец, вы можете включать или отключать действия по некоему условию на уровне запроса (и, следовательно, на уровне каждого пользователя), просто переопределив метод ModelAdmin.get_actions().

Он возвращает словарь разрешённых действий. Ключами являются имена действий, а значениями являются кортежи вида (function, name, short_description).

Чаще всего вы будете использовать данный метод для условного удаления действия из списка, полученного в родительском классе. Например, если мне надо разрешить пакетное удаление объектов только для пользователей с именами, начинающимися с буквы ‘J’, то я сделаю так:
```
class MyModelAdmin(admin.ModelAdmin):
    ...

    def get_actions(self, request):
        actions = super(MyModelAdmin, self).get_actions(request)
        if request.user.username[0].upper() != 'J':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

```

Действие “удалить выделенные объекты” использует метод QuerySet.delete() по соображениям эффективности, который имеет важный недостаток: метод delete() вашей модели не будет вызван.

Если вам потребуется изменить такое поведение, то просто напишите собственное действие, которое выполняет удаление в необходимой вам манере, например, вызывая Model.delete() для каждого выделенного элемента.

### ModelAdmin.actions_on_top
### ModelAdmin.actions_on_bottom
Определяет где на странице будет расположены панели с действиями. По умолчанию эта панель расположена сверху (actions_on_top = True; actions_on_bottom = False).

### ModelAdmin.actions_selection_counter
Указывает отображать ли счетчик выбранных объектов после списка действий. По умолчанию он отображается (actions_selection_counter = True).

### ModelAdmin.date_hierarchy
Укажите в date_hierarchy название DateField или DateTimeField поля вашей модели, и страница списка объектов будет содержать навигацию по датам из этого поля.
```
date_hierarchy = 'publish_date'
```
Навигация учитывает значения поля, например, если все значения будут датами из одного месяца, будут отображаться только дни этого месяца.

date_hierarchy использует внутри QuerySet.datetimes() (USE_TZ = True).

## ModelAdmin.exclude
Этот атрибут должен содержать список полей, которые не будут включены в форму редактирования.

Например, у нас есть следующая модель:
```
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3)
    birth_date = models.DateField(blank=True, null=True)
```
Если вам необходима форма для модели Author, которая содержит только поля name и title, вы можете определить параметр fields или exclude следующим образом:
```
from django.contrib import admin

class AuthorAdmin(admin.ModelAdmin):
    fields = ('name', 'title')

class AuthorAdmin(admin.ModelAdmin):
    exclude = ('birth_date',)
```
Так как модель содержит только три поля, name, title и birth_date, полученные формы будут содержать одинаковые поля.

## ModelAdmin.fields
Если вам необходимо внести небольшие изменения форму на странице редактирования и добавления, например, изменить список отображаемых полей, их порядок или сгруппировать их, вы можете использовать настройку fields (сложные изменения можно выполнить используя настройку fieldsets). 

fields может содержать поля указанные в ModelAdmin.readonly_fields, они не будут доступны для редактирования.

Параметр fields, в отличии от list_display, может содержать только названия полей модели или полей определенных в form. Можно указать названия функций, если они указаны в readonly_fields.

Чтобы поля отображались в одной строке, укажите их в кортеже вместе. В этом примере, поля url и title будут отображаться в одном ряду, поле content будет расположено ниже:
```
fieldsets = [
        ('Item',             {'fields': [('title','slug'),'category','content']}),
        ('Date information', {'fields': [('created_date','publish_date')], 'classes': ['collapse']}),
        ('Related tags',     {'fields': ['tags']}),
        ('Metas',            {'fields': [('status','views_count')]}),
        ('Comments',            {'fields': ['enable_comment','comment_count']}),
    ]
```

Если не определен ни атрибут fields, ни fieldsets, Django покажет все поля с editable=True кроме AutoField, в одном наборе полей в порядке, в котором они указанные в модели.

### ModelAdmin.fieldsets
Позволяет изменить макет страниц добавления и редактирования объекта.

fieldsets – это список двух-элементных кортежей, каждый представляет fieldset в форме редактирования объекта. (fieldset – группа полей в форме.)

Кортеж должен быть в формате (name, options полей), где name это название группы полей, а field_options – словарь с информацией о группе полей, включая список полей для отображения.

```
fieldsets = [
        ('Item',             {'fields': [('title','slug'),'category','content']}),
        ('Date information', {'fields': [('created_date','publish_date')], 'classes': ['collapse']}),
        ('Related tags',     {'fields': ['tags']}),
        ('Metas',            {'fields': [('status','views_count')]}),
        ('Comments',            {'fields': ['enable_comment','comment_count']}),
    ]
```

Если не определен ни атрибут fields, ни fieldsets, Django покажет все поля с editable=True кроме AutoField, в одном наборе полей в порядке, в котором они указанные в модели.

Словарь field_options может содержать следующие ключи:

- fields
Кортеж с названиями полей. Этот ключ обязателен.

```

{'fields': [('title','slug'),'category','content']}
```
Как и в атрибуте fields, чтобы отобразить поля в одной строке, добавьте их в один кортеж. В этом примере, поля title и slug будут показаны в одной строке

fields может содержать значения из ModelAdmin.readonly_fields, чтобы отображать поля без возможности их редактирования.

Добавление функции в fields аналогично добавлению в параметр fields - функция должна быть указанна в readonly_fields.

- classes
Список содержащий CSS классы, которые будут добавлены в группу полей.
```
{
'classes': ('wide', 'extrapretty'),
}
```
Django предоставляет два класса для использования: collapse и wide. Группа полей с классом collapse будет показа в свернутом виде с кнопкой “развернуть”. Группа полей с классом wide будет шире по горизонтали.

- description
Необязательный текст, который будет отображаться под названием группы полей. Этот текст не отображается для TabularInline.

Заметим, что этот текст не будет экранирован. Это позволяет добавить вам HTML на страницу. Вы можете использовать обычный текст экранировав его функцией django.utils.html.escape().

## ModelAdmin.filter_horizontal
По умолчанию, поле ManyToManyField отображается как select multiple. Однако, это поле тяжело использовать при большом количестве объектов. Добавив ManyToManyField в этот атрибут, будет использоваться “виджет” с JavaScript фильтром для поиска. 
```
filter_horizontal = ('tags',)

```
### ModelAdmin.filter_vertical
Аналогичен filter_horizontal, но использует вертикальный “виджет”.

## ModelAdmin.form
По умолчанию ModelForm создается динамически для модели. Этот атрибут используется для определения формы на страницах добавления и редактирования. Вы можете указать собственный подкласс ModelForm для переопределения этих страниц. Вы можете модифицировать форму, а не создавать с нуля свою, переопределив метод ModelAdmin.get_form().


Если вы указали атрибут Meta.model для ModelForm, необходимо также указать Meta.fields (или Meta.exclude). Однако, если поля указаны при определении настроек интерфейса администратора, атрибут Meta.fields будет проигнорирован.

Если ModelForm используется только для интерфейса администратора, проще всего не указывать атрибут Meta.model, т.к. ModelAdmin укажет правильную модель. Вы можете указать fields = [] в Meta чтобы ModelForm была правильной.

Если и ModelForm и ModelAdmin определяют опцию exclude, ModelAdmin будет иметь больший приоритет:
```
class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

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

## ModelAdmin.formfield_overrides
Позволяет быстро изменить настройки отображения различных типов Field в интерфейсе администратора. formfield_overrides – словарь указывающий параметры для классов полей, которые будут передаваться в конструкторы указанных полей.

## Install django-wysiwyg-redactor:
https://github.com/douglasmiranda/django-wysiwyg-redactor

```
pip install django-wysiwyg-redactor

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
    'redactor',
    'todo',
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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home', views.home_page, name='home'),
    url(r'^$', views.index, name='index'),
    url(r'^todo/', include(todo_urls)),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
]

```

admin.py

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
Заметим что ключ словаря класс поля, а не строка. Значение это словарь с аргументами. Это аргументы будут переданы в __init__(). 
```
'content': RedactorEditor(),

```
## tinymce

urls.py
```
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home', views.home_page, name='home'),
    url(r'^$', views.index, name='index'),
    url(r'^todo/', include(todo_urls)),
    url(r'^redactor/', include('redactor.urls')),
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

### ModelAdmin.list_display
list_display указывает какие поля отображать на странице списка объектов.

```
list_display = ('first_name', 'last_name')
```
Если list_display не указан, Django отобразить только результат __str__()``(``__unicode__() для Python 2) объекта.

Вы можете указать четыре варианта значений в list_display:

Поле модели. Например:
```
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')

```
Функция, которая принимает один аргумент - объект модели. Например:
```
def upper_case_name(obj):
    return ("%s %s" % (obj.first_name, obj.last_name)).upper()
upper_case_name.short_description = 'Name'

class PersonAdmin(admin.ModelAdmin):
    list_display = (upper_case_name,)
```
Название атрибута ModelAdmin. Работает так же, как и функция. Например:
```
class PersonAdmin(admin.ModelAdmin):
    list_display = ('upper_case_name',)

    def upper_case_name(self, obj):
        return ("%s %s" % (obj.first_name, obj.last_name)).upper()
    upper_case_name.short_description = 'Name'
```
Название атрибута модели. Работает так же, как и функция, но self в этом контексте объект модели. Например:
```
from django.db import models
from django.contrib import admin

class Person(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField()

    def decade_born_in(self):
        return self.birthday.strftime('%Y')[:3] + "0's"
    decade_born_in.short_description = 'Birth decade'

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'decade_born_in')
```
Несколько особенностей list_display:

Если указано поле ForeignKey, Django покажет результат __str__() (__unicode__() для Python 2) связанного объекта.

ManyToManyField не поддерживается, так как это влечет к созданию SQL запроса для каждого объекта. Если вам необходимо сделать это в любом случае, создайте метод модели и используйте его в list_display.

Если поле BooleanField или NullBooleanField, Django покажет красивую “on” или “off” иконку вместо True или False.
```
def was_published_recently(self):
        return self.publish_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'publish_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
```

## ModelAdmin.ordering
ordering позволяет определить сортировку на странице списка объектов. Это должен быть список или кортеж в формате аналогичном параметру ordering.

Если атрибут не указана, Django будет использовать сортировку по умолчанию модели.

Если вам необходима динамическая сортировка (например, в зависимости от пользователя или текущего языка) вы можете определить метод get_ordering().
```
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status', 'was_published_recently')
    list_filter = ['publish_date']

    ordering = ['publish_date']
```

## ModelAdmin.search_fields
search_fields позволяет добавить поиск на страницу списка объектов. Этот атрибут должен содержать список полей, которые будут использоваться при поиске.

```
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status', 'was_published_recently')
    list_filter = ['publish_date']
    search_fields = ['title']

    ordering = ['publish_date']
```

Эти поля должны быть текстовыми, таким как CharField или TextField. Вы можете указать поля из связанных объектов используя __:

- search_fields = ['foreign_key__related_fieldname']
Например, у нас есть модель записи в блоге с полем автора. Следующая настройка позволит искать записи по email адресу автора:

- search_fields = ['user__email']
При поиске Django разбивает поисковый запрос на слова и возвращает объекты, которые содержат эти слова в одном из указанных в search_fields полей. Поиск регистронезависимый. Например, если search_fields равен ['first_name', 'last_name'] и пользователь выполняет поиск по john lennon, Django создаст такое SQL условие WHERE:
```
WHERE (first_name ILIKE '%john%' OR last_name ILIKE '%john%')
AND (first_name ILIKE '%lennon%' OR last_name ILIKE '%lennon%')
```
Для определения более конкретных условий поиска используйте следующие префиксы:
```
^
```
Указывает на начало строки. Например, если search_fields установить в 
```
['^first_name', '^last_name'] 
```
и пользователь ищет john lennon, Django создаст следующее SQL условие WHERE:
```
WHERE (first_name ILIKE 'john%' OR last_name ILIKE 'john%')
AND (first_name ILIKE 'lennon%' OR last_name ILIKE 'lennon%')
```
Этот запрос более эффективный чем '%john%', так как база данных будет проверять только начало значения поля. К тому же, если поле содержит индекс, некоторые базы данных могут использовать его при поиске, даже для поиска через LIKE.
```
=
```
Полное совпадение, регистронезависимое. Например, если search_fields равно 
```
['=first_name', '=last_name'] 
```
и пользователь ищет john lennon, Django создаст следующее SQL условие WHERE:
```
WHERE (first_name ILIKE 'john' OR last_name ILIKE 'john')
AND (first_name ILIKE 'lennon' OR last_name ILIKE 'lennon')
```
Поисковый запрос разбивается по пробелам, поэтому, исходя из примера выше, нельзя найти записи с полем first_name равным ``‘john winston’``(содержащим пробел).
```
@
```
Выполняет полнотекстовый поиск. Работает как и обычный поиск, но использует индекс. На данный момент это работает только в MySQL.

Вы можете переопределить метод ModelAdmin.get_search_results(), чтобы указать дополнительные параметры при поиске, или переопределить механизм поиска.

## ModelAdmin.paginator
Класс, используемый для создания постраничного отображения. По умолчанию используется django.core.paginator.Paginator. Если конструктор вашего класса принимает параметры отличные от django.core.paginator.Paginator, вам необходимо также переопределить метод ModelAdmin.get_paginator().

## ModelAdmin.list_per_page
Используйте list_per_page, чтобы определить количество объектов на одной странице при отображении списка объектов. По умолчанию равно 100.
settings.py
```
ADMIN_LIST_PER_PAGE = 20
```
admin.py
```
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('views_count',)
    list_display_links = ('name',)
    search_fields = ['name', 'slug', 'description']
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    prepopulated_fields = {"slug": ("name",)}
```

### ModelAdmin.list_display_links
Используйте list_display_links, чтобы указать какие поля в list_display будут ссылками на страницу редактирования объекта.

По умолчанию, на страницу редактирования объекта будет вести ссылка в первой колонке – первое поле в list_display. Но list_display_links позволяет изменить это поведение:

Можно указать None, чтобы убрать ссылки.

Укажите список или кортеж полей (так же как и в list_display) чьи колонки должны быть ссылками на страницу редактирования.

Вы можете указывать одно или несколько полей. Пока указанные поля входят в list_display, Django безразлично сколько их. Единственное требование: для использования list_display_links вы должны указать list_display.

```
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('views_count',)
    list_display = ('name', 'slug')
    list_display_links = ('name',)
```
В этом примере список объектов будет без ссылок:
```
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('views_count',)
    list_display = ('name', 'slug')

    list_display_links = None

```

## ModelAdmin.readonly_fields
По умолчанию интерфейс администратора отображает все поля как редактируемые. Поля указанные в этой настройке (которая является list или tuple) будут отображаться значение без возможности редактировать, они также будут исключены из ModelForm используемой для создания и редактирования объектов. Однако, если вы определяете аргумент ModelAdmin.fields или ModelAdmin.fieldsets поля для чтения должны быть в них указаны (иначе они будут проигнорированы).

Если readonly_fields используется без определения порядка полей через атрибуты ModelAdmin.fields или ModelAdmin.fieldsets, поля из этой настройки будут отображаться после редактируемых полей.

```
readonly_fields = ('views_count', 'comment_count')
```

Read-only поле может показывать данные не только поля модели, но и метода, а также метода определенного в подклассе ModelAdmin. Работает как ModelAdmin.list_display. Это позволяет отображать различную информацию о редактируемом объекте, например:
```
from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('address_report',)

    def address_report(self, instance):
        # assuming get_full_address() returns a list of strings
        # for each line of the address and you want to separate each
        # line by a linebreak
        return format_html_join(
            mark_safe('<br/>'),
            '{}',
            ((line,) for line in instance.get_full_address()),
        ) or "<span class='errors'>I can't determine this address.</span>"

    # short_description functions like a model field's verbose_name
    address_report.short_description = "Address"
    # in this example, we have used HTML tags in the output
    address_report.allow_tags = True

```

## ModelAdmin.list_filter
Укажите list_filter, чтобы определить фильтры данных в правой панели страницы списка объектов, как показано на изображении:

list_filter - это список элементов, которые могу быть одного из следующих типов:

- название поля следующего типа: BooleanField, CharField, DateField, DateTimeField, IntegerField, ForeignKey или ManyToManyField. Например:

class PersonAdmin(admin.ModelAdmin):
    list_filter = ('is_staff', 'company')
Поле в list_filter может указывать и на связанный объект используя __, например:
```
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status', 'was_published_recently')
   
    list_filter = ['publish_date']

   
```


## ModelAdmin.save_as
Укажите save_as, чтобы включить возможность “сохранять как” на странице редактирования объекта.

По умолчанию страница содержит три кнопки: “Сохранить”, “Сохранить и продолжить редактирование” и “Сохранить и добавить новый”. Если save_as равен True, “Сохранить и добавить новый” будет заменена кнопкой “Сохранить как”.

“Сохранить как” сохранит объект как новый (с новым ID).

По умолчанию save_as равен False.

## ModelAdmin.save_on_top
Укажите save_on_top, чтобы добавить кнопки сохранения в верхней части страницы редактирования объекта.

По умолчанию кнопки сохранения отображаются под формой. Если указать save_on_top, кнопки будут отображаться и сверху и снизу.

По умолчанию save_on_top равен False.


## ModelAdmin.show_full_result_count

show_full_result_count указывает показывать ли количество всех объектов при фильтрации (например 99 results (103 total)). Если опция равна False, будет показан подобный текст: 99 results (Show all).

По умолчанию show_full_result_count=True выполняет запрос, чтобы получить количество всех объектов, что может работать очень медленно для таблиц с большим количеством данных.

## ModelAdmin.view_on_site

view_on_site определять показывать ли ссылку “Посмотреть на сайте”. Эта ссылка должна вести на страницу сохраненного объекта.

Можно указать булево или функцию. При True (по умолчанию) будет использоваться метод get_absolute_url() объекта для получения ссылки.

Если модель содержит метод get_absolute_url(), но вы не хотите показывать кнопку “Посмотреть на сайте”, укажите False в view_on_site:
```
from django.contrib import admin

class PersonAdmin(admin.ModelAdmin):
    view_on_site = False
```
Можно указать функцию, которая принимает один аргумент - объект модели. Например:
```
from django.contrib import admin
from django.core.urlresolvers import reverse

class PersonAdmin(admin.ModelAdmin):
    def view_on_site(self, obj):
        return 'http://example.com' + reverse('person-detail',
                                              kwargs={'slug': obj.slug})
```
# Настройки шаблонов
Используйте следующие настройки, чтобы переопределить шаблоны, которые используются представлениями ModelAdmin:

## ModelAdmin.add_form_template
Путь к шаблону, который используется add_view().

## ModelAdmin.change_form_template
Путь к шаблону, который используется change_view().

## ModelAdmin.change_list_template
Путь к шаблону, который используется changelist_view().

## ModelAdmin.delete_confirmation_template
Путь к шаблону, который используется delete_view() для отображения страницы подтверждения удаления одного или нескольких объектов.

## ModelAdmin.delete_selected_confirmation_template
Путь к шаблону, который используется delete_selected для отображения страницы подтверждения удаления одного или нескольких объектов. Подробности смотрите в разделе о действиях в интерфейсе администратора.

## ModelAdmin.object_history_template
Путь к шаблону, который используется history_view().

## Методы ModelAdmin

Методы ModelAdmin.save_model() и ModelAdmin.delete_model() должны сохранять/удалять объект. Их задача выполнять дополнительные операции, а не разрешать/запрещать операции удаления/сохранения.

## ModelAdmin.save_model(request, obj, form, change)

Метод save_model принимает объект HttpRequest, экземпляр модели, экземпляр ModelForm и булево значение указывающее создан объект или изменяется. В этом методе вы может выполнить дополнительные операции до или после сохранения.

Например, добавление request.user к объекту перед сохранением объекта:
```
from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
```
## ModelAdmin.delete_model(request, obj)

Метод delete_model принимает объект HttpRequest и экземпляр модели, который удаляется. В этом методе вы может выполнить дополнительные операции до или после удаления.

## ModelAdmin.save_formset(request, form, formset, change)
Метод save_formset принимает объект HttpRequest, ModelForm родительского объекта, “formset” связанных объектов и булево значение указывающее создан родительский объект или изменяется.

Например, добавление request.user к каждому объекту, измененному в наборе форм:
```
class ArticleAdmin(admin.ModelAdmin):
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()
```


# Переопределение шаблонов в интерфейсе администратора

Переопределить шаблоны, которые использует интерфейс администратора, очень легко. Вы можете переопределить шаблон для конкретного приложения или модели.

## Настройка каталогов в шаблонами
Шаблоны интерфейса администратора находятся в каталоге contrib/admin/templates/admin.

Чтобы переопределить шаблоны, для начала создайте каталог admin в каталоге templates проекта. Это может быть любой каталог, указанный в опции DIRS бэкенда DjangoTemplates` в настройке TEMPLATES. Если вы изменили опцию 'loaders', убедитесь, что 'django.template.loaders.filesystem.Loader' стоит перед 'django.template.loaders.app_directories.Loader'. Таким образом ваши шаблоны будет найдены до того, как Django найдет шаблоны из django.contrib.admin.

В каталоге admin создайте подкаталоги с названием приложений. В этих подкаталогах создайте подкаталоги для моделей. Заметим, что интерфейс администратора преобразует название модели в нижний регистр, так что убедитесь что название каталогов в нижнем регистре, если вы использует файловую систему учитывающую регистр названий каталог.

Чтобы переопределить шаблон для определенного приложения, скопируйте и отредактируйте необходимый шаблон из каталога django/contrib/admin/templates/admin и сохраните его в созданном подкаталоге.

Например, если необходимо изменить шаблон для представления списка объектов для всех моделей в приложении my_app, скопируйте contrib/admin/templates/admin/change_list.html в каталог templates/admin/my_app/ проекта и выполните необходимые изменения.

Если необходимо изменить шаблон только для модели ‘Page’, скопируйте тот же файл в каталог templates/admin/my_app/page проекта.

## Переопределение или замена шаблона в интерфейсе администратора
Учитывая модульную структуру шаблонов в интерфейсе администратора, как правило нет необходимости заменять весь шаблон. Целесообразней переопределить только необходимый блок шаблона.

Например, необходимо добавить ссылку после ссылки History для модели Page. Изучив change_form.html можно увидеть, что нам необходимо переопределить только блок object-tools-items. Вот наш новый шаблон change_form.html :
```
{% extends "admin/change_form.html" %}
{% load i18n admin_urls %}
{% block object-tools-items %}
    <li>
        <a href="{% url opts|admin_urlname:'history' original.pk|admin_urlquote %}" class="historylink">{% trans "History" %}</a>
    </li>
    <li>
        <a href="mylink/" class="historylink">My Link</a>
    </li>
    {% if has_absolute_url %}
        <li>
            <a href="{% url 'admin:view_on_site' content_type_id original.pk %}" class="viewsitelink">{% trans "View on site" %}</a>
        </li>
    {% endif %}
{% endblock %}
```
Добавим шаблон в каталог templates/admin/my_app и ссылка появится на странице редактирования объекта для всех моделей приложения my_app.

Шаблоны, которые можно переопределить для приложения или модели
Не каждый шаблон в contrib/admin/templates/admin можно переопределить для приложения или модели. Вот список переопределяемых шаблонов:
```
app_index.html
change_form.html
change_list.html
delete_confirmation.html
object_history.html
```
Остальные шаблоны вы можете все еще переопределить для всего проекта. Просто добавьте новую версию шаблона в каталог templates/admin. Это особенно полезно для переопределения страниц для 404 и 500 ошибки.

Некоторые шаблоны, такие как change_list_request.html используются для отображения включаемых тегов(inclusion tags). Вы можете переопределить их, но лучше создать собственную версию тега, которая будет использовать новый шаблон. В этом случае вы сможете использовать оба шаблона.
# Главный шаблон и шаблон страницы входа
Чтобы переопределить шаблоны главной страницы и страниц входа/выхода, лучше создать собственный экземпляр AdminSite, и изменить свойства AdminSite.index_template , AdminSite.login_template и AdminSite.logout_template.

## Объект AdminSite

## class AdminSite(name='admin')
Интерфейс администратора Django представлен экземпляром django.contrib.admin.sites.AdminSite. По умолчанию, экземпляр этого класса находится в django.contrib.admin.site и вы можете зарегистрировать модели с подклассами ModelAdmin в нем.

При создании экземпляра AdminSite, вы можете указать уникальное название экземпляра приложения передав аргумент name в конструктор. Это название используется для идентификации экземпляра что важно при поиске URL-ов интерфейса администратора. Если этот аргумент не указан, будет использовано значение по умолчанию admin. Смотрите раздел Настройка класса AdminSite о том, как настраивать класс AdminSite.

## Атрибуты AdminSite
Можно переопределить или заменить основные шаблоны в интерфейсе администратора как это описано в разделе Переопределение шаблонов в интерфейсе администратора.

## AdminSite.site_header

Текст, который отображается в заголовке каждой страницы, в h1. По умолчанию “Django administration”.

## AdminSite.site_title

Текст, который добавляется в title каждой страницы. По умолчанию “Django site admin”.

## AdminSite.site_url

URL для ссылки “View site” на верху каждой страницы админки. По умолчанию site_url равен /. Чтобы убрать эту ссылку, укажите None.

## AdminSite.index_title

Текст, который отображается в верху главной странице админки. По умолчанию “Site administration”.

## AdminSite.index_template
Шаблон, который будет использоваться для главной страницы.

## AdminSite.app_index_template
Шаблон, который будет использоваться для главной страницей приложения.

## AdminSite.login_template
Шаблон, который будет использоваться для страницы входа.

## AdminSite.login_form
Подкласс AuthenticationForm который будет использовать для представления авторизации в интерфейсе администратора.

## AdminSite.logout_template
Шаблон, который будет использоваться для страницы выхода.

## AdminSite.password_change_template
Шаблон, который будет использоваться для страницы смены пароля.

## AdminSite.password_change_done_template
Шаблон, который будет использоваться для страницы завершения смены пароля.


