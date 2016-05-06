# p21v-django unit_06

./manage.py startapp contact

ContactForm class
=================

Не нужно регистрировать в INSTALLED_APPS.

.. _forms:
.. module:: contact.forms


        from django import forms
        from django.conf import settings
        from django.contrib.sites.models import Site
        from django.contrib.sites.requests import RequestSite
        from django.utils.translation import ugettext_lazy as _
        from django.core.mail import send_mail
        from django.template import RequestContext, loader


        class ContactForm(forms.Form):
            """
            .. class:: ContactForm

            :class:`~contact.views.ContactFormView`

            1. Экземпляр формы передает текущий HttpRequest object 
               в качестве аргумента request.

            2. Для отправки формы используется метод save, который
               принимает аргумент fail_silently и устанавливает его в
               False. Этот аргумент передается Django функции 
               send_mail(), и позволяет перехватывать исключительные ситуащии 
               для отладки. Метод save ничего не  возвращает.

            Поля формы:

            """
            name = forms.CharField(max_length=100,
                                   label=_(u'Your name'))
            email = forms.EmailField(max_length=200,
                                     label=_(u'Your email address'))
            body = forms.CharField(widget=forms.Textarea,
                                   label=_(u'Your message'))

            """
                .. attribute:: from_email
               email адрес используется для заполнения From: в header 
               сообщения. По умолчанию - это DEFAULT_FROM_EMAIL.
            """

            from_email = settings.DEFAULT_FROM_EMAIL

            """
            .. attribute:: recipient_list
               Список получателей сообщения. По умолчанию - это
               email адреса, указаные в установке MANAGERS.
            """
            recipient_list = [mail_tuple[1] for mail_tuple in settings.MANAGERS]

            """
            .. attribute:: subject_template_name
               Имя шаблона для рендеринга строки subject 
               сообщения. По умолчанию 
               contact/contact_form_subject.txt.
            """
            subject_template_name = "contact/contact_form_subject.txt"

            """

            .. attribute:: template_name
               Имя шаблона для рендеринга поля body
               сообщения. По умолчанию - contact/contact_form.txt.
            """
            template_name = 'contact/contact_form.txt'

            def __init__(self, data=None, files=None, request=None,
                         recipient_list=None, *args, **kwargs):
                if request is None:
                    raise TypeError("Keyword argument 'request' must be supplied")
                self.request = request
                if recipient_list is not None:
                    self.recipient_list = recipient_list
                super(ContactForm, self).__init__(data=data, files=files,
                                                  *args, **kwargs)

            def message(self):
                """
                Рендеринг body.
                    .. method:: message()
               Возвращает body сообщения для отправки. 
                """
                if callable(self.template_name):
                    template_name = self.template_name()
                else:
                    template_name = self.template_name
                return loader.render_to_string(template_name,
                                               self.get_context())

            def subject(self):
                """
                Рендеринг subject.
                .. method:: subject()
               Возвращает subject. 
                """
                template_name = self.subject_template_name() if \
                    callable(self.subject_template_name) \
                    else self.subject_template_name
                subject = loader.render_to_string(template_name,
                                                  self.get_context())
                return ''.join(subject.splitlines())

            def get_context(self):
                """
                Возвращает context, используемый для рендеринга templates для 
                subject и body.
                .. method:: get_context()
               
                Для методов, которые рендерят части сообщения, использует
                шаблоны (по умолчанию: message и subject),
                создает контекст, используемый этими шаблонами. По умолчанию
                контекст будет RequestContext (с использованием текущего HTTP request, 
                поэтому информация о пользователях доступна), а также содержимое
                из cleaned_data словаря форме, и одну дополнительную
                переменную site
                Нужно установить django.contrib.sites
            
             следующие атрибуты/методы  не должны быть перекрыты

            .. attribute:: request
               HttpRequest object представляет текущий request. 
               Устанавлтвается автоматически в __init__(), и используется
               для генерации RequestContext для templates

                По умолчанию context включает:

                * Все провалидированые значения аормы, как переменные с
                  теми же именами что и поля формы.
                * Текущий Site object, как переменную site.
                * Другие переменные, добавленные context процессорами (RequestContext).

                """
                if not self.is_valid():
                    raise ValueError(
                        "Cannot generate Context from invalid contact form"
                    )
                if Site._meta.installed:
                    site = Site.objects.get_current()
                else:
                    site = RequestSite(self.request)
                return RequestContext(self.request,
                                      dict(self.cleaned_data,
                                           site=site))

            def get_message_dict(self):
                """
               Этот метод преобразует from_email, recipient_list, message и subject
               в словарь с ключами с соответствующими аргументфми функции send_mail
               возвращает словарь. 

                Требуются значения:

                * ``from_email``
                * ``message``
                * ``recipient_list``
                * ``subject``

                """
                if not self.is_valid():
                    raise ValueError(
                        "Message cannot be sent from invalid contact form"
                    )
                message_dict = {}
                for message_part in ('from_email', 'message',
                                     'recipient_list', 'subject'):
                    attr = getattr(self, message_part)
                    message_dict[message_part] = attr() if callable(attr) else attr
                return message_dict

            def save(self, fail_silently=False):
                """
                Строит message.
                    .. method:: save
               Если форма содержит провалидированые даные, можно посылать
               email, вызывая метод get_message_dict и передавая результат
               в функцию Django send_mail.
               """
                send_mail(fail_silently=fail_silently, **self.get_message_dict())


