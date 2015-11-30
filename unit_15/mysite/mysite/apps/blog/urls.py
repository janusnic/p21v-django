from django.conf.urls import url

from . import views

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
