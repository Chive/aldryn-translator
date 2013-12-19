import inspect
import json
import sys

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.http import HttpResponse
from django.utils.html import escape

from cms.exceptions import LanguageError
from cms.utils import get_language_from_request
from cms.utils.i18n import get_language_object, get_language_objects


def get_current_lang(request):
    current_site = Site.objects.get_current()
    try:
        return get_language_object(get_language_from_request(request), current_site.pk)
    except LanguageError:
        return False


def get_site_languages():
    return get_language_objects(Site.objects.get_current().pk)


def log_to_file(data, filename='aldryn_translator_log.txt'):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False).encode('ascii', 'xmlcharrefreplace'))


def display_data_to_web(data):
    c = json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True).encode('ascii', 'xmlcharrefreplace')
    return HttpResponse("<pre>%s</pre>" % escape(c))


def check_stage(requested, expected):
    if requested != expected:
        sys.stderr.write("###### AUTH FAIL ######\nrequested:\t%s\nexpected:\t%s\ncaller:\t%s" % (requested, expected, inspect.stack()[1][3]))
        raise PermissionDenied()


def get_creds(provider, fields):
    creds = getattr(settings, "ALDRYN_TRANSLATOR_CREDENTIALS", None)

    if creds:
        return_list = []
        for field in fields:
            try:
                return_list.append(creds[provider][field])
            except KeyError:
                raise ImproperlyConfigured("Please provide the provide credentials to use %s's api" % provider.title())

    else:
        raise ImproperlyConfigured("Please provide the provide credentials to use %s's api" % provider.title())

    return return_list


def is_dev():
    return getattr(settings, "ALDRYN_TRANSLATOR_DEV", False)


def get_blacklist():
    return getattr(settings, "ALDRYN_TRANSLATOR_FIELDS_BLACKLIST", list())
