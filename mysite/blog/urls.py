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
