# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from aldryn_translator import __version__

REQUIREMENTS = []

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='aldryn translator',
    version=__version__,
    description='Aldryn Translator',
    author='Chive (Kim Thoenen)',
    author_email='kim@smuzey.ch',
    url='https://github.com/Chive/aldryn-translator',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False
)