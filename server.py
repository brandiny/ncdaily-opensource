"""
server.py - Serves the Flask web application for the website
"""
import json
import admintools   
import credentials
from flask import Flask, render_template, request, redirect, url_for, make_response, session
import hashlib


try:
    import MySQLdb
except Exception as e:
    import os 
    os.system("pip install mysqlclient")
    import MySQLdb

import newsletter
import random
from validate_email import validate_email


app = Flask(__name__)
app.secret_key = 'any random string'

email_groups = credentials.blacklist

"""ADMIN login page"""
@app.route("/admin", methods=['GET', 'POST'])
def admin():
    """If SUBMITTING username and password """
    if request.method == 'POST':
        # Get database
        db = credentials.dbconnect()
        cursor = db.cursor()
        sql = """SELECT * FROM admin"""
        cursor.execute(sql)
        results = [i[1:] for i in cursor.fetchall()]


        # Get submitted details
        submittedCredentials = (request.form['username'], hashlib.sha256(request.form['password'].encode()).hexdigest()) 


        # Password handling
        if submittedCredentials in results:
            session['username'] = request.form['username']
            return redirect(url_for('adminpanel'))
        else:
            return render_template('adminpanel--login.html', credentialsWrong=True)


    """IF first loading the page"""
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('adminpanel'))

        else:
            return render_template('adminpanel--login.html')


"""ADMIN PANEL page
    - Change holiday intervals
    - Add days of relief
    - Remove days of relief
    - Create new admin account 
    - Change password
    - Bulk add emails
    - View email list
"""
@app.route("/adminpanel", methods=['GET', 'POST'])
def adminpanel():
    # IF LOGGED IN
    try:
        if session['username']:
            db = credentials.dbconnect()
            cursor = db.cursor()
            sql = """SELECT * FROM emails"""
            cursor.execute(sql)
            results = [i[0] for i in cursor.fetchall()]
            total_subs = len(results)
            db.commit()

            sql = """SELECT * FROM statistics"""
            cursor.execute(sql)
            db.commit()
            results = cursor.fetchall()

            # Define statistical variables
            loop_time = str(round(results[0][0], 2)) + 's'
            uptime_days = str(results[0][1]) + ' days'
            emails_sent = str(results[0][2]) + ' emails'
            import time
            try:
                os.environ["TZ"] = "Pacific/Auckland"
                time.tzset()
            except Exception as e:
                pass

            print(admintools.is_schooltime() and (not admintools.is_weekend()) and admintools.is_ON_declaredbyuser())
            

            if admintools.is_schooltime() and (not admintools.is_weekend()) and admintools.is_ON_declaredbyuser():
                return render_template('adminpanel--home.html', appON='True', username=session['username'], totalSubscribers=total_subs, emails_sent=emails_sent, loop_time=loop_time, uptime_days=uptime_days, holiday_startdate=admintools.holiday_startdate(),holiday_enddate=admintools.holiday_enddate(),**request.args) 

            else: 
                return render_template('adminpanel--home.html', appON='False', username=session['username'], totalSubscribers=total_subs, emails_sent=emails_sent, loop_time=loop_time, uptime_days=uptime_days, holiday_startdate=admintools.holiday_startdate(),holiday_enddate=admintools.holiday_enddate(), **request.args)    
        


    # ELSE TAKE BACK TO ADMIN
    except KeyError:
        return redirect(url_for('admin'))

"""LOGOUT method"""
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('home'))

@app.route('/add_emails', methods=['POST'])
def add_emails():
    if session['username']:
        details = request.form
        emails = details['emails'].split(',')
        print(emails)
        # Connect to database and fetch all
        db = credentials.dbconnect()
        cursor = db.cursor()
        sql2 = """SELECT * FROM emails"""
        cursor.execute(sql2)
        results = [i[0] for i in cursor.fetchall()]

        for email in emails:
            # Boolean for Valid Email
             # BLANK ENTRY serverside validate
            if len(email) == 0:
                return redirect(url_for('view_subscribed', empty=True))

            # SUBSCRIBING TWICE serverside validate
            if email in results:
                db.close()
                return redirect(url_for('view_subscribed', email=email, duplicate=True))

            # All serverside validation PASSED successfully
            else:
                # Add email to database
                sql = """INSERT INTO emails(emails, subscription_status, unsubscribe_code) VALUES ('{}', 1, '{:05}' )""".format(email.strip(), random.randint(0, 10000))
                cursor.execute(sql)
                db.commit()

                # Send them welcome message
                # newsletter.send_newsletter_to(email)

                # Renders the welcome page -- DOES NOT REDIRECT

        db.close()
        return redirect(url_for('view_subscribed', successfullyAdded=True))

    else:
        return 'unauthorised'
"""DELETE email method"""
@app.route('/delete_emails', methods=['POST'])
def delete_emails():
    if session['username']:
        try:
            emailScrap = request.form['emailScrap'].split(',')
            db = credentials.dbconnect()
            cursor = db.cursor()
            for email in emailScrap:
                sql = """DELETE FROM emails WHERE emails='{}'""".format(email)
                cursor.execute(sql)

            db.commit()
            db.close()
            
            return redirect(url_for('view_subscribed', numberDeleted=len(emailScrap), errorDelete=False))

        except Exception as e:
            return redirect(url_for('view_subscribed', errorDelete=True))
    else:
        return 'unauthorised'


