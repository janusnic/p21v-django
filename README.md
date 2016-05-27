# p21v-django unit_08

shop
====

    ./manage.py startapp shop


Application definition
-----------------------

        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',

            'shop',
        ]

models.py
----------

        from django.db import models
        from django.core.urlresolvers import reverse
        from django.utils.encoding import python_2_unicode_compatible

        @python_2_unicode_compatible
        class Category(models.Model):
            name = models.CharField(max_length=200, db_index=True)
            slug = models.SlugField(max_length=200, db_index=True, unique=True)

            class Meta:
                ordering = ('name',)
                verbose_name = 'category'
                verbose_name_plural = 'categories'

            def __str__(self):
                return self.name

            def get_absolute_url(self):
                return reverse('shop:product_list_by_category', args=[self.slug])

        @python_2_unicode_compatible
        class Product(models.Model):
            category = models.ForeignKey(Category, related_name='products')
            name = models.CharField(max_length=200, db_index=True)
            slug = models.SlugField(max_length=200, db_index=True)
            image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
            description = models.TextField(blank=True)
            price = models.DecimalField(max_digits=10, decimal_places=2)
            stock = models.PositiveIntegerField()
            available = models.BooleanField(default=True)
            created = models.DateTimeField(auto_now_add=True)
            updated = models.DateTimeField(auto_now=True, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
            
            class Meta:
                ordering = ('-created',)
                index_together = (('id', 'slug'),)

            def __str__(self):
                return self.name

            def get_absolute_url(self):
                return reverse('shop:product_detail', args=[self.id, self.slug])


makemigrations
--------------

        ./manage.py makemigrations shop
        ./manage.py migrate

admin.py
--------

        from django.contrib import admin
        from .models import Category, Product

        class CategoryAdmin(admin.ModelAdmin):
            list_display = ['name', 'slug']
            prepopulated_fields = {'slug': ('name',)}
        admin.site.register(Category, CategoryAdmin)


        class ProductAdmin(admin.ModelAdmin):
            list_display = ['name', 'slug', 'category', 'price', 'stock', 'available', 'created', 'updated']
            list_filter = ['available', 'created', 'updated', 'category']
            list_editable = ['price', 'stock', 'available']
            prepopulated_fields = {'slug': ('name',)}
        admin.site.register(Product, ProductAdmin)



views.py
--------

        from django.shortcuts import render, get_object_or_404
        from .models import Category, Product
        

        def product_list(request, category_slug=None):
            category = None
            categories = Category.objects.all()
            products = Product.objects.filter(available=True)
            if category_slug:
                category = get_object_or_404(Category, slug=category_slug)
                products = products.filter(category=category)
            return render(request, 'shop/product/list.html', {'category': category,
                                                              'categories': categories,
                                                              'products': products})


        def product_detail(request, id, slug):
            product = get_object_or_404(Product, id=id, slug=slug, available=True)
            
            return render(request,
                          'shop/product/detail.html',
                          {'product': product,
                        })


shop/product/list.html
----------------------

        {% extends "shop/base.html" %}
        {% load static %}

        {% block title %}
            {% if category %}{{ category.name }}{% else %}Products{% endif %}
        {% endblock %}

        {% block content %}
            <div id="sidebar">
                <h3>Categories</h3>
                <ul>
                    <li {% if not category %}class="selected"{% endif %}>
                        <a href="{% url "shop:product_list" %}">All</a>
                    </li>
                {% for c in categories %}
                    <li {% if category.slug == c.slug %}class="selected"{% endif %}>
                        <a href="{{ c.get_absolute_url }}">{{ c.name }}</a>
                    </li>
                {% endfor %}
                </ul>
            </div>
            <div id="main" class="product-list">
                <h1>{% if category %}{{ category.name }}{% else %}Products{% endif %}</h1>
                {% for product in products %}
                    <div class="item">
                        <a href="{{ product.get_absolute_url }}">
                            <img src="{% if product.image %}{{ product.image.url }}{% else %}{% static "img/no_image.png" %}{% endif %}">
                        </a>
                        <a href="{{ product.get_absolute_url }}">{{ product.name }}</a><br>
                        ${{ product.price }}
                    </div>
                {% endfor %}
            </div>
        {% endblock %}

mysite/urls.py
--------------

        urlpatterns = [
            url(r'^$', view_home.index, name='index'),
            url(r'^soc/$', view_home.home, name='home'),
            url(r'^blog/', include('blog.urls', namespace="blog")),
            url(r'^shop/', include('shop.urls', namespace='shop')),
            url(r'^contact/', include('contact.urls', namespace="contact")),
            url(r'^userprofile/', include('userprofile.urls', namespace="userprofile")),
            url(r'^admin/', admin.site.urls),
            url(r'^ckeditor/', include('ckeditor_uploader.urls')),
            url(r'', include('social.apps.django_app.urls', namespace='social'))
        ]


shop/urls.py
------------

        from django.conf.urls import url
        from . import views
        urlpatterns = [
            url(r'^$', views.product_list, name='product_list'),
            url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
            url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
        ]


shop/product/detail.html
------------------------

        {% extends "shop/base.html" %}
        {% load static %}

        {% block title %}
            {{ product.name }}
        {% endblock %}

        {% block content %}
            <div class="product-detail">
                <img src="{% if product.image %}{{ product.image.url }}{% else %}{% static "img/no_image.png" %}{% endif %}">
                <h1>{{ product.name }}</h1>
                <h2><a href="{{ product.category.get_absolute_url }}">{{ product.category }}</a></h2>
                <p class="price">${{ product.price }}</p>
                
                {{ product.description|linebreaks }}
            </div>
        {% endblock %}


Django сессии
=============
Django полностью поддерживает сессии для анонимных пользователей, позволяет сохранять и получать данные для каждой посетителя сайта. Механизм сессии сохраняет данные на сервере и самостоятельно управляет сессионными куками. Куки содержат ID сессии,а не сами данные (если только вы не используете бэкенд на основе кук).

Активируем сессии
------------------
Сессии реализованы через промежуточный слой.

Чтобы активировать сессии, выполните следующие действия:

Убедитесь что MIDDLEWARE_CLASSES содержит 'django.contrib.sessions.middleware.SessionMiddleware'. settings.py по умолчанию, созданный django-admin startproject, уже содержит SessionMiddleware.

Есди вы не собираетесь использовать сессии, вы можете удалить SessionMiddleware из MIDDLEWARE_CLASSES и 'django.contrib.sessions' из INSTALLED_APPS. Это немного повысит производительность.

Настройка сессий
----------------
По умолчанию Django хранит сессии в базе данных (используя модель django.contrib.sessions.models.Session). В некоторых случаях лучше хранить данные сессии в других хранилищах, поэтому Django позволяет использовать файловую систему или кэш.

Использование базы данных для хранения сессии
---------------------------------------------
Если вы хотите использовать базу данных для хранения сесиии, укажите 'django.contrib.sessions' в настройке INSTALLED_APPS.

После настройки выполните manage.py migrate, чтобы добавить таблицу в базу данных.

Использование кэша для хранения сессии
---------------------------------------
Для улучшения производительности вы можете использовать кэш для хранения сессии.

Для этого вы должны настроить кэш.

Вам следует использовать кэш только при использовании Memcached. Кэш в памяти не хранит данные достаточно долго, и лучше использовать файлы или базу данных для сессии, чем каждый раз обращаться к кэшу в файловой системе или базе данных. Также кэш в памяти использует различные экземпляры кэша для разных процессов.
Если вы указали несколько кэшей в CACHES, Django будет использовать кэш по умолчанию. Чтобы использовать другой кэш, укажите его название в SESSION_CACHE_ALIAS.

После настройки кэша у вас есть две опции, как хранить данные в кэше:

Указать "django.contrib.sessions.backends.cache" в SESSION_ENGINE. Данные сессии будут храниться непосредственно в кэше. Однако, данные могут быть удалены при переполнении кэша или перезагрузке сервера кэша.

Для постоянно хранения закэшированных данных укажите "django.contrib.sessions.backends.cached_db" в SESSION_ENGINE. Все записи в кэш будут продублированы в базу данных. База данных будет использоваться, если данные не найдены в кэше.

Оба варианта работают достаточно быстро, но первый немного быстрее. Для большинства случаев cached_db будет достаточно быстрым, но если производительность для вас важнее, чем надежное хранение сессии, используйте бэкенд cache.

Если вы используете cached_db, вам необходимо настроить и бэкенд базы данных.

Использование файловой системы для хранения сессии
--------------------------------------------------
Чтобы использовать файловую систему, укажите "django.contrib.sessions.backends.file" в SESSION_ENGINE.

Вы также можете указать SESSION_FILE_PATH (по умолчанию tempfile.gettempdir(), обычно это /tmp), чтобы указать Django, где сохранять сессионные файлы. Убедитесь, что ваш сервер имеет права на чтение и запись указанного каталога.

Хранение сессии в куках
-----------------------
Чтобы хранить сессию в куках, укажите "django.contrib.sessions.backends.signed_cookies" в SESSION_ENGINE. Данные сессии будут сохранены в куках, используя криптографическую подпись и значение SECRET_KEY.

Рекомендуем указать True в SESSION_COOKIE_HTTPONLY, чтобы запретить доступ JavaScript к кукам.

Если SECRET_KEY не хранить в безопасности при использовании PickleSerializer, можно пострадать от атаки удаленного выполнения кода.

Злоумышленник, узнав SECRET_KEY, может не только подделать данные сессии, но и выполнить удаленный код т.к. данные сессии используют pickle.

Если вы храните сессию в куках, храните ваш секретный ключ максимально надежно для всех систем, которые используются пользователем.

Сессионные данные подписаны, но не закодированы
-----------------------------------------------
Клиент может прочитать данные сессии, если вы храните их в куках.

MAC (Message Authentication Code) используется для защиты данных от подделки пользователем. Данные будут недействительными, если пользователь попытается их поменять. Аналогичное происходит, если клиент, который хранит коки (например, браузер пользователя), не может сохранить сессионную куку и удаляет её. Несмотря на то , что Django сжимает данные, вполне возможно превысить принятый лимит 4096 байтов на куку.

Актуальность не гарантируется
-----------------------------
Обратите внимание, хотя MAC может гарантировать авторизацию данных (что они были созданы вашим сайтом, а не кем-то другим), и целостность данных (данные не менялись и правильны), он не может гарантировать актуальность, то есть, что полученные данные последние, которые вы отсылали клиенту. Это означает, что при определенном использовании кук для сессии, ваш сайт может быть подвержен replay атакам. В отличии от других бэкендов сессии, которые хранят данные на сервере и очищают их при выходе пользователя(log out), сессия в куках не очищается, когда пользователь выходит. По этому, если атакующий украдет куки пользователя, он может использовать их для входа даже после того, как пользователь вышел с сайта. Куки будут определены как устаревшие, если только они старее чем SESSION_COOKIE_AGE.

Производительность
------------------
Наконец, размер кук может повлиять на производительность вашего сайта.
Использование сессии в представлениях
-------------------------------------
Когда SessionMiddleware активный, каждый объект HttpRequest – первый аргумент представления в Django – будет содержать атрибут session, который является объектом с интерфейсом словаря.

Вы можете читать и менять request.session в любом месте вашего представления множество раз.

            def __init__(self, request):
                """
                Initialize the cart.
                """
                self.session = request.session
                cart = self.session.get(settings.CART_SESSION_ID)
                if not cart:
                    # save an empty cart in the session
                    cart = self.session[settings.CART_SESSION_ID] = {}
                self.cart = cart

class backends.base.SessionBase
-------------------------------
Это базовый класс для всех объектов сессии. Он предоставляет набор стандартных методов словаря:

__getitem__(key)
Например: fav_color = request.session['fav_color']

__setitem__(key, value)
Например: request.session['fav_color'] = 'blue'

__delitem__(key)
Например: del request.session['fav_color']. Вызовет KeyError, если key еще не в сессии.

__contains__(key)
Например: 'fav_color' in request.session

get(key, default=None)
Например: fav_color = request.session.get('fav_color', 'red')

pop(key)
Например: fav_color = request.session.pop('fav_color')

keys()
items()
setdefault()
clear()

            def clear(self):
                # empty cart
                self.session[settings.CART_SESSION_ID] = {}
                self.session.modified = True

Также содержит следующие методы:
--------------------------------
flush()
Удаляет данные текущей сессии и сессионную куку. Можно использовать, если необходимо убедиться, что старые данные не доступны с браузера пользователя (например, функция django.contrib.auth.logout() вызывает этот метод).

set_test_cookie()
Устанавливает тестовую куку, чтобы проверить, что браузер пользователя поддерживает куки. Из-за особенностей работы кук вы не сможете проверить тестовую куку, пока пользователь не запросит следующую страницу.

test_cookie_worked()
Возвращает True или False, в зависимости от того, принял ли бразуер пользователя тестовую куку. Из-за особенностей работы кук вам необходимо вызывать в предыдущем запросе set_test_cookie().

delete_test_cookie()
Удаляет тестовую куку. Используйте, чтобы убрать за собой.

set_expiry(value)
Указывает время жизни сессии. Вы можете передать различные значения:

Если value целое число, сессия истечет после указанного количества секунд не активности пользователя. Например, request.session.set_expiry(300) установит время жизни равное 5 минутам.

Если value это datetime или timedelta, сессия истечет в указанное время. Обратите внимание, datetime и timedelta сериализуются только при использовании PickleSerializer.

Если value равно 0, сессионная кука удалится при закрытии браузера.

Если value равно None, сессия будет использовать глобальное поведение.

Чтение сессии не обновляет время жизни сессии. Время жизни просчитывается с момента последнего изменения.

            def save(self):
                # update the session cart
                self.session[settings.CART_SESSION_ID] = self.cart
                # mark the session as "modified" to make sure it is saved
                self.session.modified = True

метод __init__
==============
Вызов класса происходит, когда создается объект.
------------------------------------------------
Метод __init__ вызывается сразу после создания экземпляра класса. Соблазнительно, но не правильно называть этот метод конструктором, потому что он выглядит как конструктор (принято, чтобы __init__ был первым методом, определенным в классе), ведет себя как коструктор (это перый кусок кода, вызываемый в созданном экземпляре класса) и даже называется как коструктор. Неправильно, так как к тому времени, когда вызывается метод __init__, объект уже создан и вы имеете ссылку на созданный экземпляр класса. Но метод __init__ — это самое близкое к конструктору, из того что есть в языке Python.

Первым аргументом каждого метода класса, включая __init__, всегда является текущий экземпляр класса. Общепринято всегда называть этот аргумент self. В методе __init__ self ссылается на только что созданный объект, в других методах — на экземпляр класса, для которого метод вызывается. Хотя и необходимо явно указывать self при определении метода, вы его не указываете, когда вызываете метод; Python добавит его автоматически.

Метод __init__ может иметь несколько аргументов. Аргументы могут иметь значения по умолчанию, что сделает их необязательными. В данном случае аргумент filename имеет значение по умолчанию None.

Первый аргумент метода класса (ссылка на текущий экземпляр) принято называть self. Этот аргумент играет роль зарезервированного слова this в C++ и Java, но self не является зарезервированным словом — просто соглашение. Несмотря на это, не стоит называть его иначе, чем self.

Итераторы
=========
Когда вы создаёте список, вы можете считывать его элементы один за другим — это называется итерацией:

            >>> mylist = [1, 2, 3]
            >>> for i in mylist :
            ...    print(i)


Mylist является итерируемым объектом. Когда вы создаёте список, используя генераторное выражение, вы создаёте также итератор:

            >>> mylist = [x*x for x in range(3)]
            >>> for i in mylist :
            ...    print(i)

Всё, к чему можно применить конструкцию «for… in...», является итерируемым объектом: списки, строки, файлы… Это удобно, потому что можно считывать из них значения сколько потребуется — однако все значения хранятся в памяти, а это не всегда желательно, если у вас много значений.

Генераторы
==========
Генераторы это тоже итерируемые объекты, но прочитать их можно лишь один раз. Это связано с тем, что они не хранят значения в памяти, а генерируют их на лету:
            
            >>> mygenerator = (x*x for x in range(3))
            >>> for i in mygenerator :
            ...    print(i)

Всё то же самое, разве что используются круглые скобки вместо квадратных. НО: нельзя применить конструкцию for i in mygenerator второй раз, так как генератор может быть использован только единожды: он вычисляет 0, потом забывает про него и вычисляет 1, завершаяя вычислением 4 — одно за другим.

Yield
=====
Yield это ключевое слово, которое используется примерно как return — отличие в том, что функция вернёт генератор.
            
            >>> def createGenerator() :
            ...    mylist = range(3)
            ...    for i in mylist :
            ...        yield i*i
            ...
            >>> mygenerator = createGenerator() # создаём генератор
            >>> print(mygenerator) # mygenerator является объектом!
            <generator object createGenerator at 0xb7555c34>
            >>> for i in mygenerator:
            ...     print(i)

когда вы вызываете функцию, код внутри тела функции не исполняется. Функция только возвращает объект-генератор

Ваш код будет вызываться каждый раз, когда for обращается к генератору.

В первый запуск функции, она будет исполняться от начала до того момента, когда она наткнётся на yield — тогда она вернёт первое значение из цикла. На каждый следующий вызов будет происходить ещё одна итерация написанного цикла, возвращаться будет следующее значение — и так пока значения не кончатся.

Генератор считается пустым, как только при исполнении кода функции не встречается yield. Это может случиться из-за конца цикла, или же если не выполняется какое-то из условий «if/else».


shop/cart.py
--------------

        from decimal import Decimal
        from django.conf import settings
        from .models import Product

        class Cart(object):

            def __init__(self, request):
                """
                Initialize the cart.
                """
                self.session = request.session
                cart = self.session.get(settings.CART_SESSION_ID)
                if not cart:
                    # save an empty cart in the session
                    cart = self.session[settings.CART_SESSION_ID] = {}
                self.cart = cart

            def __len__(self):
                """
                Count all items in the cart.
                """
                return sum(item['quantity'] for item in self.cart.values())

            def __iter__(self):
                """
                Iterate over the items in the cart and get the products from the database.
                """
                product_ids = self.cart.keys()
                # get the product objects and add them to the cart
                products = Product.objects.filter(id__in=product_ids)
                for product in products:
                    self.cart[str(product.id)]['product'] = product

                for item in self.cart.values():
                    item['price'] = Decimal(item['price'])
                    item['total_price'] = item['price'] * item['quantity']
                    yield item

            def add(self, product, quantity=1, update_quantity=False):
                """
                Add a product to the cart or update its quantity.
                """
                product_id = str(product.id)
                if product_id not in self.cart:
                    self.cart[product_id] = {'quantity': 0,
                                              'price': str(product.price)}
                if update_quantity:
                    self.cart[product_id]['quantity'] = quantity
                else:
                    self.cart[product_id]['quantity'] += quantity
                self.save()

            def remove(self, product):
                """
                Remove a product from the cart.
                """
                product_id = str(product.id)
                if product_id in self.cart:
                    del self.cart[product_id]
                    self.save()

            def save(self):
                # update the session cart
                self.session[settings.CART_SESSION_ID] = self.cart
                # mark the session as "modified" to make sure it is saved
                self.session.modified = True

            def clear(self):
                # empty cart
                self.session[settings.CART_SESSION_ID] = {}
                self.session.modified = True

            def get_total_price(self):
                return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

shop/forms.py
-------------

            from django import forms


            PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


            class CartAddProductForm(forms.Form):
                quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                                  coerce=int)
                update = forms.BooleanField(required=False,
                                            initial=False,
                                            widget=forms.HiddenInput)

