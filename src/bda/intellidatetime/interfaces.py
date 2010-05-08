from zope.interface import Interface

class DateTimeConversionError(Exception): pass

class ILocalePattern(Interface):
    """Interface providing localized input date and time patterns.
    """
    
    def date(locale):
        """Return one of 3 possible patterns:
        
          * Y M D
          * D M Y
          * M D Y
        
        Y - Year
        M - Month
        D - Day
        
        @param locale - the locale string
        @return string - the date pattern
        """
    
    def time(locale):
        """Return one of two possible patterns:
        
          * H M
          * M H <- is this senceful??
        
        H - Hour
        M - Minute
        
        @param locale - the locale string
        @return string - the time pattern
        """

class IIntelliDateTime(Interface):
    """Interface for the datetime conversion.
    """
    
    def convert(date, time=None, tzinfo=None, locale='iso'):
        """Convert the input to a datetime object.
        
        The convert function accepts unicode or non-unicode strings and tries
        to parse out Date and Time information as follows:
          * First try to get the localized datetime pattern information
          * If no one is found, a default pattern is used.
          * Parse the input by the definitions of the localized datetime pattern
          * Create a datetime object and return it
        
        The 'intelligence' is defined by following behaviour:
        
        Date:
          * If only one value is found f.e. '1', this value is handled as the
            day value, for month and for year the current ones are used.
          * Respective, if two values are given, the are handled as day and
            month, year is autocompleted with the current year.
          * 3 values are a complete date information
          * as limiters are all non-numeric values accepted
          * date input can be done without limiters, therefor all characters
            must be numbers, and the string length must be either 2, 4, 6 or 8
            characters. 2 characters define the day, 4 characters the day and
            the month, 6 characters day, month and the year of the current
            century and 8characters define a complete date.
        
        Time:
          * If time is None, time is set to 00:00
          * if time is a 2-character string, it is handled as the hour, minutes
            are defined as 00
          * time input can be done without a limiter, therefor time must be an
            all numeric 4-character string, the first 2 chars are handled as
            hour, the second 2 chars as minute.
          * as limiter are all non-numeric values accepted
          * seconds are never computed and are therefor ALWAYS handled as '00'
        
        If parsing of the input values is not possible or converting the parsed
        values to numeric values is not possible or the valid date and time
        range falls out of scope, a DateTimeConversionError is raised.
        
        @param date - a date as string
        @param time - a time as string
        @param tzinfo - a tzinfo object to be considered, defaults to None
        @param locale - a locale name, which is used to determine the date and
                        time patterns. There exists a special locale named
                        'iso', define the input in ISO format which further is
                        used as default.
        @return datetime - datetime.datetime object
        @raise DateTimeConversionError - if conversion failes
        """