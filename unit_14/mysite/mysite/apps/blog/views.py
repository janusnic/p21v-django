from .models import Article, Category, Comment

from .forms import CommentForm

from django.http import HttpResponse, HttpResponseRedirect

from django.template import RequestContext, loader

from django.shortcuts import get_object_or_404, render, redirect

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse

def index(request):
    posts_list = Article.objects.order_by('-publish_date')

    paginator = Paginator(posts_list, 2)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts_list = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts_list = paginator.page(paginator.num_pages)
    
    category_list = Category.objects.order_by('name')
        
    context = {'categories_list':category_list, 'posts_list':posts_list }

    return render(request, 'blog/index.html', context)

def index1(request):
    latest_blog_list = Article.objects.order_by('-publish_date')[:10]
    
    context = {'latest_blog_list': latest_blog_list}
    return render(request, 'blog/index1.html', context)


def detail(request, blog_id):
    item = get_object_or_404(Article, pk=blog_id)
    return render(request, 'blog/detail.html', {'item': item})

def results(request, blog_id):
    response = "You're looking at the results of article %s."
    return HttpResponse(response % blog_id)

def vote(request, blog_id):
    return HttpResponse("You're voting on article %s." % blog_id)

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