shopt/urls.py
-------------

        """shop URL Configuration
        """
        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^cart/$', views.cart_detail, name='cart_detail'),
            url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
            url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
            url(r'^(?P<category_slug>[-\w]+)/$', views.index, name='product_index_by_category'),
            url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),

        ]

shopt/views.py
-------------

        from django.shortcuts import render, get_object_or_404
        from .models import Category, Product
        from .forms import CartAddProductForm


        def product_list(request, category_slug=None):
            category = None
            categories = Category.objects.all()
            products = Product.objects.filter(available=True)
            if category_slug:
                category = get_object_or_404(Category, slug=category_slug)
                products = products.filter(category=category)
            return render(request, 'shop/product/INDEX.html', {'category': category,
                                                              'categories': categories,
                                                              'products': products})

        def product_detail(request, id, slug):
            product = get_object_or_404(Product, id=id, slug=slug, available=True)
            cart_product_form = CartAddProductForm()
            return render(request,
                          'shop/product/detail.html',
                          {'product': product,
                           'cart_product_form': cart_product_form})

Система шаблонов
================

Django использует высокоуровневый API, который не привязан к конкретному бэкенду:

- Для каждого бэкенда DjangoTemplates из настройки the TEMPLATES, Django создает экземпляр Engine. DjangoTemplates оборачивает Engine, чтобы адаптировать его под API конкретного бэкенда шаблонов.
- Модуль django.template.loader предоставляет функции, такие как get_template(), для загрузки шаблонов. Они возвращают django.template.backends.django.Template, который оборачивает django.template.Template.
- Template, полученный на предыдущем шаге, содержит метод render(), который оборачивает контекст и запрос в Context и делегирует рендеринг основному объекту Template.

