## p21v-django unit 14
Модель Comments
===============

foreman run django-admin.py startapp comments mysite/apps/comments

## Модель Comment
```
class Comment(models.Model):
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'))

    article = models.ForeignKey(Article, verbose_name=_('Article'))
    comment = models.TextField(verbose_name=_('Comment'))

    def __unicode__(self):
        return unicode("%s: %s" % (self.article, self.comment[:60]))

```

verbose_name
-------------
Options.verbose_name
Читабельное название модели, в единственном числе:

verbose_name = "Comment"

Если не указано, Django создаст из названия модели: CamelCase станет camel case.

verbose_name_plural
-------------------
Options.verbose_name_plural
Название модели в множественном числе:

verbose_name_plural = "stories"

Если не указано, Django создаст по правилу verbose_name + "s".


Создаем миграции
----------------

```
foreman run django-admin.py makemigrations blog


foreman run django-admin.py migrate

```
Создаем форму
--------------

```
from django import forms

from .models import Comment


class CommentForm(forms.ModelForm): 
    class Meta: 
        model = Comment 
        exclude = ["article"]
```
Редактируем админку
-------------------
```
from django.contrib import admin
from .models import Comment 

class CommentAdmin(admin.ModelAdmin):
    list_display = ["article", "user", "created"]

admin.site.register(Comment, CommentAdmin)

```

Добавляем метод во views.py
---------------------------

```
from .models import Entry, Category, Comment

from blog.forms import CommentForm

from django.http import HttpResponseRedirect


def add_comment(request, postslug):
    """Add a new comment."""
    print ('Test user')
    p = request.POST
    if p["comment"]:
        user = request.user
       
        comment = Comment(article=Article.objects.get(slug=postslug))
        cf = CommentForm(p, instance=comment)

        cf.fields["user"].required = False
        comment = cf.save(commit=False)
        comment.user = user
        comment.save()
    
    return_path  = request.META.get('HTTP_REFERER','/')
    return redirect(return_path)


```
## Изменяем метод 
```
from django.shortcuts import render, render_to_response
from .models import Entry, Category, Comment

from blog.forms import CommentForm

from django.http import HttpResponseRedirect

from django.core.paginator import Paginator, InvalidPage, EmptyPage

def index(request):
    # result = Entry.objects.all()
    posts_list = Entry.objects.order_by('-pub_date')
    paginator = Paginator(posts_list, 2)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts_list = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts_list = paginator.page(paginator.num_pages)
    
    category_list = Category.objects.order_by('name')
        
    result = {'categories_list':category_list, 'posts_list':posts_list }

    return render(request,'blog/index.html',result)

    

def view(request, postslug):
    # result =get_object_or_404(Article,slug=postslug)
    result = Article.objects.get(slug=postslug)

    comments = Comment.objects.filter(article=result)
    
    paginator = Paginator(comments, 2)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        comments = paginator.page(page)
    except (InvalidPage, EmptyPage):
        comments = paginator.page(paginator.num_pages)

    context = {'result': result, "comments":comments,"form":CommentForm(), "user":request.user}
    return render(request,'blog/view.html', context)

```

## Создаем маршрут
blog/urls.py
```
urlpatterns = [
    
    # ex: /blog/
    url(r'^$', views.index, name='index'),
    
    url(r'^article/(?P<postslug>.*)/$', views.view, name='view' ),
    
    url(r"^add_comment/(?P<postslug>.*)/$", views.add_comment, name='add_comment'),
    # url(r"^add_comment/(?P<blog_id>[0-9]+)/$", views.add_comment, name='addcomment'),
    # ex: /blog/5/
    url(r'^(?P<blog_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /blog/5/results/
    url(r'^(?P<blog_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /blog/5/vote/
    url(r'^(?P<blog_id>[0-9]+)/vote/$', views.vote, name='vote'),
]

```

