# -*- coding: utf-8 -*-
import json
import re
import sys
from __builtin__ import unicode

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from djangocms_text_ckeditor.models import Text
import requests

from cms.models import Placeholder
from cms.utils.i18n import get_language_list
from cms.models import Title, Page, CMSPlugin
from cms.api import copy_plugins_to_language
from cms.stacks.models import Stack
from cms.utils.copy_plugins import copy_plugins_to

from helpers import get_creds, is_dev, get_blacklist


def export_plugins_by_pages(from_lang, plugin_selection=None):
    plugins = []
    for page in Page.objects.filter(publisher_is_draft=True):
        for ph in page.placeholders.all():
            for plugin in ph.get_plugins():
                plugins.append(plugin)

    return export_plugins(from_lang, plugins, plugin_selection)


def export_plugins_by_stacks(from_lang, plugin_selection=None):
    plugins = []
    for stack in Stack.objects.all():
        try:
            field = 'draft'
            getattr(stack, field)
        except AttributeError:
            # Supporting old stacks here
            field = 'content'

        finally:
            for plugin in getattr(stack, field).get_plugins():
                plugins.append(plugin)

    return export_plugins(from_lang, plugins, plugin_selection)


# Not used atm
def export_plugins_by_placeholders(from_lang):
    plugins = []
    for ph in Placeholder.objects.all():
        for plugin in ph.get_plugins():
            plugins.append(plugin)

    return export_plugins(from_lang, plugins)


def export_plugins(from_lang, plugin_list, plugin_selection=None):
    blacklist = get_blacklist()
    plugins = []
    for plugin in plugin_list:
        instance = plugin.get_plugin_instance()[0]
        if instance is not None:
            if plugin_selection and str(type(instance)) not in plugin_selection:
                continue

            if getattr(instance, "language") == from_lang:  # FIXME: could this break at some point?
                plugins.append(instance)

    plugin_data = list()
    for plugin in plugins:
        plugin_fields = []
        for field in plugin._meta.fields:
            if ((isinstance(field, models.CharField) or isinstance(field, models.TextField))
                    and not field.choices and field.editable and field):
                plugin_fields.append(field)
        if plugin_fields:
            d = dict()
            d['plugin_pk'] = getattr(plugin, "pk")
            d['plugin_type'] = str(type(plugin))
            d['fields'] = dict()
            for field in plugin_fields:
                val = getattr(plugin, field.name)
                if val not in ['', None] and field.name not in blacklist:
                    d['fields'][field.name] = val

            if d['fields']:
                plugin_data.append(d)

    # POST PROCESSING: Merging Link plugins into Text Plugins
    for i, plugin in enumerate(plugin_data):
        for key, value in plugin['fields'].items():
            matches = re.findall(
                r'(<img alt="(Link[^"]*)" id="plugin_obj_([\d]*)" src="([^"]*)" title="(Link[^"]*)">)',
                value
            )
            if matches:
                for m in matches:
                    try:
                        link_plugin = CMSPlugin.objects.get(pk=m[2]).get_plugin_instance()[0]
                    except CMSPlugin.DoesNotExist:
                        sys.stderr.write("ERROR: Could not find plugin with pk %s!\n" % str(m[2]))
                        continue

                    if getattr(link_plugin, 'mailto', False):
                        href = link_plugin.mailto
                    elif getattr(link_plugin, 'page_link', False):
                        href = link_plugin.page_link
                    else:
                        href = link_plugin.url

                    text = '<a plugin="%s" href="%s" target="%s" alt="%s" title="%s" img_src="%s">%s</a>' % (
                        m[2], href, link_plugin.target, m[1], m[4], m[3], link_plugin.name)
                    plugin_data[i]['fields'][key] = value.replace(m[0], text)

    return plugin_data


def export_page_titles(lang, plugin_selection=None):
    title_data = []
    if plugin_selection and '_pagetitle' not in plugin_selection:
        return title_data

    for page in Page.objects.all():
        try:
            title = page.title_set.filter(language=lang, page__publisher_is_draft=True)[0]
            title_data.append({
                'fields': {
                    'title': title.title,
                    'menu_title': title.menu_title,
                    'page_title': title.page_title
                },
                'title_pk': title.pk,
            })

        except IndexError:
            pass
    return title_data


