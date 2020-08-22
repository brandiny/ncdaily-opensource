"""
newsletter.py

- Contains the 'Welcome to NC Daily' function
- Contains the send 'Unsubscribe Code' function
"""

import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import time

""" Sets the file timezone to Pacific/Auckland """
# This can only run on a linux machine.
try:
    os.environ["TZ"] = "Pacific/Auckland"
    time.tzset()
except Exception as e:
    pass



def send_newsletter_to(EMAIL):
    """ Sends a welcome newsletter, with instructions, to the email in the parameter """

    import emailformatter   # builds email html
    import credentials      # takes credentials

    MY_ADDRESS = credentials.username               # email address
    MY_PASSWORD = credentials.password              # insert password on run, delete after
    HTML_MESSAGE = emailformatter.html_message      # main HTML message -- string type

    # Sign in
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.ehlo()
    s.starttls()
    s.login(MY_ADDRESS, MY_PASSWORD)
    print('sign in successful ... ')

    # Create message
    msg = MIMEMultipart()

    # Adds the personalised stuff; to, from, subject
    msg['From'] = 'NC Daily'
    msg['To'] = EMAIL
    msg['Subject'] = 'Welcome to NC Daily'

    # Attaches HTML message
    msg.attach(MIMEText(HTML_MESSAGE, 'html'))

    # Send and delete
    s.send_message(msg)
    del msg

    # Add statistics
    import MySQLdb
    db = credentials.dbconnect()
    cursor = db.cursor()
    sql = """SELECT `emails_sent` FROM statistics;"""
    cursor.execute(sql)
    db.commit()
    results = cursor.fetchall()[0][0]
    results += 1

    sql = """UPDATE statistics SET `emails_sent`={};""".format(results)
    cursor.execute(sql)
    db.commit()
    db.close()

def send_code(EMAIL, unsubscribe_code):
    """ Sends the unsubscribe code to the email in the parameter """

    import credentials                              # takes credentials

    MY_ADDRESS = credentials.username               # email address
    MY_PASSWORD = credentials.password              # insert password on run, delete after

    # Sign in
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.ehlo()
    s.starttls()
    s.login(MY_ADDRESS, MY_PASSWORD)
    print('sign in successful ... ')

    # Create message
    msg = MIMEMultipart()

    # Adds the personalised stuff; to, from, subject
    msg['From'] = 'NC Daily'
    msg['To'] = EMAIL
    msg['Subject'] = 'Unsubscribe - NC Daily'

    # Farewell message
    farewell_message = """
    <h1>NC Daily</h1>
    <p>Your unsubscribe code is {unsubscribe_code}</p>
    <br>
    <p>Thank you for using NC Daily. If you wish to resubscribe at anytime, feel free too.</p>
    """.format(unsubscribe_code=unsubscribe_code)

    # Attaches HTML message
    msg.attach(MIMEText(farewell_message, 'html'))

    # Send and delete - to prevent memory overflow
    s.send_message(msg)
    del msg


if __name__ == '__main__':
    print('debug sending to rub@newlands.school.nz')
    send_newsletter_to('rub@newlands.school.nz')
