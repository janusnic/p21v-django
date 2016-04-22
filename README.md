# p21v-django unit_05

Аутентификация пользователей в Django
=====================================
Django поставляется с системой аутентификации пользователей. Она обеспечивает пользовательские аккаунты, группы, права и сессии на основе куки.

Система аутентификации Django отвечает за оба аспекта: аутентификацию и авторизацию. аутентификация проверяет пользователя, а авторизация определяет, что аутентифицированный пользователь может делать.

Система аутентификации состоит из:
----------------------------------
1. Пользователей

2. Прав: Бинарные (да/нет) флаги, определяющие наличие у пользователя права выполнять определённые действия.

3. Групп: Общий способ назначения меток и прав на множество пользователей.

4. Настраиваемой системы хеширования паролей

5. Инструментов для форм и представлений для аутентификации пользователей или для ограничения доступа к контенту

Поддержка аутентификации скомпонована в виде модуля в django.contrib.auth. По умолчанию, требуемые настройки уже включены в settings.py, создаваемый с помощью команды django-admin startproject, и представляют собой две записи в параметре конфигурации INSTALLED_APPS:

1. 'django.contrib.auth' содержит ядро системы аутентификации и её стандартные модели.

2. 'django.contrib.contenttypes' является фреймворком типов, который позволяет правам быть назначенными на создаваемые вами модели.

две записи в параметре конфигурации MIDDLEWARE_CLASSES:
-------------------------------------------------------
1. SessionMiddleware управляет сессиями во время запросов.

2. AuthenticationMiddleware ассоциирует пользователей с запросами с помощью сессий.

При наличии этих настроек, применение команды manage.py migrate создаёт в базе данных необходимые для системы аутентификации таблицы, создаёт права для любых моделей всех зарегистрированных приложений.

Использование системы аутентификации пользователя
=================================================

Создание пользователей
----------------------
Самый простой способ создать пользователя – использовать метод create_user():

        from django.contrib.auth.models import User
        user = User.objects.create_user('janus', 'janus@ex.ua', 'januspassword')

        # At this point, user is a User object that has already been saved
        # to the database. You can continue to change its attributes
        # if you want to change other fields.
        user.last_name = 'Janus'
        user.save()

Создание суперпользователя
--------------------------
Суперпользователя можно создать с помощью команды createsuperuser:

    $ python manage.py createsuperuser --username=janus --email=janus@ex.ua

Команда попросит ввести пароль. Пользователь будет создан сразу же по завершению команды. Если не указывать --username или the --email, команда попросит ввести их.

Объект пользователя
===================
Объекты User - основа системы аутентификации. Они представляют пользователей сайта и используются для проверки прав доступа, регистрации пользователей, ассоциации данных с пользователями. Для представления пользователей в системе аутентификации используется только один класс, таким образом 'суперпользователи' или 'персонал' - это такие же объекты пользователей, просто с определёнными атрибутами.

Основные атрибуты пользователя:
==============================
- username
- password
- email
- first_name
- last_name
- groups
- user_permissions
- is_staff
- is_active
- is_superuser
- last_login
- date_joined


Профайл пользователя:
=====================
модель для профайла пользователя, которая ассоциируется как один-к-одному с моделью пользователя.

    ./manage.py startapp userprofile

Модель: models.py
-----------------
        from django.db import models
        from django.contrib.auth.models import User
        from django.utils import timezone
        from django.utils.encoding import python_2_unicode_compatible

        @python_2_unicode_compatible
        class UserProfile(models.Model):
            # This line is required. Links UserProfile to a User model instance.
            user = models.OneToOneField(User, related_name='profile')
            timezone = models.CharField(max_length=50, default='Europe/Kiev')

            # The additional attributes we wish to include.
            
            location = models.CharField(max_length=140, blank=True)  
            gender = models.CharField(max_length=140, blank=True)  
            age = models.IntegerField(blank=True)
            company = models.CharField(max_length=50, blank=True)
                
            website = models.URLField(blank=True)
            profile_picture = models.ImageField(upload_to='thumbpath', blank=True)

            # Override the __str__() method to return out something meaningful!
            def __str__(self):
                return self.user.username

