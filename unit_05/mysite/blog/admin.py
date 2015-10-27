from django.contrib import admin

# Register your models here.
from .models import Category, Tag, Article

admin.site.register(Category)
admin.site.register(Tag)
# admin.site.register(Article)
# class ArticleAdmin(admin.ModelAdmin):
#    fields = ['title','category','content','created_date','publish_date','tags','status','enable_comment','views_count','comment_count']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status', 'was_published_recently')
    list_filter = ['publish_date']
    search_fields = ['title']
    fieldsets = [
        ('Item',             {'fields': ['title','category','content']}),
        ('Date information', {'fields': ['created_date','publish_date'], 'classes': ['collapse']}),
        ('Related tags',     {'fields': ['tags']}),
        ('Metas',            {'fields': ['status','views_count']}),
        ('Comments',            {'fields': ['enable_comment','comment_count']}),
    ]


admin.site.register(Article, ArticleAdmin)