Настройка бэкенда
------------------

При создании Engine все аргументы должны передаваться как именованные:

- dirs – это список каталого, в которых бэкенд ищет файлы шаблонов. Используется для настройки filesystem.Loader. По умолчанию равен пустому списку.
- app_dirs влияет только на значение loaders по умолчанию. По умолчанию False.
- context_processors – список путей Python для импорта функций, которые используются для наполнения контекста шаблонов, если он рендерится с объектом запроса. Эти функции принимают объект запроса и возвращают dict значений, которые будут добавлены в контекст. По умолчанию равен пустому списку.
- debug – булево значение, которое включает и выключает режим отладки. При True шаблонизатор сохраняет дополнительную отладочную информацию, которая может использоваться для отображения информации ошибки, которая возникла во время рендеринга. По умолчанию False.
- loaders – список загрузчиков шаблонов, указанных строками. Каждый класс Loader знает как загрузить шаблоны из определенного источника. Вместо строки можно указать кортеж. Первым элементом должен быть путь к классу Loader, вторым – параметры, которые будут переданы в Loader при инициализации.
По умолчанию содержит список:
```
'django.template.loaders.filesystem.Loader'
'django.template.loaders.app_directories.Loader', только если app_dirs равен True.
```
- string_if_invalid значение, которые шаблонизатор выведет вместо неправильной переменной(например, с опечаткой в назчании). По умолчанию – пустая строка.
- file_charset – кодировка, которая используется при чтении файла шаблона с диска. По умолчанию 'utf-8'.