"""CHANGE PASSWORD method"""
@app.route('/adminpanel/changepassword', methods=['GET', 'POST'])
def changepassword():
    try:
        if session['username']:
            # HANDLING POST DATA
            if request.method == 'POST':
                db = credentials.dbconnect()
                cursor = db.cursor()
                sql = """SELECT password FROM admin WHERE username='{}'""".format(session['username'])
                cursor.execute(sql)
                oldPassword = cursor.fetchall()[0][0]

                # most important, check for the oldpasswords to match
                if hashlib.sha256(request.form['oldPassword'].encode()).hexdigest() == oldPassword:
                    # check for newpasswords to match, otherwise return back
                    if request.form['newPassword'] != request.form['newPassword2']:
                        return redirect(url_for('changepassword', passwordsNotMatch=True))

                    else:
                        # delete the password that preexists
                        sql_deletepassword = """DELETE FROM admin WHERE username='{username}';""".format(username=session['username'])
                        cursor.execute(sql_deletepassword)

                        # add in the new password
                        sql_changepassword = """INSERT INTO admin (username, password) VALUES ('{username}', '{passwordHash}');""".format(username=session['username'], passwordHash=hashlib.sha256(request.form['newPassword'].encode()).hexdigest())
                        print(sql_deletepassword, sql_changepassword)
                        cursor.execute(sql_changepassword)

                        # commits the changes
                        db.commit()
                        db.close()

                    return redirect(url_for('changepassword', changedPassword=True))

                    # if old password match fails, return back
                else:
                    return redirect(url_for('changepassword', incorrectPassword=True))
        
            # IF RESPONDING TO PAGE LOAD
            if request.method == "GET":
                return render_template('adminpanel--changepassword.html', username=session['username'])

    except Exception as e:
        return 'unauthorised'

"""VIEW SUBSCRIPTIONS"""
@app.route('/adminpanel/view_subscribed', methods=['GET', 'POST'])
def view_subscribed():
    try:
        if session['username']:
            db = credentials.dbconnect()
            cursor = db.cursor()
            sql = """SELECT * FROM emails"""
            cursor.execute(sql)
            emailList = [i[0] for i in cursor.fetchall()]
            emailList.sort()

            return render_template('adminpanel--view_subscribed.html', emailList=emailList)

    except Exception as e:
        return 'unauthorised'


"""HOLIDAYS"""
@app.route('/adminpanel/holidays', methods=['GET'])
def holidays():
    try:
        if session['username']:
            with open('static/json/term_dates.json') as jsonfile:
                data = json.load(jsonfile)    

            if request.method == 'GET':
                return render_template('adminpanel--holidays.html', data=data)
    
    except Exception as e:
        return 'unauthorised'

@app.route('/change_holidays', methods=['POST'])
def change_holidays():
    if request.method == 'POST':
        try:
            # check number
            term = int(request.form['term'])

            # check between 1/4
            if not (term > 0 and term <= 4):
                raise Exception

            start_date = request.form['start_date']
            end_date = request.form['end_date']
            if not (len(start_date.split('/')) == 2 and len(end_date.split('/')) == 2):
                raise Exception

            admintools.change_termdates(int(term), dateStart=start_date, dateEnd=end_date)
            
            with open('static/json/term_dates.json') as jsonfile:
                data = json.load(jsonfile)    

            return redirect(url_for('holidays', error=False, data=data))

        except:
            with open('static/json/term_dates.json') as jsonfile:
                data = json.load(jsonfile)  
            return redirect(url_for('holidays', error=True, data=data))
"""DISABLE"""
@app.route('/adminpanel/disable', methods=['GET', 'POST'])
def disable():
    if request.method == 'POST':
        with open('static/json/app_status.json', 'w+') as f:
            print(request.form['result'])
            if request.form['result'] == 'Turn off':
                f.write('{"appisON": false}')
                return render_template('adminpanel--disable.html', appON=False)  
            
            elif request.form['result'] == 'Turn on':
                f.write('{"appisON": true}')
                return render_template('adminpanel--disable.html', appON=True)  

    else:
        if admintools.is_ON_declaredbyuser():
            return render_template('adminpanel--disable.html', appON=True)  
        
        else:
            return render_template('adminpanel--disable.html', appON=False)  


