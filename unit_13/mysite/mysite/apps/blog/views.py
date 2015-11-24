from .models import Article
from django.http import HttpResponse
from django.template import RequestContext, loader

from django.shortcuts import get_object_or_404, render

def index(request):
    latest_blog_list = Article.objects.order_by('-publish_date')[:10]
    context = {'latest_blog_list': latest_blog_list}
    return render(request, 'blog/index.html', context)

def detail(request, blog_id):
    item = get_object_or_404(Article, pk=blog_id)
    return render(request, 'blog/detail.html', {'item': item})

def results(request, blog_id):
    response = "You're looking at the results of article %s."
    return HttpResponse(response % blog_id)

def vote(request, blog_id):
    return HttpResponse("You're voting on article %s." % blog_id)
