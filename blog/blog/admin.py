from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .forms import ArticleForm
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm

    list_display = [
        'title', 'author', 'is_private', 'time_created', 'time_published']
    prepopulated_fields = {'slug': ['title']}
    readonly_fields = ['time_created', 'time_modified']
    fieldsets = [
        [None, {
            'fields': [
                'title', 'body', 'tags', 'time_published', 'is_private']}],
        [_('Optional Info'), {
            'fields': ['slug', 'summary'],
            'classes': ['collapse']}],
    ]

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        obj.save()


# Registering the admins
admin.site.register(Article, ArticleAdmin)
