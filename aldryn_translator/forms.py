# -*- coding: utf-8 -*-
from django import forms
from django.forms import Select
from django.utils.translation import ugettext_lazy as _

from utils import get_site_languages
from models import TranslationRequest


class AddTranslationForm(forms.ModelForm):
    class Meta:
        model = TranslationRequest
        fields = [
            # 'from_lang', 'to_lang', added dynamically in __init__()
            'provider', 'copy_content', 'all_pages', 'all_static_placeholders',
        ]

        widgets = {
            'from_lang': Select,
            'to_lang': Select,
        }

    def __init__(self, *args, **kwargs):
        super(AddTranslationForm, self).__init__(*args, **kwargs)
        self.fields['from_lang'] = forms.ChoiceField(choices=self.build_lang_choices())
        self.fields['to_lang'] = forms.ChoiceField(choices=self.build_lang_choices())

    def build_lang_choices(self):
        choices = list()
        for lang in get_site_languages():
            choices.append((lang['code'], _(lang['name'])))
        return choices

    def clean(self):
        cleaned_data = super(AddTranslationForm, self).clean()
        if cleaned_data.get('from_lang') == cleaned_data.get('to_lang'):
            msg = _('Please select two different languages')
            self._errors['from_lang'] = self.error_class([''])
            self._errors['to_lang'] = self.error_class([msg])
        return cleaned_data


class SelectPluginsByTypeForm(forms.Form):
    plugins = None

    def __init__(self, *args, **kwargs):
        plugins = kwargs.pop('plugins')
        super(SelectPluginsByTypeForm, self).__init__(*args, **kwargs)
        choices = list()
        for plugin, count in plugins.items():
            # TODO: Get real name of plugin instead of class
            # But since we store the plugin as string we can't do that with the code below
            # plugin.get_plugin_name().capitalize()
            # We might have to do something like
            # getattr(sys.modules[__name__], p['Context'])
            # getattr(p['Context'], 'class_name')
            choices.append(("%s" % plugin, "%s (%sx)" % (plugin, count)))

            self.fields['plugins'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple,
                choices=choices, initial=[c[0] for c in choices],
                required=False
            )