URL configuration
=================

Базовые представления
=====================
Generic class-based views

Множество из встроенных CBV в Django наследуют другие представления-классы или классы-примеси. Это цепочка наследований(и порядок классов) очень важна, поэтому информация о классах-предках находится в разделе Ancestors (MRO). MRO - это акроним для Method Resolution Order.

View
----
    class django.views.generic.base.View
Самый главный класс в CBV. Все остальные представления-классы наследуются от него.

Методы
------
    dispatch()
    http_method_not_allowed()
    options()

Пример views.py:

        from django.http import HttpResponse
        from django.views.generic import View

        class MyView(View):

            def get(self, request, *args, **kwargs):
                return HttpResponse('Hello, World!')

Пример urls.py:

        from django.conf.urls import url

        from myapp.views import MyView

        urlpatterns = [
            url(r'^mine/$', MyView.as_view(), name='my-view'),
        ]

Атрибуты

http_method_names
Список методов HTTP, которые принимает(обрабатывает) данное представление.

Значения по умолчанию:

    ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

Методы

classmethod as_view(**initkwargs)
Возвращает выполняемое(callable) представление, которое принимает запрос и возвращает ответ:

response = MyView.as_view()(request)

Возвращаемое представление содержит атрибуты view_class и view_initkwargs.

dispatch(request, *args, **kwargs)
view часть представления – метод, который принимает аргумент request плюс дополнительные аргументы, и возвращает HTTP ответ(response).

Реализация по умолчанию анализирует HTTP метод запроса и делегирует его соответствующему методу класса; GET будет обработан методом get(), запрос POST делегируется к post(), и т.д.

По умолчанию, запрос HEAD будет делегирован в метод get(). Если вам необходимо обработать HEAD запрос другим способом, вы можете переопределить метод head().

http_method_not_allowed(request, *args, **kwargs)
Если представление было вызвано с неподдерживаемым методом HTTP, будет вызван данный метод.

Реализация по умолчанию возвращает HttpResponseNotAllowed со списком разрешенных методов в виде простого текста.

options(request, *args, **kwargs)
Обрабатывает запросы на определение “глаголов”(методов) OPTIONS HTTP. Возвращает список всех разрешенных для представления методов HTTP.

TemplateView
------------
    class django.views.generic.base.TemplateView
Обрабатывает заданный шаблон, используя контекст(context), содержащий параметры из URL.

Классы-предки, Ancestors (MRO)
------------------------------
Представление наследует методы и атрибуты из следующего представления:

        django.views.generic.base.TemplateResponseMixin
        django.views.generic.base.ContextMixin
        django.views.generic.base.View

методы
------
        dispatch()
        http_method_not_allowed()
        get_context_data()
Пример views.py:

        from django.views.generic.base import TemplateView

        from articles.models import Article

        class HomePageView(TemplateView):

            template_name = "home.html"

            def get_context_data(self, **kwargs):
                context = super(HomePageView, self).get_context_data(**kwargs)
                context['latest_articles'] = Article.objects.all()[:5]
                return context
Пример urls.py:

        from django.conf.urls import url

        from myapp.views import HomePageView

        urlpatterns = [
            url(r'^$', HomePageView.as_view(), name='home'),
        ]
Контекст(Context)
-----------------
Словарь ключевых аргументов, “отловленных” (через ContextMixin) из шаблона URL, который обрабатывается данным представлением.


URL /contact/:
--------------

        urlpatterns = [
            url(r'^$', view_home.home, name='home'),
            url(r'^blog/', include('blog.urls', namespace="blog")),
            url(r'^contact/', include('contact.urls', namespace="contact")),
            url(r'^userprofile/', include('userprofile.urls', namespace="userprofile")),
            url(r'^admin/', admin.site.urls),
            url(r'^ckeditor/', include('ckeditor_uploader.urls')),
        ]

TemplateView Display a Django HTML template.
--------------------------------------------
contact.urls
------------

        from django.conf.urls import url
        from django.views.generic import TemplateView

        from contact.views import ContactFormView

        urlpatterns = [
            url(r'^$',
                ContactFormView.as_view(),
                name='contact_form'),
            url(r'^sent/$',
                TemplateView.as_view(
                    template_name='contact/contact_form_sent.html'),
                name='contact_form_sent'),
        ]


