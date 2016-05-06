from django.db import models
import datetime
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
    description = models.TextField(max_length=4096)

    def __str__(self):
        return '%s' % (self.name)

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')

    def __str__(self):
        return '%s' % (self.name)

@python_2_unicode_compatible
class Article(models.Model):
    ARTICLE_STATUS = (
        ('D', 'Not Reviewed'),
        ('P', 'Published'),
        ('E', 'Expired'),
    )
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
    status = models.IntegerField(default=0)
    content = models.TextField()
    status = models.CharField(max_length=1, choices=ARTICLE_STATUS, default='D')
    category = models.ForeignKey(Category, verbose_name="the related category")
    tags = models.ManyToManyField(Tag, verbose_name="the related tags", blank=True)
        
    publish_date = models.DateTimeField(auto_now=True, editable=False, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    def was_published_recently(self):
        return self.publish_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'publish_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return '%s' % (self.title)

@python_2_unicode_compatible
class Comment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    path = models.IntegerField(blank=True, default=0) #Can't be null as using append to path for replies and can't append to a None path
    depth = models.PositiveSmallIntegerField(default=0)
    user = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    article = models.ForeignKey('Article', blank=True, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='child')
    spam = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.content