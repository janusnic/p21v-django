## p21v-django unit 13
Создание форм из моделей
============

ModelForm
----------

class ModelForm
---------------
При разработке приложения, использующего базу данных, чаще всего вы будете работать с формами, которые аналогичны моделям. Например, имея модель Profile, вам может потребоваться создать форму, которая позволит людям создавать свой профиль. В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.

По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели.

Например:
----------
```
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Profile

from django import forms 

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'password']

```

Типы полей
-----------
Сгенерированный класс Form будет содержать поле формы для каждого поля модели в порядке указанном в атрибуте fields.

Каждому полю модели соответствует стандартное поле формы. Например, CharField поле модели будет представлено на форме как CharField, а ManyToManyField поле модели будет представлено как MultipleChoiceField. 

список соответствия полей модели и формы:
-----------------------------------------

Поле модели                     Поле формы
-------------------------------------------
AutoField                       Не представлено на форме

BigIntegerField                 IntegerField с атрибутом min_value равным -9223372036854775808 и атрибутом max_value равным 9223372036854775807.

BooleanField                    BooleanField
CharField                       CharField с атрибутом max_length равным значению атрибута max_length модели

CommaSeparatedIntegerField      CharField
DateField                       DateField
DateTimeField                   DateTimeField
DecimalField                    DecimalField
EmailField                      EmailField
FileField                       FileField
FilePathField                   FilePathField
FloatField                      FloatField
ForeignKey                      ModelChoiceField (смотри далее)

ImageField                      ImageField
IntegerField                    IntegerField
IPAddressField                  IPAddressField
GenericIPAddressField           GenericIPAddressField
ManyToManyField                 ModelMultipleChoiceField (смотри далее)

NullBooleanField                CharField
PositiveIntegerField            IntegerField
PositiveSmallIntegerField       IntegerField
SlugField                       SlugField
SmallIntegerField               IntegerField
TextField                       CharField с widget=forms.Textarea

TimeField                       TimeField
URLField                        URLField

ForeignKey и ManyToManyField поля модели являются особыми случаями:

- Поле ForeignKey модели представлено полем формы ModelChoiceField, которое является обычным ChoiceField, но с вариантами значений, полученными из QuerySet.

- Поле ManyToManyField модели представлено полем формы ModelMultipleChoiceField, которое является обычным MultipleChoiceField`, но с вариантами значений, полученными из ``QuerySet.

В дополнение, каждое поле созданной формы имеет следующие атрибуты:

- Если у поля модели есть blank=True, тогда к полю формы будет добавлено required=False, иначе – required=True.

- Значением атрибута label поля будет значение поля verbose_name модели, причём первый символ этого значения будет преобразован в верхний регистр.

- Значением атрибута help_text поля формы будет значение атрибута help_text поля модели.

Если для поля модели установлен атрибут choices, тогда для поля формы будет использоваться виджет Select, который будет отображать содержимое этого атрибута. Варианты выбора обычно содержат пустой вариант, который выбран по умолчанию. Если поле является обязательным, то оно требует от пользователя сделать выбор. Пустой вариант не отображается, если у поля модели есть атрибут blank=False и явное значение default (при этом, это значение будет выбрано по умолчанию).

Вы можете переопределить поле формы, используемое для определённого поля модели. 

Рассмотрим набор полей:
```
from django.db import models
from django.forms import ModelForm

TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
)

class Author(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'title', 'birth_date']

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'authors']
```
Для этих моделей показанные выше классы ModelForm будут аналогичны следующим формам (разница будет только в методе save()):
```
from django import forms

class AuthorForm(forms.Form):
    name = forms.CharField(max_length=100)
    title = forms.CharField(max_length=3,
                widget=forms.Select(choices=TITLE_CHOICES))
    birth_date = forms.DateField(required=False)

