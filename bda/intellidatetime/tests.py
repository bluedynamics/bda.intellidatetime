# -*- coding: utf-8 -*-
#
# Copyright 2008, BDA - Blue Dynamics Alliance, Austria - www.bluedynamics.com
#
# GNU General Public Licence Version 2 or later - see LICENCE.GPL

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

import unittest
import zope.component
import zope.app.component

from zope.testing import doctest
from zope.component.testing import setUp, tearDown
from zope.configuration.xmlconfig import XMLConfig

import bda.intellidatetime

optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS

def configurationSetUp(test):
    setUp()

    XMLConfig('meta.zcml', zope.app.component)()

    # BBB conditional code for loading the utility dispatchers
    # In Zope 2.11 they are in zope.component
    try:
        XMLConfig('configure.zcml', zope.component)()
    except IOError:
        pass

    XMLConfig('configure.zcml', bda.intellidatetime)()

def configurationTearDown(test):
    tearDown()

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'converter.py',
            setUp=configurationSetUp,
            tearDown=configurationTearDown,
            optionflags=optionflags)))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
