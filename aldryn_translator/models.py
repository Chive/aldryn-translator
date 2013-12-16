# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from annoying.fields import JSONField

from cms.models import Page
from cms.stacks.models import Stack


STATUS_CHOICES = (
    ('draft', _('Draft')),
    ('selected_content', _('Selected Content')),
    ('selected_quote', _('Selected Quote')),
    ('requested', _('Requested')),
    ('done', _('Done')),
    ('fail', _('Failed'))
)

# class PageTranslation(models.Model):
#     created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
#     page = models.ForeignKey(Page)
#     from_lang = models.CharField(verbose_name=_("From Language"), max_length=10)
#     to_lang = models.CharField(verbose_name=_("From Language"), max_length=10)
#     status = models.CharField(verbose_name=_("Status"), max_length=20, choices=STATUS_CHOICES,
#                               default=STATUS_CHOICES[0])
#     price = models.DecimalField(verbose_name=_("Preis"), decimal_places=2, max_digits=20)
#     translated_at = models.DateTimeField(verbose_name=_("Translated at"))


class TranslationRequest(models.Model):
    PROVIDER_CHOICES = (
        ('supertext', _("Supertext")),
    )

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    from_lang = models.CharField(verbose_name=_("From Language"), max_length=50)
    to_lang = models.CharField(verbose_name=_("To Language"), max_length=50)
    status = models.CharField(verbose_name=_("Status"), max_length=30, choices=STATUS_CHOICES,
                              default=STATUS_CHOICES[0][0])
    price = models.DecimalField(verbose_name=_("Preis"), decimal_places=2, max_digits=20, null=True, blank=True)
    translated_at = models.DateTimeField(verbose_name=_("Translated at"), null=True, blank=True)
    all_pages = models.BooleanField(verbose_name=_("Send all pages"))
    all_stacks = models.BooleanField(verbose_name=_("Send all stacks"))
    sent_content = JSONField(verbose_name=_("Sent content"), null=True, blank=True)
    provider = models.CharField(verbose_name=_("Provider"), choices=PROVIDER_CHOICES, max_length=100,
                                default=PROVIDER_CHOICES[0][0])
    order_choice = models.CharField(verbose_name=_("Order choice"), max_length=200, null=True, blank=True)
    order_selection = models.TextField(verbose_name=("Order selection"), null=True, blank=True)
    reference = models.CharField(verbose_name=_("Reference Data"), max_length=200, null=True, blank=True)


class TranslationResponse(models.Model):
    received_at = models.DateTimeField(verbose_name=_("Recieved at"), auto_now_add=True)
    valid = models.BooleanField(verbose_name=_("Matched with TranslationRequest"))
    request = models.ForeignKey(TranslationRequest, null=True, blank=True)
    received_content = JSONField(verbose_name=_("Recieved content"), null=True, blank=True)
    debug_info = models.TextField(verbose_name=_("Debug Information"), null=True, blank=True)