Built-in views
==============

        """
        View which can render and send email from a contact form.

        """

        from django.core.urlresolvers import reverse
        from django.views.generic.edit import FormView

        from .forms import ContactForm

        class ContactFormView(FormView):
            """
            .. attribute:: recipient_list
            Список адресов электронной почты для отправки почты.

            .. attribute:: form_class
            .. attribute:: template_name
            """
            form_class = ContactForm
            recipient_list = None
            template_name = 'contact/contact_form.html'

            def form_valid(self, form):
                form.save()
                return super(ContactFormView, self).form_valid(form)

            def form_invalid(self, form):
                # tl;dr -- this method is implemented to work around Django
                # ticket #25548, which is present in the Django 1.9 release
                # (but not in Django 1.8).
                #
                # The longer explanation is that in Django 1.9,
                # FormMixin.form_invalid() does not pass the form instance to
                # get_context_data(). This causes get_context_data() to
                # construct a new form instance with the same data in order to
                # put it into the template context, and then any access to
                # that form's ``errors`` or ``cleaned_data`` runs that form
                # instance's validation. The end result is that validation
                # gets run twice on an invalid form submission, which is
                # undesirable for performance reasons.
                #
                # Manually implementing this method, and passing the form
                # instance to get_context_data(), solves this issue (which was
                # fixed in Django 1.9.1 and will not be present in Django
                # 1.10).
                return self.render_to_response(self.get_context_data(form=form))

            def get_form_kwargs(self):
                """
                    .. method:: get_form_kwargs()

               Возвращает дополнительные аргументы ключевых слов (в качестве словаря), чтобы передать
                классу формы при инициализации.

                По умолчанию - возвращает словарь, содержащий
                HttpRequest (как ключ request) и, если
                ContactFormView.recipient_list определен - его значение
                """
                # ContactForm instances require instantiation with an
                # HttpRequest.
                kwargs = super(ContactFormView, self).get_form_kwargs()
                kwargs.update({'request': self.request})

                # We may also have been given a recipient list when
                # instantiated.
                if self.recipient_list is not None:
                    kwargs.update({'recipient_list': self.recipient_list})
                return kwargs

            def get_success_url(self):
                """
                    .. method:: get_success_url()

                URL для перенаправления после успешного рендеринга формы.
                По умолчанию, это URL - contact_form.sent.
                """
                # This is in a method instead of the success_url attribute
                # because doing it as an attribute would involve a
                # module-level call to reverse(), creating a circular
                # dependency between the URLConf (which imports this module)
                # and this module (which would need to access the URLConf to
                # make the reverse() call).
                return reverse('contact_form_sent')

FormMixin

class django.views.generic.edit.FormMixin
Класс Mixin, который предоставляет средства для создания и отображения форм.

Mixins

django.views.generic.base.ContextMixin
Methods and Attributes

initial
A dictionary containing initial data for the form.

form_class
The form class to instantiate.

success_url
The URL to redirect to when the form is successfully processed.

prefix
The prefix for the generated form.

get_initial()
Retrieve initial data for the form. By default, returns a copy of initial.

get_form_class()
Retrieve the form class to instantiate. By default form_class.

get_form(form_class=None)
Instantiate an instance of form_class using get_form_kwargs(). If form_class isn’t provided get_form_class() will be used.


get_form_kwargs()
Строит ключи, необходимые для создания экземпляра формы.

Первоначальный аргумент установлен в get_initial (). Если запрос является POST или PUT, также будут предоставлены данные запроса (request.POST и request.FILES).

get_prefix()
Determine the prefix for the generated form. Returns prefix by default.

get_success_url()
Определение URL для перенаправления, когда форма успешно подтверждена. Возвращает success_url по умолчанию.

form_valid(form)
Redirects to get_success_url().

form_invalid(form)
Рендерит ответ, предоставляя неверную форму в качестве контекста.

get_context_data(**kwargs)
Вызывает get_form(), и добавляет результат к контексту данных с именем 'формы'.

Required templates
==================

    contact/contact_form.html

    contact/contact_form_sent.html


необходимо создать еще два шаблона, чтобы обработать
рендеринг сообщения: 
    contact_form_subject.txt и
    contact_form.txt для тела 

Работа с шаблонами формы
========================

Чтобы получить доступ к форме в шаблоне, просто передайте экземпляр в контекст шаблона. Если ваша форма добавлена в контекст как form, {{ form }} создаст необходимые теги label и input.

Настройки рендеринга формы
---------------------------
форма не добавляет тег form и submit кнопку. Вы должны добавить их самостоятельно.

                    <form role="form" action="" method="post">
                        {% csrf_token %}
                        {{ form.as_p }}
                        
                        <button type="submit" class="btn btn-default">Submit</button>
                    </form>

