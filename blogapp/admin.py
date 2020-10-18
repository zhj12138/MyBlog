from django.contrib import admin
from .models import *


class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


# Register your models here.
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Link, LinkAdmin)
admin.site.register(Me)
