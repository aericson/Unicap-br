# -*- coding:utf-8 -*-
from distutils.core import setup

README = open('README').read()

setup(
    name='unicap_br',
    license='MIT',
    version='0.1',
    description='Unicap book renewer',
    author='André Ericson',
    author_email='de.ericson@gmail.com',
    url='https://github.com/aericson/Unicap-br',
    packages=['unicap_br'],
    scripts=['bin/renewer.py'],
    long_description=README,
    install_requires=[
        'BeautifulSoup>=4.3',
        'mechanize>=0.2.5',
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Students',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Utilities',
        ])
