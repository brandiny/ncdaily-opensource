# -*- coding: utf-8 -*-

import datetime
from string import Template
import json
import random
from premailer import transform
import logging

# CUSTOM MODULES
import scraper  # scrapes the raw tags
import dateformatter  # formats the date in a readable manner
import makegcal  # creates the google calendar link


# GENERATE QUOTE OF THE DAY
with open('static/json/quotes.json') as json_file:
    quotes = json.load(json_file)
    qod = random.choice(quotes)

    # QOD = quote of the day , string
    if qod['quoteAuthor'] == '':
        qod = '"{quoteText}" - {quoteAuthor}'.format(quoteText=qod['quoteText'], quoteAuthor='Anon')
    else:
        qod = '"{quoteText}" - {quoteAuthor}'.format(quoteText=qod['quoteText'], quoteAuthor=qod['quoteAuthor'])
        
# LIST OF YESTERDAY NOTICES [TITLES]
archive = scraper.archive

# MAIN HTML MESSAGE, to be joined together at the end
html_message = []

# OPENS TEMPLATE.HTML to source code
html_message.append('''<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400&display=swap" rel="stylesheet">
	<style type="text/css">
	#body{font-family: Arial; max-width: 650px; margin:0 auto;padding:0}
    u + #body a {
        color: inherit;
        text-decoration: none;
        font-size: inherit;
        font-family: inherit;
        font-weight: inherit;
        line-height: inherit;
    }
    h2,p{margin:0}
    a{text-decoration:none; color:inherit;}
    .topwrapper{margin-left:2.5%}
    .topsection{display: inline-block;background:linear-gradient(90deg,#3e3874 51%,#5c3874 88%);width:97%;padding-right: 3px;padding-bottom:1%}
    .new-notices,.past-notices{margin-top:20px;padding-bottom:2%;margin-bottom:20px;background:#f05;background:linear-gradient(90deg,#f05 24%,#f43923 88%);text-align:center;width:97%;padding-right:3px}.past-notices{background:#0ac;background:linear-gradient(90deg,#0ac 24%,#00d5ff 88%)}
    #title,#title-secondary{color:#fff;font-family: Consolas, Helvetica; font-family: 'Open Sans', sans-serif; font-size:45px;padding:2% 0 0 3%;margin:0;font-weight:lighter;}
    #title-secondary{font-family:Consolas, Helvetica; font-family: 'Open Sans', sans-serif;}
    #quote{font-family: 'Open Sans', sans-serif;color:#fff;font-weight:lighter;padding:2% 0 1% 3%}
    .notice-new,.notice-past{margin-bottom:20px;background-color:#ebecf1;border-left:4px solid #f43923;padding:1%;width:95%}
    .notice-past{border-left:4px solid #0ac}
    .notice-title{display:inline-block;margin:0;width:70%}
    .date{font-family:Courier New;font-style:italic;font-weight:700;text-align:right;float:right;margin-right:1%;display:inline-block;width:80px;margin-bottom:20px}
    .details-container{text-align:left;width:80%}
    .notice-details{font-family:Courier New;font-weight:400;font-size:15px;margin:0px 6px 0px 0px;display:inline-block}
    .notice-description{margin-top: 15px;width: 98%;}
    .default {
        margin-top: -40px;
        height: 100px;
        background: rgb(244,231,35);
    }
    .bottomsection{background:#3e3874;margin-left:-6%;width:106%;padding-bottom:1%; padding-top:1%;}
    .footer-text {
        padding-left: 1%;
        border-left: 1px solid white;
        font-family: Arial;
        font-size: 12px;
        display: inline-block;
        color: white;
        margin-left: 2%;
        margin-right: 5px;
        margin-bottom: 3px;
        margin-top: 3px;
    }
    .icon{margin-top: 4px; margin-left: auto; height: 23px;display: inline-block;}
    .wrapper{margin-left: 2.5%;}
	</style>
</head>
<body id='body'>''')

# Top section of the page, containing:
title = Template("""
<div class='topwrapper'>
<div class='topsection'>
	<h1 id='title'>$date</h1>
	<p id='quote'>$quote</p>
</div>
</div>

<div class='wrapper'>
<div class='new-notices'>
	<h1 id='title-secondary'>New Notices</h2>
</div>
""").substitute(
    date=dateformatter.dateshort,
    quote=qod)
html_message.append(title)

