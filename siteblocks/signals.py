import logging
logger = logging.getLogger(__name__)  # Get an instance of a logger

from django.db.models import signals

from .models import Block
from .siteblocksapp import SiteBlocks


logger.info('Registering SiteBlocks signals')

siteblocks = SiteBlocks()

signals.post_save.connect(siteblocks._cache_list_keys_empty, sender=Block)
signals.post_delete.connect(siteblocks._cache_list_keys_empty, sender=Block)