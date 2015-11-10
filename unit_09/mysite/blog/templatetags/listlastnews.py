# -*- coding: UTF-8 -*-
from django import template
from blog.models import Article
register=template.Library()
 
@register.inclusion_tag('blog/lastnews.html') # регистрируем тег и подключаем шаблон lastnews
def lastnews():
    return {
		'last5news': Article.objects.filter(status='P')[:5],
	}
    