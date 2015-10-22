from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    description = models.TextField(max_length=4096)
        
    views_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    views_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
        
    status = models.IntegerField(default=0)
    enable_comment = models.BooleanField(default=True)
    content = models.TextField()

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
        
    publish_date = models.DateTimeField(auto_now=True)

    created_date = models.DateTimeField(auto_now_add=True)
        
    views_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title