class BookForm(forms.Form):
    name = forms.CharField(max_length=100)
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all())
```
Валидация в ModelForm
------------------------
Есть два основных шага при валидации ModelForm:

- Валидация форм
- Валидация объекта модели

Как и валидация в обычной форме валидация в модельной форме выполняется при вызове is_valid() или при обращении к атрибуту errors, или при явном вызове full_clean(), но на практике вы не будете использовать последний метод.

Валидация модели (Model.full_clean()) выполняется после валидации формы, сразу после завершения метода clean().

Процесс валидации изменяет объект модели переданный в конструктор ModelForm. Например, поля даты модели преобразуют значения в объект даты. Ошибка валидации может оставить объект в неопределенном состоянии и лучше не использовать его в последующем коде.

Переопределение метода clean()
------------------------------
Вы можете переопределить метод clean() модели для того, чтобы обеспечить дополнительную проверку. Всё это аналогично работе с обычной формой.

Экземпляр модельной формы, привязанный к объекту модели имеет атрибут instance, через который методы модельной формы имеют доступ к соответствующему экземпляру модели.

Метод ModelForm.clean() устанавливает флаг, который указывает валидации модели провалидировать уникальность полей отмеченных unique, unique_together или unique_for_date|month|year.

Если вы хотите переопределить метод clean(), вызовите метод clean() родительского класса.

Взаимодействие с механизмами модели
-----------------------------------
В процессе проверки данных ModelForm будет вызывать метод clean() каждого поля вашей модели, соответствующего полю формы. Для полей модели, которые были исключены из формы, проверка данных производиться не будет. Обратитесь к документации по проверке форм для получения информации о том, как работает проверка данных поля.

Метод модели clean() вызывается перед проверкой уникальности полей.

Определение error_messages
--------------------------
Сообщения ошибки из form field или form Meta имеют приоритет над сообщениями ошибок из model field.

Вы можете переопределить сообщения об ошибке для NON_FIELD_ERRORS, который были вызваны при валидации модели, определив ключ NON_FIELD_ERRORS в атрибут error_messages класса ModelForm.Meta:
```
from django.forms import ModelForm
from django.core.exceptions import NON_FIELD_ERRORS

class ArticleForm(ModelForm):
    class Meta:
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
```
Метод save()
------------
Каждая форма, созданная с помощью ModelForm, обладает методом save(). Этот метод создаёт и сохраняет объект в базе данных, используя для этого данные, введённые в форму. Класс, унаследованный от ModelForm, может принимать существующий экземпляр модели через именованный аргумент instance. Если такой аргумент указан, то save() обновит переданную модель. В противном случае, save() создаст новый экземпляр указанной модели:

```
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserForm, UserProfileForm

def register(request):

    # boolean value
    # Установлено в False при инициализации. Изменим на True при успешной регистрации.
    registered = False

    # Если HTTP POST, обработаем форму.
    if request.method == 'POST':
        # Получаем информацию из форм.
        # Мы используем две формы UserForm и UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # Если обе формы прошли проверку...
        if user_form.is_valid() and profile_form.is_valid():
            # Сохраним данные пользователя из формы в database.
            user = user_form.save()

       # Хешируем пароль с помощью set_password method.

            user.set_password(user.password)
            user.save()

            # Пока пользователь настраивает свой профиль не выполнять commit=False.

            profile = profile_form.save(commit=False)
            profile.user = user

            # Юзер хочет картинку?
            # Если да, предоставим ему поле для ввода картинки.
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']

            # Сохранить экземпляр модели UserProfile.
            profile.save()

            # Изменить переменную при успешной регистрации.
            registered = True
            return HttpResponseRedirect('/')

        # Ошибки?
        # Печать ошибок на terminal.
        else:
            print (user_form.errors, profile_form.errors)

    # Не HTTP POST, строим два эеземпляра ModelForm .
    # Эти формы пустые , предназначены для пользовательских вводов.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'accounts/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

```
Обратите внимание, если форма не была проверена, вызов save() выполнит ее, обратившись к form.errors. Если данные не верны, будет вызвано исключение ValueError – то есть, если form.errors равно True.

Метод save() принимает необязательный именованный аргумент commit, который может иметь значения True или False. При вызове save() с commit=False метод вернёт объект, который ещё не был сохранён в базе данных. В этом случае, вам самостоятельно придётся вызвать метод save() у полученного объекта. Это бывает полезно, когда требуется выполнить дополнительные действия над объектом до его сохранения или если вам требуется воспользоваться одним из параметров сохранения модели. Атрибут commit по умолчанию имеет значение True.

Использование commit=False также полезно в случае, когда ваша модель имеет связь “многие-ко-многим” с другой моделью. Для такой модели, если метод save() вызван с аргументом commit=False, то Django не может немедленно сохранить данные для такой связи, т.к. невозможно создать связи для объекта, который не сохранен в базе данных.

Чтобы решить эту задачу, каждый раз, когда вы сохраняете форму, указывая commit=False, Django добавляет метод save_m2m() к вашему классу ModelForm. После того, как вы вручную сохранили экземпляр формы, вы можете вызвать метод save_m2m() для сохранения данных, связанных через “многие-ко-многим”. Например:
```
# Create a form instance with POST data.
profile_form = UserProfileForm(data=request.POST)

