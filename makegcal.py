""" makegcal.py - contains the Google Calendar Link building function """

import datetime


def nzst_or_nzdt():
    """Returns NZST if nzst, otherwise NZDT if nzdt"""
    if True:
        return 'NZST'
    else:
        return 'NZDT'


def remove_spaces(string):
    """ Substitutes spaces for %20 which can be encoded properly in url """
    return '%20'.join(string.split(' '))


def urlify(datetime_tuple, title, location='', details=''):
    """
    urlify - returns string of Google Calendar link to an event

    parameters:
        datetime_tuple: (start, end) both datetime objects
        title: string
        location: string

    returns: string
    """

    datetime_start = datetime_tuple[0]
    datetime_end = datetime_tuple[1]
    string = 'http://www.google.com/calendar/event?action=TEMPLATE&dates={eightdigitdate}T{sixdigittimeUTC}Z%2F{eightdigitdate}T{sixdigittimeUTCend}Z&text={title}&location={location}&details='

    # Formats the date 1 day prior in YYYYMMDD format
    YYMMDD = str(datetime_start - datetime.timedelta(days=1))
    YYMMDD = YYMMDD.split(' ')[0]
    YYMMDD  = ''.join(YYMMDD.split('-'))

    # Google will subtract 11 or 12  hour_starts off our NZDT time to give UTC
    # Thus, we add hour_starts to cushion this
    # But first, check for daylight savings.
    if nzst_or_nzdt() == 'NZST':
        offset = 12
    else:
        offset = 11

    hour_start = int(datetime_start.hour) + offset
    if hour_start >= 24:
        YYMMDD = YYMMDD[:-1] + str(int(YYMMDD[-1]) + 1)
        hour_start %= 24

    minute_start = int(datetime_start.minute)

    hour_end = int(datetime_end.hour) + offset
    if hour_end >= 24:
        hour_end %= 24

    minute_end = int(datetime_end.minute)

    timestart = '{:02}{:02}{:02}'.format(hour_start, minute_start, 0)
    timeend = '{:02}{:02}{:02}'.format(hour_end, minute_end, 0)

    # Substitutes all of the parameters into the template.
    string = string.format(
        eightdigitdate=YYMMDD,
        sixdigittimeUTC=timestart.strip(),
        sixdigittimeUTCend=timeend.strip(),
        location=remove_spaces(location),
        details=remove_spaces(details),
        title=title)


    return string


# Debug template
if __name__ == '__main__':
    print(urlify((datetime.datetime(2020, 6, 24, 12, 0), datetime.datetime(2020, 6, 24, 12, 15)), 'debug', location='debug logcation'))