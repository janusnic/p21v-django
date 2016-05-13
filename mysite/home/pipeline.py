# -*- coding: utf-8 -*-
from django.shortcuts import redirect

from social.pipeline.partial import partial
from userprofile.models import UserProfile

@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get('ajax') or user and user.email:
        return
    elif is_new and not details.get('email'):
        email = strategy.request_data().get('email')
        if email:
            details['email'] = email
        else:
            return redirect('require_email')




def get_profile_picture(backend, user, response, details, *args, **kwargs):
    url = None
    profile = UserProfile.objects.get_or_create(user = user)[0]
    if backend.name == 'facebook':
        profile.photo  = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
    elif backend.name == "twitter":
        if response['profile_image_url'] != '':
            if not response.get('default_profile_image'):
                avatar_url = response.get('profile_image_url_https')
                if avatar_url:
                    avatar_url = avatar_url.replace('_normal.', '_bigger.')
                    profile.photo = avatar_url
    elif backend.name == "google-oauth2":
        if response['image'].get('url') is not None:
            profile.photo  = response['image'].get('url')


    profile.save()
