import MySQLdb
import smtplib, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import time
import os
import admintools
import json
import credentials

"""
DATABASE CONNECTION
connect parameters: host, user, password, table
"""
db = credentials.dbconnect()
cursor = db.cursor()
sql = """SELECT * FROM statistics"""
cursor.execute(sql)
db.commit()
results = cursor.fetchall()


# Define statistical variables
looptime = results[0][0]
uptime = results[0][1]
emails_sent = results[0][2]


# New day
uptime += 1
sql = """UPDATE statistics SET `loop_time`={looptime}, `uptime`={uptime}, `emails_sent`={emails_sent};""".format(looptime=looptime, uptime=uptime, emails_sent=emails_sent)
cursor.execute(sql)
db.commit()

""" Sets the file timezone to Pacific/Auckland """
try:
    os.environ["TZ"] = "Pacific/Auckland"
    time.tzset()
except Exception as e:
    pass

""" IF APP OFF - exit"""
if not admintools.is_ON_declaredbyuser():
    print('app turned off, exiting ...')
    sys.exit()


""" IF RUN IN THE HOLIDAYS -- exit """
if not admintools.is_schooltime():
    print('run in holidays, exiting ...')
    sys.exit()


""" IF RUN ON WEEKEND -- exit """
if admintools.is_weekend():
    print('run on weekend, exiting...')
    sys.exit()


def errorlog(message):
    """ logs message to logs.txt with date """
    with open('logs.txt', 'a') as f:
        f.write(str(datetime.date.today()) + message + '\n')
        print('error scraping message, exiting')
        sys.exit()


""" writes the email AND scrapes it """
try:
    import emailformatter                   # emailformatter for the HTML message: MUST IMPORT BEFORE ARCHIVER
except Exception:
    errorlog('emailformatter failed')


""" writes the email AND scrapes it """
try:
    import dateformatter                    # dateformatter for the date:
except Exception:
    errorlog('dateformatter failed')



# INITIAL VARIABLES
MY_ADDRESS = credentials.username               # email address
MY_PASSWORD = credentials.password              # password
html_message = emailformatter.html_message      # main HTML message -- string type


"""GET EMAILS FROM DATABASE"""
sql = """SELECT * FROM emails"""
cursor.execute(sql)
results = cursor.fetchall()         # array of all the EMAILS SUBSCRIBED.
results = [i[:2] for i in results]



""" main event flow """
def main(emails_sent):
    # Define emails to clean
    bad_emails = []

    # Define statistical variables
    start_time = time.time()

    # SIGN IN
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    # s.set_debuglevel(1)
    s.ehlo()
    s.starttls()    
    s.login(MY_ADDRESS, MY_PASSWORD)
    print('sign in successful ... ')

    # ITERATES OVER ALL EMAILS
    for address, subscription_status in results:
        # Throttle app at 50, 100, 150 ... 
        if emails_sent % 30 == 0 and emails_sent != 0:
            print('emails_sent:', emails_sent, '... throttling app for 60s')
            time.sleep(50)
            print('\t...attempting to login into smtp again')
            s.connect(host='smtp.gmail.com', port=587)
            s.ehlo()
            s.starttls() 
            s.login(MY_ADDRESS, MY_PASSWORD)
            print('sign in successful ... ')
        
        if subscription_status == 0:
            print('\tskipping', address)
            continue
        
        # Create message
        msg = MIMEMultipart()

        # Adds the personalised stuff; to, from, subject
        msg['From'] = 'NC Daily'
        msg['To'] = address
        msg['Subject'] = '{}'.format(dateformatter.dateformatted)
        # Uncomment for last name in the subject - address.split('@')[0][:-1].title())

        # Attaches HTML message
        msg.attach(MIMEText(html_message, 'html'))
        
        # Send, error check and then delete - to prevent memory overflow
        try:
            s.send_message(msg)
            emails_sent += 1
            print('\temailed ' + address)

        except Exception as e:
            print(address, 'got', e, '...adding to bad emails')
            bad_emails.append(address)

        # Delete
        del msg

    # Add statistics of looptime/emails_sent to the json file and reconnect
    db = credentials.dbconnect()
    print('uptime:',time.time() - start_time)
    sql = """UPDATE statistics SET `loop_time`={looptime}, `uptime`={uptime}, `emails_sent`={emails_sent};""".format(looptime=time.time() - start_time
,uptime=uptime, emails_sent=emails_sent)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    
    # Clean out bad emails
    for address in bad_emails:
        try:
            s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            s.connect(host='smtp.gmail.com', port=587)
            s.ehlo()
            s.starttls()    
            s.login(MY_ADDRESS, MY_PASSWORD)
            
            print('sign in successful ... ')

            # Create message
            msg = MIMEMultipart()

            # Adds the personalised stuff; to, from, subject
            msg['From'] = 'NC Daily'
            msg['To'] = address
            msg['Subject'] = '{}'.format(dateformatter.dateformatted)
            # Uncomment for last name in the subject - address.split('@')[0][:-1].title())

            # Attaches HTML message
            msg.attach(MIMEText(html_message, 'html'))

            s.send_message(msg)
            emails_sent += 1
            print('\temailed ' + address)

        except Exception as e:
            print('\tdisabling', address, '... got ', e)
            sql = """UPDATE emails SET subscription_status=0 WHERE emails='{}'""".format(address)
            cursor.execute(sql)
            db.commit()

    db.close()

    

# EXIT if not run as MAIN -- prevents accidental import execution
if __name__ == '__main__':
    main(emails_sent)
    print('done')

else:
    sys.exit()
