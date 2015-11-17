## p21v-django unit 11
django-p21v
============

![Django 1.8.6](https://img.shields.io/badge/Django-1.8.5-green.svg)
[![Django Model Builder](https://img.shields.io/badge/Django-Requirements-orange.svg)](http://mmcardle.github.io/django_builder)
[![Dependencies Status](https://img.shields.io/badge/Django-Dependencies-red.svg)](https://github.com/janusnic/p21v-django)
[![devDependencies Status](https://img.shields.io/badge/Django-devDependencies-yellowgreen.svg)](https://github.com/janusnic/p21v-django)
[![MIT License](https://img.shields.io/cocoapods/l/AFNetworking.svg)](http://opensource.org/licenses/MIT)


Профайл пользователя: Наследование моделей
==========================================

классы моделей могут наследоваться от любой существующей модели. Дополнительные поля сохраняются в отдельной таблице, которая подключается к таблице основной модели. Когда вы запрашиваете данные из своей модели, запрос использует JOIN для получения полей из неё и из базовой модели.

Наследование от User
--------------------
Вместо того, чтобы создать класс для профайла пользователя, почему бы не унаследовать класс от стандартного User и добавить несколько полей?
```
from django.contrib.auth.models import User, UserManager

class CustomUser(User):
    """User with app settings."""
    timezone = models.CharField(max_length=50, default='Europe/London')

    # Use UserManager to get the create_user method, etc.
    objects = UserManager()
```
После этого, каждый экземпляр CustomerUser будет обладать стандартными для User полями и методами, одновременно с наличием наших дополнительных полей и методов.

Мы добавим UserManager в качестве менеджера, получая таким образом доступ к стандартным методам. Например, для создания пользователя можно просто сделать так:
```
user = CustomUser.objects.create(...)
```
Если мы просто создадим пользователя через класс User, то мы не получим создание записи в таблице CustomUser. Создание пользователя необходимо производить через производный класс. Если модель CustomUser не содержит дополнительных обязательных полей, мы можем исправить создание модели User(например, при выполнении команды createsuperuser):
```
from django.db.models.signals import post_save

def create_custom_user(sender, instance, created, **kwargs):
    if created:
        values = {}
        for field in sender._meta.local_fields:
            values[field.attname] = getattr(instance, field.attname)
        user = CustomUser(**values)
        user.save()

post_save.connect(create_custom_user, User)
```
*Prerequisites: django-authtools*

django-authtools
-------------------------
- [django-authtools](https://django-authtools.readthedocs.org/en/latest/intro.html#installation) 


Install python packages
-----------------------

Install the package:

```
    $ pip install django-authtools
```

Or you can install it from source:

```    
    $ pip install -e git+http://github.com/fusionbox/django-authtools@master#egg=django-authtools-dev
```

Run the authtools migrations:
```
    $ python manage.py migrate
```

apps.accounts
-------------


settings.py:

```
EXTENSION_APPS = (
    'extensions.authtools',
    'extensions.django_rq',
    'extensions.rq_scheduler',
)

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS + EXTENSION_APPS
########## END APP CONFIGURATION

########## USER MODEL CONFIGURATION
AUTH_USER_MODEL = 'accounts.User'
########## END USER MODEL CONFIGURATION

```

urls.py:

```
    urlpatterns = patterns('',
        # ...
        url(r'^accounts/', include('authtools.urls')),
        # ...
    )

```

Наследование от User
--------------------
собственный модуль аутентификации для использования адреса электронной почты вместо логина.
```
from authtools.models import AbstractNamedUser

class User(AbstractNamedUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        ordering = ('-date_joined',)

```

Получение класса User по умолчанию
----------------------------------------

Интерфейс администратора
------------------------

```
from django.contrib import admin
from django.contrib.auth.models import Group

# Unregister Groups model which is not used
admin.site.unregister(Group)

from authtools.admin import StrippedUserAdmin
from authtools.admin import BASE_FIELDS, DATE_FIELDS, SIMPLE_PERMISSION_FIELDS

from .models import User


class UserAdmin(StrippedUserAdmin):
    list_display = ('is_active', 'name', 'email', 'date_joined', 'last_login', 'is_superuser', 'is_staff')
    list_display_links = ('name', 'email')

    search_fields = ('name', 'email')
    list_filter = ('is_active', 'is_superuser', 'is_staff')

    fieldsets = (
        BASE_FIELDS,
        DATE_FIELDS,
        SIMPLE_PERMISSION_FIELDS,
    )

admin.site.register(User, UserAdmin)


```
Test admin test_admin.py:
-----------

```
from django.test import TestCase
from django.contrib import admin
from django.contrib.auth.models import Group

from ..models import User


class AccountsAdminTestCase(TestCase):
    def test_user_in_admin(self):
        self.assertTrue(User in admin.site._registry)

    def test_group_not_in_admin(self):
        self.assertFalse(Group in admin.site._registry)

```

Test model test_models.py:
--------------------------

```
from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import User


class AccountsModelsTestCase(TestCase):
    def test_user_is_auth_user_model(self):
        self.assertEqual(get_user_model(), User)

```

Test factories test_factories.py:
---------------------------------

```
from django.test import TestCase
from django.contrib.auth import get_user_model

from ..factories import UserFactory, AdminUserFactory


class AccountsFactoriesTestCase(TestCase):
    def setUp(self):
        get_user_model().objects.all().delete()

    def test_user_factory(self):
        user = UserFactory(email='test@example.com')
        user_from_db = get_user_model().objects.get(email='test@example.com')
        self.assertEqual(user, user_from_db)

    def test_admin_user_factory(self):
        admin = AdminUserFactory(email='test@example.com')
        admin_from_db = get_user_model().objects.get(email='test@example.com')
        self.assertEqual(admin, admin_from_db)
        self.assertTrue(admin.is_superuser)

    def test_multiple_users_factory(self):
        users = []
        for i in range(10):
            users.append(UserFactory())
            users.append(AdminUserFactory())

        self.assertEqual(len(users), 20)
        self.assertEqual(len(users), len(get_user_model().objects.all()))
        self.assertEqual(len(get_user_model().objects.filter(is_superuser=True)), 10)

```


*Prerequisites: factory-boy*

- [factory-boy 2.5.2](https://github.com/rbarrois/factory_boy) - Test fixtures replacement for Python

factories.py:
-------------

```
from __future__ import absolute_import

from factory import LazyAttributeSequence, Sequence
from factory.django import DjangoModelFactory

from .models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = LazyAttributeSequence(lambda o, n: '%s-user-%s@django.com' % (o.name.split()[0].lower(), n))
    name = Sequence(lambda n: 'User #%s' % n)
    password = 'password'

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        manager = cls._get_manager(target_class)
        return manager.create_user(*args, **kwargs)


class AdminUserFactory(UserFactory):
    email = LazyAttributeSequence(lambda o, n: '%s-admin-%s@django.com' % (o.name.split()[0].lower(), n))

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        manager = cls._get_manager(target_class)
        return manager.create_superuser(*args, **kwargs)

```

Profile App
===========

```
foreman run django-admin.py startapp user_profile ./mysite/apps/user_profile
```

Profile Model:
--------------
```
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

 
class Profile(models.Model):
    # Relations
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        verbose_name=_("user")
        )
    # Attributes - Mandatory
    interaction = models.PositiveIntegerField(
        default=0,
        verbose_name=_("interaction")
        )

    # Custom Properties
    @property
    def username(self):
        return self.user.username
 
    # Methods
 
    # Meta and String
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("user",)
 
    def __str__(self):
        return self.user.username
```


Связь один-к-одному. OneToOneField:
-----------------------------------
```
class OneToOneField(othermodel[, parent_link=False, **options])
```
Работает так же, как и ForeignKey с unique=True, но “обратная” связь возвращает один объект.

В основном применяется как первичный ключ модели, которая “расширяет” другую модель. Например, Multi-table наследование работает через неявное добавление связи один-к-одному от дочерней модели к родительской.

Принимает обязательный позиционный аргумент: класс связанной модели. Работает так же как и ForeignKey, включая рекурсивную и “ленивую” связь.

Если вы не указали related_name для OneToOneField, Django будет использовать название модели в нижнем регистре.

В примере ниже:
```
from django.conf import settings
from django.db import models

class MySpecialUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    supervisor = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='supervisor_of')
модель User будет содержать следующие атрибуты:

>>> user = User.objects.get(pk=1)
>>> hasattr(user, 'myspecialuser')
True
>>> hasattr(user, 'supervisor_of')
True
```
При получении связанного объекта через обратную связь, если такой объект не существует, будет вызвано исключение DoesNotExist. Например, если пользователь не имеет соответствующего экземпляра в MySpecialUser:
```
>>> user.supervisor_of
Traceback (most recent call last):
    ...
DoesNotExist: User matching query does not exist.
```
Также OneToOneField принимает все дополнительные параметры принимаемые ForeignKey, и еще один дополнительный:

OneToOneField.parent_link
-------------------------

При True и связанной модели, которая наследуется от другой модели, определяет, что должна сохраняться связь на родительскую модель, а не поле OneToOneField дочерней модели, которое используется для организации наследования моделей.

Profile Admin:
--------------

```
# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models
 
 
@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
 
    list_display = ("username", "interaction")
 
    search_fields = ["user__username"]

```

Settings base.py:
-----------------

```
PROJECT_APPS = (
    'apps.accounts',
    'apps.blog',
    'apps.user_profile',
)

EXTENSION_APPS = (
    'extensions.authtools',
    'extensions.django_rq',
    'extensions.rq_scheduler',
)

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS + EXTENSION_APPS
########## END APP CONFIGURATION
```

Test test.py:
-------------

```
# -*- coding: utf-8 -*-
from django.test import TestCase
 
from django.contrib.auth import get_user_model
from . import models
 
 
class TestProfileModel(TestCase):
 
    def test_profile_creation(self):
        User = get_user_model()
        # New user created
        user = User.objects.create(
            username="blogger", password="django-profile")
        # Check that a Profile instance has been crated
        self.assertIsInstance(user.profile, models.Profile)
        # Call the save method of the user to activate the signal
        # again, and check that it doesn't try to create another
        # profile instace
        user.save()
        self.assertIsInstance(user.profile, models.Profile)
```
Проверим работу теста
--------------------- 

python manage.py test apps.profile

И вы увидите следующее сообщение об ошибке:

django.db.models.fields.related.RelatedObjectDoesNotExist: User has no profile.

Чтобы решить эту проблему, необходимо определить сигналы Django. Чуть ниже определения модели профиля нужно написать следующее:

```
from django.dispatch import receiver
from django.db.models.signals import post_save
 
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
```

очень важно - сигналы считываются в начале приложения Django. Поэтлму их необходимо поместить в файл models.py. Если есть много сигналов, можно поместить их в отдельный файл и импортировать этот файл в файл вашей - models.py.

Таким образом, мы определили сигнал для модели пользователя, который срабатывает каждый раз, когда экземпляр пользователя будет сохранен.

Аргументы, используемые в create_profile_for_new_user:
------------------------------------------------------

- sender: модель User
- created: логическое значение, указывающее, был ли создан новый пользователь 
- instance: экземпляр пользователя, который сохраняется

эти аргументы могут быть разными в зависимости от конкретного сигнала, который вы создаете. 


Model Profile:
--------------

```
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver
from django.db.models.signals import post_save
 
class Profile(models.Model):
    # Relations
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        related_name="profile",
        verbose_name=_("user")
        )
    # Attributes - Mandatory
    interaction = models.PositiveIntegerField(
        default=0,
        verbose_name=_("interaction")
        )

    # Custom Properties
    @property
    def username(self):
        return self.user.email
        
 
    homepage = models.URLField(blank=True)
    avatar =   models.ImageField(_("Profile Pic"), upload_to="images/", blank=True, null=True)
    # Methods
    def avatar_image(self):
        return (settings.MEDIA_URL + self.avatar.name) if self.avatar else None

 
    # Meta and String
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("user",)
 
    def __str__(self):
        return self.user.email
        

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
```


