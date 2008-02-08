# -*- coding: utf-8 -*-
#
# Copyright 2008, BDA - Blue Dynamics Alliance, Austria - www.bluedynamics.com
#
# GNU General Public Licence Version 2 or later - see LICENCE.GPL

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

import types
from datetime import datetime
from zope.interface import implements

from interfaces import DateTimeConversionError, ILocalePattern, IIntelliDateTime

class LocalePattern(object):
    """See interfaces.ILocalePattern.
    
    TODO: complete the language codes
    
    >>> from bda.intellidatetime import ILocalePattern
    >>> pattern = ILocalePattern(object())
    >>> pattern
    <bda.intellidatetime.converter.LocalePattern object at ...>
    
    >>> pattern.date(None)
    'Y M D'
    
    >>> pattern.time(None)
    'H M'
    
    >>> pattern.date('de')
    'D M Y'
    
    >>> pattern.time('de')
    'H M'
    
    """
    
    implements(ILocalePattern)
    
    __date_I = 'Y M D'
    __date_II = 'D M Y'
    __date_III = 'M D Y'
    __time_I = 'H M'
    __time_II = 'M H' # ever used ??
    
    PATTERNS = {
        'date': dict(),
        'time': dict(),
    }
    
    PATTERNS['date']['iso'] = __date_I
    PATTERNS['time']['iso'] = __time_I
    
    for locale in ['de', 'de-de', 'de-at', 'de-ch']:
        PATTERNS['date'][locale] = __date_II
    
    for locale in ['en']:
        PATTERNS['date'][locale] = __date_III
    
    for locale in ['en', 'de', 'de-de', 'de-at', 'de-ch']:
        PATTERNS['time'][locale] = __time_I
    
    def __init__(self, context): pass
    
    def date(self, locale):
        return self.PATTERNS['date'].get(locale, self.__date_I)
    
    def time(self, locale):
        return self.PATTERNS['time'].get(locale, self.__time_I)


