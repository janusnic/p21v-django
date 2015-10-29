# mysite/apps.py

from blog.apps import BlogConfig

class MysiteConfig(BlogConfig):
    verbose_name = "Janus Gypsy Project"
