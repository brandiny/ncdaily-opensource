# -*- coding: utf-8 =*=
def is_ON_declaredbyuser():
    import json
    with open('static/json/app_status.json') as f:
        data = json.load(f)

        if data['appisON'] == True:
            return True
        
        else:
            return False

def is_weekend():
    # if weekend, true, else false
    import datetime
    return (datetime.date.today().weekday() == 5 or datetime.date.today().weekday() == 6)

def is_schooltime():
    # things to import
    import json
    import datetime
    import time
    try:
        os.environ["TZ"] = "Pacific/Auckland"
        time.tzset()
    except Exception as e:
        pass
    # open file
    with open('static/json/term_dates.json') as f:
        is_schooltime = False
        data = json.load(f)
        today =  (datetime.date.today().month, datetime.date.today().day)
        # print(data)
        # print(today)
        for term in data:
            start = tuple([int(i) for i in term['start'].split('/')][::-1])
            end = tuple([int(i) for i in term['end'].split('/')][::-1])
            # print(start, end)
            # print(start <= today and today <= end)
            if start <= today and today <= end:
                is_schooltime = True
                return is_schooltime

    # returns boolean.
    return is_schooltime


def insert_emails(emailArray):
    """Deletes all of the emails in such array"""
    pass


def change_termdates(term, dateStart, dateEnd):
    #things to import
    import json
    # Changes item in json file in static/json/term_dates.json
    # ...
    data = []

    # writes to data array
    with open('static/json/term_dates.json') as f:
        data = json.load(f)
        for d in data:
            if d['term'] == term:
                d['start'] = dateStart
                d['end'] = dateEnd

            else:
                continue

    # saves data array to json file
    with open('static/json/term_dates.json', 'w') as f:
        json.dump(data, f)

def holiday_startdate():
    import json
    import datetime


    data = ''

    # get todays date
    today =  (datetime.date.today().month, datetime.date.today().day)

    with open('static/json/term_dates.json') as f:
        data = json.load(f)
        for d in data:
            start = tuple([int(i) for i in d['start'].split('/')[::-1]])
            end = tuple([int(i) for i in d['end'].split('/')[::-1]])
            if start <= today and today <= end:
                return d['end']


    return False
    


def holiday_enddate():
    import json
    import datetime

    holidays = {}

    # define holiday variables.
    data = ''
    with open('static/json/term_dates.json') as f:
        data = json.load(f)
        for i in range(0, len(data) - 1):
            start = tuple([int(i) for i in data[i]['end'].split('/')][::-1]) 
            end = tuple([int(i) for i in data[i+1]['start'].split('/')][::-1]) 
            holidays['term' + str(i+1) + 'holidays'] = (start, end)



    # get todays date
    today =  (datetime.date.today().month, datetime.date.today().day)


    which_holiday = 0
    # get which holiday im in
    for holidaykey in holidays:
        holidayvalue = holidays[holidaykey]
        start = holidayvalue[0]
        end = holidayvalue[1]
 
        if start <= today and today <= end:
            which_holiday = int(holidaykey[4:-8]) + 1

    if today < tuple([int(i) for i in data[0]['start'].split('/')[::-1]]):
        return 'Wait till term 1 starts'

    if today > holidays['term3holidays'][1]:
        return 'Wait till next year'

    elif which_holiday == 0:
        return False

    else:
        app_turn_on_date = ''
        with open('static/json/term_dates.json') as f:
            data = json.load(f)
            for d in data:
                if d['term'] == which_holiday:
                    app_turn_on_date = d['start']
                
        return app_turn_on_date

if __name__ == '__main__':
    print('IS schooltime:', is_schooltime())