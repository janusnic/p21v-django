# from django.shortcuts import render

# Create your views here.
from .models import Article
from django.http import HttpResponse
from django.template import RequestContext, loader

from django.shortcuts import get_object_or_404, render

def index0(request):
    return HttpResponse("Hello, world. You're at the blog index.")

def index1(request):
    latest_blog_list = Article.objects.order_by('-publish_date')[:5]
    output = ', '.join([p.title for p in latest_blog_list])
    return HttpResponse(output)

def index2(request):
    latest_blog_list = Article.objects.order_by('-publish_date')[:15]
    template = loader.get_template('blog/index.html')
    context = RequestContext(request, {
        'latest_blog_list': latest_blog_list,
    })
    return HttpResponse(template.render(context))

def index(request):
    latest_blog_list = Article.objects.order_by('-publish_date')[:10]
    context = {'latest_blog_list': latest_blog_list}
    return render(request, 'blog/index.html', context)

def detail0(request, blog_id):
    return HttpResponse("You're looking at article %s." % blog_id)

def detail1(request, blog_id):
    try:
        item = Article.objects.get(pk=blog_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    return render(request, 'blog/detail.html', {'item': item})

def detail(request, blog_id):
    item = get_object_or_404(Article, pk=blog_id)
    return render(request, 'blog/detail.html', {'item': item})

def results(request, blog_id):
    response = "You're looking at the results of article %s."
    return HttpResponse(response % blog_id)

def vote(request, blog_id):
    return HttpResponse("You're voting on article %s." % blog_id)
