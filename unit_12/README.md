## p21v-django unit 12
django-p21v
============

Интернационализация и локализация
=================================

Django обладает полным набором средств для решения этой задачи: перевод текста, форматирование даты, времени и чисел и поддержка часовых поясов.

- Django позволяет разработчикам и авторам шаблонов указывать какие именно части их приложений должны быть переведены или отформатированы под используемые языки и традиции.

- Django использует эти метки для локализации веб приложений под конкретного пользователя, учитывая его настройки.

Интернационализация
--------------------
Подготовка программного обеспечения для локализации. Обычно выполняется разработчиками.

Локализация
------------
Создание переводов и локальных форматов. Обычно выполняется переводчиками.

Перевод и форматирование контролируются параметрами USE_I18N and USE_L10N соответственно. Тем не менее, оба функционала участвуют в интернационализации и локализации. 

locale name
------------
Имя локали, либо спецификация языка в виде ll или комбинация языка и спецификации страны в виде ll_CC. Примеры: it, de_AT, es, pt_BR. Языковая часть всегда указывается в нижнем регистре, а часть, определяющая страну, – в верхнем регистре. Разделителем является символ подчёркивания.

language code
-------------
Представляет имя языка. Используя этот формат, браузеры отправляют имена языков, контент на которых они предпочитают принять, в HTTP заголовке Accept-Language. Примеры: it, de-at, es, pt-br. Обе части (язык и страна) указываются в нижнем регистре, но HTTP заголовок Accept-Language регистронезависимый. Разделителем является символ тире.

message file
-------------
Файл сообщения является обычным текстовым файлом, представляющим единственный язык, который содержит все доступные строки перевода и правила их отображения для данного языка. Файлы сообщений имеют расширение .po.

translation string
------------------
Строка, которая может быть переведена.

format file
------------
Файл формата является модулем языка Python и определяет форматы данных для данной локали.


Django предоставляет утилиты для извлечения переводимых строк в файл сообщений. Этот файл является удобным средством, которое позволяет переводчикам делать свою работу. После того, как перевод строк этого файла завершён, файл должен быть скомпилирован. Этот процесс обеспечивает набор средств GNU gettext.

При наличии скомпилированного ресурса с переводом строк, Django обеспечивает автоматический перевод веб приложений для каждого доступного языка, в соответствии с языковыми настройками пользователя.

Механизм интернационализации Django включен по умолчанию, т.е. в определённых местах фреймворка всегда присутствует небольшая трата ресурсов на его работу. Если вы не используете интернационализацию, то вам следует потратить пару секунд на установку USE_I18N = False в файле конфигурации. Это позволит Django выполнять некоторую оптимизацию, не подгружая библиотеки интернационализации.

Есть также независимый, но связанный параметр USE_L10N, который управляет применением локального форматирования для данных. 

Удостоверьтесь, что вы активировали механизм перевода для вашего проекта, для этого достаточно проверить наличие django.middleware.locale.LocaleMiddleware в параметре конфигурации MIDDLEWARE_CLASSES. 

Интернационализация в коде
--------------------------

Обычный перевод
---------------
Укажите переводимую строку с помощью функции ugettext(). Удобно импортировать её с помощью краткого псевдонима, _ (символ подчеркивания), чтобы сократить затраты на ввод.

Модуль gettext стандартной библиотеки языка Python определяет _() в качестве псевдонима для gettext() в глобальном пространстве имён.

Для поддержки интернационального набора символов (Unicode), функция ugettext() гораздо более полезна, чем gettext(). Иногда вам потребуется использовать функцию ugettext_lazy() в качестве стандартного метода выделения переводимой строки в определённом файле. При отсутствии _() в глобальном пространстве имён разработчик сам решает какая функция будет ему наиболее полезна в каждом конкретном случае.

Символ подчёркивания (_) используется в интерактивном интерпретаторе Python и в доктестах в качестве “результата предыдущей операции”. Определение глобальной функции _() приведёт к путанице. Явное импортирование ugettext() в виде _() решает эту проблему.

В данном примере, текст "Welcome to my site." помечается как переводимая строка:
```
from django.utils.translation import ugettext as _
from django.http import HttpResponse

def my_view(request):
    output = _("Welcome to my site.")
    return HttpResponse(output)
```
Этот пример идентичен предыдущему:
```
from django.utils.translation import ugettext
from django.http import HttpResponse

def my_view(request):
    output = ugettext("Welcome to my site.")
    return HttpResponse(output)
```
Перевод работает с вычисляемыми значениями. Этот пример идентичен предыдущим двум:
```
def my_view(request):
    words = ['Welcome', 'to', 'my', 'site.']
    output = _(' '.join(words))
    return HttpResponse(output)
```
Перевод работает с переменными. И снова, аналогичный пример:
```
def my_view(request):
    sentence = 'Welcome to my site.'
    output = _(sentence)
    return HttpResponse(output)
```

Строка, передаваемая в _() или ugettext(), может принимать заполнители (placeholders), определённые стандартом языка Python для строк. Пример:
```
def my_view(request, m, d):
    output = _('Today is %(month)s %(day)s.') % {'month': m, 'day': d}
    return HttpResponse(output)
```
Такой подход позволяет при необходимости менять порядок слов при переводе. Например, английский текст "Today is November 20." может быть переведён на испанский как "Сеглдня 20 Ноября.". Как видно, заполнители для месяца и дня поменялись местами.

По этой причине, вы должны использовать именованные заполнители (т.е., %(day)s) вместо позиционных (т.е., %s или %d), в случае, если в строку подставляется больше одного параметра. При использовании позиционных заполнителей переводчики не будут иметь возможность изменять оригинальный порядок слов.

Комментарии для переводчиков
----------------------------
Если необходимо дать переводчикам подсказку по переводимой строке, вы можете добавить комментарий с префиксом Translators в строке предшествующей переводимой, например:
```
def my_view(request):
    # Translators: This message appears on the home page only
    output = ugettext("Welcome to my site.")
```
Комментарий появится в результирующем .po файле, который связан с переводимой конструкцией расположенной далее, и должен быть отображён большинством средств перевода.

Для полноты изложения приведём соответствующий фрагмент .po файла:
```
#. Translators: This message appears on the home page only
# path/to/python/file.py:123
msgid "Welcome to my site."
msgstr ""
```
Этот подход также работает в шаблонах. 

Пометка строк как no-op
-----------------------
Используйте функцию django.utils.translation.ugettext_noop() для пометки строки как переводимой, но не переводя её. Такая строка будет переведена позже с помощью переменной.

Используйте этот подход в случае, когда у вас есть строковые константы, которые должны быть сохранены в исходном коде по причине того, что они изменяются системой или пользователями Примером могут служить строки из базы данных, которые следует переводить в самый последний момент, перед непосредственным их отображением пользователю.

Множественное число
-------------------
Используйте функцию django.utils.translation.ungettext() для указания сообщений во множественном числе.

Функция ungettext принимает три аргумента: строка в единственном числе, строка во множественном числе и количество объектов.

Эта функция очень полезна, когда требуется локализовать Django приложение на языки, в которых количество и сложность множественных форм превышает два варианта как в английском языке (‘object’ для единственного числа и ‘objects’ для всех остальных случаем, когда count отличается от единицы, независимо от своего значения.)

Например:
```
from django.utils.translation import ungettext
from django.http import HttpResponse

def hello_world(request, count):
    page = ungettext(
        'there is %(count)d object',
        'there are %(count)d objects',
    count) % {
        'count': count,
    }
    return HttpResponse(page)
```
В этом примере количество объектов передаётся в перевод в переменной count.

