"""
credentials.py - PROCESSES all the sensitive details for the app

Including:
- Email username
- Email password
- Database username
- Database password
- Blacklist

"""
import MySQLdb

username = 'emailaddress'
password = 'password'


def dbconnect():
     return MySQLdb.connect("hostlocation","password","dbname","table", connect_timeout=10000)

blacklist = {'emailtoblacklist', 'etc'}
