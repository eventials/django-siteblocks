from django.contrib import admin

from .models import Block, EventSiteBlock


class BlockAdmin(admin.ModelAdmin):

    list_display = ('alias', 'description', 'url', 'hidden')
    search_fields = ['alias', 'url']
    list_filter = ['hidden']
    ordering = ['alias']


class EventSiteBlockAdmin(admin.ModelAdmin):

    list_display = ('event', 'hidden')
    search_fields = ['event', 'url']
    list_filter = ['hidden']
    ordering = ['event']


admin.site.register(Block, BlockAdmin)
admin.site.register(EventSiteBlock, EventSiteBlockAdmin)