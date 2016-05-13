from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
@python_2_unicode_compatible
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, related_name='profile')
    timezone = models.CharField(max_length=50, default='Europe/Kiev')
    photo = models.TextField(blank=True)

    # The additional attributes we wish to include.
    
    location = models.CharField(max_length=140, blank=True)  
    gender = models.CharField(max_length=140, blank=True)  
    age = models.IntegerField(blank=True,default=0)
    company = models.CharField(max_length=50, blank=True)
        
    website = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='thumbpath', blank=True)

    # Override the __str__() method to return out something meaningful!
    def __str__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)