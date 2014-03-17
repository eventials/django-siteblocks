# -*- coding: utf-8 -*-
from django.core.cache import cache
from .models import EventSiteBlock

CACHE_KEY = 'event_siteblock-%d'

def track_event(user_id, event, obj):
    qset = EventSiteBlock.objects.filter(event=event, hidden=False)
    if qset.count() > 0:
        esb = qset[0]
        cache.set(CACHE_KEY % user_id, esb.render_template(obj), 3 * 60)
