Datetime converter
==================

Locale pattern
--------------

.. code-block:: pycon

    >>> from bda.intellidatetime import LocalePattern
    >>> pattern = LocalePattern()
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


Converter
---------

Get The IntelliDateTime converter:

.. code-block:: pycon

    >>> from bda.intellidatetime import IntelliDateTime
    >>> converter = IntelliDateTime()
    >>> converter
    <bda.intellidatetime.converter.IntelliDateTime object at ...>

Check if Interface implementation fits the definitions:

.. code-block:: pycon

    >>> from bda.intellidatetime import IIntelliDateTime
    >>> from zope.interface.verify import verifyObject
    >>> verifyObject(IIntelliDateTime, converter)
    True

Test the internal _isNumeric() function:

.. code-block:: pycon

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

Test the internal _splitValue() function:

.. code-block:: pycon

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

Special case whole year:

.. code-block:: pycon

    >>> converter._splitValue('01012008')
    '01012008'

Cases when numeric values break:

.. code-block:: pycon

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

Insane input is accepted wherever possible:

.. code-block:: pycon

    >>> converter._splitValue('1 xyz 4 :_; 2008 foo bar baz')
    [1, 4, 2008]

    >>> converter._splitValue('1___4AEIOU2008')
    [1, 4, 2008]

    >>> converter._splitValue('aa123 _ bb789ll  ')
    [123, 789]

Test the internal _timeMap() function:

.. code-block:: pycon

    >>> converter._timeMap('H M')
    [0, 1]

    >>> converter._timeMap('M H')
    [1, 0]

Test the internal _parseTime() function. Default return if senceless data
given is '00:00':

.. code-block:: pycon

    >>> converter._parseTime(None, 'en')
    [0, 0]

    >>> converter._parseTime(object(), 'en')
    [0, 0]

    >>> converter._parseTime('', 'en')
    [0, 0]

Raise if invalid number of input parts is found:

.. code-block:: pycon

    >>> converter._parseTime('1, 2, 3', 'en')
    Traceback (most recent call last):
      ...
    DateTimeConversionError: Invalid number of parts for time.

Now get a senceful time:

.. code-block:: pycon

    >>> converter._parseTime('10', 'en')
    [10, 0]

    >>> converter._parseTime('1030', 'en')
    [10, 30]

    >>> converter._parseTime('10:35', 'en')
    [10, 35]

Test the internal _dateMap() function:

.. code-block:: pycon

    >>> converter._dateMap('Y M D')
    [0, 1, 2]

    >>> converter._dateMap('D M Y')
    [2, 1, 0]

    >>> converter._dateMap('Y D M')
    [0, 2, 1]

    >>> converter._dateMap('M D Y')
    [2, 0, 1]

Test the internal _splitDate() function:

.. code-block:: pycon

    >>> converter._splitDate('20080201', converter._dateMap('Y M D'))
    [2008, 2, 1]

    >>> converter._splitDate('01022008', converter._dateMap('D M Y'))
    [2008, 2, 1]

    >>> converter._splitDate('02012008', converter._dateMap('M D Y'))
    [2008, 2, 1]

Test the internal _parseDate() function:

.. code-block:: pycon

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

    >>> from datetime import datetime
    >>> this_month = datetime.now().month
    >>> this_year = datetime.now().year
    >>> converter._parseDate('20080201', 'iso')
    [2008, 2, 1]

    >>> converter._parseDate('02012008', 'en')
    [2008, 2, 1]

    >>> converter._parseDate('01022008', 'de')
    [2008, 2, 1]

    >>> converter._parseDate('01022008', 'cs')
    [2008, 2, 1]

    >>> converter._parseDate('01', 'de') == [this_year, this_month, 1]
    True

    >>> converter._parseDate('01', 'en') == [this_year, this_month, 1]
    True

    >>> converter._parseDate('0102', 'de') == [this_year, 2, 1]
    True

    >>> converter._parseDate('0201', 'en') == [this_year, 2, 1]
    True

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

Test the public interface:

.. code-block:: pycon

    >>> converter.convert('1.1.08', time=None, tzinfo=None, locale='de')
    datetime.datetime(2008, 1, 1, 0, 0)

    >>> converter.convert('5.1.08', time=None, tzinfo=None, locale='cs')
    datetime.datetime(2008, 1, 5, 0, 0)

    >>> converter.convert('20080201')
    datetime.datetime(2008, 2, 1, 0, 0)

    >>> converter.convert('35.1.08', time=None, tzinfo=None, locale='de')
    Traceback (most recent call last):
      ...
    DateTimeConversionError: day is out of range for month

Convenience convert function
----------------------------

.. code-block:: pycon

    >>> from bda.intellidatetime import convert
    >>> convert('1.1.08', locale='de')
    datetime.datetime(2008, 1, 1, 0, 0)
