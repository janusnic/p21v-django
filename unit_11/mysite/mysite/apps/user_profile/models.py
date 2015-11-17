# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver
from django.db.models.signals import post_save
 
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
        return self.user.email
        
 
    homepage = models.URLField(blank=True)
    avatar =   models.ImageField(_("Profile Pic"), upload_to="images/", blank=True, null=True)
    # Methods
    def avatar_image(self):
        return (settings.MEDIA_URL + self.avatar.name) if self.avatar else None

 
    # Meta and String
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("user",)
 
    def __str__(self):
        return self.user.email
        

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()