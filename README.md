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

### Python Files
<table>
    <tr>
        <td>credentials.py</td>
        <td>Handles the sensitive information (credentials and blacklists)</td>
    </tr>
    <tr>
        <td>emailformatter.py</td>
        <td>Compiles the contents of the newsletter into an HTML string.</td>
    </tr>
    <tr>
        <td>main.py</td>
        <td>Driver program which sends out the newsletter to email pool.</td>
    </tr>
     <tr>
        <td>makegcal.py</td>
        <td>Handles the construction of the Google calendar link and the mail:to link</td>
    </tr>
    <tr>
        <td>newsletter.py</td>
        <td>Sends a single welcome newsletter to a new subscriber.</td>
    </tr>
    <tr>
        <td>scraper.py</td>
        <td>Responsible for web scraping and sorting the data from the parent portal website.</td>
    </tr>
    <tr>
        <td>server.py</td>
        <td>The flask backend for the web application.</td>
    </tr>
</table>
   
### Folders
<table>
    <tr>
        <td>static/</td>
        <td>Has all of the static files: CSS, JS and pictures</td>
    </tr>
    <tr>
        <td>templates/</td>
        <td>Has all of the HTML served by Flask (website files)</td>
    </tr>
    <tr>
        <td>templates/</td>
        <td>Has all of the HTML served by Flask (website files)</td>
    </tr>
</table>


#### Other files
##### quotes.json
A large compilation of quote JSON objects.

##### requirements.txt
A pip freeze of all of the packages required in this project