# template for 5-td-notices which are new (RED EDGE)
template5 = Template('''
<div class='notice-new'>
	<h2 class='notice-title'>$title</h2>
	<p class='date'>$when</p>
	<div class='details-container'>
		<p class='notice-details'>$where</p><p class='notice-details'>$author</p>
	</div>

	<p class='notice-description'>$description</p>
	<div style='text-align: right;'><a href='mailto:$authorr@newlands.school.nz?subject=$subject'><img class='icon' style='margin-bottom: 2px;' src='https://cdn.pixabay.com/photo/2019/10/19/17/24/gmail-4561841_960_720.png'></a>
	<a href='$gcal' target='_blank'><img class='icon' style='height: 30px;margin-left: 5px;' src='https://purepng.com/public/uploads/large/purepng.com-calendar-icon-android-lollipopsymbolsiconsgooglegoogle-iconsandroid-lollipoplollipop-iconsandroid-50-721522597143e6f1s.png'></a>
	</div>
</div>
''')

# template for 5-td-notices which are old (blue edge)
template5old = Template('''
<div class='notice-past'>
	<h2 class='notice-title'>$title</h2>
	<p class='date'>$when</p>
	<div class='details-container'>
		<p class='notice-details'>$where</p><p class='notice-details'>$author</p>
	</div>

	<p class='notice-description'>$description</p>
    <div style='text-align: right;'><a href='mailto:$authorr@newlands.school.nz?subject=$subject'><img class='icon' style='margin-bottom: 2px;' src="https://cdn.pixabay.com/photo/2019/10/19/17/24/gmail-4561841_960_720.png"></a>
    <a href='$gcal' target='_blank'><img class='icon' style='height: 30px;margin-left: 5px;' src='https://purepng.com/public/uploads/large/purepng.com-calendar-icon-android-lollipopsymbolsiconsgooglegoogle-iconsandroid-lollipoplollipop-iconsandroid-50-721522597143e6f1s.png'></a>
    </div>
</div>
''')

'''
PROCESSES ALL OF THE 5-td-notices
    old ones moved to the old messages array
    new ones directly appended to the html file (as we are currently up to the new notices section on the page)
'''
oldmessages = []
for i in scraper.notices_5:
    # anomalous case, where author:ekai has an email:ekairuna and email_address (note extra r) corrects this
    if i[4].rstrip().lower() == 'ekai':
        email_address = 'ekairuna'

    elif i[4].rstrip().lower() == 'mul':
        email_address = 'kmulholland'
    # but in all other cases, the author tag is = to thee email_address
    else:
        email_address = i[4].rstrip().lower()

    # TRY-EXCEPT is to catch the potential lack of entry in the archive for yesterday.
    try:
        # If the title(lowercase) is not in the archive, it must be new
        if i[1].lower() not in archive:
            # print(dateformatter.makenumericdate(i[3]))
            html_message.append(
                template5.substitute(authorr=email_address, subject=makegcal.remove_spaces(i[1].title()), float='right', backgroundcolor='#fcfc64',
                                     titlecolor=title, who='',
                                     title=i[1].upper(), where=i[2], when=i[3], author=i[4].rstrip().upper(),
                                     description=i[5],
                                     gcal=makegcal.urlify(dateformatter.makenumericdate(i[3]), i[1].lower().title())))

        # Otherwise it must be inside it, hence old, and added to oldmessages.
        else:
            oldmessages.append(
                template5old.substitute(authorr=email_address, subject=makegcal.remove_spaces(i[1].title()), float='right', backgroundcolor='#fcfc64',
                                        titlecolor=title, who='',
                                        title=i[1].upper(), where=i[2], when=i[3], author=i[4].rstrip().upper(),
                                        description=i[5],
                                        gcal=makegcal.urlify(dateformatter.makenumericdate(i[3]),
                                                             i[1].lower().title())))

    # If there is no archive entry, then we will assume all of the entries are to be new, and none are old.
    except KeyError:
        html_message.append(
            template5.substitute(authorr=email_address, subject=makegcal.remove_spaces(i[1].title()), float='right', backgroundcolor='#fcfc64',
                                 titlecolor=title, who='',
                                 title=i[1].upper(), where=i[2], when=i[3], author=i[4].rstrip().upper(),
                                 description=i[5],
                                 gcal=makegcal.urlify(dateformatter.makenumericdate(i[3]), i[1].lower().title())))

# template for 3-td-notices which are new (RED EDGE)
template3 = Template('''
<div class='notice-new'>
	<h2 class='notice-title'>$title</h2>
	<div class='details-container'>
		<p class='notice-details'>$author</p>
	</div>

	<p class='notice-description'>$description</p>
	<div style='text-align: right;'><a href='mailto:$authorr@newlands.school.nz?subject=$subject'><img class='icon' style='margin-bottom: 2px;' src="https://cdn.pixabay.com/photo/2019/10/19/17/24/gmail-4561841_960_720.png"></a>
	<a href='$gcal' target='_blank'><img class='icon' style='height: 30px;margin-left: 5px;' src='https://purepng.com/public/uploads/large/purepng.com-calendar-icon-android-lollipopsymbolsiconsgooglegoogle-iconsandroid-lollipoplollipop-iconsandroid-50-721522597143e6f1s.png'></a>
	</div>
</div>
''')