Вы можете использовать следующие варианты рендеринга label/input:
-----------------------------------------------------------------
- {{ form.as_table }} выведет их в таблице, в ячейках тега tr

- {{ form.as_p }} обернет их в тег p

- {{ form.as_ul }} выведет в теге li

тег table или ul вы должны добавить сами.

Вот результат {{ form.as_p }} для нашей формы UserForm:

        <form role="form" action="" method="post">
            <input type='hidden' name='csrfmiddlewaretoken' value='xz6VDB3sfGrsnqU00ZKGTujyXwl6ko2M' />
            <p>
                <label for="id_name">Your name:</label> 
                <input id="id_name" maxlength="100" name="name" type="text" /></p>
            <p>
                <label for="id_email">Your email address:</label> 
                <input id="id_email" maxlength="200" name="email" type="email" /></p>
            <p>
                <label for="id_body">Your message:</label> 
                <textarea cols="40" id="id_body" name="body" rows="10"></textarea></p>
                        
            <button type="submit" class="btn btn-default">Submit</button>
        </form>

каждое поле формы обладает атрибутом с идентификатором id_field-name, с помощью которого обеспечивается связь с тегом метки. Это позволяет формам быть дружественными к вспомогательным технологиям, например, это поможет работе ПО для слепых. Также вы можете настроить способ генерации меток и идентификаторов.

        {% extends "base.html" %}
        {% load latest_posts %}
        {% block head_title %} {{ block.super }} - Blog Contact{% endblock %}

        {% block content %} 
        <div class="row">
            <div class="col-md-8">
            {% block main %} 
            <!-- Header section End -->
            <!--contact us section start-->
            <div class="orange-container top-margin-88">
                <div class="inner ">
                    <h1 class="contactname left">Contact Us</h1>
                    <div class="bridcrumb right">Home &gt;  contact us</div>
                    <div class="clear"></div>
                </div>
            </div>

            <div class="inner2">
                <div class="row">
                    <!-- Contact information -->
                    <div class="col-md-4">
                        <h2 class=" h2class4">Contact Address</h2>
                        <div class="addul"><i class="fa fa-road"></i><span>Your Address here, Location, City, Country </span>
                        </div>
                        <div class="addul1"><i class="fa fa-phone"></i><span>+44 (0) 1232 456 789</span>
                        </div>
                        <div class="addul2"><i class="fa fa-envelope"></i><span>info@example.com</span>
                        </div>
                        <div class="addul3"><i class="fa fa-check"></i><span>www.example.com</span>
                        </div>
                    </div>
                    <!-- Contact information end-->

                    <!-- Contact form -->
                    <div class="col-lg-8">
                        <h2 class=" h2class4">Get in Touch</h2>
                        <div class="form1">
                            <form role="form" action="" method="post">
                            {% csrf_token %}
                            {{ form.as_p }}
                                
                                <button type="submit" class="btn btn-default">Submit</button>
                            </form>
                        </div>
                        <div class="height"></div>
                    </div>
                    <!-- Contact form end-->
                </div>
            </div>

          {% endblock main %} 
          </div>
           <div class="col-md-4">   
             {% block aside %} 
                {{ block.super }}
                <h2>Latest Posts</h2>
                  <div>
                      {% latest_posts %}
                  </div>
             {% endblock aside %}
           </div>    
         </div>
        {% endblock content %}

Рендеринг полей вручную
-----------------------
Мы можем не использовать полный рендеринг формы и отрендерить каждое поле отдельно (например, чтобы поменять порядок полей). Каждое поле формы можно получить через атрибут формы {{ form.name_of_field }}:

                <form role="form" action="" method="post">
                    {% csrf_token %}
                    {{ form.non_field_errors }}
                       <div class="input-group ">
                            <span class="input-group-addon"><i class="fa fa-user"></i></span>
                            {{ form.name.errors }}
                            <label for="{{ form.name.id_for_label }}">Your name:</label>
                            {{ form.name }}
                        </div>
                        <div class="input-group ">
                            <span class="input-group-addon"><i class="fa fa-envelope"></i></span>
                             {{ form.email.errors }}
                             <label for="{{ form.email.id_for_label }}">Your email address:</label>
                             {{ form.email }}
                        </div>
                        <div class="input-group ">
                            {{ form.body.errors }}
                            <label for="{{ form.body.id_for_label }}">Your message:</label>
                            {{ form.body }}
                        </div>
                        <button type="submit" class="btn btn-default">Submit</button>
                </form>


Элемент label также может быть создан с помощью метода label_tag(). Например:

        <div class="fieldWrapper">
            {{ form.email.errors }}
            {{ form.email.label_tag }}
            {{ form.email }}
        </div>


Рендеринг ошибок проверки
-------------------------
Список ошибок можно вывести используя {{ form.name_of_field.errors }}. Они будут выглядеть приблизительно как:

        <ul class="errorlist">
            <li>Sender is required.</li>
        </ul>