# Create, but don't save the new profile instance.
profile = profile_form.save(commit=False)

# Modify the profile in some way.
profile.avatar = request.FILES['avatar']

# Save the new instance.
profile.save()

# Now, save the many-to-many data for the form.
profile_form.save_m2m()
```
Вызов метода save_m2m() требуется только в случае, если вы используете save(commit=False). Если вы просто используете save() для формы, то все данные (включая связи “многие-ко-многим”), будут сохранены, не требуя для этого дополнительных действий. 

Если не принимать во внимание методы save() и save_m2m(), то ModelForm работает аналогично обычной Form. Например, метод is_valid() используется для проверки данных, метод is_multipart() используется для определения загрузки файла (в этом случае request.FILES должен быть передан форме) и так далее. 

Указываем какие поля использовать
------------------------------------
Настоятельно рекомендуем явно указать все поля отображаемые в форме, используя параметр fields. Иначе по ошибке, при добавлении нового поля в модель, можно позволить его редактировать пользователям и таким образом создать уязвимость. В зависимости от способа рендеринга формы, такая ошибка может быть не легко заметна на сайте.

Самый простой способ указать поля - автоматически добавить все или исключить определенные.

Но если вы уверены в том, что делаете, вот как использовать этот подход:

В параметре fields указать специальное значение '__all__', которое указывает использовать все поля модели. Например:
```
from django.forms import ModelForm

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
```
Используйте атрибут exclude внутреннего класса ModelForm.Meta. Этот атрибут, если он указан, должен содержать список имён полей, которые не должны отображаться на форме.

Например:
```
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['title']
```
При использовании одного из этих способов, порядок полей в форме будет аналогичен порядку полей в модели, ManyToManyField поля будут в конце.

Если поле модели содержит editable=False, каждая форма, созданная по модели с помощью ModelForm, не будет включать в себя это поле.

Поля, которые не определены в форме, не будут учитываться при вызове метода save(). Также, если вы вручную добавите в форму исключенные поля, то они не будут заполняться из экземпляра модели.

Django будет препятствовать всем попыткам сохранить неполную модель. Таким образом, если модель требует заполнения определённых полей и для них не предоставлено значение по умолчанию, то сохранить форму для такой модели не получится. Для решения этой проблемы вам потребуется создать экземпляр такой модели, передав ему начальные значения для обязательных, но незаполненных полей:
```
author = Author(title='Mr')
form = PartialAuthorForm(request.POST, instance=author)

form.save()
```
В качестве альтернативы, вы можете использовать save(commit=False) и вручную определить все необходимые поля:
```
form = PartialAuthorForm(request.POST)
author = form.save(commit=False)
author.title = 'Mr'
author.save()
```

Ссылки на модель User
---------------------
Если вы ссылаетесь на User непосредственно (например, ссылаясь на него в качестве внешнего ключа), ваш код не будет работать в проектах, где настройка AUTH_USER_MODEL была изменена на другую модель User.

get_user_model()
-----------------
Вместо ссылки на User напрямую, вы должны ссылаться на пользовательскую модель с использованием django.contrib.auth.get_user_model(). Данный метод возвращает текущий активный модель User - модель пользовательского User если она указана, или User иначе.

При определении внешнего ключа или отношения много-ко-многим к модели User, вы должны указать пользовательскую модель с помощью параметра AUTH_USER_MODEL. Например:
```

from django.conf import settings
from django.db import models

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)