shop/views.py
-------------

        from django.shortcuts import render, redirect, get_object_or_404
        from django.views.decorators.http import require_POST
        from .models import Product
        from .cart import Cart
        from .forms import CartAddProductForm


        @require_POST
        def cart_add(request, product_id):
            cart = Cart(request)
            product = get_object_or_404(Product, id=product_id)
            form = CartAddProductForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                cart.add(product=product,
                         quantity=cd['quantity'],
                         update_quantity=cd['update'])
            return redirect('shop:cart_detail')


        def cart_remove(request, product_id):
            cart = Cart(request)
            product = get_object_or_404(Product, id=product_id)
            cart.remove(product)
            return redirect('shop:cart_detail')


        def cart_detail(request):
            cart = Cart(request)
            for item in cart:
                item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                           'update': True})
            return render(request, 'shop/product/cart.html', {'cart': cart})

Процессоры контекста
====================
список процессоров контекста по умолчанию:
------------------------------------------
1. django.contrib.auth.context_processors.auth
Если включить этот процессор, в RequestContext будут добавлены следующие переменные:
- user – объект auth.User текущего авторизованного пользователя или объект AnonymousUser, если пользователь не авторизованный).
- perms – объект django.contrib.auth.context_processors.PermWrapper, которые содержит права доступа текущего пользователя.

2. django.template.context_processors.debug
Если включить этот процессор, в RequestContext будут добавлены следующие переменные, но только при DEBUG равном True и, если IP адрес запроса (request.META['REMOTE_ADDR']) указан в INTERNAL_IPS:
- debug – True. Вы можете использовать эту переменную, чтобы определить DEBUG режим в шаблоне.
- sql_queries – список словарей {'sql': ..., 'time': ...}, который содержит все SQL запросы и время их выполнения, которые были выполнены при обработке запроса. Список отсортирован в порядке выполнения SQL запроса.

3. django.template.context_processors.i18n
Если включить этот процессор, в RequestContext будут добавлены следующие переменные:
- LANGUAGES – значение настройки LANGUAGES.
- LANGUAGE_CODE – request.LANGUAGE_CODE, если существует. Иначе значение LANGUAGE_CODE.

4. django.template.context_processors.media
Если включить этот процессор, в RequestContext будет добавлена переменная MEDIA_URL, которая содержит значение MEDIA_URL.

5. django.template.context_processors.static
Если включить этот процессор, в RequestContext будет добавлена переменная STATIC_URL, которая содержит значение STATIC_URL.

6. django.template.context_processors.csrf
Этот процессор добавляет токен, который используется тегом csrf_token для защиты от CSRF атак.

7. django.template.context_processors.request
Если включить этот процессор, в RequestContext будет добавлена переменная request, содержащая текущий HttpRequest.

8. django.contrib.messages.context_processors.messages
Если включить этот процессор, в RequestContext будут добавлены следующие переменные:
- messages – список сообщений (строки), которые были добавлены с помощью фреймворка сообщений.
- DEFAULT_MESSAGE_LEVELS – словарь приоритетов сообщений и их числовых кодов.

Как создать свой процессор контекста
------------------------------------
Интерфейс процессора контекста - это функция Python, которая принимает один аргумент, объект HttpRequest, и возвращает словарь, которая будет добавлен в контекст шаблона. Процессор контекста обязательно должен возвращать словарь.

Код процессора может находится где угодно. Главное не забыть указать его в опции 'context_processors' настройки:setting:TEMPLATES, или передать аргументом context_processors в Engine.


shop/processors/context_processors.py
-------------------------------------

        from ..cart import Cart

        def cart(request):
            return {'cart': Cart(request) }