Списку назначен CSS-класс errorlist, что позволяет вам настроить параметры его отображения. Если потребуется более тонкая настройка отображения ошибок, вы можете это организовать с помощью цикла по ним:

        {% if form.email.errors %}
           <ol>
              {% for error in form.email.errors %}
                  <li><strong>{{ error|escape }}</strong></li>
              {% endfor %}
            </ol>
        {% endif %}

Ошибки, не относящиеся к полям, (и/или ошибки скрытых полей, которые отображаются наверху формы при использовании методов подобных form.as_p()) будут отображаться с дополнительным классом nonfield, что поможет их отделить от ошибок полей формы. Например, {{ form.non_field_errors }} может выглядеть так:

        <ul class="errorlist nonfield">
            <li>Generic validation error</li>
        </ul>

Цикл по полям формы
-----------------------
Если вы используете однотипный HTML для каждого поля формы, вы можете избежать дублирования кода, используя тег {% for %} для прохода по полям формы:

        {% for field in form %}
            <div class="fieldWrapper">
                {{ field.errors }}
                {{ field.label_tag }} {{ field }}
            </div>
        {% endfor %}

Полезные атрибуты {{ field }}:
------------------------------
- {{ field.label }}
Метка поля, т.е. Email address.

- {{ field.label_tag }}
Метка поля, обёрнутая в соответствующий HTML тег <label>. Также включает атрибут формы label_suffix. Например, по умолчания label_suffix содержит двоеточие:

    <label for="id_email">Email address:</label>

- {{ field.id_for_label }}
ID, которое будет использоваться для этого поля (id_email в примере выше). Вы можете использовать его вместо label_tag, если самостоятельно генерируете label для поля. Так полезно при генерации JavaScript, если вы не хотите “хардкодить” ID.

- {{ field.value }}
Значение поля, например someone@example.com.

- {{ field.html_name }}
Имя поля, которое будет использовано в HTML-поле. Здесь учитывается префикс формы, если он был установлен.

- {{ field.help_text }}
Любой вспомогательный текст, который привязан к полю.

- {{ field.errors }}
Вывод ul class="errorlist", содержащий все ошибки валидации, относящиеся к полю. Вы можете настраивать представление списка ошибок с помощью цикла {% for error in field.errors %}. В этом случае, каждый объект в цикле является простой строкой, содержащей сообщение об ошибке.