```

Работа с шаблонами формы
========================

Чтобы получить доступ к форме в шаблоне, просто передайте экземпляр в контекст шаблона. Если ваша форма добавлена в контекст как form, {{ form }} создаст необходимые теги label и input.

Настройки рендеринга формы
---------------------------
Обратите внимание, форма не добавляет тег form и submit кнопку. Вы должны добавить их самостоятельно.

```
    
    <form method="post" id="user_form" enctype="multipart/form-data">
      
      
      <p class="submitRow">
        
        <input type="submit" value="{% trans "Register" %}" />
      </p>
    </form>
```

Вы можете использовать следующие варианты рендеринга label/input:
-----------------------------------------------------------------
- {{ form.as_table }} выведет их в таблице, в ячейках тега tr

- {{ form.as_p }} обернет их в тег p

- {{ form.as_ul }} выведет в теге li

Обратите внимание, тег table или ul вы должны добавить сами.

Вот результат {{ form.as_p }} для нашей формы UserForm:

```
    
    <form method="post" id="user_form" enctype="multipart/form-data">
      <input type='hidden' name='csrfmiddlewaretoken' value='EqDadmKcPL9un0u2FS7jadsJaqc8MbOi' />
      
        <p>
            <label for="id_name">Name:</label> <input id="id_name" maxlength="255" name="name" type="text" />
        </p>
          
        <p>
            <label for="id_email">Email address:</label> <input id="id_email" maxlength="255" name="email" type="email" />
        </p>
          
        <p>
            <label for="id_password">Password:</label> <input id="id_password" name="password" type="password" />
        </p>
          
        <p>
            <label for="id_homepage">Homepage:</label> <input id="id_homepage" maxlength="200" name="homepage" type="url" />
        </p>
        
        <p>
            <label for="id_avatar">Profile Pic:</label> <input id="id_avatar" name="avatar" type="file" />
        </p>
      
        <p class="submitRow">
       
            <input type="submit" value="Register" />
        </p>
    </form>
```

Следует отметить, что каждое поле формы обладает атрибутом с идентификатором id_field-name, с помощью которого обеспечивается связь с тегом метки. Это позволяет формам быть дружественными к вспомогательным технологиям, например, это поможет работе ПО для слепых. Также вы можете настроить способ генерации меток и идентификаторов.

Рендеринг полей вручную
-----------------------
Мы можем не использовать полный рендеринг формы и отрендерить каждое поле отдельно (например, чтобы поменять порядок полей). Каждое поле формы можно получить через атрибут формы {{ form.name_of_field }}. Например:
```

{{ form.non_field_errors }}
<div class="fieldWrapper">
    {{ form.subject.errors }}
    <label for="{{ form.subject.id_for_label }}">Email subject:</label>
    {{ form.subject }}
</div>
<div class="fieldWrapper">
    {{ form.message.errors }}
    <label for="{{ form.message.id_for_label }}">Your message:</label>
    {{ form.message }}
</div>
<div class="fieldWrapper">
    {{ form.sender.errors }}
    <label for="{{ form.sender.id_for_label }}">Your email address:</label>
    {{ form.sender }}
</div>
<div class="fieldWrapper">
    {{ form.cc_myself.errors }}
    <label for="{{ form.cc_myself.id_for_label }}">CC yourself?</label>
    {{ form.cc_myself }}
</div>
```
Элемент label также может быть создан с помощью метода label_tag(). Например:
```
<div class="fieldWrapper">
    {{ form.subject.errors }}
    {{ form.subject.label_tag }}
    {{ form.subject }}
</div>
```
Рендеринг ошибок проверки
-------------------------

Список ошибок можно вывести используя {{ form.name_of_field.errors }}. Они будут выглядеть приблизительно как:
```
<ul class="errorlist">
    <li>Sender is required.</li>
</ul>
```
Списку назначен CSS-класс errorlist, что позволяет вам настроить параметры его отображения. Если потребуется более тонкая настройка отображения ошибок, вы можете это организовать с помощью цикла по ним:
```
{% if form.subject.errors %}
    <ol>
    {% for error in form.subject.errors %}
        <li><strong>{{ error|escape }}</strong></li>
    {% endfor %}
    </ol>
{% endif %}
```
Ошибки, не относящиеся к полям, (и/или ошибки скрытых полей, которые отображаются наверху формы при использовании методов подобных form.as_p()) будут отображаться с дополнительным классом nonfield, что поможет их отделить от ошибок полей формы. Например, {{ form.non_field_errors }} может выглядеть так:
```
<ul class="errorlist nonfield">
    <li>Generic validation error</li>
