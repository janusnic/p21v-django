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

def index(request):

    blog_list = Article.objects.order_by('-publish_date')
    category_list = Category.objects.order_by('name')
    tags_name = Tag.objects.order_by('name')

    context = {'categories_list':category_list, 'blog_list': blog_list , 'tags_name':tags_name, 'months':monthly_archive_list()}

    return render(request, 'blog/index.html', context)

def news(request):
    blog_list = Article.objects.filter(category__name='news')
    context = {'blog_list': blog_list}
    return render(request, 'blog/index.html', context)

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
            
    
    comment_tree = Comment.objects.select_related('user').filter(article=result.id, deleted=False, spam=False).order_by('path')

    
    return render(request, 'blog/detail.html', {'categories_list':category_list, 'item': result, 'tags_name':tags_name, 'months':monthly_archive_list(),'form':form,'comment_tree':comment_tree})

def category(request, categoryslug):
    name = Category.objects.get(slug=categoryslug)
    posts = Article.objects.filter(category=name)
    category_list = Category.objects.order_by('name')
    context = {'categories_list':category_list, 'blog_list': posts}
    return render(request, 'blog/singlecategory.html', context)

def tags(request):
    tags_name = Tag.objects.order_by('name')

    context = {'tags_name':tags_name}
    return render(request, 'blog/singlecategory.html', context)

def monthly_archive_list():
    """Make a list of months to show archive links."""

    if not Article.objects.count(): return []

    # set up vars
    year, month = time.localtime()[:2]
    first = Article.objects.order_by("created_date")[0]
    fyear = first.created_date.year
    fmonth = first.created_date.month
    months = []

    # loop over years and months
    for y in range(year, fyear-1, -1):
        start, end = 12, 0
        if y == year: start = month
        if y == fyear: end = fmonth-1

        for m in range(start, end, -1):
            months.append((y, m, month_name[m]))
    return months

def monthly_archive(request, year, month):
    """Monthly archive."""

    posts = Article.objects.filter(created_date__year=year, created_date__month=month)

    paginator = Paginator(posts, 2)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    return render(request,"blog/month_archive.html",dict(blog_list=posts, months=monthly_archive_list(), archive=True))


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