# p21v-django unit_09

Django REST Framework
---------------------

pip install -U djangorestframework

./manage.py startapp blab

models.py
---------
        from django.db import models

        class Category(models.Model):
            name = models.CharField(max_length=50)

            class Meta:
                verbose_name = "Category"
                verbose_name_plural = "Categories"

            def __str__(self):
                return self.name

        class Post(models.Model):
            title = models.CharField(max_length=200)
            content = models.TextField()
            category = models.ForeignKey(Category)
            updated = models.DateTimeField(auto_now=True)
            created = models.DateTimeField(auto_now_add=True)

            class Meta:
                ordering = ['created']
                verbose_name = "Post"
                verbose_name_plural = "Posts"

            def __str__(self):
                return self.title

settings.py
-----------
        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
         
            'blab',
        ]


admin.py
--------

        from django.contrib import admin
        from .models import Post, Category

        admin.site.register(Category)
        admin.site.register(Post)


serializers.py
--------------

        from rest_framework import serializers
        from .models import Category, Post

        class PostSerializer(serializers.ModelSerializer):
            class Meta:
                model = Post

        class CategorySerializer(serializers.ModelSerializer):
            class Meta:
                model = Category



views.py
--------

        from rest_framework import viewsets
        from .models import Post, Category
        from .serializers import PostSerializer, CategorySerializer

        class PostViewSet(viewsets.ModelViewSet):
            queryset = Post.objects.all()
            serializer_class = PostSerializer

        class CategoryViewSet(viewsets.ModelViewSet):
            queryset = Category.objects.all()
            serializer_class = CategorySerializer


mysite/urls.py
--------------
        from django.conf.urls import url, include
        from django.contrib import admin
        from django.conf import settings

        urlpatterns = [
            url(r'^admin/', admin.site.urls),
            url(r'^api/', include('blab.urls', namespace='blab')),
               
        ]
        if settings.DEBUG:
            from django.conf.urls.static import static
            urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
            urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

settings.py
-----------

        STATIC_URL = '/static/'

        # STATIC FILE CONFIGURATION
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
        STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

        # See:
        # https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
        STATICFILES_DIRS = (
            os.path.join(BASE_DIR, 'static'),
        )

        STATICFILES_FINDERS = (
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        )
        # END STATIC FILE CONFIGURATION

        # MEDIA CONFIGURATION
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
        MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'media'))

        # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
        MEDIA_URL = '/media/'
        # END MEDIA CONFIGURATION

blab/urls.py
------------
        from django.conf.urls import url, include
        from rest_framework import routers
        from .views import PostViewSet, CategoryViewSet

        router = routers.DefaultRouter()
        router.register(r'posts', PostViewSet)
        router.register(r'categories', CategoryViewSet)

        urlpatterns = router.urls


django-rest-swagger
-------------------
https://github.com/marcgibbons/django-rest-swagger

    pip install django-rest-swagger

urls.py
-------
        from django.conf.urls import url, include
        from rest_framework import routers
        from .views import PostViewSet, CategoryViewSet

        router = routers.DefaultRouter()
        router.register(r'posts', PostViewSet)
        router.register(r'categories', CategoryViewSet)

        urlpatterns = [
            url(r'^docs/', include('rest_framework_swagger.urls')),
        ]

        urlpatterns += router.urls


settings.py
-----------

        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'rest_framework_swagger',
            'blab',
        ]

users
=====

models.py
---------
        from __future__ import unicode_literals

        # from django.db import models
        # from django.utils.translation import ugettext_lazy as _
        from django.contrib.auth.models import AbstractUser


        class User(AbstractUser):

            def __str__(self):
                return self.username


permissions.py
--------------

        from rest_framework import permissions


        class IsOwnerOrReadOnly(permissions.BasePermission):
            """
            Object-level permission to only allow owners of an object to edit it.
            Assumes the model instance has an `owner` attribute.
            """

            def has_object_permission(self, request, view, obj):

                if request.method in permissions.SAFE_METHODS:
                    return True

                return obj == request.user