class IntelliDateTime(object):
    """See interfaces.IIntelliDateTime.
    
    Get The IntelliDateTime converter
    >>> from bda.intellidatetime import IIntelliDateTime
    >>> converter = IIntelliDateTime(object())
    >>> converter
    <bda.intellidatetime.converter.IntelliDateTime object at ...>
    
    Check if Interface implementation fits the definitions.
    >>> from zope.interface.verify import verifyObject
    >>> verifyObject(IIntelliDateTime, converter)
    True
    
    Test the internal _isNumeric() function.
    >>> converter._isNumeric(None)
    False
    >>> converter._isNumeric(object())
    False
    >>> converter._isNumeric('1234567890abcdefg')
    False
    >>> converter._isNumeric('1 2 3')
    False
    >>> converter._isNumeric('')
    False
    >>> converter._isNumeric('1234567890')
    True
    
    Test the internal _splitValue() function.
    >>> converter._splitValue(None)
    Traceback (most recent call last):
      ...
    DateTimeConversionError: Empty value or unknown value type.
    >>> converter._splitValue(object())
    Traceback (most recent call last):
      ...
    DateTimeConversionError: Empty value or unknown value type.
    >>> converter._splitValue('')
    Traceback (most recent call last):
      ...
    DateTimeConversionError: Empty value or unknown value type.
    >>> converter._splitValue(' 1   ')
    [1]
    >>> converter._splitValue('1 2')
    [1, 2]
    >>> converter._splitValue('1 2 3')
    [1, 2, 3]
    >>> converter._splitValue('0101')
    [1, 1]
    >>> converter._splitValue('010101')
    [1, 1, 1]
    >>> converter._splitValue('1, 2, 3')
    [1, 2, 3]
    
    Special case whole year
    >>> converter._splitValue('01012008')
    '01012008'
    
    Cases when numeric values break
    >>> converter._splitValue('000')
    Traceback (most recent call last):
      ...
    DateTimeConversionError: Numeric value given, but not parseable.
    >>> converter._splitValue('00000')
    Traceback (most recent call last):
      ...
    DateTimeConversionError: Numeric value given, but not parseable.
    >>> converter._splitValue('0000000')
    Traceback (most recent call last):
      ...
    DateTimeConversionError: Numeric value given, but not parseable.
    >>> converter._splitValue('000000000')
    Traceback (most recent call last):
      ...
    DateTimeConversionError: Numeric value given, but not parseable.
    
    Insane input is accepted wherever possible
    >>> converter._splitValue('1 xyz 4 :_; 2008 foo bar baz')
    [1, 4, 2008]
    >>> converter._splitValue('1___4AEIOU2008')
    [1, 4, 2008]
    >>> converter._splitValue('aa123 _ bb789ll  ')
    [123, 789]
    
    Test the internal _timeMap() function.
    >>> converter._timeMap('H M')
    [0, 1]
    >>> converter._timeMap('M H')
    [1, 0]
    
    Test the internal _parseTime() function.
    Default return if senceless data given is '00:00'
    >>> converter._parseTime(None, 'en')
    [0, 0]
    >>> converter._parseTime(object(), 'en')
    [0, 0]
    >>> converter._parseTime('', 'en')
    [0, 0]
    
    Raise if invalid number of input parts is found
    >>> converter._parseTime('1, 2, 3', 'en')
    Traceback (most recent call last):
      ...
    DateTimeConversionError: Invalid number of parts for time.
    
    Now get a senceful time
    >>> converter._parseTime('10', 'en')
    [10, 0]
    >>> converter._parseTime('1030', 'en')
    [10, 30]
    >>> converter._parseTime('10:35', 'en')
    [10, 35]
    
    Test the internal _dateMap() function.
    >>> converter._dateMap('Y M D')
    [0, 1, 2]
    >>> converter._dateMap('D M Y')
    [2, 1, 0]
    >>> converter._dateMap('Y D M')
    [0, 2, 1]
    >>> converter._dateMap('M D Y')
    [2, 0, 1]
    
    Test the internal _splitDate() function.
    >>> converter._splitDate('20080201', converter._dateMap('Y M D'))
    [2008, 2, 1]
    >>> converter._splitDate('01022008', converter._dateMap('D M Y'))
    [2008, 2, 1]
    >>> converter._splitDate('02012008', converter._dateMap('M D Y'))
    [2008, 2, 1]
    
    
    Test the internal _parseDate() function.
    >>> converter._parseDate(None, 'en')
    Traceback (most recent call last):
      ...
    DateTimeConversionError: Invalid date input.
    >>> converter._parseDate(object(), 'en')
    Traceback (most recent call last):
      ...
    DateTimeConversionError: Invalid date input.
    >>> converter._parseDate('', 'en')
    Traceback (most recent call last):
      ...
    DateTimeConversionError: Invalid date input.
    >>> converter._parseDate('20080201', 'iso')
    [2008, 2, 1]
    >>> converter._parseDate('02012008', 'en')
    [2008, 2, 1]
    >>> converter._parseDate('01022008', 'de')
    [2008, 2, 1]
    >>> converter._parseDate('01', 'de') # this will fail next month
    [2008, 2, 1]
    >>> converter._parseDate('01', 'en') # this will fail next month
    [2008, 2, 1]
    >>> converter._parseDate('0102', 'de') # this will fail next year
    [2008, 2, 1]
    >>> converter._parseDate('0201', 'en') # this will fail next year
    [2008, 2, 1]
    >>> converter._parseDate('010208', 'de')
    [2008, 2, 1]
    >>> converter._parseDate('010210', 'de')
    [2010, 2, 1]
    >>> converter._parseDate('020110', 'en')
    [2010, 2, 1]
    >>> converter._parseDate('2 1 8', 'en')
    [2008, 2, 1]
    >>> converter._parseDate('1 2 8', 'de')
    [2008, 2, 1]
    >>> converter._parseDate('1 2 2007', 'de')
    [2007, 2, 1]
    >>> converter._parseDate('1 2 100', 'de')
    [100, 2, 1]
    >>> converter._parseDate('10 02 01 99', 'en')
    Traceback (most recent call last):
      ...
    DateTimeConversionError: Invalid number of parts for date.
    
    Test the public interface
    >>> converter.convert('1.1.08', time=None, tzinfo=None, locale='de')
    datetime.datetime(2008, 1, 1, 0, 0)
    >>> converter.convert('20080201')
    datetime.datetime(2008, 2, 1, 0, 0)
    >>> converter.convert('35.1.08', time=None, tzinfo=None, locale='de')
    Traceback (most recent call last):
      ...
    DateTimeConversionError: day is out of range for month
    
    """
    
    implements(IIntelliDateTime)
    
    _numbers = [str(n) for n in range(10)]
    
    def __init__(self, context):
        self.pattern = ILocalePattern(context)
    
    def convert(self, date, time=None, tzinfo=None, locale='iso'):
        datedefs = self._parseDate(date, locale)
        timedefs = self._parseTime(time, locale)
        datetimedefs = datedefs + timedefs
        kwargs = {
            'tzinfo': tzinfo,
        }
        try:
            return datetime(*datetimedefs, **kwargs)
        except ValueError, e:
            raise DateTimeConversionError(e)
    
    def _parseDate(self, date, locale):
        if not date or not type(date) in types.StringTypes:
            raise DateTimeConversionError(u"Invalid date input.")
        
        date = self._splitValue(date)
        pattern = self.pattern.date(locale)
        map = self._dateMap(pattern)
        if type(date) in types.StringTypes:
            return self._splitDate(date, map)
        
        if len(date) == 1:
            dt = datetime.now()
            return [dt.year, dt.month, date[0]]
        
        if len(date) == 2:
            dt = datetime.now()
            if map[1] == 1 and map[2] == 0:
                return [dt.year, date[1], date[0]]
            else:
                return [dt.year, date[0], date[1]]
        
        if len(date) == 3:
            year = str(date[map[0]])
            if len(year) in [3, 4]:
                return [int(year), date[map[1]], date[map[2]]]
            if len(year) == 1:
                year = '0%s' % year
            dt = datetime.now()
            year = int('%s%s' % (str(dt.year)[:2], year))
            return [year, date[map[1]], date[map[2]]]
        
        raise DateTimeConversionError(u"Invalid number of parts for date.")
    
    def _parseTime(self, time, locale):
        if not time or not type(time) in types.StringTypes:
            return [0, 0]
        
        time = self._splitValue(time)
        if len(time) not in [1, 2]:
            raise DateTimeConversionError(u"Invalid number of parts for time.")
        
        pattern = self.pattern.time(locale)
        map = self._timeMap(pattern)
        
        if len(time) == 1:
            return [time[0], 0]
        
        ret = [0, 0]
        for i in range(2):
            ret[i] = time[map[i]]
        return ret
    
    def _dateMap(self, pattern):
        pattern = pattern.split(' ')
        mapper = { 'y': 0, 'm': 1, 'd': 2, }
        map = [None, None, None]
        for i in range(3):
            map[mapper[pattern[i].lower()]] = i
        return map
    
    def _timeMap(self, pattern):
        pattern = pattern.split(' ')
        if pattern[0].lower() == 'h':
            return [0, 1]
        return [1, 0]
    
    def _splitDate(self, date, map):
        ret = list()
        for i in range(3):
            if i == 0 and map[0] > 1:
                start = map[0] * 2
                end = start + 4
            elif i == 0 and map[0] == 0:
                start = 0
                end = 4
            elif i != 0 and map[i] > map[0]:
                start = (map[i] -1) * 2 + 4
                end = start + 2
            else:
                start = map[i] * 2
                end = start + 2
            ret.append(int(date[start:end]))
        return ret
    
    def _splitValue(self, value):
        if not value or not type(value) in types.StringTypes:
            raise DateTimeConversionError(u"Empty value or unknown value type.")
        
        value = value.strip()
        if self._isNumeric(value):
            l = len(value)
            if l in [1, 2]:
                return [int(value)] # case D or H
            elif l == 4: # case MH, HM, DM, MD
                return [int(value[:2]), int(value[2:])]
            elif l == 6: # case DMY, MDY, YMD
                return [int(value[:2]), int(value[2:4]), int(value[4:])]
            elif l == 8: # any year case, return whole value
                return value
            raise DateTimeConversionError(u"Numeric value given, but not"
                                          " parseable.")
        parts = list()
        pointer = 0
        for i in range(len(value)):
            if not self._isNumeric(value[i]):
                parts.append(value[pointer:i])
                pointer = i + 1
        parts.append(value[pointer:])
        return [int(p) for p in parts if self._isNumeric(p.strip())]

    def _isNumeric(self, value):
        if not value or not type(value) in types.StringTypes:
            return False
         
        for c in value:
            if not c in self._numbers:
                return False
        return True
