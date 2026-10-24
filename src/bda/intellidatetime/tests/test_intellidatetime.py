from bda.intellidatetime import convert
from bda.intellidatetime import DateTimeConversionError
from bda.intellidatetime import IIntelliDateTime
from bda.intellidatetime import IntelliDateTime
from bda.intellidatetime import LocalePattern
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from datetime import tzinfo
from zope.interface.verify import verifyObject
import unittest


class PytzLikeTimezone(tzinfo):
    """Timezone providing the ``normalize`` API of pytz timezones."""

    def __init__(self, normalized_tzinfo):
        self.normalized_tzinfo = normalized_tzinfo

    def normalize(self, dt):
        return dt.replace(tzinfo=self.normalized_tzinfo)


class TestIntellidatetime(unittest.TestCase):
    def assertConversionError(self, message, func, *args, **kw):
        with self.assertRaises(DateTimeConversionError) as cm:
            func(*args, **kw)
        self.assertEqual(str(cm.exception), message)

    def test_locale_pattern(self):
        pattern = LocalePattern()
        self.assertEqual(pattern.date(None), 'Y M D')
        self.assertEqual(pattern.time(None), 'H M')
        self.assertEqual(pattern.date('de'), 'D M Y')
        self.assertEqual(pattern.time('de'), 'H M')

    def test_converter_interface_verify(self):
        converter = IntelliDateTime()
        self.assertTrue(verifyObject(IIntelliDateTime, converter))

    def test_converter_is_numeric(self):
        converter = IntelliDateTime()
        self.assertFalse(converter._isNumeric(None))
        self.assertFalse(converter._isNumeric(object()))
        self.assertFalse(converter._isNumeric('1234567890abcdefg'))
        self.assertFalse(converter._isNumeric('1 2 3'))
        self.assertFalse(converter._isNumeric(''))
        self.assertTrue(converter._isNumeric('1234567890'))

    def test_converter_split_value(self):
        converter = IntelliDateTime()
        message = 'Empty value or unknown value type.'
        self.assertConversionError(message, converter._splitValue, None)
        self.assertConversionError(message, converter._splitValue, object())
        self.assertConversionError(message, converter._splitValue, '')
        self.assertEqual(converter._splitValue(' 1   '), [1])
        self.assertEqual(converter._splitValue('1 2'), [1, 2])
        self.assertEqual(converter._splitValue('1 2 3'), [1, 2, 3])
        self.assertEqual(converter._splitValue('0101'), [1, 1])
        self.assertEqual(converter._splitValue('010101'), [1, 1, 1])
        self.assertEqual(converter._splitValue('1, 2, 3'), [1, 2, 3])
        # Special case whole year
        self.assertEqual(converter._splitValue('01012008'), '01012008')
        # Cases when numeric values break
        message = 'Numeric value given, but not parseable.'
        self.assertConversionError(message, converter._splitValue, '000')
        self.assertConversionError(message, converter._splitValue, '00000')
        self.assertConversionError(message, converter._splitValue, '0000000')
        self.assertConversionError(message, converter._splitValue, '000000000')
        # Insane input is accepted wherever possible
        self.assertEqual(
            converter._splitValue('1 xyz 4 :_; 2008 foo bar baz'), [1, 4, 2008]
        )
        self.assertEqual(converter._splitValue('1___4AEIOU2008'), [1, 4, 2008])
        self.assertEqual(converter._splitValue('aa123 _ bb789ll  '), [123, 789])

    def test_converter_time_map(self):
        converter = IntelliDateTime()
        self.assertEqual(converter._timeMap('H M'), [0, 1])
        self.assertEqual(converter._timeMap('M H'), [1, 0])

    def test_converter_parse_time(self):
        converter = IntelliDateTime()
        # Default returned if senceless data given is '00:00'
        self.assertEqual(converter._parseTime(None, 'en'), [0, 0])
        self.assertEqual(converter._parseTime(object(), 'en'), [0, 0])
        self.assertEqual(converter._parseTime('', 'en'), [0, 0])
        # Raise if invalid number of input parts is found
        self.assertConversionError(
            'Invalid number of parts for time.', converter._parseTime, '1, 2, 3', 'en'
        )
        # Now get a senceful time
        self.assertEqual(converter._parseTime('10', 'en'), [10, 0])
        self.assertEqual(converter._parseTime('1030', 'en'), [10, 30])
        self.assertEqual(converter._parseTime('10:35', 'en'), [10, 35])

    def test_converter_date_map(self):
        converter = IntelliDateTime()
        self.assertEqual(converter._dateMap('Y M D'), [0, 1, 2])
        self.assertEqual(converter._dateMap('D M Y'), [2, 1, 0])
        self.assertEqual(converter._dateMap('Y D M'), [0, 2, 1])
        self.assertEqual(converter._dateMap('M D Y'), [2, 0, 1])

    def test_converter_split_date(self):
        converter = IntelliDateTime()
        self.assertEqual(
            converter._splitDate('20080201', converter._dateMap('Y M D')), [2008, 2, 1]
        )
        self.assertEqual(
            converter._splitDate('01022008', converter._dateMap('D M Y')), [2008, 2, 1]
        )
        self.assertEqual(
            converter._splitDate('02012008', converter._dateMap('M D Y')), [2008, 2, 1]
        )

    def test_converter_parse_date(self):
        converter = IntelliDateTime()
        message = 'Invalid date input.'
        self.assertConversionError(message, converter._parseDate, None, 'en')
        self.assertConversionError(message, converter._parseDate, object(), 'en')
        self.assertConversionError(message, converter._parseDate, '', 'en')
        self.assertEqual(converter._parseDate('20080201', 'iso'), [2008, 2, 1])
        self.assertEqual(converter._parseDate('02012008', 'en'), [2008, 2, 1])
        self.assertEqual(converter._parseDate('01022008', 'de'), [2008, 2, 1])
        self.assertEqual(converter._parseDate('01022008', 'cs'), [2008, 2, 1])
        this_month = datetime.now().month
        this_year = datetime.now().year
        self.assertEqual(converter._parseDate('01', 'de'), [this_year, this_month, 1])
        self.assertEqual(converter._parseDate('01', 'en'), [this_year, this_month, 1])
        self.assertEqual(converter._parseDate('0102', 'de'), [this_year, 2, 1])
        self.assertEqual(converter._parseDate('0201', 'en'), [this_year, 2, 1])
        self.assertEqual(converter._parseDate('010208', 'de'), [2008, 2, 1])
        self.assertEqual(converter._parseDate('010210', 'de'), [2010, 2, 1])
        self.assertEqual(converter._parseDate('020110', 'en'), [2010, 2, 1])
        self.assertEqual(converter._parseDate('2 1 8', 'en'), [2008, 2, 1])
        self.assertEqual(converter._parseDate('1 2 8', 'de'), [2008, 2, 1])
        self.assertEqual(converter._parseDate('1 2 2007', 'de'), [2007, 2, 1])
        self.assertEqual(converter._parseDate('1 2 100', 'de'), [100, 2, 1])
        self.assertConversionError(
            'Invalid number of parts for date.',
            converter._parseDate,
            '10 02 01 99',
            'en',
        )

    def test_converter_convert(self):
        converter = IntelliDateTime()
        self.assertEqual(
            converter.convert('1.1.08', time=None, tzinfo=None, locale='de'),
            datetime(2008, 1, 1, 0, 0),
        )
        self.assertEqual(
            converter.convert('5.1.08', time=None, tzinfo=None, locale='cs'),
            datetime(2008, 1, 5, 0, 0),
        )
        self.assertEqual(converter.convert('20080201'), datetime(2008, 2, 1, 0, 0))
        with self.assertRaises(DateTimeConversionError) as cm:
            converter.convert('35.1.08', time=None, tzinfo=None, locale='de')
        # The message of the ``ValueError`` raised by ``datetime`` is passed
        # through. Its wording depends on the Python version.
        self.assertIn('day', str(cm.exception))

    def test_converter_convert_normalizes_tzinfo(self):
        # The given time is kept, only the tzinfo is replaced by the
        # normalized (DST aware) one of the timezone.
        cest = timezone(timedelta(hours=2), 'CEST')
        converter = IntelliDateTime()
        dt = converter.convert(
            '1.7.08', time='10:30', tzinfo=PytzLikeTimezone(cest), locale='de'
        )
        self.assertEqual(dt, datetime(2008, 7, 1, 10, 30, tzinfo=cest))
        self.assertIs(dt.tzinfo, cest)

    def test_convert(self):
        self.assertEqual(convert('1.1.08', locale='de'), datetime(2008, 1, 1, 0, 0))
