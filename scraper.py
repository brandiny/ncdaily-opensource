""" scraper.py
Handles the webscraping of the app.

Key variables
    - scraper.archive == Array of the titles of old notices
    - scraper.notices_5 == Array of Meetings/Practices (has ALL INFORMATION)
    - scraper.notices_3 == Array of Notices (has ALL INFORMATION BUT date and location)

Each is explained further below
"""

import datetime                     # datetime: so we can rewind -1 days to find yesterdays stuff.
import requests                     # requests: access URLs and download source
from bs4 import BeautifulSoup       # bs4: HTML parser - access tags
import dateformatter                # contains the daily scraped date formatted into a sentence


# INITIAL VARIABLES
URL = 'https://parents.newlands.school.nz/index.php/notices'                # URL to notices of the school
URL_PAST = URL + '/' + str(dateformatter.dt - datetime.timedelta(days=1))   # URL to yesterdays notices

PAGE = requests.get(URL)                                                    # download source
SOUP = BeautifulSoup(PAGE.text, 'html.parser')                              # todays notices as bs4 soup object
SOUP_OLD = BeautifulSoup(requests.get(URL_PAST).text, 'html.parser')        # yesterday's notices as bs4 soup object


# PROCESSING OF TODAY'S NOTICES
TR_SOUP = SOUP.find_all('tr')        # Finds all the <table row> tags in the given page
'''
Notices format:

********TYPE #1:************** <td> elements: 5
<tr>
    <td>                $who is this notice for </td>
    <td>                $title of the notice    </td>
    <td>                $where is this event    </td>
    <td>                $when is it             </td>
    <td>                $who wrote this notice  </td>
</tr>

        Succeded by...
<tr>
    <td>  $description of the notice  </td>
</tr>

********TYPE #2:************** td elements: 3
<tr>
    <td>                $who is this notice for </td>
    <td>                $title of the notice    </td>
    <td>                $who wrote this notice  </td>
</tr>

        followed by...
<tr>
    <td>  $description of the notice  </td>
</tr>

Hence, the HTML is parsed by the number of td elements, which determines the notice type, I or II
'''

notices_5 = []          # Array to hold 5 td element notices
notices_3 = []          # Array to hold 3 td element notices

td_count = 0            # Counts the number of td elements iterated over
for tr in TR_SOUP:
    # Extract all <td> from the table
    td = tr.find_all('td')

    # If the table empty, pass over it
    if len(td) == 0:
        continue

    # If the table has 5 elements, it is a 5td notice
    elif len(td) == 5:
        notices_5.append([i.text for i in td])
        td_count = 5

    # If the table has 3 elements, it is a 3td notice
    elif len(td) == 3:
        notices_3.append([i.text for i in td])
        td_count = 3

    # If the table has 1 element, it must be the description, hence we add to either notices3/5
    elif len(td) == 1:
        td = str(list(td)[0])  # Turns it into a string

        # If there have been 5 prev <td> elements, it is a descriptor of a 5_td_element notice, hence goes into 5notices
        # the list slicing from 15/16 --> 16 is to remove the <td></td> tags
        if td_count == 5:
            notices_5[-1].append(td[16:-16])

        # If there have been 3 prev <td> elements, it is a descriptor of a 3_td_element notice, hence goes into 3notices
        elif td_count == 3:
            notices_3[-1].append(td[15:-16])


"""PROCESSING OF YESTERDAY'S NOTICES"""
TR_SOUP_OLD = SOUP_OLD.find_all('tr')
notices_5_old, notices_3_old = [], []
td_count = 0

# This is processed the same way as Today's notices -- read the ABOVE section for documentation
for tr in TR_SOUP_OLD:
    td = tr.find_all('td')
    if len(td) == 0:
        continue

    elif len(td) == 5:
        notices_5_old.append([i.text for i in td])
        td_count = 5

    elif len(td) == 3:
        notices_3_old.append([i.text for i in td])
        td_count = 3

    elif len(td) == 1:
        td = str(list(td)[0])
        if td_count == 5:
            notices_5_old[-1].append(td[16:-16])
        elif td_count == 3:
            notices_3_old[-1].append(td[15:-16])


# Only contains titles of the old notices -- no other info needed to check duplicity.
archive = set([i[1].lower() for i in notices_3_old] + [i[1].lower() for i in notices_5_old])


# Debug Content
if __name__ == '__main__':
    print('Notices 5: ')
    for i in notices_5:
        print(i)


    print('\nNotices 3: ')
    for i in notices_3:
        print(i)

    print('Notices old:', archive)