settings.py
-----------
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(BASE_DIR, "templates")],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                        'shop.processors.context_processors.cart',
                    ],
                },
            },
        ]


shop/product/cart.html
------------------------

        {% extends "base.html" %}
        {% load static %}

        {% block title %}Your shopping cart{% endblock %}

        {% block content %}
            <div class="container">
              <!-- row of columns -->
              <div class="row">
                <div class="col-md-4 sidebar">
                    <h3>Categories</h3>
                    <ul>
                        <li {% if not category %}class="selected"{% endif %}>
                            <a href="{% url "shop:index" %}">All</a>
                        </li>
                    {% for c in categories %}
                        <li {% if category.slug == c.slug %}class="selected"{% endif %}>
                            <a href="{{ c.get_absolute_url }}">{{ c.name }}</a>
                        </li>
                    {% endfor %}
                    </ul>
                </div>

            <div id="main" class="col-md-8 product-list">
            
            <h1>Your shopping cart</h1>
            <table class="cart">
                <thead>
                    <tr>
                        <th>Image</th>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Remove</th>
                        <th>Unit price</th>                
                        <th>Price</th>
                    </tr>
                </thead>
                <tbody>
                {% for item in cart %}
                    {% with product=item.product %}
                    <tr>
                        <td>
                            <a href="{{ product.get_absolute_url }}">
                                <img src="{% if product.image %}{{ product.image.url }}{% else %}{% static "img/no_image.png" %}{% endif %}">
                            </a>
                        </td>
                        <td>{{ product.name }}</td>
                        <td>
                            <form action="{% url "shop:cart_add" product.id %}" method="post">
                                {{ item.update_quantity_form.quantity }}
                                {{ item.update_quantity_form.update }}
                                <input type="submit" value="Update">
                                {% csrf_token %}
                            </form>
                        </td>
                        <td><a href="{% url "shop:cart_remove" product.id %}">Remove</a></td>
                        <td class="num">${{ item.price }}</td>
                        <td class="num">${{ item.total_price }}</td>
                    </tr>
                    {% endwith %}
                {% endfor %}
                <tr class="total">
                    <td>Total</td>
                    <td colspan="4"></td>
                    <td class="num">${{ cart.get_total_price }}</td>
                </tr>
                </tbody>
            </table>
            <p class="text-right">
                <a href="{% url "shop:index" %}" class="button light">Continue shopping</a>
                <a href="#" class="button">Checkout</a>
            </p>

         </div>
        </div>
        <hr>

        {% endblock %}


redirect
========
redirect(to, [permanent=False, ]*args, **kwargs)
Возвращает перенаправление(HttpResponseRedirect) на URL указанный через аргументы.

В аргументах можно передать:

- Экземпляр модели: как URL будет использоваться результат вызова метода get_absolute_url().

- Название представления, возможно с аргументами: для вычисления URL-а будет использоваться функция urlresolvers.reverse.

- Абсолютный или относительный URL, который будет использован для перенаправления на указанный адрес.

По умолчанию использует временное перенаправление, используйте аргумент permanent=True для постоянного перенаправления.

Функцию redirect() можно использовать несколькими способами.
------------------------------------------------------------
Передавая объект; в качестве URL-а для перенаправления будет использоваться результат вызова метода get_absolute_url():

        from django.shortcuts import redirect

        def my_view(request):
            ...
            object = MyModel.objects.get(...)
            return redirect(object)
Передавая название представления и необходимые позиционные или именованные аргументы; URL будет вычислен с помощью функции reverse():

        def my_view(request):
            ...
            return redirect('some-view-name', foo='bar')

Передавая непосредственно URL:

        def my_view(request):
            ...
            return redirect('/some/url/')
Работает также с полным URL-ом:

        def my_view(request):
            ...
            return redirect('http://example.com/')
По умолчанию, redirect() возвращает временное перенаправление. Все варианты выше принимают аргумент permanent; если передать True будет использоваться постоянное перенаправление:

        def my_view(request):
            ...
            object = MyModel.objects.get(...)
            return redirect(object, permanent=True)

Form.is_valid()
---------------
Главной задачей объекта Form является проверка данных. У заполненного экземпляра Form вызовите метод is_valid() для выполнения проверки и получения её результата:

        >>> data = {'subject': 'hello',
        ...         'message': 'Hi there',
        ...         'sender': 'foo@example.com',
        ...         'cc_myself': True}
        >>> f = ContactForm(data)
        >>> f.is_valid()
        True
Начнём с неправильных данных. В этом случае поле subject будет пустым (ошибка, так как по умолчанию все поля должны быть заполнены), а поле sender содержит неправильный адрес электронной почты:

        >>> data = {'subject': '',
        ...         'message': 'Hi there',
        ...         'sender': 'invalid email address',
        ...         'cc_myself': True}
        >>> f = ContactForm(data)
        >>> f.is_valid()
        False
Form.errors
-----------
Обратитесь к атрибуту errors для получения словаря с сообщениями об ошибках:

        >>> f.errors
        {'sender': ['Enter a valid email address.'], 'subject': ['This field is required.']}
В этом словаре, ключами являются имена полей, а значениями – списки юникодных строк, представляющих сообщения об ошибках. Сообщения хранятся в виде списков, так как поле может иметь множество таких сообщений.

Обращаться к атрибуту errors можно без предварительного вызова методе call is_valid(). Данные формы будут проверены при вызове метода is_valid() или при обращении к errors.

Процедуры проверки выполняются один раз, независимо от количества обращений к атрибуту errors или вызова метода is_valid(). Это означает, что если проверка данных имеет побочное влияние на состояние формы, то оно проявится только один раз.


Доступ к “чистым” данным
========================
Form.cleaned_data
-----------------
Каждое поле в классе Form отвечает не только за проверку, но и за нормализацию данных. Это приятная особенность, так как она позволяет вводить данные в определённые поля различными способами, всегда получая правильный результат.

После создания экземпляра Form, привязки данных и их проверки, вы можете обращаться к “чистым” данным через атрибут cleaned_data:

        >>> data = {'subject': 'hello',
        ...         'message': 'Hi there',
        ...         'sender': 'foo@example.com',
        ...         'cc_myself': True}
        >>> f = ContactForm(data)
        >>> f.is_valid()
        True
        >>> f.cleaned_data
        {'cc_myself': True, 'message': 'Hi there', 'sender': 'foo@example.com', 'subject': 'hello'}
Следует отметить, что любое текстовое поле, такое как CharField или EmailField, всегда преобразует текст в юникодную строку. Мы рассмотрим применения кодировок далее.