settings.py
-----------
        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'ckeditor',
            'ckeditor_uploader',
            'blog',
            'userprofile',
        ]

makemigrations
--------------
        ./manage.py makemigrations userprofile
        Migrations for 'userprofile':
          0001_initial.py:
            - Create model UserProfile
        ./manage.py migrate
        Operations to perform:
          Apply all migrations: userprofile, admin, blog, auth, contenttypes, sessions
        Running migrations:
          Rendering model states... DONE
          Applying userprofile.0001_initial... OK

admin.py
--------

        from django.contrib import admin
        from .models import UserProfile

        admin.site.register(UserProfile)


runserver
----------

        ./manage.py runserver

Создание форм в Django Класс RegistrationForm, UserProfileForm 
==============================================================
Максимальное количество символом в значении мы указали с помощью параметра max_length. Он используется для двух вещей. Будет добавлен атрибут maxlength="30" в HTML тег input (теперь браузер не позволит пользователю ввести больше символов, чем мы указали). Также Django выполнит проверку введенного значения, когда получит запрос с браузера с введенными данными.

Экземпляр Form содержит метод is_valid(), который выполняет проверку всех полей формы. Если все данные правильные, это метод:
- вернет True
- добавит данные формы в атрибут cleaned_data.

userprofile/forms.py
--------------------

        from django import forms
        from django.contrib.auth.models import User
        from .models import UserProfile

        class RegistrationForm(forms.ModelForm):
            username = forms.RegexField(label="Username", max_length=30,
                regex=r'^[\w.-]+$', error_messages={'invalid': 
                    'This value may contain only letters, numbers and ./-/_ characters.'})

            email = forms.EmailField(label='E-mail')
            email_repeat = forms.EmailField(label='E-mail (repeat)', required=True)

            password = forms.CharField(label='Password',
                widget=forms.PasswordInput(render_value=False))
            password_repeat = forms.CharField(label='Password (repeat)',
                widget=forms.PasswordInput(render_value=False))

            first_name = forms.CharField(label='First name', required=False)
            last_name = forms.CharField(label='Last name', required=False)

            class Meta:
                model = User
                fields = ('username', 'email', 'email_repeat', 'password', 'password_repeat', 'first_name', 'last_name')

        class UserProfileForm(forms.ModelForm):
            class Meta:
                model = UserProfile
                exclude = ['user']
                #fields = '__all__'

После рендеринга наша форма будет выглядеть следующим образом:

        <p><label for="id_username">Username:</label> <input class="form-control" id="id_username" maxlength="30" name="username" placeholder="Enter Your User Name" type="text" /></p>
        <p><label for="id_email">E-mail:</label> <input class="form-control" id="id_email" name="email" placeholder="johndoe@company.com" type="email" /></p>
        <p><label for="id_password">Password:</label> <input class="form-control" id="id_password" name="password" placeholder="Easy to remember, hard to guess" type="password" /></p>

Обратите внимание, она не содержит тег form, или кнопку отправки. Вам необходимо самостоятельно их добавить в шаблоне.

User Registration View and Template
====================================

Creating the register() View
-----------------------------

