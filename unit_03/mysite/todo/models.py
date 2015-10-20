from django.db import models

# Create your models here.
# class Item(object):
class Item(models.Model):
    # pass
    text = models.TextField()