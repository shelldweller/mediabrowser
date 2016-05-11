#!/usr/bin/env python

from setuptools import setup
import mediabrowser


setup(
    name='mediabrowser',
    version=mediabrowser.VERSION,
    description='Django media browser for WYSIWYG HTML editor',
    install_requires=["easy_thumbnails"],
    author='Sergiy Kuzmenko',
    author_email='sergiy@kuzmenko.org',
    url='https://github.com/shelldweller/mediabrowser',
    packages=['mediabrowser'],
    include_package_data=True,
    license="MIT",
    platforms=['any'],
    zip_safe=False,
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
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)