Если данные не прошли проверку, то атрибут cleaned_data будет содержать только значения тех полей, что прошли проверку:

        >>> data = {'subject': '',
        ...         'message': 'Hi there',
        ...         'sender': 'invalid email address',
        ...         'cc_myself': True}
        >>> f = ContactForm(data)
        >>> f.is_valid()
        False
        >>> f.cleaned_data
        {'cc_myself': True, 'message': 'Hi there'}
Атрибут cleaned_data всегда содержит только данные для полей, определённых в классе Form, даже если вы передали дополнительные данные при определении Form. В этом примере, мы передаём набор дополнительных полей в конструктор ContactForm, но cleaned_data содержит только поля формы:

        >>> data = {'subject': 'hello',
        ...         'message': 'Hi there',
        ...         'sender': 'foo@example.com',
        ...         'cc_myself': True,
        ...         'extra_field_1': 'foo',
        ...         'extra_field_2': 'bar',
        ...         'extra_field_3': 'baz'}
        >>> f = ContactForm(data)
        >>> f.is_valid()
        True
        >>> f.cleaned_data # Doesn't contain extra_field_1, etc.
        {'cc_myself': True, 'message': 'Hi there', 'sender': 'foo@example.com', 'subject': 'hello'}
Если Form прошла проверку, то cleaned_data будет содержать ключ и значение для всех полей формы, даже если данные не включают в себя значение для некоторых необязательных полей. В данном примере, словарь данных не содержит значение для поля nick_name, но cleaned_data содержит пустое значение для него:

        >>> from django.forms import Form
        >>> class OptionalPersonForm(Form):
        ...     first_name = CharField()
        ...     last_name = CharField()
        ...     nick_name = CharField(required=False)
        >>> data = {'first_name': 'John', 'last_name': 'Lennon'}
        >>> f = OptionalPersonForm(data)
        >>> f.is_valid()
        True
        >>> f.cleaned_data
        {'nick_name': '', 'first_name': 'John', 'last_name': 'Lennon'}


EmailField
-----------
    class EmailField([max_length=75, **options])
Поле CharField для хранения правильного email-адреса.

Значение max_length в 75 символов не достаточно для хранения всех возможных значений в соответствии RFC3696/5321. Для хранения всех возможных вариантов необходимо значение max_length в 254. Значение в 75 символов сложилось исторически и не изменяется для обратной совместимости.

DecimalField
-------------
        class DecimalField(max_digits=None, decimal_places=None[, **options])
Десятичное число с фиксированной точностью, представленное объектом Decimal Python. Принимает два обязательных параметра:

- DecimalField.max_digits
Максимальное количество цифр в числе - это число должно быть больше или равно decimal_places.

- DecimalField.decimal_places
Количество знаков после запятой.

Например, для хранения числа до 999 с двумя знаками после запятой, используйте:

- models.DecimalField(..., max_digits=5, decimal_places=2)
Для хранения числа до миллиарда и 10 знаков после запятой:

- models.DecimalField(..., max_digits=19, decimal_places=10)
Виджет по умолчанию для этого поля TextInput.


PositiveIntegerField
---------------------
        class PositiveIntegerField([**options])
Как и поле IntegerField, но значение должно быть больше или равно нулю (0). Можно использовать значение от 0 до 2147483647. Значение 0 принимается для обратной совместимости.

Orders
======
shop/models.py
---------------

        @python_2_unicode_compatible
        class Order(models.Model):
            first_name = models.CharField(max_length=50)
            last_name = models.CharField(max_length=50)
            email = models.EmailField()
            address = models.CharField(max_length=250)
            postal_code = models.CharField(max_length=20)
            city = models.CharField(max_length=100)
            created = models.DateTimeField(auto_now_add=True)
            updated = models.DateTimeField(auto_now=True)
            paid = models.BooleanField(default=False)

            class Meta:
                ordering = ('-created',)

            def __str__(self):
                return 'Order {}'.format(self.id)

            def get_total_cost(self):
                return sum(item.get_cost() for item in self.items.all())

        @python_2_unicode_compatible
        class OrderItem(models.Model):
            order = models.ForeignKey(Order, related_name='items')
            product = models.ForeignKey(Product, related_name='order_items')
            price = models.DecimalField(max_digits=10, decimal_places=2)
            quantity = models.PositiveIntegerField(default=1)

            def __str__(self):
                return '{}'.format(self.id)

            def get_cost(self):
                return self.price * self.quantity


ModelAdmin.raw_id_fields
-------------------------
По умолчанию Django использует select для полей ForeignKey. Если связанных объектов очень много, создание select может быть очень затратным процессом.

raw_id_fields содержит список полей, которые будут использовать поле Input для ForeignKey или ManyToManyField:

        class ArticleAdmin(admin.ModelAdmin):
            raw_id_fields = ("newspaper",)
Виджет поля для raw_id_fields будет содержать значение первичного ключа для ForeignKey или список ключей для ManyToManyField. Возле поля есть кнопка поиска и выбора связанных объектов


Объект InlineModelAdmin
-----------------------
- class InlineModelAdmin
- class TabularInline
- class StackedInline

Интерфейс администратора позволяет редактировать связанные объекты на одной странице с родительским объектом. Это называется “inlines”. Например, у нас есть две модели:

    from django.db import models

    class Author(models.Model):
       name = models.CharField(max_length=100)

    class Book(models.Model):
       author = models.ForeignKey(Author)
       title = models.CharField(max_length=100)

Вы можете редактировать книги автора на странице редактирования автора. Вы добавляете “inlines” к модели добавив их в ModelAdmin.inlines:

        from django.contrib import admin

        class BookInline(admin.TabularInline):
            model = Book

        class AuthorAdmin(admin.ModelAdmin):
            inlines = [
                BookInline,
            ]
Django предоставляет два подкласса InlineModelAdmin:
----------------------------------------------------
- TabularInline
- StackedInline
Разница между ними только в используемом шаблоне.

Параметры InlineModelAdmin
---------------------------
InlineModelAdmin содержит некоторые возможности ModelAdmin и собственные. Общие методы и атрибуты определены в классе BaseModelAdmin:

form
fieldsets
fields
formfield_overrides
exclude
filter_horizontal
filter_vertical
ordering
prepopulated_fields
get_queryset()
radio_fields
readonly_fields
raw_id_fields
formfield_for_choice_field()
formfield_for_foreignkey()
formfield_for_manytomany()
has_add_permission()
has_change_permission()
has_delete_permission()

Параметры класса InlineModelAdmin:
----------------------------------
- InlineModelAdmin.model
Модель используемая в “inline”. Обязательный параметр.

- InlineModelAdmin.fk_name
Название внешнего ключа модели. В большинстве случаев он определяется автоматически, но вы должны указать fk_name, если модель содержит несколько внешних ключей к родительской модели.

