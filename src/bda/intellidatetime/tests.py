from bda.intellidatetime import DateTimeConversionError
from bda.intellidatetime import IIntelliDateTime
from bda.intellidatetime import IntelliDateTime
from bda.intellidatetime import LocalePattern
from bda.intellidatetime import convert
from datetime import datetime
from zope.interface.verify import verifyObject
import unittest


class TestIntellidatetime(unittest.TestCase):

    def expect_error(self, exc, func, *args, **kw):
        try:
            func(*args, **kw)
        except exc as e:
            return e
        else:
            msg = 'Expected \'{}\' when calling \'{}\''.format(exc, func)
            raise Exception(msg)

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
        err = self.expect_error(
            DateTimeConversionError,
            converter._splitValue,
            None
        )
        self.assertEqual(str(err), 'Empty value or unknown value type.')
        err = self.expect_error(
            DateTimeConversionError,
            converter._splitValue,
            object()
        )
        self.assertEqual(str(err), 'Empty value or unknown value type.')
        err = self.expect_error(
            DateTimeConversionError,
            converter._splitValue,
            ''
        )
        self.assertEqual(str(err), 'Empty value or unknown value type.')
        self.assertEqual(converter._splitValue(' 1   '), [1])
        self.assertEqual(converter._splitValue('1 2'), [1, 2])
        self.assertEqual(converter._splitValue('1 2 3'), [1, 2, 3])
        self.assertEqual(converter._splitValue('0101'), [1, 1])
        self.assertEqual(converter._splitValue('010101'), [1, 1, 1])
        self.assertEqual(converter._splitValue('1, 2, 3'), [1, 2, 3])
        # Special case whole year
        self.assertEqual(converter._splitValue('01012008'), '01012008')
        # Cases when numeric values break
        err = self.expect_error(
            DateTimeConversionError,
            converter._splitValue,
            '000'
        )
        self.assertEqual(str(err), 'Numeric value given, but not parseable.')
        err = self.expect_error(
            DateTimeConversionError,
            converter._splitValue,
            '00000'
        )
        self.assertEqual(str(err), 'Numeric value given, but not parseable.')
        err = self.expect_error(
            DateTimeConversionError,
            converter._splitValue,
            '0000000'
        )
        self.assertEqual(str(err), 'Numeric value given, but not parseable.')
        err = self.expect_error(
            DateTimeConversionError,
            converter._splitValue,
            '000000000'
        )
        self.assertEqual(str(err), 'Numeric value given, but not parseable.')
        # Insane input is accepted wherever possible
        self.assertEqual(
            converter._splitValue('1 xyz 4 :_; 2008 foo bar baz'),
            [1, 4, 2008]
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
        err = self.expect_error(
            DateTimeConversionError,
            converter._parseTime,
            '1, 2, 3',
            'en'
        )
        self.assertEqual(str(err), 'Invalid number of parts for time.')
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
            converter._splitDate('20080201', converter._dateMap('Y M D')),
            [2008, 2, 1]
        )
        self.assertEqual(
            converter._splitDate('01022008', converter._dateMap('D M Y')),
            [2008, 2, 1]
        )
        self.assertEqual(
            converter._splitDate('02012008', converter._dateMap('M D Y')),
            [2008, 2, 1]
        )

    def test_converter_parse_date(self):
        converter = IntelliDateTime()
        err = self.expect_error(
            DateTimeConversionError,
            converter._parseDate,
            None,
            'en'
        )
        self.assertEqual(str(err), 'Invalid date input.')
        err = self.expect_error(
            DateTimeConversionError,
            converter._parseDate,
            object(),
            'en'
        )
        self.assertEqual(str(err), 'Invalid date input.')
        err = self.expect_error(
            DateTimeConversionError,
            converter._parseDate,
            '',
            'en'
        )
        self.assertEqual(str(err), 'Invalid date input.')
        self.assertEqual(converter._parseDate('20080201', 'iso'), [2008, 2, 1])
        self.assertEqual(converter._parseDate('02012008', 'en'), [2008, 2, 1])
        self.assertEqual(converter._parseDate('01022008', 'de'), [2008, 2, 1])
        self.assertEqual(converter._parseDate('01022008', 'cs'), [2008, 2, 1])
        this_month = datetime.now().month
        this_year = datetime.now().year
        self.assertTrue(
            converter._parseDate('01', 'de') == [this_year, this_month, 1]
        )
        self.assertTrue(
            converter._parseDate('01', 'en') == [this_year, this_month, 1]
        )
        self.assertTrue(converter._parseDate('0102', 'de') == [this_year, 2, 1])
        self.assertTrue(converter._parseDate('0201', 'en') == [this_year, 2, 1])
        self.assertEqual(converter._parseDate('010208', 'de'), [2008, 2, 1])
        self.assertEqual(converter._parseDate('010210', 'de'), [2010, 2, 1])
        self.assertEqual(converter._parseDate('020110', 'en'), [2010, 2, 1])
        self.assertEqual(converter._parseDate('2 1 8', 'en'), [2008, 2, 1])
        self.assertEqual(converter._parseDate('1 2 8', 'de'), [2008, 2, 1])
        self.assertEqual(converter._parseDate('1 2 2007', 'de'), [2007, 2, 1])
        self.assertEqual(converter._parseDate('1 2 100', 'de'), [100, 2, 1])
        err = self.expect_error(
            DateTimeConversionError,
            converter._parseDate,
            '10 02 01 99',
            'en'
        )
        self.assertEqual(str(err), 'Invalid number of parts for date.')

    def test_converter_convert(self):
        converter = IntelliDateTime()
        self.assertEqual(
            converter.convert('1.1.08', time=None, tzinfo=None, locale='de'),
            datetime(2008, 1, 1, 0, 0)
        )
        self.assertEqual(
            converter.convert('5.1.08', time=None, tzinfo=None, locale='cs'),
            datetime(2008, 1, 5, 0, 0)
        )
        self.assertEqual(
            converter.convert('20080201'),
            datetime(2008, 2, 1, 0, 0)
        )
        err = self.expect_error(
            DateTimeConversionError,
            converter.convert,
            '35.1.08',
            time=None,
            tzinfo=None,
            locale='de'
        )
        self.assertEqual(str(err), 'day is out of range for month')

    def test_convert(self):
        self.assertEqual(
            convert('1.1.08', locale='de'),
            datetime(2008, 1, 1, 0, 0)
        )


if __name__ == '__main__':
    unittest.main()
