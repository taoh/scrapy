import re
from scrapy.utils.markup import replace_tags, unquote_markup
from scrapy.utils.python import str_to_unicode
from scrapy.item.adaptors import adaptize

def remove_tags(tags=()):
    """
    Factory that returns an adaptor for removing each
    tag in the `tags` parameter found in the given value.
    If no `tags` are specified, all of them are removed.

    Input: string/unicode
    Output: unicode
    """
    def _remove_tags(value):
        return replace_tags(value, tags)
    return _remove_tags

_remove_root_re = re.compile(r'^\s*<.*?>(.*)</.*>\s*$', re.DOTALL)
def remove_root(value):
    """
    This adaptor removes the root tag of the given string/unicode,
    if it's found.

    Input: string/unicode
    Output: unicode
    """
    m = _remove_root_re.search(value)
    if m:
        value = m.group(1)
    return str_to_unicode(value)

def unquote(keep=None):
    """
    This factory returns an adaptor that
    receives a string or unicode, removes all of the
    CDATAs and entities (except the ones in CDATAs, and the ones
    you specify in the `keep` parameter) and then, returns a new
    string or unicode.

    Input: string/unicode
    Output: string/unicode
    """
    default_keep = [] if keep is None else keep

    def unquote(value, adaptor_args):
        keep = adaptor_args.get('keep_entities', default_keep)
        return unquote_markup(value, keep=keep)
    return unquote