- InlineModelAdmin.formset
По умолчанию – BaseInlineFormSet. Использование собственного класса предоставляет большие возможности для переопределения поведения по умолчанию. Смотрите раздел о наборах модельных форм.

- InlineModelAdmin.form
Значение form по умолчанию – ModelForm. Это значение передается в inlineformset_factory() при создании набора форм.

При добавлении собственной валидации в форму InlineModelAdmin, учитывайте состояние родительской модели. Если родительская форма не пройдет валидацию, она может содержать не консистентные данные.

- InlineModelAdmin.extra
Указывает количество пустых форм для добавления объектов в наборе форм. Подробности смотрите в разделе о наборе форм.

Если JavaScript включен в браузере, ссылка “Add another” позволит добавить новую пустую форму в дополнение к формам указанным параметром extra.

Ссылка не появится если количество отображаемых форм превышает значение в параметре max_num, или если у пользователя отключен JavaScript.

InlineModelAdmin.get_extra() позволяет указать количество дополнительных форм.

- InlineModelAdmin.max_num
Указывает максимальное количество форм. Этот параметр не определяет количество связанных объектов. Подробности смотрите в разделе Ограничение количества редактируемых объектов.

InlineModelAdmin.get_max_num() позволяет указать максимальное количество дополнительных форм.

- InlineModelAdmin.min_num
Указывает минимальное количество отображаемых форм.

InlineModelAdmin.get_min_num() позволяет указать минимальное количество отображаемых форм.

- InlineModelAdmin.raw_id_fields
По умолчанию Django использует select для полей ForeignKey. Если связанных объектов очень много, создание select может быть очень затратным процессом.

- raw_id_fields – список полей которые должны использовать Input виджет для полей ForeignKey или ManyToManyField:

        class BookInline(admin.TabularInline):
            model = Book
            raw_id_fields = ("pages",)
        InlineModelAdmin.template
Шаблон для отображения.
-----------------------
- InlineModelAdmin.verbose_name
Позволяет переопределить значение verbose_name класса Meta модели.

- InlineModelAdmin.verbose_name_plural
Позволяет переопределить значение verbose_name_plural класса Meta модели.

- InlineModelAdmin.can_delete
Определяет можно ли удалять связанные объекты. По умолчанию равно True.

- InlineModelAdmin.get_formset(request, obj=None, **kwargs)
Возвращает BaseInlineFormSet, который будет использоваться на странице создания/редактирования.

- InlineModelAdmin.get_extra(request, obj=None, **kwargs)
Возвращает количество форм. По умолчанию возвращает значение атрибута InlineModelAdmin.extra.

Вы можете переопределить метод и добавить логику для определения количества форм. Например, учитывать данные объекта модели(передается как именованный аргумент obj):

        class BinaryTreeAdmin(admin.TabularInline):
            model = BinaryTree

            def get_extra(self, request, obj=None, **kwargs):
                extra = 2
                if obj:
                    return extra - obj.binarytree_set.count()
                return extra

- InlineModelAdmin.get_max_num(request, obj=None, **kwargs)
Возвращает максимальное количество дополнительных форм. По умолчанию возвращает значение атрибута InlineModelAdmin.max_num.

Вы можете переопределить метод и добавить логику для определения максимального количества форм. Например, учитывать данные объекта модели(передается как именованный аргумент obj):

        class BinaryTreeAdmin(admin.TabularInline):
            model = BinaryTree

            def get_max_num(self, request, obj=None, **kwargs):
                max_num = 10
                if obj.parent:
                    return max_num - 5
                return max_num
- InlineModelAdmin.get_min_num(request, obj=None, **kwargs)
Возвращает минимальное количество дополнительных форм. По умолчанию возвращает значение атрибута InlineModelAdmin.min_num.

Вы можете переопределить метод и добавить логику для определения минимального количества форм. Например, учитывать данные объекта модели(передается как именованный аргумент obj).


shop/admin.py
--------------

from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    
admin.site.register(Order, OrderAdmin)


shop/views.py
--------------

        from django.shortcuts import render
        from .models import OrderItem
        from .forms import OrderCreateForm
        from .tasks import order_created
        from .cart import Cart

        def order_create(request):
            cart = Cart(request)
            if request.method == 'POST':
                form = OrderCreateForm(request.POST)
                if form.is_valid():
                    order = form.save()
                    for item in cart:
                        OrderItem.objects.create(order=order,
                                                 product=item['product'],
                                                 price=item['price'],
                                                 quantity=item['quantity'])
                    # clear the cart
                    cart.clear()
                    # launch task
                    order_created(order.id)
                    return render(request, 'shop/orders/created.html', {'order': order})
            else:
                form = OrderCreateForm()
            return render(request, 'shop/orders/create.html', {'cart': cart,
                                                        'form': form})

shop/forms.py
---------------
```
from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']

```
shop/tasks.py
---------------
```
from django.core.mail import send_mail
from .models import Order

def order_created(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order. Your order id is {}.'.format(order.first_name,
                                                                             order.id)
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_sent

```

shop/orders/create.html
-----------------------

        {% extends "shop/base.html" %}

        {% block title %}  Checkout {% endblock %}

        {% block content %}
            <h1>Checkout</h1>
            <div class="order-info">
                <h3>Your order</h3>
                <ul>
                    {% for item in cart %}
                        <li>{{ item.quantity }}x {{ item.product.name }} <span>${{ item.total_price }}</span></li>
                    {% endfor %}
                </ul>
                <p>Total: ${{ cart.get_total_price }}</p>
            </div>
            <form action="." method="post" class="order-form">
                {{ form.as_p }}
                <p><input type="submit" value="Place order"></p>
                {% csrf_token %}
            </form>
        {% endblock %}


shop/orders/created.html
------------------------

        {% extends "shop/base.html" %}

        {% block title %}
            Thank you
        {% endblock %}

        {% block content %}
            <h1>Thank you</h1>
            <p>Your order has been successfully completed. Your order number is <strong>{{ order.id }}</strong>.</p>
        {% endblock %}


shop/urls.py
-------------

        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^create/$', views.order_create, name='order_create'),
        ]