# template for 3-td-notices which are new (BLUE edge)
template3old = Template('''
<div class='notice-past'>
	<h2 class='notice-title'>$title</h2>
	<div class='details-container'>
		<p class='notice-details'>$author</p>
	</div>

	<p class='notice-description'>$description</p>
    <div style='text-align: right;'><a href='mailto:$authorr@newlands.school.nz?subject=$subject'>
    <img class='icon' style='margin-bottom: 2px;' src="https://cdn.pixabay.com/photo/2019/10/19/17/24/gmail-4561841_960_720.png"></a>
    <a href='$gcal' target='_blank'><img class='icon' style='height: 30px;margin-left: 5px;' src='https://purepng.com/public/uploads/large/purepng.com-calendar-icon-android-lollipopsymbolsiconsgooglegoogle-iconsandroid-lollipoplollipop-iconsandroid-50-721522597143e6f1s.png'></a>
    </div>
</div>
''')


'''
PROCESSES ALL OF THE 3-td-notices
    old ones moved to the oldmessages array
    new ones directly appended to the html file (as we are currently still up to the new notices section on the page)
'''
for i in scraper.notices_3:
    # Corrects anomaly - explained in greater detail above.
    if i[2].rstrip().lower() == 'ekai':
        email_address = 'ekairuna'

    elif i[2].rstrip().lower() == 'mul':
        email_address = 'kmulholland'

    else:
        email_address = i[2].rstrip().lower()

    try:
        # If inside the archive: move to old messages
        if i[1].lower() not in archive:
            html_message.append(
                template3.substitute(authorr=email_address, subject=makegcal.remove_spaces(i[1].title()), who='', title=i[1].upper(), author=i[2].upper(),
                                     description=i[3],
                                     gcal=makegcal.urlify(dateformatter.makenumericdate(i[3]), i[1].lower().title())))

        # Otherwise, it is added straight to the HTML email
        else:
            oldmessages.append(
                template3old.substitute(authorr=email_address, subject=makegcal.remove_spaces(i[1].title()), who='', title=i[1].upper(), author=i[2].upper(),
                                        description=i[3],
                                        gcal=makegcal.urlify((datetime.datetime.today(), datetime.datetime.today()), i[1].lower().title())))


    except:
        html_message.append(
            template3.substitute(authorr=email_address, subject=makegcal.remove_spaces(i[1].title()), who='', title=i[1].upper(), author=i[2].upper(),
                                 description=i[3],
                                 gcal=makegcal.urlify((datetime.datetime.today(), datetime.datetime.today()), i[1].lower().title())))

# If sum of OLD messages == the total number of messages, then there is no new messages, hence, we add a NO NEW NOTICES
if len(oldmessages) == len(scraper.notices_5) + len(scraper.notices_3):
    html_message.append('''<div class='notice-new'>
	<h2 class='notice-title'>There are no new notices today</h2><p style='margin-top: 3px;'></p>
</div>''')


# Adds the old notices heading block (blue)
html_message.append('''<div class='past-notices'>
	<h1 id='title-secondary'>Past Notices</h2>
</div>
''')

# Note to self: You should add a no old notices thing too.
if len(oldmessages) == 0:
    html_message.append('''<div class='notice-past'>
	<h2 class='notice-title'>There are no old notices today.</h2><p style='margin-top: 3px;'></p>
</div>''')

# Adds all of the old messages
html_message.append(''.join(oldmessages))

# Adds the footer AND IMPORTANTLY, closes the wrapper of the notices.
html_message.append('''</div>
</div>
<div class='bottomsection'>
	<a href='https://notices.newlands.school.nz/faq'><p class='footer-text'>FAQ</p></a>
	<a href='https://notices.newlands.school.nz/unsubscribe'><p class='footer-text'>Unsubscribe</p></a>
</div>
</body>

''')

# INLINES THE CSS AND DELETES IT
html_message = transform(''.join(html_message), cssutils_logging_level=logging.ERROR)  # joins the entire message, a more efficient way than concatenation

# IF RUN DIRECTLY, you can test the html / css by checking the file in their before - writing to this file.
# it is excluded by default for efficiency.
if __name__ == "__main__":
    file = 'emailformatter.html'
    with open(file, 'w+', encoding="utf-8") as f:
        # f.write('{% extends "template.html" %}')
        # f.write('{% block content %}')
        f.write(html_message)
        # f.write('{% endblock %}')
