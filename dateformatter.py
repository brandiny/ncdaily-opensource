# -*- coding: utf-8 -*-
"""
dateformatter.py - Contains formatted strings of the date - formatted or short

- Formatted format example: 'Tuesday, 16th of June - NC Notices'
- Short format example: 'Tue, Jun 16'

These are accessed with:
- dateformatter.dateformatted
- dateformatter.short
"""

import datetime
import time
import os

# Sets the file timezone to Pacific/Auckland
try:
    os.environ["TZ"] = "Pacific/Auckland"
    time.tzset()
except Exception as e:
    pass

# Tuple of weekdays, starting from index 0, e.g. weekdays[0] == Monday
weekdays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
weekdays_short = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

# Tuple of months, starting from index 0, e.g months[0] == Jan
months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')


suffix = ''                     # Basically, what the day ends in; 1st, 2nd, etc
dt = datetime.date.today()      # Datetime object with today's attributes. E.g. dt.day == today's date


# Formats the day prefix
if 4 <= dt.day <= 20 or 24 <= dt.day <= 30:
    # Days 4/5/.../20 end in th. Furthermore, 24/25/.../30 also end in th
    suffix = "th"

else:
    # Days 1/2/3 and 21/22/23 end in st/nd/rd, respectively
    suffix = ["st", "nd", "rd"][dt.day % 10 - 1]


# dateshort: e.g. 'Tue, Jun 17'
dateshort = '{WEEKDAY}, {MONTH} {NUM_DAY}'.format(\
    NUM_DAY=dt.day,
    MONTH=months[int(dt.month) - 1],
    WEEKDAY=weekdays[dt.weekday()]
)


# dateformatted: e.g Tuesday, Jun 16 -- NC Notices
dateformatted = '{WEEKDAY}, {MONTH} {NUM_DAY}{SUFFIX} {emdash} NC Notices'.format(\
    NUM_DAY=dt.day,
    SUFFIX=suffix,
    MONTH=months[int(dt.month) - 1],
    WEEKDAY=weekdays[dt.weekday()],
    emdash='-')


def makenumericdate(string):
    """ Example input: Wed 17 Jun Period 2 """
    """ Turns the notice's time and date into a Datetime Object """

    string = string.split(' ')
    # Time is a string that has had its SPACES removed and LOWERCASE
    time = ''.join([i.lower() for i in string[3:]])
    time = time.replace(':', '.')

    try:
        # If lunchtime in it
        if 'lunch' in time:
            if string[0].lower() == 'thu':
                start_time = [13, 20, 00] # special lunch start , later on thur
                end_time = [13, 35, 00]
            else:
                start_time = [13, 00, 00] # lunch start
                end_time = [13, 15, 00]

                # interval
        elif 'interval' in time:
            if string[0].lower() == 'thu':
                start_time = [11, 00, 00] # special lunch start , later on thur
                end_time = [11, 15, 00]
            else:
                start_time = [10, 40, 00] # lunch start
                end_time = [10, 55, 00]

        # see notes
        elif 'notes' in time or time == '':
            start_time = [8, 00, 00]
            end_time = [8, 15, 00]

        # dash separated condition
        elif '-' in time or 'to' in time:
            if '-' in time:
                time = [i.strip() for i in time.split('-')]

            if 'to' in time:
                time = [i.strip() for i in time.split('to')]

            start_time = time[0]
            end_time = time[1]

            """START TIME PROCESSING"""
            # pm case
            if 'pm' in start_time:
                start_time = float(start_time.strip('pm')) + 12

            # am case
            elif 'am' in start_time:
                start_time = float(start_time.strip('am'))

            # if not pm/am given, predict it using School intervals
            else:
                start_time = float(start_time)
                if (start_time > 1 and start_time < 7):
                    start_time += 12

                else:
                    start_time = start_time

            """END TIME PROCESSING"""
            # pm case
            if 'pm' in end_time:
                end_time = float(end_time.strip('pm')) + 12

            # am case
            elif 'am' in end_time:
                end_time = float(end_time.strip('am'))

            # if not pm/am given, predict it using School intervals
            else:
                end_time = float(end_time)
                if (end_time > 1 and end_time < 7):
                    end_time += 12

                else:
                    end_time = end_time

        # no dash processing
        else:
            start_time = time

            """START TIME PROCESSING"""
            # pm case
            if 'pm' in start_time:
                if float(start_time.strip('pm')) == 12:
                    start_time = float(start_time.strip('pm'))

                else:
                    start_time = float(start_time.strip('pm')) + 12

            # am case
            elif 'am' in start_time:
                start_time = float(start_time.strip('am'))

            # if not pm/am given, predict it using School intervals
            else:
                start_time = float(start_time)
                if (start_time > 1 and start_time < 7):
                    start_time += 12

                else:
                    start_time = start_time

            if start_time + 0.15 - int(start_time) >= 0.598:
                end_time = int(start_time) + 1 + (start_time - int(start_time) + 0.15 - 0.6)

            else:
                end_time = start_time + 0.15

    # If all fails
    except Exception:
        start_time = 8.40 
        end_time = 8.55

    # converts decimals to times as current start_time and end_time are in form
    # 13.4 = 1340 time
    try:
        start_time = '{0:.2f}'.format(start_time)
        end_time = '{0:.2f}'.format(end_time)

        start_time = [int(i) for i in str(start_time).split(".")]
        end_time = [int(i) for i in str(end_time).split(".")]

        start_time.append(0)
        end_time.append(0)

    except:
        start_time = [8, 40, 0]
        end_time = [8, 55, 0]

    # Numeric Date, 12, 21 etc
    date = string[1]

    # Short Month, Jun, Jul etc.
    month = string[2]
    month = '{:02d}'.format(months.index(month) + 1)    # Turns it into numeric 2 digit MINIMUM

    # Turns it into numeric 2 digit MINIMUM
    date = '{:02d}'.format(int(date))


    # IF no time, just return datetime object with 00:00:00 time
    try:
        return datetime.datetime(2020, int(month), int(date), *start_time), datetime.datetime(2020, int(month), int(date), *end_time)

    except:
        return datetime.datetime(2020, int(month), int(date)), datetime.datetime(2020, int(month), int(date))


# Debug content
if __name__ == '__main__':
    print('Date Short:', dateshort)
    print('Date Formatted: ', dateformatted)
    print(makenumericdate('Wed 24 Jun 8.50am'))