- {{ field.is_hidden }}
Значение этого атрибута равно True, если поле является скрытым, и False в противном случае. Данный атрибут обычно не используется при выводе формы, но может быть полезен в условиях подобных этому:

        {% if field.is_hidden %}
           {# Do something special #}
        {% endif %}

- {{ field.field }}
Экземпляр Field из класса формы, который обёрнут с помощью BoundField. Он предоставляет доступ к атрибутам Field, например {{ char_field.field.max_length }}.

Цикл по скрытым и отображаемым полям
-------------------------------------
Если вы вручную размещаете форму в шаблоне, то у вас появляется возможность трактовать поля вида input type="hidden" по своему. Например, так как скрытые поля не отображаются на форме, размещение сообщений об ошибке для поля “перейти далее” может смутить пользователей. Такие ошибки следует обрабатывать другим способом.

Django предоставляет два метода, которые позволяют организовать раздельные циклы по скрытым и отображаемым полям: hidden_fields() и visible_fields(). Покажем как изменится наш пример, если воспользоваться этими методами:

        {# Include the hidden fields #}
        {% for hidden in form.hidden_fields %}
        {{ hidden }}
        {% endfor %}
        {# Include the visible fields #}
        {% for field in form.visible_fields %}
            <div class="fieldWrapper">
                {{ field.errors }}
                {{ field.label_tag }} {{ field }}
            </div>
        {% endfor %}

Этот пример не обрабатывает ошибки в скрытых полях. Обычно ошибка в скрытом поле означает наличие подмены в форме, так как обычный сценарий работы с формами не предполагает изменения этих полей. Тем не менее, вы можете реализовать отображение таких ошибок формы.

Повторное использование шаблонов форм
--------------------------------------
Если на вашем сайте используется однотипная логика отображения форм, вы можете избежать дублирования кода, сохранив цикл по полям формы в отдельном шаблоне и подключая его в другие шаблоны с помощью тега include:

        # In your form template:
        {% include "form_snippet.html" %}

        # In form_snippet.html:
        {% for field in form %}
            <div class="fieldWrapper">
                {{ field.errors }}
                {{ field.label_tag }} {{ field }}
            </div>
        {% endfor %}

Если объект формы, переданный в шаблон, имеет другое имя в контексте, вы можете создать для него псевдоним, используя аргумент with тега include:

    {% include "form_snippet.html" with form=comment_form %}

Если вам придётся делать такое часто, то можно создать собственный включающий тег.

Отправка электронных писем
===========================
Код находится в модуле django.core.mail.

Пример

        from django.core.mail import send_mail

        send_mail('Subject here', 'Here is the message.', 'from@example.com',
            ['to@example.com'], fail_silently=False)

Письмо отправлено через SMTP хост и порт, которые указаны в настройках EMAIL_HOST и EMAIL_PORT. Настройки EMAIL_HOST_USER и EMAIL_HOST_PASSWORD, если указаны, используются для авторизации на SMTP сервере, а настройки EMAIL_USE_TLS и EMAIL_USE_SSL указывают использовать ли безопасное соединение.

При отправке письма через django.core.mail будет использоваться кодировка из DEFAULT_CHARSET.
send_mail()

        send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)

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

        send_mail('Subject', 'Message.', 'from@example.com',
            ['john@example.com', 'jane@example.com'])


Бэкенды для отправки электронной почты
---------------------------------------
Непосредственная отправка электронного письма происходит в бэкенде.

Django предоставляет несколько бэкендов. Эти бэкенды, кроме SMTP (который используется по умолчанию), полезны только при разработке или тестировании. Вы можете создать собственный бэкенд.

SMTP бэкенд
===========

Это бэкенд по умолчанию. Почта отправляется через SMTP сервер. Адрес сервера и параметры авторизации указаны в настройках EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS, EMAIL_USE_SSL, EMAIL_TIMEOUT, EMAIL_SSL_CERTFILE и EMAIL_SSL_KEYFILE.

SMTP бэкенд используется в Django по умолчанию. Если вы хотите указать его явно, добавьте в настройки:

        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

Dummy бэкенд
------------
Этот бэкенд ничего не делает с почтой. Чтобы указать этот бэкенд, добавьте следующее в настройки:

        EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

Этот бэкенд не следует использовать на боевом сервере, он создавался для разработки.

Настройка почты при разработке
==============================

Самый простой способ настроить почту для разработки – использовать бэкенд console. Этот бэкенд перенаправляет всю почту в stdout, позволяя увидеть содержимое писем.

settings.py
-----------

        EMAIL_BACKEND =
          'django.core.mail.backends.console.EmailBackend' 
        DEFAULT_FROM_EMAIL = 'testing@example.com'
        EMAIL_HOST_USER = ''
        EMAIL_HOST_PASSWORD = ''
        EMAIL_USE_TLS = False 
        EMAIL_PORT = 1025

Также можно использовать file. Этот бэкенд сохраняет содержимое каждого SMTP-соединения в файл.

Еще один способ – использовать локальный SMTP-сервер, который принимает письма и выводит их в консоль, но никуда их не оправляет. Python позволяет создать такой сервер одной командой:

        python -m smtpd -n -c DebuggingServer localhost:1025

Эта команда запускает простой SMTP-сервер, который слушает 1025 порт на localhost. Этот сервер выводит заголовки и содержимое полученных писем в консоль. Вам необходимо указать в настройках EMAIL_HOST и EMAIL_PORT. Подробности об этом SMTP-сервер смотрите в документации Python к модулю smtpd.

settings.py
-----------

        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
        EMAIL_HOST = 'localhost'
        EMAIL_HOST_USER = 'janusnic@gmail.com'
        EMAIL_PORT = 1025


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

        EMAIL_HOST = 'smtp.gmail.com'
        EMAIL_HOST_USER = 'your-username@gmail.com'
        EMAIL_HOST_PASSWORD = 'Application spectific password(for eg: smbumqjiurmqrywn)'
        EMAIL_PORT = 587
        EMAIL_USE_TLS = True

You can use the shell to test it:

        python manage.py shell
        from django.core.mail import send_mail
        send_mail('Test', 'This is a test', 'your@email.com', ['toemail@email.com'],
             fail_silently=False)


        class Comment(models.Model):
            post = models.ForeignKey(
                Article, related_name='comments', verbose_name=_("post"))
            bodytext = models.TextField(verbose_name=_("message"))

            post_date = models.DateTimeField(
                auto_now_add=True, verbose_name=_("post date"))
            ip_address = models.GenericIPAddressField(
                default='0.0.0.0', verbose_name=_("ip address"))

            user = models.ForeignKey(
                'auth.User', null=True, blank=True, verbose_name=_("user"), related_name='comment_user')
            user_name = models.CharField(
                max_length=50, default='anonymous', verbose_name=_("user name"))
            user_email = models.EmailField(blank=True, verbose_name=_("user email"))

            class Meta:
                verbose_name = _('comment')
                verbose_name_plural = _('comments')
                ordering = ['post_date']

forms.py
--------
        from django import forms
        from .models import Comment, Article

        class CommentForm(forms.ModelForm):
            ancestor = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'ancestor'}), required=False)
            content = forms.CharField(widget=forms.Textarea(attrs={'cols': '65', 'rows': '6'}))
            
            class Meta:
                model = Comment
                fields = ('name', 'website', 'content',)