## Изменяем представление
templates/blog/index.html
--------------------------
```
{% extends "base.html" %} 
{% load staticfiles %}
{% block title %} {{ block.super }} - SECTION NAME {% endblock %}

{% block content %} 

<h2>Blog Index page</h2>
        

        {% if user.is_authenticated %}
        <h1>Blog says... hello {{ user.name }}!</h1>
        {% else %}
        <h1>Blog says... hello world!</h1>
        <a href="/myauth/login/">Login</a>
        {% endif %}

        {% if categories_list %}       
            <ul>
                {% for category in categories_list %}
                <li>{{ category.name }}</li>
                {% endfor %}
            </ul>
         

        {% else %}
            <strong>There are no categories present.</strong>
        {% endif %}

    {% if posts_list %}
      {% for article in posts_list %} 
        <div> 
            
            <h2><a href="/blog/article/{{ article.slug }}/"> 
                {{ article.title }} 
            </a></h2> 
                <span>{{ article.publish_date|date:"SHORT_DATE_FORMAT" }}   
                </span>
        </div> 


      {% endfor %}
       <!-- Next/Prev page links  --> 
      {% if posts_list.object_list and posts_list.paginator.num_pages > 1 %} 
        <div class="pagination" style="margin-top: 20px; margin-left: -20px; "> 
            <span class="step-links"> 
                {% if posts_list.has_previous %} 
                    <a href= "?page={{ posts_list.previous_page_number }}">newer entries &lt;&lt; </a> 
                {% endif %} 

                <span class="current"> 
                    &nbsp;Page {{ posts_list.number }} of {{ posts_list.paginator.num_pages }} 
                </span> 

                {% if posts_list.has_next %} 
                    <a href="?page={{ posts_list.next_page_number }}"> &gt;&gt; older entries</a> 
                {% endif %} 
            </span> 
        </div> 
       {% endif %}
    {% else %}
            <strong>There are no posts present.</strong>
    {% endif %}


{% endblock %}

```
templates/blog/view.html
------------------------
```
{% extends "base.html" %}
{% block content %}
        <div id="singlepost">
                <p>{{ result.title }}</p>
                <span>{{ result.publish_date|date:"SHORT_DATE_FORMAT" }} 
                </span>
                <p>
                {% autoescape off %}
                {{ result.content }} 
                {% endautoescape %}

                </p>
                        <!-- Comments  --> 
                  {% if comments %} 
                      <p>Comments: {{ comments|length }} </p> 
                  {% endif %} 

                  {% for comment in comments %} 
                      <div class="comment"> 
                          <div class="time">{{ comment.created }} | {{ comment.user }}</div> 
                          <div class="body">{{ comment.comment|linebreaks }}</div> 
                      </div> 
                  {% endfor %}

                    <!-- Next/Prev page links  --> 
      {% if comments.object_list and comments.paginator.num_pages > 1 %} 
        <div class="pagination" style="margin-top: 20px; margin-left: -20px; "> 
            <span class="step-links"> 
                {% if comments.has_previous %} 
                    <a href= "?page={{ comments.previous_page_number }}">newer entries &lt;&lt; </a> 
                {% endif %} 

                <span class="current"> 
                    &nbsp;Page {{ comments.number }} of {{ comments.paginator.num_pages }} 
                </span> 

                {% if comments.has_next %} 
                    <a href="?page={{ comments.next_page_number }}"> &gt;&gt; older entries</a> 
                {% endif %} 
            </span> 
        </div> 
       {% endif %}


                  {% if user.is_authenticated %} 
                  <div id="addc">Add a comment</div> 
                  <!-- Comment form  --> 
                      <form action="/blog/add_comment/{{ result.slug }}/" method="POST">{% csrf_token %} <!-- защита против CSRF атак -->
                          <div id="cform"> 
                  
                              <p>{{ form.comment|linebreaks }}</p> 
                          </div> 
                          <div id="submit"><input type="submit" value="Submit"></div> 
                      </form> 
                      {% endif %}       
                  </div>

        </div>
{% endblock %}
```

## Счираем коментарии
```
           <!-- Comments  --> 
                  {% if comments %} 
                      <p>Comments: {{ comments|length }} </p> 
                  {% endif %} 

```

## Постраничное листание публикаций
Изменяем метод
```
from django.core.paginator import Paginator, InvalidPage, EmptyPage



def index(request):
    # result = Entry.objects.all()
    posts_list = Entry.objects.order_by('-pub_date')
    paginator = Paginator(posts_list, 2)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts_list = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts_list = paginator.page(paginator.num_pages)
    
    category_list = Category.objects.order_by('name')
        
    result = {'categories_list':category_list, 'posts_list':posts_list }

    return render(request,'blog/index.html',result)

```
## Изменяем представление
index.html
```
<!-- Next/Prev page links  --> 
      {% if posts_list.object_list and posts_list.paginator.num_pages > 1 %} 
        <div class="pagination" style="margin-top: 20px; margin-left: -20px; "> 
            <span class="step-links"> 
                {% if posts_list.has_previous %} 
                    <a href= "?page={{ posts_list.previous_page_number }}">newer entries &lt;&lt; </a> 
                {% endif %} 

                <span class="current"> 
                    &nbsp;Page {{ posts_list.number }} of {{ posts_list.paginator.num_pages }} 
                </span> 

                {% if posts_list.has_next %} 
                    <a href="?page={{ posts_list.next_page_number }}"> &gt;&gt; older entries</a> 
                {% endif %} 
            </span> 
        </div> 
       {% endif %}
```


## Постраничное листание коментариев
```
def view(request, postslug):
    result = Entry.objects.get(slug=postslug)

    comments = Comment.objects.filter(post=result)

    paginator = Paginator(comments, 2)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        comments = paginator.page(page)
    except (InvalidPage, EmptyPage):
        comments = paginator.page(paginator.num_pages)

        

    context = {'result': result, "comments":comments,"form":CommentForm(), "user":request.user}
    return render(request,'blog/view.html', context)


```
## Представление 
```
                       <!-- Comments  --> 
                  {% if comments %} 
                      <p>Comments: {{ comments|length }} </p> 
                  {% endif %} 

                  {% for comment in comments %} 
                      <div class="comment"> 
                          <div class="time">{{ comment.created }} | {{ comment.author }}</div> 
                          <div class="body">{{ comment.body|linebreaks }}</div> 
                      </div> 
                  {% endfor %}

                    <!-- Next/Prev page links  --> 
      {% if comments.object_list and comments.paginator.num_pages > 1 %} 
        <div class="pagination" style="margin-top: 20px; margin-left: -20px; "> 
            <span class="step-links"> 
                {% if comments.has_previous %} 
                    <a href= "?page={{ comments.previous_page_number }}">newer entries &lt;&lt; </a> 
                {% endif %} 

                <span class="current"> 
                    &nbsp;Page {{ comments.number }} of {{ comments.paginator.num_pages }} 
                </span> 

                {% if comments.has_next %} 
                    <a href="?page={{ comments.next_page_number }}"> &gt;&gt; older entries</a> 
                {% endif %} 
            </span> 
        </div> 
       {% endif %}
```