from django.conf.urls import url

from todo import views

urlpatterns = [
    url(r'^new$', views.new_todo, name='new_todo'),
    url(r'^(\d+)/$', views.view_todo, name='view_todo'),
    url(r'^(\d+)/add_item$', views.add_item, name='add_item'),
]