views.py:
---------
        from django.shortcuts import render
        from .forms import RegistrationForm, UserProfileForm

        def register(request):

            # A boolean value for telling the template whether the registration was successful.
            # Set to False initially. Code changes value to True when registration succeeds.
            registered = False

            # If it's a HTTP POST, we're interested in processing form data.
            if request.method == 'POST':
                # Attempt to grab information from the raw form information.
                # Note that we make use of both RegistrationForm and UserProfileForm.
                user_form = RegistrationForm(data=request.POST)
                profile_form = UserProfileForm(data=request.POST)

                # If the two forms are valid...
                if user_form.is_valid() and profile_form.is_valid():
                    # Save the user's form data to the database.
                    user = user_form.save()

                    # Now we hash the password with the set_password method.
                    # Once hashed, we can update the user object.
                    user.set_password(user.password)
                    user.save()

                    # Now sort out the UserProfile instance.
                    # Since we need to set the user attribute ourselves, we set commit=False.
                    # This delays saving the model until we're ready to avoid integrity problems.
                    profile = profile_form.save(commit=False)
                    profile.user = user

                    # Did the user provide a profile picture?
                    # If so, we need to get it from the input form and put it in the UserProfile model.
                    if 'profile_picture' in request.FILES:
                        profile.profile_picture = request.FILES['profile_picture']

                    # Now we save the UserProfile model instance.
                    profile.save()

                    # Update our variable to tell the template registration was successful.
                    registered = True

                # Invalid form or forms - mistakes or something else?
                # Print problems to the terminal.
                # They'll also be shown to the user.
                else:
                    print (user_form.errors, profile_form.errors)

            # Not a HTTP POST, so we render our form using two ModelForm instances.
            # These forms will be blank, ready for user input.
            else:
                user_form = RegistrationForm()
                profile_form = UserProfileForm()

            # Render the template depending on the context.
            return render(request,
                    'userprofile/register.html',
                    {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

userprofile/urls.py
-------------------
        from django.conf.urls import url
        from . import views

        urlpatterns = [
            
            url(r'^register/$', views.register, name='register'),
        ]

urls.py
-------
            urlpatterns = [
                url(r'^$', view_home.home, name='home'),
                url(r'^blog/', include('blog.urls', namespace="blog")),
                url(r'^userprofile/', include('userprofile.urls', namespace="userprofile")),
                url(r'^admin/', admin.site.urls),
                url(r'^ckeditor/', include('ckeditor_uploader.urls')),
            ]

Creating the Registration Template
==================================

templates/userprofile/register.html:
------------------------------------
        {% extends "base.html" %}
        {% block head_title %} {{ block.super }} - Register with Janus {% endblock %}

        {% block content %}

            <div class="row">
                  <div class="col-md-12">
                  {% block main %} 
                  <h2>Register with Janus</h2>
                    {% if registered %}
                        Janus says: <strong>thank you for registering!</strong>
                        <a href="/blog/">Return to the homepage.</a><br />
                    {% else %}
                        Janus says: <strong>register here!</strong><br />

                        <form id="user_form" method="post" action="/userprofile/register/"
                                enctype="multipart/form-data">
                            {% csrf_token %}

                            <!-- Display each form. The as_p method wraps each element in a paragraph
                                 (<p>) element. This ensures each element appears on a new line,
                                 making everything look neater. -->
                            {{ user_form.as_p }}
                            {{ profile_form.as_p }}

                            <!-- Provide a button to click to submit the form. -->
                          <p>
                          <input type="submit" name="submit" class="btn btn-default" value="Register" />
                          </p>
                        </form>
                    {% endif %}

                  {% endblock main %} 
                  </div>
                 </div>
        {% endblock %}


Подделка межсайтового запроса (CSRF)
====================================

Промежуточный слой CSRF и шаблонный тег предоставляют легкую-в-использовании защиту против Межсайтовой подделки запроса. Этот тип атак случается, когда злонамеренный Web сайт содержит ссылку, кнопку формы или некоторый javascript, который предназначен для выполнения некоторых действий на вашем Web сайте, используя учетные данные авторизованного пользователя, который посещал злонамеренный сайт в своем браузере. Сюда также входит связанный тип атак, ‘login CSRF’, где атакуемый сайт обманывает браузер пользователя, авторизируясь на сайте с чужими учетными данными.

Первая защита против CSRF атак - это гарантирование того, что GET запросы (и другие ‘безопасные’ методы, определенные в 9.1.1 Safe Methods, HTTP 1.1, RFC 2616) свободны от побочных эффектов. Запросы через ‘небезопасные’ методы, такие как POST, PUT и DELETE могут быть защищены при помощи шагов, описанных ниже.

Для того чтобы включить CSRF защиту для ваших представлений, выполните следующие шаги:

Промежуточный слой CSRF активирован по умолчанию и находится в настройке MIDDLEWARE_CLASSES. Если вы переопределяете эту настройку, помните, что ``‘django.middleware.csrf.CsrfViewMiddleware’``должен следовать перед промежуточными слоями, которые предполагают, что запрос уже проверен на CSRF атаку.

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


Если вы отключили защиту, что не рекомендуется, вы можете использовать декоратор csrf_protect() в части представлений, которые вы хотите защитить.

{% csrf_token %}
-----------------
В любом шаблоне, который использует POST форму, используйте тег csrf_token внутри элемента form если форма для внутреннего URL, т. е.:

        <form action="." method="post">{% csrf_token %}

Это не должно делаться для POST форм, которые ссылаются на внешние URL’ы, поскольку это может вызвать утечку CSRF токена, что приводит к уязвимости.

В соответствующих функциях представления, убедитесь, что 'django.template.context_processors.csrf' контекстный процессор используется. Обычно, это может быть сделано в один из двух способов:

Использовать RequestContext, который всегда использует 'django.template.context_processors.csrf' (не зависимо от параметра TEMPLATES ). Если вы используете общие представления или contrib приложения, вы уже застрахованы, так как эти приложения используют RequestContext повсюду.

Вручную импортировать и использовать процессор для генерации CSRF токена и добавить в шаблон контекста. т.е.:

        from django.shortcuts import render_to_response
        from django.template.context_processors import csrf

        def my_view(request):
            c = {}
            c.update(csrf(request))
            # ... view code here
            return render_to_response("a_template.html", c)


includes/mainmenu.html
-----------------------

          <ul class="nav navbar-nav">
            <li class="active"><a href="/">Home <span class="sr-only">(current)</span></a></li>
            <li><a href="/blog">Blog</a></li>
            <li><a href="/blog/news">News</a></li>
          
            <li><a href="/userprofile/register">Register</a></li>
          </ul>


Login Functionality
===================

Как авторизовать пользователя
-----------------------------
Если вы ходите привязать к сессии авторизованного пользователя, используйте функцию login().

        login(request, user)

Чтобы авторизовать пользователя в представлении, используйте функцию login(). Она принимает объект HttpRequest и объект User. Функция login() сохраняет идентификатор пользователя в сессии, используя Django приложение для работы с сессиями.

Следует отметить, что любые данные установленные в анонимной сессии будут сохранены в сессии пользователя после его авторизации.

пример показывает как использовать обе функции authenticate() и login():

        from django.contrib.auth import authenticate, login

        def my_view(request):
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to a success page.
                else:
                    # Return a 'disabled account' error message
                    ...
            else:
                # Return an 'invalid login' error message.
                ...
Сначала вызывайте authenticate()
---------------------------------
Когда вы самостоятельно авторизуете пользователя, вы должны успешно выполнить его аутентификацию с помощью функции authenticate() перед вызовом функции login(). Функция authenticate() устанавливает атрибут у класса User, указывающий бэкенд относительно которого был успешно аутентифицирован данный пользователь (обратитесь к документации на бэкенды для подробностей), эта информация понадобится позже для процесса авторизации. При попытке авторизации объекта пользователя, который был получен из базы напрямую, будет выброшена ошибка.

userprofile/views.py:
---------------------
        from django.contrib.auth import authenticate, login
        from django.http import HttpResponseRedirect, HttpResponse

        def user_login(request):

            # If the request is a HTTP POST, try to pull out the relevant information.
            if request.method == 'POST':
                # Gather the email and password provided by the user.
                # This information is obtained from the login form.
                        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                        # because the request.POST.get('<variable>') returns None, if the value does not exist,
                        # while the request.POST['<variable>'] will raise key error exception
                username = request.POST.get('username')
                password = request.POST.get('password')

                # Use Django's machinery to attempt to see if the email/password
                # combination is valid - a User object is returned if it is.
                user = authenticate(username=username, password=password)

                # If we have a User object, the details are correct.
                # If None (Python's way of representing the absence of a value), no user
                # with matching credentials was found.
                if user:
                    # Is the account active? It could have been disabled.
                    if user.is_active:
                    # If the account is valid and active, we can log the user in.
                        # We'll send the user back to the homepage.
                        login(request, user)
                        return HttpResponseRedirect('/blog/')
                    else:
                        # An inactive account was used - no logging in!
                        return HttpResponse("Your User account is disabled.")
                else:
               # Bad login details were provided. So we can't log the user in.
                    print ("Invalid login details: {0}, {1}".format(username, password))
                    return HttpResponse("Invalid login details supplied.")

            # The request is not a HTTP POST, so display the login form.
            # This scenario would most likely be a HTTP GET.
            else:
                # No context variables to pass to the template system, hence the
                # blank dictionary object...
                # return render(request, 'blog/login.html', {})
                # return render(request, 'blog/index.html', {})
                return render(request, 'userprofile/login.html', {})

Creating a Login Template
=========================
templates/userprofile/login.html:
---------------------------------

        <!DOCTYPE html>
        <html>
            <head>
                <!-- Is anyone getting tired of repeatedly entering the header over and over?? -->
                <title>Blog</title>
            </head>
            <body>
                <h1>Login to Blog</h1>
                <form id="login_form" method="post" action="/userprofile/login/">
                    {% csrf_token %}
                    Username: <input type="text" name="username" value="" size="50" />
                    <br />
                    Password: <input type="password" name="password" value="" size="50" />
                    <br />
                    <input type="submit" value="submit" />
                </form>

            </body>
        </html>

Mapping the Login View to a URL
-------------------------------

userprofile/urls.py:
-------------------
        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^register/$', views.register, name='register'),
            url(r'^login/$', views.user_login, name='login'), 
        ]


includes/mainmenu.html
----------------------

        <li><a href="/userprofile/register">Register</a></li>
        <li><a href="/userprofile/login">Login</a></li>

Restricting Access
==================
Ограничение доступа для неавторизованных пользователей
------------------------------------------------------

Самым простым способом ограничить доступ к страницам является использование метода request.user.is_authenticated() и, при необходимости, перенаправление на страницу авторизации:

        from django.conf import settings
        from django.shortcuts import redirect

        def my_view(request):
            if not request.user.is_authenticated():
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
            # ...

или отображение сообщения об ошибке:

        from django.shortcuts import render

        def my_view(request):
            if not request.user.is_authenticated():
                return render(request, 'myapp/login_error.html')
            # ...
Декоратор login_required
------------------------
        login_required(redirect_field_name='next', login_url=None)
Для краткости кода вы можете использовать декоратор login_required():

        from django.contrib.auth.decorators import login_required

        @login_required
        def my_view(request):
            ...
Функция login_required() делает следующее:
------------------------------------------
Если пользователь не авторизован, то перенаправляет его на URL, указанный в параметре конфигурации settings.LOGIN_URL, передавая текущий абсолютный путь в запросе. Например: /accounts/login/?next=/polls/3/.

Если пользователь авторизован, то выполняет код представления. В коде представления не требуется выполнять проверку авторизован ли пользователь или нет.

По умолчанию, в параметре "next" строки запроса хранится путь, по которому должен быть перенаправлен пользователь в результате успешной аутентификации. Если вам потребуется использовать другое имя для этого параметра, то воспользуйтесь необязательным аргументом redirect_field_name декоратора login_required():

        from django.contrib.auth.decorators import login_required

        @login_required(redirect_field_name='my_redirect_field')
        def my_view(request):
            ...

если вы воспользуетесь аргументом redirect_field_name, то вам скорее всего потребуется внести изменения в ваш шаблон авторизации, так как переменная контекста шаблона, которая содержит путь перенаправления, будет использовать значение аргумента redirect_field_name в качестве своего ключа, а не стандартное значение "next".

Декоратор login_required() также принимает необязательный аргумент login_url. Например:

        from django.contrib.auth.decorators import login_required

        @login_required(login_url='/accounts/login/')
        def my_view(request):
            ...
если вы не укажите аргумент login_url, то вам потребуется проверить параметр конфигурации settings.LOGIN_URL и ваше представление для авторизации соответственно настроены. Например, пользуясь стандартным поведением, добавьте следующие строки к вашей схеме URL:

        from django.contrib.auth import views as auth_views

        url(r'^accounts/login/$', auth_views.login),
Параметр конфигурации settings.LOGIN_URL также принимает имена представлений и именованные шаблоны URL. Это позволяет вам свободно переносить ваше представление для авторизации пользователя внутри схемы URL без необходимости изменения настроек.

Декоратор login_required() не проверяет свойство is_active объекта пользователя.

Если вы создаёте собственные представления для интерфейса администратора (или вам нужна та же аутентификация, что используются встроенными представлениями), то вам может пригодиться декоратор django.contrib.admin.views.decorators.staff_member_required() в качестве полезной альтернативы login_required().


Restricting Access with a Decorator
-----------------------------------
views.py:
----------

        from django.contrib.auth.decorators import login_required

        @login_required
        def restricted(request):
            return HttpResponse("Since you're logged in, you can see this text!")

urls.py
--------

        urlpatterns = [
            url(r'^register/$', views.register, name='register'),
            url(r'^login/$', views.user_login, name='login'), 
            url(r'^restricted/', views.restricted, name='restricted'),
        ]

logout
======

Как отменить авторизацию пользователя
-------------------------------------
        logout(request)
Для отмены авторизации пользователя, который был авторизован с помощью функции django.contrib.auth.login(), следует использовать функцию django.contrib.auth.logout() в коде вашего представления. Функция принимает объект HttpRequest и не возвращает никаких значений. Например:

        from django.contrib.auth import logout

        def logout_view(request):
            logout(request)
            # Redirect to a success page.

функция logout() не выбрасывает никаких ошибок, если пользователь не был ранее авторизован.

При вызове функции logout() в рамках текущего запроса будут очищены все данные сессии. Все существующие данные будут стёрты. Это происходит для того, чтобы предотвратить возможность доступа к этим данным для другого пользователя, который будет использовать тот же браузер для своей авторизации. Если потребуется поместить некие данные в сессию, которые должны быть доступны пользователя сразу после отмены его авторизации, выполняйте это после вызова функции django.contrib.auth.logout().

views.py:
----------

        from django.contrib.auth import logout

        # Use the login_required() decorator to ensure only those logged in can access the view.
        @login_required
        def user_logout(request):
            # Since we know the user is logged in, we can now just log them out.
            logout(request)

            # Take the user back to the homepage.
            return HttpResponseRedirect('/blog/')


userprofile/urls.py:
--------------------
        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^register/$', views.register, name='register'),
            url(r'^login/$', views.user_login, name='login'), 
            url(r'^restricted/', views.restricted, name='restricted'),
            url(r'^logout/$', views.user_logout, name='logout'),
        ]


