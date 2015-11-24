from django.conf.urls import include, url

urlpatterns = [
    
    url(r'^register/$', 'apps.accounts.views.register', name='register'),
    url(r'^loginuser/$', 'apps.accounts.views.user_login', name='loginuser'),
    url(r'^restricted/', 'apps.accounts.views.restricted', name='restricted'),
    url(r'^logoutuser/$', 'apps.accounts.views.user_logout', name='logoutuser'),
    url(r'^profile/$', 'apps.accounts.views.profile', name='profile'),

]