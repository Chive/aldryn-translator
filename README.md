aldryn translator
=================

Setup
-----

```bash
pip install aldryn-translator  # from pkg.divio.ch
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
```