"""
Index/Home page
    - Subscription field
    - Vector from vecteezy
    - Introductory information to the app
"""
@app.route("/", methods=['GET', 'POST'])
def home():
    db = credentials.dbconnect()
    cursor = db.cursor()
    sql = """SELECT `subscription_status` FROM emails"""
    cursor.execute(sql)
    results = [i[0] for i in cursor.fetchall()]
    num_students = ((len(results) // 10) * 10) + 10

    """ IF RESPONDING TO REGULAR GET REQUEST """
    if request.method == 'GET':
        return render_template('home.html', num_students=num_students)


    """ IF RESPONDING TO SUBSCRIBE POST REQUEST """
    if request.method == "POST":
        # Define INITIAL VARIABLES
        details = request.form
        email = details['email']

        #uncomment for disable
        #return render_template('home.html', num_students=num_students, disabled=True)
       
        # Boolean for Valid Email
        # is_valid = validate_email(email_address=email, \
        #     check_regex=True, check_mx=True, \
        #     smtp_timeout=2, dns_timeout=2, use_blacklist=True)

        # BLANK ENTRY serverside validate
        if len(email) == 0:
            return render_template('home.html', num_students=num_students, empty=True)

        # # INVALID EMAIL serverside validate
        # elif not is_valid:
        #     return render_template('home.html', num_students=num_students,invalid_email=True)

        # Connect to database and fetch all
        db = credentials.dbconnect()
        cursor = db.cursor()
        sql2 = """SELECT * FROM emails"""
        cursor.execute(sql2)
        results = [i[0] for i in cursor.fetchall()]

        # SUBSCRIBING TWICE serverside validate
        if email in results:
            db.commit()
            db.close()
            return render_template('home.html', num_students=num_students, email=email, duplicate=True)

        if email in email_groups:
            return render_template('home.html', num_students=num_students, email=email, blocked=True)
        # All serverside validation PASSED successfully
        else:
            # Add email to database
            sql = """INSERT INTO emails(emails, subscription_status, unsubscribe_code) VALUES ('{}', 1, '{:05}' )""".format(email, random.randint(0, 10000))
            cursor.execute(sql)
            db.commit()
            db.close()

            # Send them welcome message
            newsletter.send_newsletter_to(email)

            # Renders the welcome page -- DOES NOT REDIRECT
            return render_template('landing.html', email=email)


"""
About page
    - How to use it
    - How it works
    - Who made it
"""
@app.route('/about')
def about():
    return render_template('about.html')


"""
FAQ
    - All the questions people ask
    - Contact details of the administrator
"""
@app.route('/faq')
def faq():
    return render_template('faq.html')


"""
Notices
    - ***SECRET PAGE ***
    - Testing environment with the email newsletter
"""
@app.route('/notices')
def notices():
    return render_template('emailformatter.html')



"""
Unsubscribe
    - Unsubscribe option
"""
@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
    """ IF JUST LOADING THE PAGE """
    if request.method == "GET":
        return render_template('unsub.html')


    """ OTHERWISE RESPONDING TO UNSUBSCRIBE POST REQUEST """
    if request.method == "POST":
        # return render_template('unsub.html', disabled=True) # uncomment for disable
        details = request.form
        email = details['email']

        # LOGIN TO DB
        db = credentials.dbconnect()
        cursor = db.cursor()
        sql2 = """SELECT * FROM emails"""
        cursor.execute(sql2)

        results = [i[0] for i in cursor.fetchall()]

        # BLANK ENTRY serverside validate
        if len(email) == 0:
            return render_template('unsub.html', subscribed='False')

        # FALSE UNSUBSCRIBE serverside check
        elif email not in results:
            db.commit()
            db.close()
            return render_template('unsub.html', subscribed='False')

        # If all serverside checking has PASSED
        else:
            # REDIRECT to the confirm unsubscribe page, with given email
            return redirect(url_for('confirm_unsubscribe', email=details['email']))

"""
Confirm Unsubscribe
    - Enter correct code
    - Prevents unwanted unsubscription
"""
@app.route('/confirm_unsubscribe', methods=['GET', 'POST'])
def confirm_unsubscribe():
    email = request.args['email']
    db = credentials.dbconnect()
    cursor = db.cursor()
    sql = """SELECT * FROM emails WHERE emails='{}' """.format(email)
    cursor.execute(sql)
    unsubscribe_code = cursor.fetchall()[0][2]


    """ IF THE PAGE IS LOADED WITH INITITALLY, SEND AN EMAIL TO """
    if request.method == 'GET':
        newsletter.send_code(email, unsubscribe_code)
        return render_template('confirm_unsubscribe.html', email=email)

    """ CODE CHECK - POST REQUEST """
    if request.method == 'POST':
        details = request.form

        # If it matches the code -- DELETE QUERY
        if details['unsubscribe_code'] == unsubscribe_code:
            sql = """DELETE FROM emails WHERE emails='{}' """.format(email)
            cursor.execute(sql)
            db.commit()
            db.close()

            # FAREWELL page render
            return render_template('farewell.html')

        # Otherwise, re-request
        else:
            return render_template('confirm_unsubscribe.html', wrong='False')


@app.route('/cronjob', methods=['GET'])
def cronjob():
    return 'OK'

@app.route('/testing', methods=['GET'])
def testing():
    return render_template("confirm_unsubscribe.html", email='anyone')

@app.route('/tryitout', methods=['GET'])
def tryitout():
    return render_template("emailformatter.html")

if __name__ == "__main__":
    app.run(debug=True)