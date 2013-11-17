#!/usr/bin/env python

from distutils.core import setup
import mediabrowser

setup(
    name='mediabrowser',
    version=mediabrowser.VERSION,
    description='Django media browser for WYSIWYG HTML editor',
    author='Sergiy Kuzmenko',
    author_email='sergiy@kuzmenko.org',
    url='https://github.com/shelldweller/mediabrowser',
    packages=['mediabrowser'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Graphics",
    ],
)