Аутентификация пользователей
============================
Аутентификация в запросах
-------------------------
Django использует сессию и промежуточный слой для работы системы аутентификации в объекте запроса.

Этот механизм предоставляет атрибут request.user для каждого запроса, который возвращает текущего пользователя. Если текущий пользователь не авторизован, атрибут содержит экземпляр AnonymousUser, иначе экземпляр User.

Различить их можно с помощью метода is_authenticated():

        if request.user.is_authenticated():
            # Do something for authenticated users.
            ...
        else:
            # Do something for anonymous users.
            ...
authenticate(**credentials)
---------------------------
Для аутентификации пользователя по имени и паролю используйте authenticate(). Параметры авторизации передаются как именованные аргументы, по умолчанию это username и password, если пароль и имя пользователя верны, будет возвращен объект User. Если пароль не правильный, authenticate() возвращает None.

            {% if user.is_authenticated %}
              <li><a href="/userprofile/logout/">Logout</a></li>
            {% else %}
              <li><a href="/userprofile/register">Register</a></li>

              <form class="navbar-form navbar-right" role="form" method="post" action="/userprofile/login">
            {% csrf_token %}
              <div class="form-group">
                <input type="text" placeholder="Username" name="username" class="form-control">
              </div>
              <div class="form-group">
                <input type="password" placeholder="Password" name="password" class="form-control">
              </div>
              <button type="submit" class="btn btn-success">Sign in</button>
            </form>
          {% endif %}