</ul>
```

Цикл по полям формы
-----------------------
Если вы используете однотипный HTML для каждого поля формы, вы можете избежать дублирования кода, используя тег {% for %} для прохода по полям формы:
```
{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
    </div>
{% endfor %}
```
Полезные атрибуты {{ field }}:
------------------------------
- {{ field.label }}
Метка поля, т.е. Email address.

- {{ field.label_tag }}
Метка поля, обёрнутая в соответствующий HTML тег <label>. Также включает атрибут формы label_suffix. Например, по умолчания label_suffix содержит двоеточие:
```
<label for="id_email">Email address:</label>
```
- {{ field.id_for_label }}
ID, которое будет использоваться для этого поля (id_email в примере выше). Вы можете использовать его вместо label_tag, если самостоятельно генерируете <label> для поля. Так полезно при генерации JavaScript, если вы не хотите “хардкодить” ID.

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
```
{% if field.is_hidden %}
   {# Do something special #}
{% endif %}
```
- {{ field.field }}
Экземпляр Field из класса формы, который обёрнут с помощью BoundField. Он предоставляет доступ к атрибутам Field, например {{ char_field.field.max_length }}.

Цикл по скрытым и отображаемым полям
-------------------------------------
Если вы вручную размещаете форму в шаблоне, то у вас появляется возможность трактовать поля вида input type="hidden" по своему. Например, так как скрытые поля не отображаются на форме, размещение сообщений об ошибке для поля “перейти далее” может смутить пользователей. Такие ошибки следует обрабатывать другим способом.

Django предоставляет два метода, которые позволяют организовать раздельные циклы по скрытым и отображаемым полям: hidden_fields() и visible_fields(). Покажем как изменится наш пример, если воспользоваться этими методами:
```
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
```
Этот пример не обрабатывает ошибки в скрытых полях. Обычно ошибка в скрытом поле означает наличие подмены в форме, так как обычный сценарий работы с формами не предполагает изменения этих полей. Тем не менее, вы можете реализовать отображение таких ошибок формы.

Повторное использование шаблонов форм
--------------------------------------
Если на вашем сайте используется однотипная логика отображения форм, вы можете избежать дублирования кода, сохранив цикл по полям формы в отдельном шаблоне и подключая его в другие шаблоны с помощью тега include:
```
# In your form template:
{% include "form_snippet.html" %}

# In form_snippet.html:
{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
    </div>
{% endfor %}
```
Если объект формы, переданный в шаблон, имеет другое имя в контексте, вы можете создать для него псевдоним, используя аргумент with тега include:
```
{% include "form_snippet.html" with form=comment_form %}
```
Если вам придётся делать такое часто, то можно создать собственный включающий тег.


Register accounts/register.html:
--------------------------------
```
{% extends "accounts/base.html" %}
{% load i18n %}

{% block title %}{% trans "Register Here!" %}{% endblock %}
{% block header %}
        <h1>{% block page_title %}Register Here!{% endblock page_title %}</h1>
      {% endblock header %}
{% block content %}
  <section class="form short">
    <h1>{% trans "Register" %}</h1>
    <form method="post" id="user_form" enctype="multipart/form-data">
      {% csrf_token %}
      {{ user_form.as_p }}
      {{ profile_form.as_p }}
      
      <p class="submitRow">
        
        <input type="submit" value="{% trans "Register" %}" />
      </p>
    </form>
  </section>
{% endblock %}

```
Login accounts/views.py:
------------------------
```
# -*- coding:utf-8 -*-
from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse

from .forms import UserForm, UserProfileForm
from .models import User

def user_login(request):

    # Если значение request = HTTP POST, попробуем вытащить соответствующую информацию.
    if request.method == 'POST':
        # Собираем из POST имя пользователя и пароль, введенные пользователем.
        # Эту информацию выбираем из login form.
                # Здесь используем request.POST.get('<variable>') вместо request.POST['<variable>'],
                # т.к. request.POST.get('<variable>') возвращает None, если значение не существует,
                # в таком случае request.POST['<variable>'] порождает key error exception
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Используем Django-проверку на совпадение email/password
        # возвращает экземпляр User object если совпадение достигнуто.
        user = authenticate(email=email, password=password)

        # Получив User object, проверяем детали.
        # Если None, значит нет такого пользователя
        
        if user:
            # Если account активный 
            if user.is_active:
            # account существует и активный, разрешаем вход для пользователя.
                # Перенаправляем user на его homepage.
                login(request, user)
                return HttpResponseRedirect('/blog/')
            else:
                # Неактивный account - logging in невозможен!
                return HttpResponse("Your Blog account is disabled.")
        else:
       # Неудачный login. 
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # Значение request не равно HTTP POST, тогда показать login form.
    # Это также соответствует HTTP GET.
    else:
        # Поля формы не заполнены - перенаправляем пользователя 
        # на страницу вхлда
        return render(request, 'accounts/ulogin.html', {})

```

accounts/ulogin.html:
---------------------
```
{% extends "accounts/base.html" %}
{% load i18n %}

{% block title %}{% trans "Log In" %}{% endblock %}

{% block content %}
  <section class="form short">
    <h1>{% trans "Log In" %}</h1>
    <form method="post" id="login_form" action="{% url 'auth.login' %}">
      {% csrf_token %}
            Email: <input type="email" name="email" value="" size="50" />
            <br />
            Password: <input type="password" name="password" value="" size="50" />
            <br />
        <p class="submitRow">
        <a href="{% url 'password_reset' %}">{% trans "Forgot Password?" %}</a>
        <input type="submit" value="{% trans "Log In" %}" />
      </p>
    </form>
  </section>
{% endblock %}

```
accounts/urls.py:
---------------------

```
from django.conf.urls import include, url

urlpatterns = [
    
    url(r'^register/$', 'apps.accounts.views.register', name='register'),
    url(r'^login/$', 'apps.accounts.views.user_login', name='login'),

]
```
accounts/views.py:
---------------------

```
from django.contrib.auth.decorators import login_required

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')
```

accounts/urls.py:
---------------------

```
from django.conf.urls import include, url

urlpatterns = [
    
    url(r'^register/$', 'apps.accounts.views.register', name='register'),
    url(r'^login/$', 'apps.accounts.views.user_login', name='login'),
    url(r'^restricted/', 'apps.accounts.views.restricted', name='restricted'),
    url(r'^logout/$', 'apps.accounts.views.user_logout', name='logout'),
]
```
templates/base.html:
--------------------

```
        
        <div id="navbar" class="navbar-collapse collapse">
                  <div class="navbar-form navbar-right" role="form">
                  {% if user.is_authenticated %}
                    <a id="logout" href="{% url 'authuser:logoutuser' %}" class="btn btn-success">Logout</a>
                  {% else %} 
                    <a id="login" href="{% url 'authuser:register' %}" class="btn btn-success">Register</a>
                    <a id="login" href="{% url 'authuser:loginuser' %}" class="btn btn-success">Sign in</a>
                  {% endif %}
                    
                  </div>
        </div><!--/.navbar-collapse -->
```

namespace='authuser' - urls.py:
-------------------------------

```

urlpatterns += i18n_patterns(
    # Core URLs
    url(r'^', include('core.urls', namespace='core')),

    # Accounts URLs
    # https://github.com/fusionbox/django-authtools/blob/master/authtools/urls.py
    url(r'^', include('extensions.authtools.urls')),
    url(r'^auth/', include('apps.accounts.urls', namespace='authuser')),
```

accounts/urls.py:
---------------------

```
from django.conf.urls import include, url

urlpatterns = [
    
    url(r'^register/$', 'apps.accounts.views.register', name='register'),
    url(r'^loginuser/$', 'apps.accounts.views.user_login', name='loginuser'),
    url(r'^restricted/', 'apps.accounts.views.restricted', name='restricted'),
    url(r'^logoutuser/$', 'apps.accounts.views.user_logout', name='logoutuser'),

]
```


accounts/views.py - HttpResponseRedirect('/auth/loginuser/'):
-------------------------------------------------------------
```
def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']

            profile.save()

            # Изменить переменную при успешной регистрации.
            registered = True
            return HttpResponseRedirect('/auth/loginuser/')
        else:
            print (user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
            'accounts/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

```
accounts/ulogin.html:
---------------------
```
{% extends "accounts/base.html" %}
{% load i18n %}

{% block title %}{% trans "Log In" %}{% endblock %}

{% block content %}
  <section class="form short">
    <h1>{% trans "Log In" %}</h1>
    <form method="post" id="login_form" action="{% url 'authuser:loginuser' %}">
      {% csrf_token %}
            Email: <input type="email" name="email" value="" size="50" />
            <br />
            Password: <input type="password" name="password" value="" size="50" />
            <br />
        <p class="submitRow">
        <a href="{% url 'password_reset' %}">{% trans "Forgot Password?" %}</a>
        <input type="submit" value="{% trans "Log In" %}" />
      </p>
    </form>
    <a id="google_login" href="/accounts/google/login" class="btn btn-success">
                        Sign in with Google
    </a>
    <a id="twitter_login" href="/accounts/twitter/login" class="btn btn-success">Sign in with Twitter
    </a>
  </section>
{% endblock %}

```
Profile:
========

accounts/views.py:
------------------
```
from django.shortcuts import render, render_to_response

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from .forms import UserForm, UserProfileForm
from .models import User, Profile

@login_required
def profile(request):
    context = RequestContext(request)
    u = User.objects.get(name=request.user.name)

    try:
        up = Profile.objects.get(user=u)
    except:
        up = None

    context_dict = {}
    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render_to_response('accounts/profile.html', context_dict, context)
```
accounts/profile.html:
----------------------
```
{% extends "accounts/base.html" %}
{% load i18n %}

{% block title %}{% trans "Profile" %}{% endblock %}

{% block content %}
  <section class="form short">
    <h1>{% trans "Profile" %}</h1>
    <h2>{{ user.name }}</h2>
    <h3>{{ user.email }}</h3>
    {% if userprofile %}
        <p>Website: <a href="{{ userprofile.homepage }}">{{ userprofile.homepage }}</a></p>
        <br/>
        {% if userprofile.avatar %}
            <img src="{{ userprofile.avatar.url }}"  />
        {% endif %}
    {% endif %}
  </section>
{% endblock %}
```
accounts/urls.py:
-----------------
```
from django.conf.urls import include, url

urlpatterns = [
    
    url(r'^register/$', 'apps.accounts.views.register', name='register'),
    url(r'^loginuser/$', 'apps.accounts.views.user_login', name='loginuser'),
    url(r'^restricted/', 'apps.accounts.views.restricted', name='restricted'),
    url(r'^logoutuser/$', 'apps.accounts.views.user_logout', name='logoutuser'),
    url(r'^profile/$', 'apps.accounts.views.profile', name='profile'),

]
```

accounts/viewx.py:
------------------
```
def user_login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/auth/profile/')
            else:
                return HttpResponse("Your Blog account is disabled.")
        else:
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'accounts/ulogin.html', {})

```

Использование объекта Context
=============================

Обычно при создании объекта Context сразу передается словарь со всеми переменными. Но вы можете менять содержимое объекта Context и после его инициализации, использую стандартный API словарей:
```
>>> from django.template import Context
>>> c = Context({"foo": "bar"})
>>> c['foo']
'bar'
>>> del c['foo']
>>> c['foo']
''
>>> c['newvariable'] = 'hello'
>>> c['newvariable']
'hello'
```
Context.get(key, otherwise=None)
`````````````````````````````````
Возвращает значение для key, если key находится в контексте, иначе возвращает otherwise.

Context.pop() Context.push() exception ContextPopException
----------------------------------------------------------
Объект Context работает как стек. Поэтому можно использовать методы push() и pop(). Если вызывать pop() слишком часто, будет вызвано исключение django.template.ContextPopException:
```
>>> c = Context()
>>> c['foo'] = 'first level'
>>> c.push()
{}
>>> c['foo'] = 'second level'
>>> c['foo']
'second level'
>>> c.pop()
{'foo': 'second level'}
>>> c['foo']
'first level'
>>> c['foo'] = 'overwritten'
>>> c['foo']
'overwritten'
>>> c.pop()
Traceback (most recent call last):
...

```
ContextPopException
-------------------

push() можно использовать как менеджер контекста, чтобы быть уверенным, что будет pop() вызван в конце.
```
>>> c = Context()
>>> c['foo'] = 'first level'
>>> with c.push():
>>>     c['foo'] = 'second level'
>>>     c['foo']
'second level'
>>> c['foo']
'first level'
```
Все аргументы push() будут переданы в конструктор dict при создании нового слоя в контексте.
```
>>> c = Context()
>>> c['foo'] = 'first level'
>>> with c.push(foo='second level'):
>>>     c['foo']
'second level'
>>> c['foo']
'first level'
```
update(other_dict)
------------------
Кроме push() и pop() объект Context также предоставляет метод update(). Работает как и push(), но принимает словарь в качестве аргумента и добавляет его в стек.
```
>>> c = Context()
>>> c['foo'] = 'first level'
>>> c.update({'foo': 'updated'})
{'foo': 'updated'}
>>> c['foo']
'updated'
>>> c.pop()
{'foo': 'updated'}
>>> c['foo']
'first level'
```
Использовать Context, как стек, удобно в собственных тегах..

Context.flatten()
-----------------

Метод flatten() возвращает весь стек Context одним словарём, включая встроенные переменные.
```
>>> c = Context()
>>> c['foo'] = 'first level'
>>> c.update({'bar': 'second level'})
{'bar': 'second level'}
>>> c.flatten()
{'True': True, 'None': None, 'foo': 'first level', 'False': False, 'bar': 'second level'}
```
Метод flatten() также используется для сравнения объектов Context внутри системы шаблонов.
```
>>> c1 = Context()
>>> c1['foo'] = 'first level'
>>> c1['bar'] = 'second level'
>>> c2 = Context()
>>> c2.update({'bar': 'second level', 'foo': 'first level'})
{'foo': 'first level', 'bar': 'second level'}
>>> c1 == c2
True
```
Результат flatten() можно использовать в тестах для сравнения Context и dict:
```
class ContextTest(unittest.TestCase):
    def test_against_dictionary(self):
        c1 = Context()
        c1['update'] = 'value'
        self.assertEqual(c1.flatten(), {
            'True': True,
            'None': None,
            'False': False,
            'update': 'value',
        })

```
Классы наследники Context: RequestContext
-----------------------------------------
```
class RequestContext(request[, dict_][, processors])
```
Django предоставляет специальный класс Context, django.template.RequestContext, который немного отличается от обычного django.template.Context. Первое отличие – он принимает HttpRequest первым аргументом. Например:
```
c = RequestContext(request, {
    'foo': 'bar',
})
```
Еще одно отличие – он автоматически добавляет различные переменные в соответствии с опцией context_processors шаблонизатора.

context_processors содержит кортеж функций, которые называются процессорами контекста. Они принимают объект запроса в качестве аргумента и возвращают словарь переменных, которые будут добавлены в контекст. По умолчанию context_processors равна:
```
[
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
]
```

Кроме этого RequestContext всегда использует django.core.context_processors.csrf. Этот процессор контекста используется для безопасности админкой и другими встроенными приложениями. Чтобы исключить его случайное отключение, он захардкоден и не может быть выключен с помощью настройки context_processors.

Процессоры контекста применяются по очереди. Это означает, что один процессор может перетереть переменную, которую добавил предыдущий. Процессоры по умолчанию описаны ниже.

Процессоры контекста применяются после инициализации контекста. То есть процессор может перезаписать переменную, которую вы добавили в Context или RequestContext. Поэтому избегайте названий переменных, которые используются процессорами.

Если вы хотите, чтобы переменная контекста перезаписывала переменные процессора контекста, используйте следующий подход:
```
from django.template import RequestContext

request_context = RequestContext(request)
request_context.push({"my_name": "Adrian"})
```
Django использует такой способ, чтобы перезаписать процессоры контекста во внутреннем API, например render() и TemplateResponse.
Также в RequestContext можно передать список дополнительных процессоров контекста, используя третий необязательный аргумент processors. В это примере в RequestContext будет добавлена переменная ip_address:
```
from django.http import HttpResponse
from django.template import RequestContext

def ip_address_processor(request):
    return {'ip_address': request.META['REMOTE_ADDR']}

def some_view(request):
    # ...
    c = RequestContext(request, {
        'foo': 'bar',
    }, [ip_address_processor])
    return HttpResponse(t.render(c))
```
