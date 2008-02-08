# -*- coding: utf-8 -*-
#
# Copyright 2008, BDA - Blue Dynamics Alliance, Austria - www.bluedynamics.com
#
# GNU General Public Licence Version 2 or later - see LICENCE.GPL

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

from setuptools import setup, find_packages
import sys, os

version = '1.0-beta1'
shortdesc = "converter adapter for date and time input to datetime object."
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

setup(name='bda.intellidatetime',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Development Status :: beta1',
            'Environment :: Web Environment',
            'Framework :: Zope2',
            'License :: OSI Approved :: General Public Licence',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',            
      ], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Robert Niedereiter',
      author_email='rnix@squarewave.at',
      url='',
      license='General Public Licence',
      packages=find_packages(exclude=['ez_setup',]),
      namespace_packages=['bda'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',                        
          # -*- Extra requirements: -*
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

