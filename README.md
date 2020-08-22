# NC Daily
Notices aggregator for Kamar Website. Code is in a continuous deployment environment, so any changes made to master branch will automatically deploy to ncdaily.herokuapp.com

## Python files
#### credentials.py 
Handles the credentials and global variables.

#### dateformatter.py
Handles Timezone and date string conversion stuff.

#### emailformatter.py
Writes the whole newsletter and compliles it into a string

#### main.py
Sends the email to the database list of emails. 

#### makegcal.py
Handles the creation of the Google calendar link and the mail:to link

#### newsletter.py
Sends the welcome message and is also used to test the email 



#### scraper.py
Handles the web scraping and sorting of the data from the parent portal
#### server.py
WEB APP, flask backend for the website





## Folders
#### static/
Has all of the static files: CSS, JS (no external JS at the moment) and pictures
#### templates/
Has all of the html served by Flask - template.html is the base file
#### venv/
Is the virtual environment for python - essentially the external packages that the program uses packaged up into a folder with python 3.7 I think.

## Other files
#### quotes.json
Random quotation data
#### requirements.txt
all packages used
#### login.txt
passwords for the driver account


