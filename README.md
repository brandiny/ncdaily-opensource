# NC Daily
NC Daily is a notices aggregator for the Kamar Parent Portal notices page.

The noticeboard of a school is crucial. It serves as a hub for student participation and information dissemination.  However, there is an inherent flaw in the concept of a "noticeboard": cognitive friction. Many students frequently forget to check the notices and as a result, don't fully participate.


Instead of students having to remember to check the school noticeboard, NC Daily sends out a collated email newsletter to all of its subscribers. Arriving at 7.30am in each student's inbox, this process minimises the cognitive friction involved.

# Features
In addition to the notices, NC Daily offers extra features.
* Notices can be added to Google Calendar in one click
* Notices are sorted chronologically.
* Notice authors can be emailed using a mail:to link
* Daily motivational quotes
* Searchable, using email search function.

# Hosting
This web app is hosted using Heroku, and which builds from source code located on Github. The maintanence cost of the app is $0.00 per month, and is highly affordable.


# Explanation of important files
#### Python files
<strong>credentials.py</strong> Handles all sensitive information (credentials and blacklists)

##### dateformatter.py
Manages timezone changes and date string manipulation.

##### emailformatter.py
Compiles the contents of the newsletter into an HTML string.

##### main.py
Pilot file which sends out the newsletter to email pool.

##### makegcal.py
Handles the construction of the Google calendar link and the mail:to link

##### newsletter.py
Sends a single welcome newsletter to new subscribers.



##### scraper.py
Responsible for web scraping and sorting the data from the parent portal website.

##### server.py
The flask backend for the web application.

#### Folders
##### static/
Has all of the static files: CSS, JS and pictures

##### templates/
Has all of the HTML served by Flask (website files)

##### venv/
This is the virtual environment for this python project -  the external packages that the program uses packaged up into a folder with python 3.7.

#### Other files
##### quotes.json
A large compilation of quote JSON objects.

##### requirements.txt
A pip freeze of all of the packages required in this project