Если вам нужно будет ограничить доступ только авторизованным пользователям, используйте декоратор login_required().

{% if user.is_authenticated %}
===============================

        <h1>Blog says... hello {{ user.username }}!</h1>
        {% else %}
        <h1>Blog says... hello world!</h1>
        {% endif %}


includes/mainmenu.html
----------------------

        <ul class="nav  navbar-nav navbar-right">
            {% if user.is_authenticated %}
              <li><a href="/userprofile/logout/">Logout</a></li>
            {% else %}
              <li><a href="/userprofile/register">Register</a></li>

              <form class="navbar-form navbar-right" role="form" method="post" action="/userprofile/login">
            {% csrf_token %}
              <div class="form-group">
                <input type="text" placeholder="Username" name="username" class="form-control">
              </div>
              <div class="form-group">
                <input type="password" placeholder="Password" name="password" class="form-control">
              </div>
              <button type="submit" class="btn btn-success">Sign in</button>
            </form>
          {% endif %}
         </ul>

profile_view views.py
---------------------

        @login_required
        def profile_view(request):
            user = request.user
            
            context = {
                'first_name':user.first_name, 'last_name':user.last_name
            }
            return render(request, 'userprofile/profile.html', context)

userprofile/profile.html
------------------------

        {% extends "base.html" %}
        {% block head_title %} {{ block.super }} - Profile {{ user.username }} {% endblock %}

        {% block content %}
             <div class="row">
                  <div class="col-md-8">
                  {% block main %} 
                  <h2>Welcome back {{ user.username }}!</h2>
                  <p>
                    Your First Name: {{ first_name }}
                  </p>
                  <p>
                    Your Last Name: {{ last_name }}
                  </p>
                  {% endblock main %} 
                  
                  </div>
                   <div class="col-md-4">   
                     {% block aside %} 
                        <h2>My Profile</h2>
                          <div>
                          <ul>
                          <li><a href="/userprofile/profile/">My Profile</a></li>
                          <li><a href="/userprofile/profile/edit/">Edit Profile</a></li>
                          </ul>
                          </div>        
                     {% endblock aside %}
                   </div>    
                 </div>
        {% endblock %}

