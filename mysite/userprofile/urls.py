from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'), 
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),

]
