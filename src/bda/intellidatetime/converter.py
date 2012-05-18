import types
from datetime import datetime
from zope.interface import implementer
from bda.intellidatetime.interfaces import (
    DateTimeConversionError,
    ILocalePattern,
    IIntelliDateTime,
)


def convert(date, time=None, tzinfo=None, locale='iso'):
    return IntelliDateTime().convert(date, time, tzinfo, locale)


@implementer(ILocalePattern)
class LocalePattern(object):
    """See interfaces.ILocalePattern.
    
    XXX: complete the language codes
    """
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
    
    for locale in ['de', 'de-de', 'de-at', 'de-ch',
                   'es', 'fr', 'uk', 'it', 'cs']:
        PATTERNS['date'][locale] = __date_II
    
    for locale in ['en']:
        PATTERNS['date'][locale] = __date_III
    
    for locale in ['iso', 'en', 'de', 'de-de', 'de-at', 'de-ch', 
                   'es', 'fr', 'uk', 'it', 'cs']:
        PATTERNS['time'][locale] = __time_I
    
    def __init__(self, context=None):
        """BBB signature.
        """
        pass
    
    def date(self, locale):
        return self.PATTERNS['date'].get(locale, self.__date_I)
    
    def time(self, locale):
        return self.PATTERNS['time'].get(locale, self.__time_I)


@implementer(IIntelliDateTime)
class IntelliDateTime(object):
    """See interfaces.IIntelliDateTime.
    """
    _numbers = [str(n) for n in range(10)]
    
    def __init__(self, context=None):
        """BBB context kwarg.
        """
        self.pattern = LocalePattern()
    
    def convert(self, date, time=None, tzinfo=None, locale='iso'):
        datedefs = self._parseDate(date, locale)
        timedefs = self._parseTime(time, locale)
        datetimedefs = datedefs + timedefs
        kwargs = {'tzinfo': tzinfo }
        try:
            dt = datetime(*datetimedefs, **kwargs)
        except ValueError, e:
            raise DateTimeConversionError(e)
        if tzinfo:
            # set to normalized tz (in case of DST), keep input in tz and DST
            # aware time -> dont add one hour
            dt = dt.replace(tzinfo=tzinfo.normalize(dt).tzinfo)
        return dt
    
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