urls.py
-------

        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^register/$', views.register, name='register'),
            url(r'^login/$', views.user_login, name='login'), 
            url(r'^restricted/', views.restricted, name='restricted'),
            url(r'^logout/$', views.user_logout, name='logout'),
            url(r'^profile/$', views.profile_view, name='profile'),
        ]

edit_profile views.py
---------------------

        @login_required
        def edit_profile(request):

            user = request.user
            form = EditProfileForm(request.POST or None, initial={'first_name':user.first_name, 'last_name':user.last_name})
            if request.method == 'POST':
                if form.is_valid():

                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.save()
                    return HttpResponseRedirect('%s'%(reverse('userprofile:profile')))

            context = {
                "edit_form": form
            }

            return render(request, "userprofile/edit_profile.html", context)


userprofile/edit_profile.html
-----------------------------
        {% extends "base.html" %}
        {% block head_title %} {{ block.super }} - Profile {{ user.username }} {% endblock %}

        {% block content %}
             <div class="row">
                  <div class="col-md-8">
                  {% block main %} 
                  <h2>Profile of {{ user.username }}'s</h2>
                        <form id="user_form" method="post" action="/userprofile/profile/edit/"
                                enctype="multipart/form-data">
                            {% csrf_token %}
                            {{ edit_form.as_p }}
                          <p>
                          <input type="submit" name="submit" class="btn btn-default" value="Save" />
                          </p>
                        </form>
                  {% endblock main %} 
                  </div>
                   <div class="col-md-4">   
                     {% block aside %} 
                        <h2>My Profile</h2>
                          <div>
                          <ul>
                          <li><a href="/userprofile/profile/">My Profile</a></li>
                          <li><a href="/userprofile/profile/edit/">Edit Profile</a></li>
                          
                          </ul>
                          </div>        
                     {% endblock aside %}
                   </div>    
                 </div>
        {% endblock %}

