from django.db import models as models
import datetime
from django.utils import timezone
# from tinymce.models import HTMLField
from django.core.urlresolvers import reverse

from django_extensions.db import fields as extension_fields


class Category(models.Model):

    # Fields
    name = models.CharField(max_length=100, verbose_name='name')
    slug = extension_fields.AutoSlugField(populate_from='name', unique=True, verbose_name='slug')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    description = models.TextField(max_length=255)
    views_count = models.IntegerField(default=0, verbose_name='views count')


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('blog_category_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('blog_category_update', args=(self.slug,))

    def __str__(self):
        return self.name

class Tag(models.Model):

    # Fields
    name = models.CharField(max_length=100, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    views_count = models.IntegerField(default=0)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('blog_tag_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('blog_tag_update', args=(self.slug,))

    def __str__(self):
        return self.name


class Article(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    EXPIRED ='E'
    ARTICLE_STATUS = (
        (DRAFT, 'Not Reviewed'),
        (PUBLISHED, 'Published'),
        (EXPIRED, 'Expired'),
    )
    def was_published_recently(self):
        return self.publish_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'publish_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    # Fields
    title = models.CharField(max_length=255, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='title', unique=True, verbose_name='slug')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    publish_date = models.DateTimeField(auto_now=False, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    enable_comment = models.BooleanField(default=True)
    content = models.TextField()
    views_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    status = models.CharField(max_length=1, choices=ARTICLE_STATUS, default=DRAFT)

    # Relationship Fields
    category = models.ForeignKey('blog.Category',verbose_name="the related category")
    tags = models.ManyToManyField('blog.Tag',verbose_name="the related tags", blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('blog_article_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('blog_article_update', args=(self.slug,))
