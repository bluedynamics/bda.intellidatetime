from setuptools import setup, find_packages
import sys, os

version = '1.0.1'
shortdesc = "Converter adapter for date and time input to datetime object."
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

setup(name='bda.intellidatetime',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Web Environment',
            'Framework :: Zope3',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',            
      ], # http://www.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Robert Niedereiter',
      author_email='rnix@squarewave.at',
      url=u'https://svn.plone.org/svn/collective/bda.intellidatetime',
      license='General Public Licence',
      packages=find_packages(exclude=['ez_setup',]),
      namespace_packages=['bda'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',    
          'zope.interface',                    
      ],
      tests_require=['interlude'],
      test_suite="bda.intellidatetime.tests.test_suite",
      entry_points="""
      # -*- Entry points: -*-
      """,
      )