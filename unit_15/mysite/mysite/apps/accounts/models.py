from authtools.models import AbstractNamedUser
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver
from django.db.models.signals import post_save

class User(AbstractNamedUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        ordering = ('-date_joined',)

 
class Profile(models.Model):
    # Relations
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        related_name="profile",
        verbose_name=_("user")
        )
    # Attributes - Mandatory
    interaction = models.PositiveIntegerField(
        default=0,
        verbose_name=_("interaction")
        )

    # Custom Properties
    @property
    def username(self):
        return self.user.name   
 
    
    avatar =   models.ImageField(_("Profile Pic"), upload_to="images/", blank=True, null=True)
    biography = models.TextField(null=True, blank=True)
    homepage = models.URLField(null=True, blank=True)
    
    twitter = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    
    # Methods
    def avatar_image(self):
        return (settings.MEDIA_URL + self.avatar.name) if self.avatar else None

 
    # Meta and String
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("user",)
 
    def __str__(self):
        return self.user.name
        
class SocialInfo(models.Model):
    SOCIAL_CHOICES = (
    ('fa-facebook', 'Facebook'),
    ('fa-github', 'Github'),
    ('fa-twitter', 'Twitter'),
    ('fa-google-plus', 'Google Plus'),
    ('fa-weibo', 'Weibo'),)
    ('fa-bookmark', 'Other'),

    user = models.ForeignKey(User)
    social = models.CharField(choices=SOCIAL_CHOICES, max_length='128')
    url = models.URLField()

    def __str__(self):
        return user.name + '-' + social


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance=None, created=False, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()