Следует отметить, что приведение существительного к множественному числу является непростой задачей и работает по-разному в каждом языке. Сравнение count с 1 не всегда будет корректным правилом. Следующий код выглядит разумно, но будет выдавать неверный результат для некоторых языков:
```
from django.utils.translation import ungettext
from myapp.models import Report

count = Report.objects.count()
if count == 1:
    name = Report._meta.verbose_name
else:
    name = Report._meta.verbose_name_plural

text = ungettext(
    'There is %(count)d %(name)s available.',
    'There are %(count)d %(name)s available.',
    count
) % {
    'count': count,
    'name': name
}
```
Не стоит пытаться реализовать собственную логику для создания множественного числа, она не будет работать корректно. В этом случае, рассмотрите использование следующего подхода:
```
text = ungettext(
    'There is %(count)d %(name)s object available.',
    'There are %(count)d %(name)s objects available.',
    count
) % {
    'count': count,
    'name': Report._meta.verbose_name,
}
```
При использовании ungettext(), проверьте, что вы используете уникальное имя для каждой переменной, указанной в строке. В вышеприведённом примере, обратите внимание на то, как мы используем переменную name в обоих строках. Следующий пример, будучи неверным для некоторых языков, выдаст ошибку:
```
text = ungettext(
    'There is %(count)d %(name)s available.',
    'There are %(count)d %(plural_name)s available.',
    count
) % {
    'count': Report.objects.count(),
    'name': Report._meta.verbose_name,
    'plural_name': Report._meta.verbose_name_plural
}
```
Вы получите ошибку при запуске django-admin compilemessages:
```
a format specification for argument 'name', as in 'msgstr[0]', doesn't exist in 'msgid'
```

Множественная форма и файлы перевода
------------------------------------

Django не поддерживает собственные правила множественного числа в файлах перевода. Так как все файлы перевода объединяются вместе, будет использоваться только правило главного файла перевода Django (из django/conf/locale/lang_code/LC_MESSAGES/django.po). Правила множественной формы всех остальных *.po файлов будут проигнорированы. Поэтому вам не следует использовать их в вашем проекте и приложении.

Контекстные маркеры
-------------------
Некоторые слова имеют множество значений, такие как "May" в английском языке, которое может означать название месяца или глагол. Для упрощения жизни переводчиков вы можете использовать функцию django.utils.translation.pgettext() или функцию django.utils.translation.npgettext(), для множественного числа. Обе функции принимают описание контекста в качестве первого аргумента.

В результате, в файле .po, переводимая строка появится столько раз, сколько есть различных контекстов для неё (контекстная информация будет указана в строке msgctxt), позволяя перевести каждую из них в соответствии со смыслом.

Например:
```
from django.utils.translation import pgettext

month = pgettext("month name", "May")
```
или:
```
from django.db import models
from django.utils.translation import pgettext_lazy

class MyThing(models.Model):
    name = models.CharField(help_text=pgettext_lazy(
        'help text for MyThing model', 'This is the help text'))
```
появится в файле .po в виде:
```
msgctxt "month name"
msgid "May"
msgstr ""
```
Контекстные маркеры также поддерживаются шаблонными тегами trans и blocktrans.

Ленивый перевод
---------------
Используйте ленивые версии функций перевода из django.utils.translation (их легко опознать по суффиксу lazy в их именах) для отложенного перевода строк – перевод производится во время обращения к строке, а не когда вызывается функция.

Эти функции хранят ленивую ссылку на строку, не на её перевод. Сам перевод будет выполнен во время использования строки в строковом контексте, например, во время обработки шаблона.

Это полезно, когда функция перевода вызывается при загрузке модуля.

Такое может легко произойти во время определения моделей, форм или модельных форм, так как в Django их поля реализованы в виде атрибутов класса. По этой причине, надо использовать ленивый перевод в следующих случаях:

- Поля модели и связанные с ними значения атрибутов verbose_name и help_text
Например, для перевода подсказки для поля name в следующей модели, действуйте так:
```
from django.db import models
from django.utils.translation import ugettext_lazy as _

class MyThing(models.Model):
    name = models.CharField(help_text=_('This is the help text'))
```
Вы можете перевести имена связей ForeignKey, ManyToManyField или OneToOneField с помощью их атрибута verbose_name:
```
class MyThing(models.Model):
    kind = models.ForeignKey(ThingKind, related_name='kinds',
                             verbose_name=_('kind'))
```
Подобно тому, как вы делаете для verbose_name, вы должны предоставить текст метки (строчными буквами) для связи, а Django автоматически преобразует первую букву в прописную когда это необходимо.

Значения для подписи модели
-----------------------------
Рекомендуется всегда предоставлять явные значения для verbose_name и verbose_name_plural, а не надеяться на механизм их автоматического определения через имя класса:
```
from django.db import models
from django.utils.translation import ugettext_lazy as _

class MyThing(models.Model):
    name = models.CharField(_('name'), help_text=_('This is the help text'))

    class Meta:
        verbose_name = _('my thing')
        verbose_name_plural = _('my things')
```
Значения атрибута short_description у методов модели
----------------------------------------------------
Для методов модели вы можете с помощью атрибута short_description предоставить перевод для Django и интерфейса администратора:
```
from django.db import models
from django.utils.translation import ugettext_lazy as _

class MyThing(models.Model):
    kind = models.ForeignKey(ThingKind, related_name='kinds',
                             verbose_name=_('kind'))

    def is_mouse(self):
        return self.kind.type == MOUSE_TYPE
    is_mouse.short_description = _('Is it a mouse?')
```
Работа с ленивыми объектами перевода
-------------------------------------
Результат вызова ugettext_lazy() может быть использован везде, где требуется юникодная строка (объект типа unicode). Если вы попытаетесь использовать её там, где ожидается обычная строка (объект типа str), то не получите ожидаемый результат, так как объект ugettext_lazy() не знает, как преобразовать себя в обычную строку. Вы не можете использовать юникодную строку внутри обычной, что, в общем, является обычным поведением в Python. Например:
```
# This is fine: putting a unicode proxy into a unicode string.
"Hello %s" % ugettext_lazy("people")

# This will not work, since you cannot insert a unicode object
# into a bytestring (nor can you insert our unicode proxy there)
b"Hello %s" % ugettext_lazy("people")
```
Если вы встретили нечто подобное 
```
"hello <django.utils.functional...>", 
```
значит вы попытались вставить результат ugettext_lazy() в обычную строку. Это ошибка в вашем коде.

Если вам не нравится писать такое длинное имя, как ugettext_lazy, в можете создать для него псевдоним _ (символ подчеркивания), вот так:
```
from django.db import models
from django.utils.translation import ugettext_lazy as _

class MyThing(models.Model):
    name = models.CharField(help_text=_('This is the help text'))
```
Использование ugettext_lazy() и ungettext_lazy() для пометки строк в моделях и в прикладных функциях является обычной операцией. Работая с этими объектами в вашем коде, вы должны быть уверены, что вы не преобразовываете их случайно в строки, так как это преобразование должно происходить как можно позже (и будет приниматься во внимание правильная локаль). Это потребует использования вспомогательной функции, описанной далее.

Ленивый перевод и перевод множественного числа
-----------------------------------------------
Используя ленивый перевод для срок с множественным числом ([u]n[p]gettext_lazy), вы не знаете значение аргумента number при определении строки. Однако, вы можете использовать аргумент number вместо числа. При определении перевода number будет определяться из переданных аргументов. Например:
```
from django import forms
from django.utils.translation import ugettext_lazy

class MyForm(forms.Form):
    error_message = ungettext_lazy("You only provided %(num)d argument",
        "You only provided %(num)d arguments", 'num')

    def clean(self):
        # ...
        if error:
            raise forms.ValidationError(self.error_message % {'num': number})
```
Если строка принимает только один аргумент, вы можете передать непосредственно number:
```
class MyForm(forms.Form):
    error_message = ungettext_lazy("You provided %d argument",
        "You provided %d arguments")

    def clean(self):
        # ...
        if error:
            raise forms.ValidationError(self.error_message % number)
```
Объединение строк: string_concat()
----------------------------------
Стандартное для Python объединение строк (''.join([...])) не будет работать со списками, которые содержат объекты отложенного перевода. Для этого вы можете использовать функцию django.utils.translation.string_concat(), создающую ленивый объект, который объединяет своё содержимое и преобразует его в строку, только когда результат функции включается в строку. Например:
```
from django.utils.translation import string_concat
from django.utils.translation import ugettext_lazy
...
name = ugettext_lazy('John Lennon')
instrument = ugettext_lazy('guitar')
result = string_concat(name, ': ', instrument)
```
В данном случае, отложенный перевод в result будет преобразован в строку только когда сам result будет использован в строке (обычно это происходит во время обработки шаблона).