views.py
--------

        def detail(request, postslug):
            result = get_object_or_404(Article, slug=postslug)
            form = CommentForm(request.POST or None)
            try:
                result.views = result.views + 1
                result.save()
            except:
                pass
            category_list = Category.objects.order_by('name')
            tags_name = Tag.objects.order_by('name')

            if request.method == 'POST':
                if form.is_valid():
                    form2 = form.save(commit=False)
                    if form['ancestor'].value() == '':
                        form2.user = request.user if request.user.is_authenticated() else None
                        form2.article = result
                    else:
                        try:
                            parent = Comment.objects.get(id=int(form['ancestor'].value()))
                            form2.parent = parent
                            form2.user = request.user if request.user.is_authenticated() else None
                            form2.article = result
                        except:
                            messages.error(request, 'The comment you are replying to does not exist.')
                   
                    form2.spam = False
                    
                    form2.save()
                    messages.success(request, 'Thanks for commenting!')
                    return redirect('blog:detail', postslug=postslug)
                else:
                    messages.error(request, 'There was a problem submitting your comment. Please try agian.')
                    
            #Users don't need to pass a captcha and checking that this is the initial value so there will be no error codes

            comment_tree = Comment.objects.select_related('user').filter(article=result.id, deleted=False, spam=False).order_by('path')

            return render(request, 'blog/detail.html', {'categories_list':category_list, 'item': result, 'tags_name':tags_name, 'months':monthly_archive_list(),'form':form,'comment_tree':comment_tree})

detail.html
-----------

      <h3 id="comments">Comments:</h3>
        <form id="postcomment" method="post" action="{% url 'blog:detail' item.slug %}">
        <ul>
          {% if not request.user.is_authenticated %}
                <li><label for="id_name">{{form.name.label}}:</label> {{form.name}} <span class="about">(optional)</span></li>
                <li><label for="id_website">{{form.website.label}}:</label> {{form.website}} <span class="about">(optional)</span></li>
          {% endif %}
              <li>{{form.content}}</li>
              <li><small><em><a href="http://daringfireball.net/projects/markdown/syntax">(Supports Markdown Syntax)</a></em></small></li>
              <li><input type="submit" value="Submit Comment" /></li>
              <li>{{form.ancestor}}</li>
        </ul>
    {% csrf_token %}
    </form>

django.contrib.humanize
-----------------------
Набор шаблонных фильтров Django, которые помогают отображать данные в читабельном виде.

Чтобы использовать эти фильтры, добавьте 'django.contrib.humanize' в настройку INSTALLED_APPS. Затем добавьте в шаблоне {% load humanize %}. Теперь вам доступны следующие фильтры.

apnumber
--------
Для чисел 1-9 возвращает их тестовое название. Иначе возвращает число. Соответствует стилю Associated Press.

Например:

    1 станет one.
    2 станет two.
    10 станет 10.

Можно передать число или строку, представляющую число.

intcomma
--------
Конвертирует число в строку, разделенную запятой через каждые три цифры.

Например:

    4500 станет 4,500.
    45000 станет 45,000.
    450000 станет 450,000.
    4500000 станет 4,500,000.

Используется формат из текущей локализации, если он доступен и включена локализация.
Можно передать число или строку, представляющую число.

intword
-------
Конвертирует большое число в читабельное тестовое представление. Лучше всего работает для чисел больше 1 миллиона.

Например:

        1000000 станет 1.0 million.
        1200000 станет 1.2 million.
        1200000000 станет 1.2 billion.

Поддерживаются число до 10^100 (Googol).

Используется формат из текущей локализации, если он доступен и включена локализация.
Можно передать число или строку, представляющую число.

naturalday
----------
Для даты равной текущей, или плюс/минус один день, возвращает “today”, “tomorrow” или “yesterday” соответственно. Иначе форматирует дату, используя переданный формат.

Пример (если текущая дата 17 февраля 2007):

        16 Feb 2007 станет yesterday.
        17 Feb 2007 станет today.
        18 Feb 2007 станет tomorrow.

Любая другая дата будет отформатирована в соответствии с переданным аргументом, или форматом из настройки DATE_FORMAT, если формат не передан в фильтр через аргумент.

naturaltime
-----------
Для значений datetime вернет текстовое представление сколько секунд, минут или часов прошло. Если значение больше одного дня, используется результат фильтра timesince. Работает для дат в будущем.

Пример (если текущая дата и время 17 февраля 2007 16:30:00):

        17 Feb 2007 16:30:00 станет now.
        17 Feb 2007 16:29:31 станет 29 seconds ago.


ordinal
-------
Преобразование целое число в порядковый номер.

Например:

        1 станет 1st.
        2 станет 2nd.
        3 станет 3rd.