def prepare_data(obj, from_lang, to_lang, plugin_source_lang=None):
    """
    By default, you get the plugins from the 'from_lang' language.
    If you want to override this behaviour, use 'plugin_source_lang' instead
    """

    if plugin_source_lang:
        source = plugin_source_lang
    else:
        source = from_lang

    raw_data = []

    if obj.all_pages:
        raw_data += export_plugins_by_pages(source, obj.order_selection)

    if obj.all_stacks:
        raw_data += export_plugins_by_stacks(source, obj.order_selection)

    raw_data += export_page_titles(source, obj.order_selection)

    if not raw_data:
        raise UserWarning("No content could be found.")

    if obj.provider == 'supertext':
        supertext_langs = {
            'de': 'de-de',
            'en': 'en-us'
        }

        if from_lang in supertext_langs:
            from_lang = supertext_langs[from_lang]

        if to_lang in supertext_langs:
            to_lang = supertext_langs[to_lang]


        # TODO: this would be nicer
        # for l in [from_lang, to_lang]:
        #     if l in supertext_langs:
        #         l = supertext_langs[l]


        data = dict()
        data['ContentType'] = 'text/html'
        data['Currency'] = 'chf'  # TODO: move to model and to form
        data['SourceLang'] = from_lang
        data['TargetLanguages'] = [to_lang]
        data['Groups'] = list()

        for item in raw_data:
            group = dict()
            if 'plugin_pk' in item:
                group['GroupId'] = item['plugin_pk']
                group['Context'] = item['plugin_type']

            elif 'title_pk' in item:
                group['GroupId'] = item['title_pk']
                group['Context'] = '_pagetitle'

            group['Items'] = list()

            for name, val in item['fields'].items():
                if val and val is not None and val != "":
                    i = dict()
                    i['Id'] = name
                    i['Content'] = val
                    group['Items'].append(i)

            if group['Items']:  # if group['Items'] != []:
                data['Groups'].append(group)
    else:
        raise NotImplementedError()
    return data


def prepare_order_data(request, obj):
    res = dict()
    if obj.provider == 'supertext':
        res['Referrer'] = "Aldryn Translator"
        res['ReferenceData'] = obj.reference
        res['OrderName'] = obj.order_name
        res['OrderTypeId'], res['DeliveryId'] = obj.order_choice.split("_")
        res['CallbackUrl'] = request.build_absolute_uri(reverse('admin:process_response'))

    else:
        raise NotImplementedError()

    return res


def get_quote(provider, data):
    if provider == 'supertext':
        if is_dev():
            url = 'http://dev.supertext.ch/api/v1/translation/quote'
        else:
            url = 'http://supertext.ch/api/v1/translation/quote'
        headers = {'Content-type': 'application/json; charset=UTF-8', 'Accept': '*'}
        r = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode('ascii', 'xmlcharrefreplace'),
                          headers=headers)
        return r.content

    else:
        raise NotImplementedError()


def get_order(provider, data):
    if provider == 'supertext':
        user, api_key = get_creds('SUPERTEXT', ['USER', 'API_KEY'])
        if is_dev():
            url = 'http://dev.supertext.ch/api/v1/translation/order'
        else:
            url = 'http://supertext.ch/api/v1/translation/order'
        headers = {'Content-type': 'application/json; charset=UTF-8', 'Accept': '*'}
        r = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode('ascii', 'xmlcharrefreplace'),
                          headers=headers, auth=(user, api_key))
        return r.content

    else:
        raise NotImplementedError()


# copied from cms > management
def copy_page(from_lang, to_lang):
    site = settings.SITE_ID

    #test both langs
    if from_lang == to_lang:
        raise Exception("from_lang must be different from to_lang!")

    try:
        assert from_lang in get_language_list(site)
        assert to_lang in get_language_list(site)
    except AssertionError:
        raise Exception("Could not languages from site")

    for page in Page.objects.on_site(site).drafts():
        # copy title
        if from_lang in page.get_languages():
            try:
                title = page.get_title_obj(to_lang, fallback=False)
            except Title.DoesNotExist:
                title = page.get_title_obj(from_lang)
                title.id = None
                title.language = to_lang
                title.save()
            # copy plugins using API
            copy_plugins_to_language(page, from_lang, to_lang)

    for stack in Stack.objects.all():
        plugin_list = []
        for plugin in stack.draft.get_plugins():
            if plugin.language == from_lang:
                plugin_list.append(plugin)

        if plugin_list:
            copy_plugins_to(plugin_list, stack.draft, to_lang)


def insert_response(provider, response):
    if provider == 'supertext':
        for obj in response['Groups']:
            if obj['Context'] == '_pagetitle':
                # Page Title objects
                title = Title.objects.get(pk=obj['GroupId'])
                for field in obj['Items']:
                    setattr(title, field['Id'], field['Content'])
                title.save()

            else:
                # Plugin objects
                plugin_class = CMSPlugin.objects.get(pk=obj['GroupId'])
                instance = plugin_class.get_plugin_instance()[0]
                for field in obj['Items']:
                    f_content = field['Content']
                    f_id = field['Id']
                    # Check for 'serialized' link plugin
                    exp = r'(<a plugin="([\d]*)" href="[^"]*" target="[^"]*" alt="([^"]*)" title="([^"]*)" img_src="([^"]*)">(.*[^</a>])</a>)'
                    matches = re.findall(exp, field['Content'])
                    if matches:
                        for m in matches:
                            try:
                                linkplugin = CMSPlugin.objects.get(pk=m[1]).get_plugin_instance()[0]
                            except CMSPlugin.DoesNotExist:
                                sys.stderr.write("ERROR: Could not find plugin with pk %s\n" % str(m[0]))

                            # Save changes to linkplugin
                            linkplugin.name = m[5]
                            linkplugin.save()

                            # Save changes to parent text plugin
                            text = '<img alt="%s" id="plugin_obj_%s" src="%s" title="%s">' % (m[2], m[1], m[4], m[3])
                            f_content = f_content.replace(m[0], text)

                    setattr(instance, f_id, f_content)

                instance.save()
    else:
        raise NotImplementedError()
