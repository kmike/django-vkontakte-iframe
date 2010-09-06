#!/usr/bin/env python
from distutils.core import setup

version='0.1'

setup(
    name='django-vkontakte-iframe',
    version=version,
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',

    packages=['vk_iframe', 'vk_iframe.migrations'],
    package_data={
        'vk_iframe': ['templates/vk_iframe/default/403.html', 'fixtures/vk-geo.json']
    },

    url='http://bitbucket.org/kmike/django-vkontakte-iframe/',
    download_url = 'http://bitbucket.org/kmike/django-vkontakte-iframe/get/tip.zip',
    license = 'MIT license',
    description = "Django app for developing vk.com (aka vkontakte.ru) iframe applications",

    long_description = open('README.rst').read(),

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