Можно передать число или строку, представляющую число.


blog/detail.html
----------------

        <ul id="commenters">
            {% for comment in comment_tree %}
              {% if comment.user %}
                <li id="{{comment.id}}" class="comment" style="margin-left:{{comment.depth|add:comment.depth}}em;"><p class="poster"><span class="user">{% if comment.user.get_full_name %}{{comment.user.get_full_name}}{% else %}{{comment.user.username}}{% endif %}</span> - {{comment.date|naturaltime}}</p><p>{{comment.content|safe}}</p><p><a href="" class="reply">reply</a></p></li>
              {% elif comment.name %}
                <li id="{{comment.id}}" class="comment" style="margin-left:{{comment.depth|add:comment.depth}}em;"><p class="poster">{% if comment.website %}<a href="{{comment.website}}">{{comment.name}}</a>{% else %}{{comment.name}}{% endif %} - {{comment.date|naturaltime}}</p><p>{{comment.content|safe}}</p><p><a href="" class="reply">reply</a></p></li>
              {% elif comment.deleted %}
                <li id="{{comment.id}}" class="comment" style="margin-left:{{comment.depth|add:comment.depth}}em;">[Deleted] - {{comment.date|naturaltime}}<p>This comment was removed</p></li>
              {% else %}
                <li id="{{comment.id}}" class="comment" style="margin-left:{{comment.depth|add:comment.depth}}em;"><p class="poster">Anonymous - {{comment.date|naturaltime}}</p><p>{{comment.content|safe}}</p><p><a href="" class="reply">reply</a></p></li>
              {% endif %}
            {% empty %}
              <li>There are currently no comments. You can be first!</li>
            {% endfor %}
          </ul>

Search
======

        from django.shortcuts import get_object_or_404, render, redirect, render_to_response
        from django.http import HttpResponse
        from django.template import RequestContext
        from .models import *
        from .forms import *
        import datetime
        from django.core.paginator import Paginator, InvalidPage, EmptyPage
        import time
        from calendar import month_name
        from django.contrib import messages

        import re
        from django.db.models import Q

        def normalize_query(query_string,
                            findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                            normspace=re.compile(r'\s{2,}').sub):
            ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
                and grouping quoted words together.
                Example:
                
                >>> normalize_query('  some random  words "with   quotes  " and   spaces')
                ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
            
            '''
            return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

        def get_query(query_string, search_fields):
            ''' Returns a query, that is a combination of Q objects. That combination
                aims to search keywords within a model by testing the given search fields.
            
            '''
            query = None # Query to search for every search term        
            terms = normalize_query(query_string)
            for term in terms:
                or_query = None # Query to search for a given term in each field
                for field_name in search_fields:
                    q = Q(**{"%s__icontains" % field_name: term})
                    if or_query is None:
                        or_query = q
                    else:
                        or_query = or_query | q
                if query is None:
                    query = or_query
                else:
                    query = query & or_query
            return query

        def search_for_blog(request):
            query_string = ''
            found_entries = None
            if ('q' in request.GET) and request.GET['q'].strip():
                query_string = request.GET['q']
                entry_query = get_query(query_string, ['title', 'content'])
                found_entries = Article.objects.filter(entry_query).order_by('-publish_date')

            return render_to_response('blog/template-result.html',
                    { 'query_string': query_string, 'found_entries': found_entries },
                    context_instance=RequestContext(request)
                )

index.html
----------

           <div class="col-md-4">   
             {% block aside %} 
                {{ block.super }}
                <h2>Latest Posts</h2>
                  <div>
                      {% latest_posts %}
                  </div>
                  <h3>Monthly Archive</h3>
                  <div>
                      {% for month in months %} 
                           <a href="{% url 'blog:archive' month.0 month.1 %}">{{ month.2 }}</a> <br /> 
                      {% endfor %}
                  </div> 
                  <form class="" method="get" action="{% url 'blog:search_for_blog' %}">
                      <input name="q" id="id_q" type="text" class="form-control" placeholder="Search" />
                      <button type="submit">Search</button>
                  </form>
        
             {% endblock aside %}

blog/template-result.html
-------------------------

        {% if found_entries %}

           {% for field in found_entries %}
                {{ field.title }}</br>
                
           {% endfor %}
        {% endif %}


urls.py
-------

        from django.conf.urls import url

        from . import views

        urlpatterns = [
            
            url(r'^$', views.index, name='index'),
            url(r'^news/$', views.news, name='news'),
            
            url(r"^archive/(\d+)/(\d+)/$", views.monthly_archive , name='archive'),
            url(r'^category/(?P<categoryslug>.*)/$', views.category, name='category' ),
            url(r'^results/$', views.search_for_blog, name='search_for_blog'),
            url(r'^(?P<postslug>.*)/$', views.detail, name='detail' ),


        ]

