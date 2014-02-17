aldryn-translator
=================

This is work in progress. Try at your own risk

Setup
-----

```bash
pip install -e git+https://github.com/Chive/aldryn-translator#egg=aldryn-translator
```


```python

# settings.py

INSTALLED_APPS += [
    'aldryn_translator'
]

ALDRYN_TRANSLATOR_CREDENTIALS = {
    'SUPERTEXT': {
        'USER': '',
        'API_KEY': '',
    }
}

ALDRYN_TRANSLATOR_DEV = True/False
ALDRYN_TRANSLATOR_FIELDS_BLACKLIST = ['reverse_id', 'additional_classes', 'custom_classes', 'width', 'height']
ALDRYN_TRANSLATOR_LOG_TO_FILE = True/False  # log data to file for debugging
```