admin.py
--------
        from __future__ import absolute_import, unicode_literals

        from django import forms
        from django.contrib import admin
        from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
        from django.contrib.auth.forms import UserChangeForm, UserCreationForm

        from .models import User


        class CustomUserChangeForm(UserChangeForm):

            class Meta(UserChangeForm.Meta):
                model = User


        class CustomUserCreationForm(UserCreationForm):

            # http://james.lin.net.nz/2013/06/08/django-custom-user-model-in-admin-relation-auth_user-does-not-exist/
            def clean_username(self):
                # Since User.username is unique, this check is redundant,
                # but it sets a nicer error message than the ORM. See #13147.
                username = self.cleaned_data["username"]
                try:
                    User._default_manager.get(username=username)
                except User.DoesNotExist:
                    return username
                raise forms.ValidationError(self.error_messages['duplicate_username'])

            class Meta(UserCreationForm.Meta):
                model = User


        @admin.register(User)
        class UserAdmin(AuthUserAdmin):
            form = CustomUserChangeForm
            add_form = CustomUserCreationForm

serializers.py
--------------

        from rest_framework import serializers

        from .models import User


        class UserSerializer(serializers.ModelSerializer):

            class Meta:
                model = User
                fields = ('id', 'username', 'first_name', 'last_name',)
                read_only_fields = ('username', )


        class CreateUserSerializer(serializers.ModelSerializer):

            def create(self, validated_data):
                # call create_user on user object. Without this
                # the password will be stored in plain text.
                user = User.objects.create_user(**validated_data)
                return user

            class Meta:
                model = User
                fields = ('id', 'username', 'password', 'auth_token')
                read_only_fields = ('auth_token',)
                write_only_fields = ('password',)


views.py
--------

        from rest_framework import viewsets, mixins
        from rest_framework.permissions import AllowAny

        from .models import User
        from .permissions import IsOwnerOrReadOnly
        from .serializers import CreateUserSerializer, UserSerializer


        class UserViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
            """
            Creates, Updates, and retrives User accounts
            """
            queryset = User.objects.all()
            serializer_class = UserSerializer
            permission_classes = (IsOwnerOrReadOnly,)

            def create(self, request, *args, **kwargs):
                self.serializer_class = CreateUserSerializer
                self.permission_classes = (AllowAny,)
                return super(UserViewSet, self).create(request, *args, **kwargs)

authentication
==============

models.py
---------

        from django.conf import settings
        from django.db.models.signals import post_save
        from django.dispatch import receiver
        from rest_framework.authtoken.models import Token


        @receiver(post_save, sender=settings.AUTH_USER_MODEL)
        def create_auth_token(sender, instance=None, created=False, **kwargs):
            if created:
                Token.objects.create(user=instance)



urls.py
-------

        from django.conf.urls import include, url

        from rest_framework.authtoken import views

        urlpatterns = [
            url(r'^api-token-auth/', views.obtain_auth_token),
            url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        ]

mysite/urls.py
--------------

        from django.conf.urls import url, include
        from django.contrib import admin
        from django.conf import settings
        from rest_framework.routers import DefaultRouter
        from users.views import UserViewSet

        router = DefaultRouter()
        router.register(r'users', UserViewSet)

        urlpatterns = [
            url(r'^admin/', admin.site.urls),
            url(r'^api/', include('blab.urls', namespace='blab')),
            url(r'^api/v1/', include('authentication.urls')),
            url(r'^api/v1/', include(router.urls)),
               
        ]
        if settings.DEBUG:
            from django.conf.urls.static import static
            urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
            urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



settings.py
-----------

        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'rest_framework.authtoken',  # token authentication
            'rest_framework_swagger',
            'blab',
            'authentication',
            'users',
        ]

        # Custom user app
        AUTH_USER_MODEL = 'users.User'

        # Django Rest Framework
        REST_FRAMEWORK = {
            'PAGINATE_BY': 30,
            'PAGINATE_BY_PARAM': 'per_page',
            'MAX_PAGINATE_BY': 1000,
            "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
            'DEFAULT_RENDERER_CLASSES': (
                'rest_framework.renderers.JSONRenderer',
                'rest_framework.renderers.BrowsableAPIRenderer',
            ),
            'DEFAULT_PERMISSION_CLASSES': [
                'rest_framework.permissions.IsAuthenticated',
            ],
            'DEFAULT_AUTHENTICATION_CLASSES': (
                'rest_framework.authentication.SessionAuthentication',
                'rest_framework.authentication.TokenAuthentication',
            )
        }