Другое использование ленивости в отложенных переводах
------------------------------------------------------
Для остальных случаев, когда вам надо отсрочить перевод, но приходится передавать переводимую строку в качестве аргумента другой функции, вы можете обернуть эту функцию в ленивый вызов. Например:
```
from django.utils import six  # Python 3 compatibility
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

mark_safe_lazy = lazy(mark_safe, six.text_type)
```
А затем:
```
lazy_string = mark_safe_lazy(_("<p>My <strong>string!</strong></p>"))
```
Локализованные названия языков
------------------------------
get_language_info()
-------------------
Функция get_language_info() предоставляет детальную информацию о языках:
```
>>> from django.utils.translation import get_language_info
>>> li = get_language_info('de')
>>> print(li['name'], li['name_local'], li['bidi'])
German Deutsch False
```
Атрибуты name и name_local содержат название языка на английском и на этом самом языке соответственно. Атрибут bidi установлен в True только для двунаправленных языков.

Источником информации о языках является модуль django.conf.locale. Аналогичный доступ к информации о языках есть и на уровне шаблонов.

Интернационализация: в коде шаблонов
------------------------------------
Для перевода текста в шаблонах Django используют два шаблонных тега и немного отличающийся от Python синтаксис. Чтобы воспользоваться этими тегами, поместите {% load i18n %} в начало шаблона. Аналогично остальным шаблонным тегам, данный тег должен быть указан во всех шаблонах, которые применяют механизм переводов, даже в тех, которые расширяются из других шаблонов, имеющих в себе тег i18n.

Шаблонный тег trans
-------------------
Шаблонный тег {% trans %} может переводить как обычную строку, заключенную в одинарные или двойные кавычки, так и содержимое переменой:
```
<title>{% trans "This is the title." %}</title>
<title>{% trans myvar %}</title>
```
При использовании опции noop, обращение к переменной происходит, но перевод не выполняется. Это удобно, когда надо пометить контент для перевода в будущем:
```
<title>{% trans "myvar" noop %}</title>
```
Перевод подстроки выполняется с помощью функции ugettext().

В случае передачи шаблонной переменой в тег, тег сначала преобразовывает её в строку, а затем ищет для неё перевод в каталогах сообщений.

Невозможно использовать шаблонные переменные внутри строки для тега {% trans %}. Если же ваш перевод требует наличия переменой в строке, используйте шаблонный тег {% blocktrans %}.

Если требуется получать переведённые строки без их отображения, то вы можете использовать следующий синтаксис:
```
{% trans "This is the title" as the_title %}

<title>{{ the_title }}</title>
<meta name="description" content="{{ the_title }}">
```
На практике вы будете применять это для получения строк, которые используются во множестве мест шаблона или должны быть использованы в качестве аргументов для других шаблонных тегов или фильтров:
```
{% trans "starting point" as start %}
{% trans "end point" as end %}
{% trans "La Grande Boucle" as race %}

<h1>
  <a href="/" title="{% blocktrans %}Back to '{{ race }}' homepage{% endblocktrans %}">{{ race }}</a>
</h1>
<p>
{% for stage in tour_stages %}
    {% cycle start end %}: {{ stage }}{% if forloop.counter|divisibleby:2 %}<br />{% else %}, {% endif %}
{% endfor %}
</p>
```
Тег {% trans %} также поддерживает контекстные маркеры с помощью атрибута context:
```
{% trans "May" context "month name" %}
```
Шаблонный тег blocktrans
------------------------
В отличии от тега trans, тег blocktrans позволяет отмечать сложные предложения, состоящие из строк и переменных, обеспечивая перевод с помощью подстановок:
```
{% blocktrans %}This string will have {{ value }} inside.{% endblocktrans %}
```
Для перевода шаблонных выражений, скажем, с доступом к атрибутам объекта или с использованием шаблонных фильтров, потребуется связать выражение с локальной переменной для использования внутри переводимого блока. Примеры:
```
{% blocktrans with amount=article.price %}
That will cost $ {{ amount }}.
{% endblocktrans %}

{% blocktrans with myvar=value|filter %}
This will have {{ myvar }} inside.
{% endblocktrans %}
```
Вы можете использовать несколько выражений внутри одного тега blocktrans:
```
{% blocktrans with book_t=book|title author_t=author|title %}
This is {{ book_t }} by {{ author_t }}
{% endblocktrans %}
```

Как и прежде, тег поддерживает старое форматирование: {% blocktrans with book|title as book_t and author|title as author_t %}
Внутри тега blocktrans запрещается использовать другие блочные теги (например {% for %} или {% if %}).

Если невозможно вычисление хотя бы одного из аргументов блока, тогда тег переключается на язык по умолчанию с помощью функции deactivate_all().

Этот тег также поддерживает склонение, например:

Определите переменную count и свяжите с ней значение счётчика. По этому значению будет выбираться форма склонения.

Укажите единственную и множественную формы, разделив их с помощью тега {% plural %} внутри тегов {% blocktrans %} и {% endblocktrans %}.

Пример:
```
{% blocktrans count counter=list|length %}
There is only one {{ name }} object.
{% plural %}
There are {{ counter }} {{ name }} objects.
{% endblocktrans %}
```
Более сложный пример:
```
{% blocktrans with amount=article.price count years=i.length %}
That will cost $ {{ amount }} per year.
{% plural %}
That will cost $ {{ amount }} per {{ years }} years.
{% endblocktrans %}
```
Когда используете и возможности склонения, и присвоение значения локальным переменным в дополнение к значению счетчика, помните, что конструкция blocktrans на низком уровне преобразовывается в вызов ungettext. Это означает, что к ней применяются замечания для переменных ungettext.

Обратное разрешение URL не можно быть выполнено внутри blocktrans и должно выполняться заранее:
```
{% url 'path.to.view' arg arg2 as the_url %}
{% blocktrans %}
This is a URL: {{ the_url }}
{% endblocktrans %}
```
Тег {% blocktrans %} также поддерживает контекстные маркеры с помощью атрибута context:

{% blocktrans with name=user.username context "greeting" %}Hi {{ name }}{% endblocktrans %}
Другой особенностью {% blocktrans %} является поддержка опции trimmed. Эта опция удаляет символы завершения строки из начала и конца содержимого данного тега, убирая пробелы в начале и конце строк и объединяя все строки в одну, разделяя их пробелами. Это очень удобно при форматировании контента тега с помощью отступов, так как эти пробелы не попадают в содержимое PO файлов, упрощая процесс перевода.

Например, следующий тег {% blocktrans %}:
```
{% blocktrans trimmed %}
  First sentence.
  Second paragraph.
{% endblocktrans %}
```
выразится в записи``”First sentence. Second paragraph.”`` внутри PO файла, что несравнимо с "\n  First sentence.\n  Second sentence.\n", в случае когда опция trimmed не используется.

Строки передаваемые в шаблонные теги и фильтры
----------------------------------------------
Для перевода строк, передаваемых в теги и фильтры, можно использовать _():
```
{% some_tag _("Page not found") value|yesno:_("yes,no") %}
```
В этом случае, и тег, и фильтр увидят заранее переведённую строку, т.е. им не надо будет беспокоиться о переводе.

