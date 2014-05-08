from django.db.models import signals

from .models import Block
from .siteblocksapp import SiteBlocks

siteblocks = SiteBlocks()

signals.post_save.connect(siteblocks._cache_list_keys_empty, sender=Block)
signals.post_delete.connect(siteblocks._cache_list_keys_empty, sender=Block)