urls.py
-------

        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^register/$', views.register, name='register'),
            url(r'^login/$', views.user_login, name='login'), 
            url(r'^restricted/', views.restricted, name='restricted'),
            url(r'^logout/$', views.user_logout, name='logout'),
            url(r'^profile/$', views.profile_view, name='profile'),
            url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
        ]

views.py
--------

        def user_login(request):
            if request.method == 'POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('%s'%(reverse('userprofile:profile')))
                        # return HttpResponseRedirect('/blog/')
                    else:
                        return HttpResponse("Your User account is disabled.")
                else:
                    print ("Invalid login details: {0}, {1}".format(username, password))
                    return HttpResponse("Invalid login details supplied.")
            else:
                return render(request, 'blog/index.html', {})




        @login_required
        def edit_profile(request):

            user = request.user
            
            form = EditProfileForm(request.POST or None, initial={'first_name':user.first_name, 'last_name':user.last_name})
            #profileform = UserProfileForm(instance=UserProfile.objects.get(user=user))

            user_profile = request.user.profile
            if request.method == 'POST':
                profileform = UserProfileForm(request.POST, instance=user_profile)
                if form.is_valid() and profileform.is_valid():
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.save()
                    profileform.save()
                    return HttpResponseRedirect('%s'%(reverse('userprofile:profile')))
            else:
                profileform = UserProfileForm(instance=user_profile)
            
            context = {
                "edit_form": form, "profileform":profileform
            }

            return render(request, "userprofile/edit_profile.html", context)


userprofile/edit_profile.html

        {% extends "base.html" %}
        {% block head_title %} {{ block.super }} - Profile {{ user.username }} {% endblock %}

        {% block content %}
             <div class="row">
                  <div class="col-md-8">
                  {% block main %} 
                  <h2>Profile of {{ user.username }}'s</h2>
                        <form id="user_form" method="post" action="/userprofile/profile/edit/"
                                enctype="multipart/form-data">
                            {% csrf_token %}
                            {{ edit_form.as_p }}
                            {{ profileform.as_p }}
                          <p>
                          <input type="submit" name="submit" class="btn btn-default" value="Save" />
                          </p>
                        </form>
                  {% endblock main %} 
                  </div>
                   <div class="col-md-4">   
                     {% block aside %} 
                        <h2>My Profile</h2>
                          <div>
                          <ul>
                          <li><a href="/userprofile/profile/">My Profile</a></li>
                          <li><a href="/userprofile/profile/edit/">Edit Profile</a></li>
                          </ul>
                          </div>        
                     {% endblock aside %}
                   </div>    
                 </div>
        {% endblock %}