В этом примере в модуль перевода будет передана строка "yes,no", а не отдельные строки "yes" и "no". Перевод этой строки должен содержать запятую так, чтобы код парсера фильтра знал как разбить эту строку. Например, немецкий переводчик может переводить строку "yes,no" как "ja, nein", сохраняя нетронутой запятую.
Комментарии для переводчиков шаблонов
-------------------------------------
Аналогично случаю с кодом на языке Python, такие пометки для переводчиков могут быть сделаны с помощью комментариев, например с помощью тега comment:
```
{% comment %}Translators: View verb{% endcomment %}
{% trans "View" %}

{% comment %}Translators: Short intro blurb{% endcomment %}
<p>{% blocktrans %}A multiline translatable
literal.{% endblocktrans %}</p>
```
или с помощью {# ... #} однострочного комментария:
```
{# Translators: Label of a button that triggers search #}
<button type="submit">{% trans "Go" %}</button>

{# Translators: This is a text of the base template #}
{% blocktrans %}Ambiguous translatable block of text{% endblocktrans %}
```

Для полноты изложения приведём соответствующий фрагмент .po файла:
```
#. Translators: View verb
# path/to/template/file.html:10
msgid "View"
msgstr ""

#. Translators: Short intro blurb
# path/to/template/file.html:13
msgid ""
"A multiline translatable"
"literal."
msgstr ""

# ...

#. Translators: Label of a button that triggers search
# path/to/template/file.html:100
msgid "Go"
msgstr ""

#. Translators: This is a text of the base template
# path/to/template/file.html:103
msgid "Ambiguous translatable block of text"
msgstr ""
```
Переключения языка в шаблоне
------------------------------
Если вы хотите выбрать язык в шаблоне, используйте тег language:
```
{% load i18n %}

{% get_current_language as LANGUAGE_CODE %}
<!-- Current language: {{ LANGUAGE_CODE }} -->
<p>{% trans "Welcome to our page" %}</p>

{% language 'en' %}
    {% get_current_language as LANGUAGE_CODE %}
    <!-- Current language: {{ LANGUAGE_CODE }} -->
    <p>{% trans "Welcome to our page" %}</p>
{% endlanguage %}
```
Первая фраза “Welcome to our page” будет использовать текущий язык, в то время как вторая будет на Английском.

Другие теги
------------
Эти теги также требуют наличия {% load i18n %} в шаблоне.

Шаблонная конструкция {% get_available_languages as LANGUAGES %} возвращает список кортежей в которых, первый элемент является кодом языка, а второй - его названием (переведённым в язык текущей локали).

Шаблонная конструкция {% get_current_language as LANGUAGE_CODE %} возвращает предпочитаемый язык текущего пользователя в виде строки. Например: en-us. (Обратитесь к Как Django определяет языковую настройку.)

Шаблонная конструкция {% get_current_language_bidi as LANGUAGE_BIDI %} возвращает направление текста текущей локали. Если True, то имеем дело с “обратным” языком, т.е.: еврейский, арабский. Если False, то это “стандартный для нас” язык, т.е.: английский, французский, немецкий и так далее.

Если вы активировали контекстный процессор django.template.context_processors.i18n, то каждый экземпляр RequestContext будет обладать доступом к переменным LANGUAGES, LANGUAGE_CODE и LANGUAGE_BIDI, описанным выше.

Вы также можете получить информацию о любом доступном языке, используя предоставленные шаблонные теги и фильтры. Для получения информации об одном языке используйте тег {% get_language_info %}:
```
{% get_language_info for LANGUAGE_CODE as lang %}
{% get_language_info for "pl" as lang %}
```
Затем вы можете узнать следующее:
```
Language code: {{ lang.code }}<br />
Name of language: {{ lang.name_local }}<br />
Name in English: {{ lang.name }}<br />
Bi-directional: {{ lang.bidi }}
```
Также вы можете использовать шаблонный тег {% get_language_info_list %} для получения информации о списке языков (т.е. об активных языках, которые указаны в параметре конфигурации LANGUAGES). 

В дополнение к стилю вложенных кортежей из параметра конфигурации LANGUAGES, шаблонный тег {% get_language_info_list %} поддерживает простой список кодов языка. Если вы сделаете следующее в своём представлении:
```
context = {'available_languages': ['en', 'es', 'fr']}
return render(request, 'mytemplate.html', context)
```
вы можете по очереди пройтись по этим языкам в шаблоне:
```
{% get_language_info_list for available_languages as langs %}
{% for lang in langs %} ... {% endfor %}
```
Также для удобства есть простые фильтры:
```
{{ LANGUAGE_CODE|language_name }} (“Немецкий”)

{{ LANGUAGE_CODE|language_name_local }} (“Deutsch”)
{{ LANGUAGE_CODE|language_bidi }} (False)
```
Интернационализация на уровне кода JavaScript
----------------------------------------------

Добавление переводов в JavaScript вызывает ряд проблем:

- JavaScript код не имеет доступа к механизму gettext.

- JavaScript код не имеет доступа к файлам .po или .mo, их надо передавать с сервера.

- Каталог с переводами для JavaScript должен иметь минимально возможный размер.

Django предоставляет интегрированное решение для этих проблем. Перевод внедряется в JavaScript, т.е. вы можете использовать gettext и остальные функции в JavaScript коде.

Представление javascript_catalog
---------------------------------
javascript_catalog(request, domain='djangojs', packages=None)
Основным решением описанных проблем является представление django.views.i18n.javascript_catalog(), которое выдаёт библиотеку с кодом JavaScript, функции которой реализуют интерфейс gettext, а также массив переведённых строк. Переведённые строки собираются из приложений или Django, в зависимости от того, что вы указали info_dict или URL. Пути, указанные в параметре конфигурации LOCALE_PATHS, также принимаются во внимание.

Вы можете использовать это так:
```
from django.views.i18n import javascript_catalog

js_info_dict = {
    'packages': ('your.app.package',),
}

urlpatterns = [
    url(r'^jsi18n/$', javascript_catalog, js_info_dict),
]
```
Каждая строка в packages должна быть представлена в точечном формате Python (формат аналогичен формату параметра конфигурации INSTALLED_APPS) и должна ссылаться на пакет, у которого есть каталог locale. Если вы указываете несколько пакетов, все их каталоги сообщений будут собраны в единый каталог. Это полезно, если ваш JavaScript код использует строки из нескольких приложений.

Приоритет переводов таков, что пакеты, определённые позже, имеют более высокий приоритет, чем определённые ранее. Это важно, если переводы совпадают в разных приложениях.

По умолчанию, представление использует домен djangojs (речь идёт о домене gettext). Это поведение может быть изменено с помощью аргумента domain.

Вы можете сделать представление динамическим, поместив пакеты в шаблон URL:
```
urlpatterns = [
    url(r'^jsi18n/(?P<packages>\S+?)/$', javascript_catalog),
]
```
Используя это, вы определяете пакеты в виде списка их имён, разделённых с помощью знака плюс в URL. Это особенно полезно, если ваши страницы используют код из разных приложений, всегда из разных, и вам не хочется собирать весь перевод в один большой каталог. Для безопасности, все эти значения могут быть взяты либо из django.conf, либо из любого пакета, определённого в параметре конфигурации INSTALLED_APPS.

Переводы JavaScript, найденные по путям, перечисленным в параметре конфигурации LOCALE_PATHS всегда используются. Для сохранения целостности в работе алгоритма поиска переводов, используемом для Python и шаблонов, каталоги, указанные в параметре конфигурации LOCALE_PATHS имеют убывающий приоритет от начала к концу.

Использование каталога переводов JavaScript
-------------------------------------------
Для использования этого каталога, просто запросите динамически генерируемый скрипт, как показано ниже:
```
<script type="text/javascript" src="{% url 'django.views.i18n.javascript_catalog' %}"></script>
```
Здесь используется запрос на поиск URL для представления, генерирующего JavaScript-каталог. После загрузки каталога, ваш JavaScript код может использовать стандартный интерфейс gettext для доступа к каталогу:
```
document.write(gettext('this is to be translated'));
```
Также можно использовать интерфейс ngettext:
```
var object_cnt = 1 // or 0, or 2, or 3, ...
s = ngettext('literal for the singular case',
        'literal for the plural case', object_cnt);
```
и даже функцию интерполяции строк:
```
function interpolate(fmt, obj, named);
```
Синтаксис интерполяции заимствован из Python, т.е. функция interpolate поддерживает как позиционные, так и именованные интерполяции:

Позиционная интерполяция: obj содержит объект Array, чьи значения элементов затем последовательно интерполируются в соответствующие подстановки fmt, в порядке их определения. Например:
```
fmts = ngettext('There is %s object. Remaining: %s',
        'There are %s objects. Remaining: %s', 11);
s = interpolate(fmts, [11, 20]);
// s is 'There are 11 objects. Remaining: 20'
```
Именованная интерполяция: Этот режим выбирается при передаче необязательного параметра named (named=True). Параметр obj содержит JavaScript объект или ассоциативный массив. Например:
```
d = {
    count: 10,
    total: 50
};

fmts = ngettext('Total: %(total)s, there is %(count)s object',
'there are %(count)s of a total of %(total)s objects', d.count);
s = interpolate(fmts, d, true);
```
Не злоупотребляйте интерполяцией строк, помните: это всё JavaScript, и для проверки используются регулярные выражения. Интерполяция в JavaScript выполняется не так быстро, как на Python, так что используйте её только при реальной необходимости.

Комментарий о производительности
--------------------------------
Представление javascript_catalog() создаёт каталог из .mo файлов при каждом запросе. И раз вывод предоставления неизменен, как минимум для текущей версии сайта, его следует закэшировать.

Кэширование на стороне сервера снизит нагрузку на ЦПУ. С помощью декоратора cache_page() организовать кэширование несложно. Для сброса кэша при изменении переведённых ресурсов следует предоставлять префикс, зависящий от номера версии, как это показано на следующем примере, или подключить представление к URL, содержащему номер версии.
```
from django.views.decorators.cache import cache_page
from django.views.i18n import javascript_catalog

# The value returned by get_version() must change when translations change.
@cache_page(86400, key_prefix='js18n-%s' % get_version())
def cached_javascript_catalog(request, domain='djangojs', packages=None):
    return javascript_catalog(request, domain, packages)
```
Кэширование на стороне клиента экономит пропускную способность и ускоряет отклик сайта. Если вы используете ETags (USE_ETAGS = True), у вас уже всё включено. С другой стороны, вы можете использовать условные декораторы. В следующем примере, кэш сбрасывается при перезапуске сервера приложений.
```
from django.utils import timezone
from django.views.decorators.http import last_modified
from django.views.i18n import javascript_catalog

last_modified_date = timezone.now()

@last_modified(lambda req, **kw: last_modified_date)
def cached_javascript_catalog(request, domain='djangojs', packages=None):
    return javascript_catalog(request, domain, packages)
```
Также вы можете заранее создавать javascript-каталог во время процесса выкладывания кода на сервер и использовать его как статичный файл. Такой подход используется в django-statici18n.

Интернационализация: в шаблонах URL
-----------------------------------

Django предоставляет два способа интернационализации шаблонов URL:

- Добавление языкового префикса в начало шаблонов URL, чтобы класс LocaleMiddleware мог определить требуемый язык по запрошенному ресурсу.

- Перевод самих шаблонов URL с помощью функции django.utils.translation.ugettext_lazy().

Использование любой из этих возможностей требует, чтобы активный язык был установлен при каждом запросе. Другими словами, в должны указать django.middleware.locale.LocaleMiddleware в настройках MIDDLEWARE_CLASSES.

Перевод шаблонов URL
--------------------
Шаблоны URL могут быть помечены как подлежащие переводу с помощью функции ugettext_lazy(). Например:
```
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _

from about import views as about_views
from news import views as news_views
from sitemaps.views import sitemap

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap, name='sitemap_xml'),
]

news_patterns = [
    url(r'^$', news_views.index, name='index'),
    url(_(r'^category/(?P<slug>[\w-]+)/$'), news_views.category, name='category'),
    url(r'^(?P<slug>[\w-]+)/$', news_views.details, name='detail'),
]

urlpatterns += i18n_patterns(
    url(_(r'^about/$'), about_views.main, name='about'),
    url(_(r'^news/'), include(news_patterns, namespace='news')),
)
```
После создания перевода функция reverse() будет возвращать URL для активного языка. Например:
```
from django.core.urlresolvers import reverse
from django.utils.translation import activate

>>> activate('en')
>>> reverse('news:category', kwargs={'slug': 'recent'})
'/en/news/category/recent/'

>>> activate('nl')
>>> reverse('news:category', kwargs={'slug': 'recent'})
'/nl/nieuws/categorie/recent/'
```

В большинстве случаев, лучше применять переведенные URL только внутри блока, который добавляет языковой префикс для шаблонов (using i18n_patterns()), это поможет избежать конфликта небрежно переведенных URL с непереведёнными шаблонами.
Генерация URL в шаблонах
------------------------
Если локализованные URL генерируются в шаблонах, они всегда используют текущий язык. Для получения URL для другого языка следует использовать шаблонный тег language. Этот тег включает выбранный язык внутри своего блока:
```
{% load i18n %}

{% get_available_languages as languages %}

{% trans "View this category in:" %}
{% for lang_code, lang_name in languages %}
    {% language lang_code %}
    <a href="{% url 'category' slug=category.slug %}">{{ lang_name }}</a>
    {% endlanguage %}
{% endfor %}
```
Шаблонный тег language принимает в качестве аргумента код языка.

Локализация: как создать языковые файлы
----------------------------------------

После того, как текстовые ресурсы приложения были помечены для перевода, следует выполнить (или получить) сам перевод. Вот как это работает.

Файлы сообщений
---------------
Первым шагом будет создание файла сообщений для нового языка. Файл сообщений является простым текстовым файлом, предоставляющим один язык, который содержит все переводимые строки и правила их представления на этом языке. Файлы сообщений имеют расширение .po.

Django поставляется с утилитой, django-admin makemessages, которая автоматизирует создание и обновление этих файлов.

Утилиты Gettext
----------------
Команда makemessages (и compilemessages) использует команды из утилит набора GNU gettext: xgettext, msgfmt, msgmerge и msguniq.

Минимальной поддерживаемой версией утилит gettext является 0.15.

Для создания или обновления файла сообщений запустите эту команду:
```
django-admin makemessages -l de
```
... где de является названием локали для создаваемого файла сообщений. Например, это pt_BR для бразильского варианта португальского языка и de_AT для австрийского варианта немецкого языка или id для индонезийского.

Этот скрипт должен быть запущен из одного из двух мест:

- Корневой каталог вашего Django проекта (который содержит manage.py)

- Корневой каталог одного из приложений Django.

Скрипт просматривает дерево исходного кода вашего проекта или приложения и извлекает все строки, помеченные для перевода(смотрите Как Django находит переводы и убедитесь что LOCALE_PATHS настроен правильно). Затем скрипт создаёт (или обновляет) файл сообщений в каталоге locale/LANG/LC_MESSAGES. В случае примера с de, файл будет создан в locale/de/LC_MESSAGES/django.po.

По умолчанию, django-admin makemessages просматривает каждый файл с расширениями .html или .txt. Если вам надо изменить это поведение, используйте опцию --extension или -e для указания нужного расширения для просматриваемых файлов:
```
django-admin makemessages -l de -e txt
```
Разделяйте множество расширений с помощью запятой и/или используйте опцию многократно:
```
django-admin makemessages -l de -e html,txt -e xml
```

При создании файлов сообщений на основе Javascript вам потребуется использовать специальный домен ‘djangojs’, а не опцию -e js.

Если у вас не установлены утилиты gettext, тогда makemessages создаст пустые файлы. Если вы столкнулись с такой проблемой, тогда либо установите утилиты gettext, либо скопируйте файл сообщений для английского языка (locale/en/LC_MESSAGES/django.po), если он доступен, и используйте его как стартовую точку; это просто пустой файл переводов.

Если вы используете Windows и вам надо установить утилиты GNU gettext для работы makemessages, обратитесь к gettext на Windows за дополнительной информацией.
Формат .po файлов несложен. Каждый .po файл содержит небольшой заголовок, например, контактную информацию ответственного. Но основная часть файла является списком сообщений – простое сопоставление переводимых строк с переводами на конкретный язык.

Например, если ваше Django приложение содержит переводимую строку "Welcome to my site.", так:
```
_("Welcome to my site.")
```
...тогда django-admin makemessages создаст .po файл, содержащий следующие данные – сообщение:
```
#: path/to/python/module.py:23
msgid "Welcome to my site."
msgstr ""
```
Краткое объяснение:

- msgid является переводимой строкой, которая определена в исходном коде. Не изменяйте её.

- msgstr является местом, где вы пишите свой перевод. Обычно оно пустое, именно вы отвечаете за его наполнение. Удостоверьтесь, что вы сохранили кавычки вокруг перевода.

Для удобства, каждое сообщение включает, в виде закомментированной строки, размещенной выше строки msgid, имя файла и номер строки из которой была получена переводимая строка.

Длинные сообщения являются особым случаем. Так, первая строка сразу после msgstr (или msgid) всегда пустая. Затем идёт длинный перевод, разбитый на несколько строк. Эти строки будут собраны в одну. Не забывайте вставлять завершающие пробелы, иначе итоговая строка будет собрана без них!

Укажите свою кодировку
----------------------
Из-за особенностей внутренней работы утилит пакета gettext и нашего желания позволить использование не-ASCII символов в строках кода Django и ваших приложений, вы должны использовать UTF-8 в качестве кодировки ваших PO файлов (по умолчанию при их создании). Это означает, что все будут использовать одинаковую кодировку, что очень важно в момент, когда Django обрабатывает PO файлы.
Для повторного прохода по всему исходному коду и шаблонам в поисках новых переводимых строк и для обновления всех файлов с сообщениями для всех языков, выполните это:
```
django-admin makemessages -a
```
Компиляция файлов с сообщениями
-------------------------------
После того, как вы создали файл с сообщениями, а также после каждого его обновления, вам следует скомпилировать этот файл, чтобы позволить gettext его использовать. Сделайте это с помощью утилиты django-admin compilemessages.

Эта команда обрабатывает все имеющиеся .po файлы и создаёт на их основе .mo файлы, которые являются бинарными файлами, оптимизированными для использования gettext. Запускать django-admin compilemessages надо в том же каталоге, что и django-admin makemessages, вот так:
```
django-admin compilemessages
```

Если вы используете Windows и желаете установить утилиты GNU gettext для работы django-admin compilemessages, обратитесь к gettext на Windows для подробностей.

.po файлы: Кодировка и использование BOM
-----------------------------------------
Django поддерживает .po файлы только в кодировке UTF-8 и без меток BOM (Byte Order Mark). Если ваш редактор по умолчанию добавляет такие метки в начало файла, вам следует изменить это поведение.

Создание файлов сообщений из JavaScript кода
--------------------------------------------
Вы создаёте и обновляете файлы сообщений аналогично обычным файлам, т.е. с помощью команды django-admin makemessages. С единственной разницей в том, что надо указать домен djangojs, добавив параметр -d djangojs, вот так:
```
django-admin makemessages -d djangojs -l de
```
Этот пример создаёт или обновляет файл сообщений для JavaScript для немецкого языка. После обновления файлов сообщений просто выполните django-admin compilemessages, как вы это делаете для обычных файлов сообщений.

gettext на Windows
------------------
Эта информация нужна только тем, кому надо создавать/обновлять файлы сообщений или компилировать их (.po). Сам процесс перевода заключается в редактировании существующих файлов данного типа. Однако, если вам надо создавать свои собственные файлы сообщений, надо проверить или скомпилировать изменённый файл сообщений, тогда вам потребуются утилиты gettext:

Скачайте следующие архивы с серверов GNOME https://download.gnome.org/binaries/win32/dependencies/
```
gettext-runtime-X.zip
gettext-tools-X.zip
```
X является версией, мы требуем версию 0.15 или выше.

Извлеките содержимое каталогов bin\ обоих архивов в такой же каталог на вашей системе (т.е. C:\Program Files\gettext-utils).

Обновите системный PATH:
```
Control Panel > System > Advanced > Environment Variables.
```
В списке System variables, выберите Path, затем Edit.

Добавьте 
```
;C:\Program Files\gettext-utils\bin в конец поля Variable value.
```
Вы также можете использовать бинарники gettext, взятые где-то, если команда xgettext --version работает правильно. Не пытайтесь выполнять команды Django, использующие пакет gettext, если команда xgettext --version, введённая в консоли Windows, выбрасывает окно с текстом “xgettext.exe has generated errors and will be closed by Windows”.

Настройка команды makemessages
-------------------------------
Если вам требуется передать дополнительные параметры в xgettext, вам следует создать свою команду makemessages и переопределить её атрибут xgettext_options:
```
from django.core.management.commands import makemessages

class Command(makemessages.Command):
    xgettext_options = makemessages.Command.xgettext_options + ['--keyword=mytrans']
```
Если вам необходим больший контроль, вы также можете добавить новый аргумент в вашу реализацию команды makemessages:
```
from django.core.management.commands import makemessages

class Command(makemessages.Command):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--extra-keyword', dest='xgettext_keywords',
                            action='append')

    def handle(self, *args, **options):
        xgettext_keywords = options.pop('xgettext_keywords')
        if xgettext_keywords:
            self.xgettext_options = (
                makemessages.Command.xgettext_options[:] +
                ['--keyword=%s' % kwd for kwd in xgettext_keywords]
            )
        super(Command, self).handle(*args, **options)
```

Перенаправляющее представление set_language
-------------------------------------------
set_language(request)
---------------------
Для удобства Django поставляется с представлением django.views.i18n.set_language(), которое устанавливает язык для пользователя и перенаправляет его на указанный URL или, по умолчанию, обратно на ту же страницу.

Активируйте это представление, добавив следующую строку в конфигурацию URL:
```
url(r'^i18n/', include('django.conf.urls.i18n')),
```
(данный пример привязывает представление к /i18n/setlang/.)

Удостоверьтесь, что вы не подключили вышеприведённый URL внутрь i18n_patterns(), это представление не должно зависеть от текущего языка.
Представление должно вызываться через метод POST, в запросе должен быть установлен параметр language. При активированной поддержке сессий, представление сохраняет выбор пользователя в его сессии. Иначе выбранный язык сохраняется в cookie с именем по умолчанию django_language. (Имя может быть изменено через параметр конфигурации LANGUAGE_COOKIE_NAME.)

После сохранения выбора текущего языка Django перенаправляет пользователя, руководствуясь следующим алгоритмом:

- Django обращается к параметру next в словаре данных POST.

- Если такого ключа там нет или он пуст, Django ищет URL в заголовке Referrer.

- Если и там пусто, браузер пользователя не прислал такой заголовок, тогда перенаправление будет выполнено на корень сайта (/).

Приведём пример HTML кода шаблона:
```
{% load i18n %}
<form action="{% url 'set_language' %}" method="post">
{% csrf_token %}
<input name="next" type="hidden" value="{{ redirect_to }}" />
<select name="language">
{% get_current_language as LANGUAGE_CODE %}
{% get_available_languages as LANGUAGES %}
{% get_language_info_list for LANGUAGES as languages %}
{% for language in languages %}
<option value="{{ language.code }}"{% if language.code == LANGUAGE_CODE %} selected="selected"{% endif %}>
    {{ language.name_local }} ({{ language.code }})
</option>
{% endfor %}
</select>
<input type="submit" value="Go" />
</form>
```
В этом примере Django ищет URL страницы, на которую будет перенаправлен пользователь, в контекстной переменной redirect_to.

Явное указание активного языка
------------------------------
Вам может потребоваться явно указать активный язык для текущей сессии. Например, возможно, что информация об языке, предпочитаемым пользователем, будет извлекаться из другой системы. Вы уже встречались с функцией django.utils.translation.activate(). Она влияет только на текущий поток. Для указания языка для всей сессии надо модифицировать LANGUAGE_SESSION_KEY:
```
from django.utils import translation
user_language = 'fr'
translation.activate(user_language)
request.session[translation.LANGUAGE_SESSION_KEY] = user_language
```
Вам обычно потребуется использовать оба подхода: вызывать django.utils.translation.activate() для изменения языка внутри потока и изменять сессию для влияния на последующие запросы.

Если вы не используете сессии, то активный язык будет сохранён в куке, имя которой определяется с помощью LANGUAGE_COOKIE_NAME. Например:
```
from django.utils import translation
from django import http
from django.conf import settings
user_language = 'fr'
translation.activate(user_language)
response = http.HttpResponse(...)
response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
```
Использование перевода вне представлений и шаблонов
------------------------------------------------------
Несмотря на то, что Django предоставляет богатый набор инструментов интернационализации представлений и шаблонов, она не ограничивает их использование в другом коде. Механизмы перевода Django могут быть использованы для перевода отдельных текстов на любой из языков, поддерживаемых Django (т.е. соответствующий каталог с переводами есть в наличии). Вы можете загрузить каталог переводов, активировать его и переводить текст на нужный язык, но не забудьте вернуться на оригинальный язык, так как активация каталога переводов выполняется на уровне потока и такое изменение будет влиять на код, работающий в том же потоке.

Например:
```
from django.utils import translation
def welcome_translated(language):
    cur_language = translation.get_language()
    try:
        translation.activate(language)
        text = translation.ugettext('welcome')
    finally:
        translation.activate(cur_language)
    return text
```
Вызов этой функции с параметром ‘de’ вернёт "Willkommen", независимо от значения параметра конфигурации LANGUAGE_CODE и языка, установленного через мидлварь.

Вас могут заинтересовать функции django.utils.translation.get_language(), которая возвращает язык, используемый в текущем потоке, django.utils.translation.activate(), которая активирует каталог переводов для текущего потока, и django.utils.translation.check_for_language(), которая проверяет, поддерживается ли данный язык Django.

Кука для языка
----------------
Ряд настроек может быть использован для управления опциями куки языка:
```
LANGUAGE_COOKIE_NAME
Добавлено в Django 1.7.
LANGUAGE_COOKIE_AGE
LANGUAGE_COOKIE_DOMAIN
LANGUAGE_COOKIE_PATH
```

Особенности перевода Django
---------------------------
Механизм перевода Django использует стандартный модуль gettext, идущей в поставке Python. Если вы знакомы с gettext, вам может быть интересен подход Django к его использованию:

Строковый домен может быть django или djangojs. Он используется для идентификации ресурсов множества приложений, которые хранятся в общей библиотеке(обычно /usr/share/locale/). Домен django используется для перевода текстовых ресурсов Python кода и шаблонов, загружается в общие каталоги перевода. Домен djangojs используется только для каталогов с текстовыми ресурсами для JavaScript, чтобы сделать их мелкими, насколько это возможно.

Django не использует только xgettext. Она использует Python-обёртки для xgettext и msgfmt. Так сделано для удобства.

Как Django определяет языковую настройку
----------------------------------------
После подготовки своего перевода, или если вы желаете использовать перевод, поставляемый с Django, надо просто активировать перевод для своего приложения.

Django обладает очень гибкой моделью принятия решения о том, какой язык следует использовать: на уровне проекта, для отдельного пользователя или в обоих случаях.

Глобально язык определяется через параметр конфигурации LANGUAGE_CODE. Django использует указанный язык в качестве основного и обращается к нему, если больше никакой не найден мидлваром локализации.

Если вам просто нужно запустить проект на определенном языке, укажите его в LANGUAGE_CODE и убедитесь, что существует необходимый файл перевода и его скомпилированная версия (.mo).

Если вам надо позволить отдельным пользователям указывать предпочитаемый язык, используйте LocaleMiddleware. LocaleMiddleware обеспечивает выбор языка по данным из запроса. Эта мидлварь настраивает контент под каждого пользователя.

Чтобы использовать LocaleMiddleware, добавьте 'django.middleware.locale.LocaleMiddleware' в настройку MIDDLEWARE_CLASSES. Так как порядок middleware важен, используйте следующую инструкцию:

- Удостоверьтесь, что она указана одной из первых мидлварей.

- Она должна идти после SessionMiddleware, так как LocaleMiddleware использует сессию. И она должна идти до CommonMiddleware, так как CommonMiddleware нуждается в активном языке для определения запрошенного URL.

- Если вы используете CacheMiddleware, поместите LocaleMiddleware после неё.

Например, ваш MIDDLEWARE_CLASSES может выглядеть так:
```
MIDDLEWARE_CLASSES = (
   'django.contrib.sessions.middleware.SessionMiddleware',
   'django.middleware.locale.LocaleMiddleware',
   'django.middleware.common.CommonMiddleware',
)
```

LocaleMiddleware пытается определить язык пользователя, используя следующий алгоритм:

- Сначала, проверяется наличие префикса в запрошенном URL. Эта проверка выполняется только если вы используете функцию i18n_patterns в корневом URLconf. Обратитесь к Интернационализация: в шаблонах URL для получения подробностей по языковым префиксам и интернационализации шаблонов URL.

- Если с префиксом не получилось, то проверяется ключ LANGUAGE_SESSION_KEY сессии текущего пользователя.

- Если и с сессией не сложилось, то принимается за cookie.

Имя cookie определяется параметром конфигурации LANGUAGE_COOKIE_NAME. (Название про умолчанию django_language.)

Если опять не повезло, то заглядывает в HTTP заголовок Accept-Language. Этот заголовок отправляется браузером, чтобы указать серверу, какой язык вы предпочитаете, в порядке приоритета. Django проверяет наличие поддержки каждого языка из заголовка.

Если совсем всё плохо, тогда используется значение параметра конфигурации LANGUAGE_CODE.

Везде подразумевается, что значение языка указано в стандартном формате, в виде строки. Например, для бразильского варианта португальского языка это будет pt-br.

Если базовый язык доступен, а вариант нет, то Django будет использовать базовый язык. Например, если пользователь указал de-at (австрийский вариант немецкого), но у Django есть только de, то именно он и будет использоваться.

Выбор может производиться только из списка, определенного параметром конфигурации LANGUAGES. Если вам надо ограничить диапазон имеющихся языков (потому что ваше приложение не имеет столько переводов), укажите в LANGUAGES список поддерживаемых языков. Например:
```
LANGUAGES = (
  ('de', _('German')),
  ('en', _('English')),
)
```
Данный пример ограничивает число доступных для автоматического выбора языков немецким и английским языками (и любыми диалектами, например, de-ch или en-us).

Если вы определяете параметр конфигурации LANGUAGES, как было показано выше, вы можете помечать имена языков как переводимые. Но следует использовать ugettext_lazy() вместо ugettext(), чтобы исключить циклический импорт.

Приведёт пример файла настроек:
```
from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('de', _('German')),
    ('en', _('English')),
)
```
После того, как LocaleMiddleware определяет предпочитаемый язык, она делает его доступным через request.LANGUAGE_CODE для каждого запроса HttpRequest. Вы можете спокойно его использовать в коде своих представлений. Вот простой пример:
```
from django.http import HttpResponse

def hello_world(request, count):
    if request.LANGUAGE_CODE == 'de-at':
        return HttpResponse("You prefer to read Austrian German.")
    else:
        return HttpResponse("You prefer to read another language.")
```
Следует отметить, что для статичного перевода (без мидлвари) язык надо брать из settings.LANGUAGE_CODE, а для динамичного перевода (с мидлварью) — из request.LANGUAGE_CODE.

Как Django находит переводы
---------------------------
Во время своей работы Django создаёт в памяти унифицированный каталог с переводами. Для этого он использует следующий алгоритм, учитывая порядок нахождения путей для загрузки файлов сообщений (.mo) и приоритет множества перевода для одного слова:

- Каталоги, указанные в LOCALE_PATHS, имеют повышенный приоритет, список представлен по убыванию приоритета.

- Затем происходит поиск каталога locale в каждом установленном приложении, указанном в INSTALLED_APPS. Тут тоже приоритет идёт по убыванию.

- Наконец, используется базовый перевод Django из django/conf/locale.

Имя каталога, содержащего перевод, должно быть названо в соответствии соглашению по наименованию локалей. Т.е. de, pt_BR, es_AR и так далее.

Таким образом, вы можете создавать приложения, которые содержат свои собственные переводы и вы можете изменять базовые переводы в вашем проекте. Или вы можете создать большой проект из нескольких приложений, объединив всё их переводы в единый ресурс.

Все репозитории с файлами сообщений имеют одинаковую структуру:

Во всех указанных путях в параметре конфигурации LOCALE_PATHS происходит поиск language/LC_MESSAGES/django.(po|mo)
```
$APPPATH/locale/<language>/LC_MESSAGES/django.(po|mo)
$PYTHONPATH/django/conf/locale/<language>/LC_MESSAGES/django.(po|mo)
```
Для создания файлов сообщений надо использовать django-admin makemessages. Для компиляции файлов перевода надо использовать django-admin compilemessages, это приведёт к созданию бинарных .mo файлов, которые нужны для работы gettext.

Перечислив в параметре конфигурации LOCALE_PATHS список обрабатываемых каталогов, его можно передать компилятору: django-admin compilemessages --settings=path.to.settings.


mkdir mysite/locale

settings/base.py

```
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
########## END GENERAL CONFIGURATION


########## TEMPLATE CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/templates/
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            normpath(join(PROJECT_ROOT, 'templates')),
            normpath(join(PROJECT_ROOT, 'extensions')),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'string_if_invalid': 'NULL',
        },
    },
]
########## END TEMPLATE CONFIGURATION

########## MIDDLEWARE CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

########## GENERAL CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Europe/Kiev'

from django.utils.translation import ugettext_lazy as _
LANGUAGES = (
    ('en', _('English')),
    ('uk', _('Ukraine')),
    ('ru', _('Russian')),
)


LOCALE_PATHS = (
    normpath(join(PROJECT_ROOT, 'locale')),
    # os.path.join(BASE_DIR, 'locale'),
)
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

```

Home page:
```
mysite.com/en
mysite.com/uk

```

urls.py file:
-------------
```
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.views.generic.base import RedirectView, TemplateView

urlpatterns = [
    # Root-level redirects for common browser requests
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'img/compressed/favicon.ico'), name='favicon.ico'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots.txt'),
]

urlpatterns += i18n_patterns(
    # Core URLs
    url(r'^', include('core.urls', namespace='core')),

    # Accounts URLs
    # https://github.com/fusionbox/django-authtools/blob/master/authtools/urls.py
    url(r'^', include('extensions.authtools.urls')),
    url(r'^redactor/', include('redactor.urls')),

    
    # Admin URLs
    url(r'^admin/rq/', include('extensions.django_rq.urls')),
    url(r'^admin/rq/scheduler/', include('extensions.rq_scheduler.urls', namespace='rq_scheduler')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

admin.site.site_header = '%s Headquarters' % settings.PROJECT_NAME
admin.site.index_title = 'Base of Operations'

if settings.DEBUG:
    urlpatterns += [
        # Testing 404 and 500 error pages
        url(r'^404/$', TemplateView.as_view(template_name='404.html'), name='404'),
        url(r'^500/$', TemplateView.as_view(template_name='500.html'), name='500'),
    ]

    try:
        from django.conf.urls.static import static
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

        import debug_toolbar
        urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]

    # Should only occur when debug mode is on for production testing
    except ImportError as e:
        import logging
        l = logging.getLogger(__name__)
        l.warning(e)
```

Internationalization – Translation
-----------------------------------

```
foreman run django-admin.py makemessages -l uk

$ python manage.py makemessages -l uk
```


GNU gettext 
===========

installed (if you don’t get the error, good for you! skip this installation part then!). Go to the 
GNU gettext home page
---------------------
https://www.gnu.org/software/gettext/

```
$ ./configure

$ make

$ make check

$ make install
```

djamgo.po
```
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2015-11-19 15:27+0200\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"Language: \n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n"
"%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);\n"

#: mysite/apps/user_profile/models.py:15
msgid "user"
msgstr "користувач"

#: mysite/apps/user_profile/models.py:20
msgid "interaction"
msgstr "взаємодія"

#: mysite/apps/user_profile/models.py:30
msgid "Profile Pic"
msgstr "Світлина профілю"

#: mysite/apps/user_profile/models.py:38
msgid "Profile"
msgstr "Профіль"

#: mysite/apps/user_profile/models.py:39
msgid "Profiles"
msgstr "Профілі"

#: mysite/config/settings/base.py:154
msgid "English"
msgstr "Англійська"

#: mysite/config/settings/base.py:155
msgid "Ukraine"
msgstr "Українська"

#: mysite/config/settings/base.py:156
msgid "Russian"
msgstr "Російська"

#: mysite/templates/accounts/login.html:4
#: mysite/templates/accounts/login.html:8
#: mysite/templates/accounts/login.html:14
msgid "Log In"
msgstr "Увійти"

#: mysite/templates/accounts/login.html:13
msgid "Forgot Password?"
msgstr "Забули пароль?"

#: mysite/templates/accounts/logout.html:4
msgid "Log Out"
msgstr "Вийти"

#: mysite/templates/accounts/logout.html:7
msgid "Logged Out"
msgstr ""

#: mysite/templates/accounts/password_change.html:4
#: mysite/templates/accounts/password_change.html:7
msgid "Password Change"
msgstr ""

#: mysite/templates/accounts/password_change.html:9
msgid ""
"Please enter your old password, for security's sake, and then enter your new "
"password twice so we can verify you typed it in correctly."
msgstr ""

#: mysite/templates/accounts/password_change.html:16
msgid "cancel"
msgstr ""

#: mysite/templates/accounts/password_change.html:17
msgid "Change my password"
msgstr ""

#: mysite/templates/accounts/password_change_done.html:4
#: mysite/templates/accounts/password_change_done.html:7
msgid "Password Change Successful"
msgstr ""

#: mysite/templates/accounts/password_change_done.html:9
msgid "Your password was changed."
msgstr ""

#: mysite/templates/accounts/password_change_done.html:9
msgid "Back to homepage"
msgstr ""

#: mysite/templates/accounts/password_reset.html:4
#: mysite/templates/accounts/password_reset.html:7
#: mysite/templates/accounts/password_reset_confirm.html:4
msgid "Password Reset"
msgstr ""

#: mysite/templates/accounts/password_reset.html:9
msgid ""
"Forgotten your password? Enter your e-mail address below, and we'll e-mail "
"instructions for setting a new one."
msgstr ""

#: mysite/templates/accounts/password_reset.html:14
msgid "Password reset"
msgstr ""

#: mysite/templates/accounts/password_reset_complete.html:4
#: mysite/templates/accounts/password_reset_complete.html:7
msgid "Password Reset Complete"
msgstr ""

#: mysite/templates/accounts/password_reset_complete.html:9
msgid "Your password has been set. You may go ahead and log in now."
msgstr ""

#: mysite/templates/accounts/password_reset_complete.html:11
msgid "Log in"
msgstr ""

#: mysite/templates/accounts/password_reset_confirm.html:9
msgid "Enter New Password"
msgstr ""

#: mysite/templates/accounts/password_reset_confirm.html:10
msgid ""
"Please enter your new password twice so we can verify you typed it in "
"correctly."
msgstr ""

#: mysite/templates/accounts/password_reset_confirm.html:15
msgid "Change My Password"
msgstr ""

#: mysite/templates/accounts/password_reset_confirm.html:18
msgid "Password Reset Unsuccessful"
msgstr ""

#: mysite/templates/accounts/password_reset_confirm.html:19
msgid ""
"The password reset link was invalid, possibly because it has already been "
"used.  Please request a new password reset."
msgstr ""

#: mysite/templates/accounts/password_reset_done.html:4
#: mysite/templates/accounts/password_reset_done.html:7
msgid "Password Reset Successful"
msgstr ""

#: mysite/templates/accounts/password_reset_done.html:9
msgid ""
"We've e-mailed you instructions for setting your password to the e-mail "
"address you submitted. You should be receiving it shortly."
msgstr ""

#: mysite/templates/accounts/password_reset_email.html:3
#, python-format
msgid ""
"You're receiving this email because you requested a password reset for your "
"user account at %(site_name)s."
msgstr ""

#: mysite/templates/accounts/password_reset_email.html:5
msgid "Please go to the following page and choose a new password:"
msgstr ""

#: mysite/templates/accounts/password_reset_email.html:9
msgid "Your email, in case you've forgotten:"
msgstr ""

#: mysite/templates/accounts/password_reset_email.html:11
#, python-format
msgid "Thanks for using %(site_name)s!"
msgstr ""

#: mysite/templates/accounts/password_reset_email.html:13
#, python-format
msgid "The %(site_name)s team"
msgstr ""

#: mysite/templates/accounts/password_reset_subject.txt:1
msgid "Password Reset On"
msgstr ""

```
compilemessages
---------------
```
foreman run django-admin.py compilemessages -l uk

python manage.py compilemessages -l uk
```

Localization
=============

base.py
-------
```
USE_L10N = True
```

template index.html:
--------------------
```
{% load l10n %}


{{var}}
{{var|unlocalize}}

{% localize off %} code without localization {% endlocalize %}
```

