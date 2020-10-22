from django.contrib import admin
from .models import *


class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'name_slug')
    exclude = ['name_slug']
    # prepopulated_fields = {'name_slug': (slugify('name'),)}


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", 'name_slug', 'mod_date')
    exclude = ['name_slug', 'likes', 'views']
    # prepopulated_fields = {"name_slug": ("title", )}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "name_slug", 'mod_date')
    exclude = ['name_slug', 'article_num', 'total_views', 'total_likes']
    # prepopulated_fields = {'name_slug': (slugify('name'),)}


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "name_slug")
    exclude = ['name_slug', 'article_num', 'total_views', 'total_likes']
    # prepopulated_fields = {'name_slug': ('name', )}


# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Me)
