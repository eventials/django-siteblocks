import logging
import re
from random import choice
from collections import defaultdict

from django.core.cache import cache
from django.core.urlresolvers import resolve, Resolver404
from django.db.models import signals
from django.template import Context, Template

from .models import Block


# siteblocks objects are stored in Django cache for a year (60 * 60 * 24 * 365 = 31536000 sec).
# Cache is only invalidated on block item change.
CACHE_TIMEOUT = 31536000
CACHE_KEY_PREFIX = 'siteblocks'
CACHE_LIST_KEYS_KEY = 'siteblocks_keys'

# Holds dynamic blocks.
_DYNAMIC_BLOCKS = defaultdict(list)


def register_dynamic_block(alias, callable):
    """Registers a callable that produces contents for a dynamic block.

    Callable on call will get the following kwargs:

        * `block_alias` - block alias,
        * `block_context` - template context for block

    Example::

        # Put the following code somewhere where it'd be triggered as expected. E.g. in app view.py.

        from random import choice
        # Import the register function.
        from siteblocks.siteblocksapp import register_dynamic_block


        # The following function will be used as a block contents producer.
        def get_quote(**kwargs):
            quotes = [  # From Terry Pratchett's Discworld novels.
                'Ripples of paradox spread out across the sea of causality.',
                'Early to rise, early to bed, makes a man healthy, wealthy and dead.',
                'Granny had nothing against fortune-telling provided it was done badly by people with no talent for it.',
                'Take it from me, there\'s nothing more terrible than someone out to do the world a favour.',
                'The duke had a mind that ticked like a clock and, like a clock, it regularly went cuckoo.',
                'Most gods find it hard to walk and think at the same time.',
                'They didn\'t have to be funny - they were father jokes',
                'Speak softly and employ a huge man with a crowbar.',
            ]
            return choice(quotes)

        # And we register our siteblock.
        register_dynamic_block('quote', get_quote)

    """
    global _DYNAMIC_BLOCKS
    _DYNAMIC_BLOCKS[alias].append(callable)


def get_dynamic_blocks():
    """Returns a dictionary with currently registered dynamic blocks."""
    return _DYNAMIC_BLOCKS


class SiteBlocks(object):

    def __init__(self):
        signals.post_save.connect(self._cache_list_keys_empty, sender=Block)
        signals.post_delete.connect(self._cache_list_keys_empty, sender=Block)

    def _cache_list_keys_init(self):
        """Initializes local cache from Django cache."""
        cache_ = cache.get(CACHE_LIST_KEYS_KEY)
        if cache_ is None:
            cache_ = defaultdict(list)
        self._cache = cache_

    def _cache_list_keys_save(self):
        cache.set(CACHE_LIST_KEYS_KEY, self._cache, CACHE_TIMEOUT)

    def _save_key(self, key):
        self._cache_list_keys_init()
        self._cache['keys'].append(key)
        self._cache_list_keys_save()

    def _cache_list_keys_empty(self, **kwargs):
        self._cache_list_keys_init()
        for key in self._cache['keys']:
            cache.delete(key)

        self._cache = None
        cache.delete(CACHE_LIST_KEYS_KEY)

    def _cache_get(self, key):
        key = '%s_%s' % (CACHE_KEY_PREFIX, key)
        self._save_key(key)
        return cache.get(key, False)

    def _cache_set(self, key, value):
        key = '%s_%s' % (CACHE_KEY_PREFIX, key)
        cache.set(key, value, CACHE_TIMEOUT)

    def _cache_and_return(self, key, value):
        self._cache_set(key, value)
        return value

    def _get_resolved_view_name(self, current_url):
        # Resolve current view name to support view names as block URLs.
        try:
            resolver_match = resolve(current_url)
            namespace = ''
            if resolver_match.namespaces:
                # More than one namespace, really? Hmm.
                namespace = resolver_match.namespaces[0]
            return ':%s:%s' % (namespace, resolver_match.url_name)
        except Resolver404:
            return None

    def get_content_static(self, block_alias, context):
        def render_template(contents):
            try:
                return Template(contents).render(Context(context))
            except:
                logging.exception("Error rendering siteblock template.")
                return ""

        if 'request' not in context:
            # No use in further actions as we won't ever know current URL.
            return ''

        current_url = context['request'].path

        key = block_alias
        re_index = self._cache_get(key)
        print re_index
        if True:
            blocks = Block.objects.filter(alias=block_alias, hidden=False).only('url', 'contents')
            re_index = defaultdict(list)
            for block in blocks:
                if block.url == '*':
                    url_re = block.url
                elif block.url.startswith(':'):
                    url_re = block.url
                    # Normalize URL name to include namespace.
                    if url_re.count(':') == 1:
                        url_re = ':%s' % url_re
                else:
                    url_re = re.compile(r'%s' % block.url)

                re_index[url_re].append(block.contents)
            self._cache_set(key, re_index)

        resolved_view_name = self._get_resolved_view_name(current_url)

        if resolved_view_name in re_index:
            contents = choice(re_index[resolved_view_name])
            return render_template(contents)
        else:
            for url, contents_list in re_index.items():
                if hasattr(url, 'match') and url.match(current_url):
                    contents = choice(contents_list)
                    return render_template(contents)

        if '*' in re_index:
            contents = choice(re_index['*'])
            return render_template(contents)

        return ''

    def get_content_dynamic(self, block_alias, context):
        dynamic_block = get_dynamic_blocks().get(block_alias, [])
        if not dynamic_block:
            return ''

        dynamic_block = choice(dynamic_block)
        return dynamic_block(block_alias=block_alias, block_context=context)

    def get(self, block_alias, context):
        contents = []

        dynamic_block_contents = self.get_content_dynamic(block_alias, context)
        if dynamic_block_contents:
            contents.append(dynamic_block_contents)

        static_block_contents = self.get_content_static(block_alias, context)
        if static_block_contents:
            contents.append(static_block_contents)

        if not contents:
            return ''

        return choice(contents)


class SiteBlocksError(Exception):
    """Exception class for siteblocks application."""
    pass
