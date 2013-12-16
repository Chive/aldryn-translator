# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.exceptions import LanguageError
from cms.toolbar.items import Break
from cms.utils import get_language_from_request
from cms.utils.i18n import get_language_object, get_language_objects
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.cms_toolbar import LANGUAGE_MENU_IDENTIFIER, ADD_PAGE_LANGUAGE_BREAK, ADMIN_MENU_IDENTIFIER, ADMIN_SITES_BREAK


@toolbar_pool.register
class LanguageToolbar(CMSToolbar):
    def global_translation(self):
        admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER, _('Site'))
        position = admin_menu.find_first(Break, identifier=ADMIN_SITES_BREAK)
        admin_menu.add_modal_item(_("Translate this Website"), reverse('add_translation'), position=position)

    def single_page_translation(self):
        current_site = Site.objects.get_current()
        try:
            current_lang = get_language_object(get_language_from_request(self.request), current_site.pk)
        except LanguageError:
            current_lang = None
        language_menu = self.toolbar.get_or_create_menu(LANGUAGE_MENU_IDENTIFIER, _('Language'))
        position = language_menu.find_first(Break, identifier=ADD_PAGE_LANGUAGE_BREAK)
        menu = language_menu.get_or_create_menu('aldryn-translator', _('Get this page translated'), position=position)
        for language in get_language_objects(current_site.pk):
            if language['code'] != current_lang['code']:
                menu.add_modal_item(_('to %s' % language['name']), "%s?from_lang=%s&to_lang=%s" % (
                    reverse('admin:aldryn_translator_translation_add'), current_lang['code'], language['code']))

    def populate(self):
        return  # TODO: Does not work at the moment
        if not self.request.user.has_module_perms('aldryn_translator'):
            return

        self.global_translation()
        # self.single_page_translation()
