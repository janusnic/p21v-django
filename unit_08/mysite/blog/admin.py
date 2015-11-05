from django.contrib import admin

from django import forms
from redactor.widgets import RedactorEditor

from .models import Category, Tag, Article
from django.conf import settings

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('views_count',)
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ['name', 'slug', 'description']
    list_per_page = settings.ADMIN_LIST_PER_PAGE


    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag)

def make_published(modeladmin, request, queryset):
    queryset.update(status='P')
make_published.short_description = "Mark selected stories as published"

class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'content': RedactorEditor(),
        }

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status', 'was_published_recently')
    list_filter = ['publish_date']
    search_fields = ['title']

    ordering = ['publish_date']

    prepopulated_fields = {"slug": ("title",)}

    fieldsets = [
        ('Item',             {'fields': [('title','slug'),'category','content']}),
        ('Date information', {'fields': [('created_date','publish_date')], 'classes': ['collapse']}),
        ('Related tags',     {'fields': ['tags']}),
        ('Metas',            {'fields': [('status','views_count')]}),
        ('Comments',            {'fields': ['enable_comment','comment_count']}),
    ]
    actions = [make_published,'make_draft','make_expired']

    actions_on_top = True 
    actions_on_bottom = False 
    actions_selection_counter = True

    date_hierarchy = 'publish_date'

    filter_horizontal = ('tags',)

    readonly_fields = ('views_count', 'comment_count')

    form = ArticleAdminForm

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()

    def make_draft(self, request, queryset):
        queryset.update(status='D')
    make_draft.short_description = "Mark selected stories as draft"

    def make_expired(self, request, queryset):
        rows_updated = queryset.update(status='E')
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as expired." % message_bit)
    make_expired.short_description = "Mark selected stories as expired"


admin.site.register(Article, ArticleAdmin)