shop/product/detail.html
------------------------

            {% extends "shop/base.html" %}
            {% load static %}

            {% block title %}
                Your shopping cart
            {% endblock %}

            {% block content %}
                <h1>Your shopping cart</h1>
                <table class="cart">
                    <thead>
                        <tr>
                            <th>Image</th>
                            <th>Product</th>
                            <th>Quantity</th>
                            <th>Remove</th>
                            <th>Unit price</th>                
                            <th>Price</th>
                        </tr>
                    </thead>
                    <tbody>
                    {% for item in cart %}
                        {% with product=item.product %}
                        <tr>
                            <td>
                                <a href="{{ product.get_absolute_url }}">
                                    <img src="{% if product.image %}{{ product.image.url }}{% else %}{% static "img/no_image.png" %}{% endif %}">
                                </a>
                            </td>
                            <td>{{ product.name }}</td>
                            <td>
                                <form action="{% url "shop:cart_add" product.id %}" method="post">
                                    {{ item.update_quantity_form.quantity }}
                                    {{ item.update_quantity_form.update }}
                                    <input type="submit" value="Update">
                                    {% csrf_token %}
                                </form>
                            </td>
                            <td><a href="{% url "shop:cart_remove" product.id %}">Remove</a></td>
                            <td class="num">${{ item.price }}</td>
                            <td class="num">${{ item.total_price }}</td>
                        </tr>
                        {% endwith %}
                    {% endfor %}
                    <tr class="total">
                        <td>Total</td>
                        <td colspan="4"></td>
                        <td class="num">${{ cart.get_total_price }}</td>
                    </tr>
                    </tbody>
                </table>
                <p class="text-right">
                    <a href="{% url "shop:product_list" %}" class="button light">Continue shopping</a>
                    <a href="{% url "shop:order_create" %}" class="button">Checkout</a>
                </p>
            {% endblock %}

Отправка электронных писем
===========================
Код находится в модуле django.core.mail.

Пример
```
from django.core.mail import send_mail

send_mail('Subject here', 'Here is the message.', 'from@example.com',
    ['to@example.com'], fail_silently=False)
```
Письмо отправлено через SMTP хост и порт, которые указаны в настройках EMAIL_HOST и EMAIL_PORT. Настройки EMAIL_HOST_USER и EMAIL_HOST_PASSWORD, если указаны, используются для авторизации на SMTP сервере, а настройки EMAIL_USE_TLS и EMAIL_USE_SSL указывают использовать ли безопасное соединение.

При отправке письма через django.core.mail будет использоваться кодировка из DEFAULT_CHARSET.
send_mail()
```
send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)
```
Самый простой способ отправить письмо – использовать django.core.mail.send_mail().

Параметры subject, message, from_email и recipient_list являются обязательными.
-------------------------------------------------------------------------------
1. subject: строка.
2. message: строка.
3. from_email: строка.
4. recipient_list: список строк, каждая является email. Каждый получатель из recipient_list будет видеть остальных получателей в поле “To:” письма.
5. fail_silently: булево. При False send_mail вызовет smtplib.SMTPException. 
6. auth_user: необязательное имя пользователя, которое используется при авторизации на SMTP сервере. Если не указано, Django будет использовать значение EMAIL_HOST_USER.
7. auth_password: необязательный пароль, который используется при авторизации на SMTP сервере. Если не указано, Django будет использовать значение EMAIL_HOST_PASSWORD.
8. connection: необязательный бэкенд, который будет использоваться для отправки письма. Если не указан, будет использоваться бэкенд по умолчанию. 
9. html_message: если html_message указано, письмо будет с multipart/alternative, и будет содержать message с типом text/plain, и html_message с типом text/html.

Возвращает количество успешно отправленных писем (которое будет 0 или 1, т.к. функция отправляет только одно письмо).

Пример
------
Отправляет одно письмо john@example.com и jane@example.com, они оба указаны в “To:”:
```
send_mail('Subject', 'Message.', 'from@example.com',
    ['john@example.com', 'jane@example.com'])
```

Бэкенды для отправки электронной почты
---------------------------------------
Непосредственная отправка электронного письма происходит в бэкенде.

Django предоставляет несколько бэкендов. Эти бэкенды, кроме SMTP (который используется по умолчанию), полезны только при разработке или тестировании. Вы можете создать собственный бэкенд.

SMTP бэкенд
===========

Это бэкенд по умолчанию. Почта отправляется через SMTP сервер. Адрес сервера и параметры авторизации указаны в настройках EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS, EMAIL_USE_SSL, EMAIL_TIMEOUT, EMAIL_SSL_CERTFILE и EMAIL_SSL_KEYFILE.

SMTP бэкенд используется в Django по умолчанию. Если вы хотите указать его явно, добавьте в настройки:
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```
Dummy бэкенд
------------
Этот бэкенд ничего не делает с почтой. Чтобы указать этот бэкенд, добавьте следующее в настройки:
```
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
```
Этот бэкенд не следует использовать на боевом сервере, он создавался для разработки.

Настройка почты при разработке
==============================

Самый простой способ настроить почту для разработки – использовать бэкенд console. Этот бэкенд перенаправляет всю почту в stdout, позволяя увидеть содержимое писем.

Также можно использовать file. Этот бэкенд сохраняет содержимое каждого SMTP-соединения в файл.

Еще один способ – использовать локальный SMTP-сервер, который принимает письма и выводит их в консоль, но никуда их не оправляет. Python позволяет создать такой сервер одной командой:
```
python -m smtpd -n -c DebuggingServer localhost:1025
```
Эта команда запускает простой SMTP-сервер, который слушает 1025 порт на localhost. Этот сервер выводит заголовки и содержимое полученных писем в консоль. Вам необходимо указать в настройках EMAIL_HOST и EMAIL_PORT. Подробности об этом SMTP-сервер смотрите в документации Python к модулю smtpd.

settings.py
-----------
```
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = 'janusnic@gmail.com'
EMAIL_PORT = 1025

```
Пароли приложений Gmail
=======================
https://support.google.com/accounts/
Если вы пользуетесь двухэтапной аутентификацией, то специальные пароли понадобятся вам для входа в некоторые приложения (например, Outlook или почтовый клиент на iPhone/Mac). Вам не нужно запоминать эти пароли – наша система сгенерирует их автоматически. Подробнее...

Откройте настройки аккаунта Google на своем устройстве и введите шестнадцатизначный пароль, указанный выше.
Этот пароль открывает приложению или устройству доступ к вашему аккаунту Google (как и обычный пароль). Его не нужно запоминать. Также просим вас не записывать его и никому не показывать.


Create an Application specific password
---------------------------------------
- Visit your Google Account security page.
- In the 2-Step Verification box, click Settings(if there is no settings link, you may want to create a new one. you can skip step 3 & 4).
- Click the tab for App-specific passwords.
- Click Manage your application specific passwords.
- Under the Application-specific passwords section, enter a descriptive name for the application you want to authorize, such as "Django gmail" then click Generate application-specific password button.
- note down the password. for example: smbumqjiurmqrywn 

Then add the appropriate values to settings.py:
------------------------------------------------
```
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your-username@gmail.com'
EMAIL_HOST_PASSWORD = 'Application spectific password(for eg: smbumqjiurmqrywn)'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```
You can use the shell to test it:
```
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'This is a test', 'your@email.com', ['toemail@email.com'],
     fail_silently=False)
```