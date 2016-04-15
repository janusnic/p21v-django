from django.contrib import admin

from .models import Category, Tag, Article

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

class CategoryAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ['name', 'slug', 'description']

    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category,CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ['name', 'slug']
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Tag, TagAdmin)

class ArticleAdminForm(forms.ModelForm):
    
    content = forms.CharField(widget=CKEditorWidget())
    content = forms.CharField(widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Article
        fields = '__all__'


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status', 'was_published_recently')
    list_filter = ['publish_date']
    search_fields = ['title']

    ordering = ['publish_date']

    filter_horizontal = ('tags',)

    prepopulated_fields = {"slug": ("title",)}

    form = ArticleAdminForm

    date_hierarchy = 'publish_date'
    readonly_fields = ('publish_date','created_date')
    fieldsets = [
        ('Item',             {'fields': [('title','slug'),'category','content']}),
        ('Date information', {'fields': [('publish_date','created_date')], 'classes': ['collapse']}),
        ('Related tags',     {'fields': ['tags']}),
        ('Metas',            {'fields': [('status')]}),
    ]

admin.site.register(Article, ArticleAdmin)

