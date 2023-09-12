# Wildlife-Tagger
Wildlife Tagger by ATL Wildin' (JIC-1128)
## About
The Wildlife Tagger sit is a solution to the need for researchers to quantify biodiversity on GT’s campus. Our application, currently hosted at http://wildlife-tagger.herokuapp.com/, aims to provide a fun interface for taggers to identify animals based on their genus/species and for researchers to collect data efficiently. 
## Release Notes
### v1.0 Notes:
v1.0 is the initial release of Wildlife Tagger, where most critical features of the application were completed. The following list represents features completed during v1.0:
- Login/Authentication
- User Dashboard
- Leaderboard
- Tagging Animals
- Test to transition from beginner -> advanced tagger
- Profile Management for Taggers
- (Researcher) Animal Statistics View
- (Researcher) Manage Users & Disable Users
- (Researcher) Upload Images
- Infrastructure: MySQL DB created & hosted on RDS, Image File Server created on S3, Website hosting on Heroku
#### Bug Fixes:
- Images not rendering on the "tagging" portion of the site ("Access Denied"). Fixed by removing images in MySQL DB that weren't in S3 bucket and reconfiguring the S3 bucket to become fully public.
- Disable Users functionality having inconsistent timezones on MySQL and Django. Fixed by converting all UTC timezones utilized by MySQL into EST before rendering on site.
- Leaderboard UI not updating in real time. Fixed by using an asynchronous view rather than a regular view.
### Outstanding Issues/Bugs:
- Inconsistent image rendering on "Test" for taggers to transition from beginner -> advanced users. At random times, images are not rendering for taggers; still yet to figure out why this is happening.
- Converting Animal Data from Animal Statistics View into CSV still incomplete (i.e. button not fully functional yet).

## Setup and Install Guide:

Ensure that python 3.9 is installed on your local machine. To install python 3.9, navigate to https://www.python.org/downloads/.

To replicate the project on your local machine, clone the repository & navigate into the root folder:

```sh
$ git clone https://github.com/apramodz/Wildlife-Tagger-1128.git
$ cd Wildlife-Tagger-1128
```

All project dependencies are in the `requirements.txt` file. To install all dependencies in this file, run:

```sh
$ pip3 install -r requirements.txt
```

## Testing and Deployment
To run site locally, run:
```sh
$ python3 manage.py runserver
```
while in the root folder and navigate to `http://127.0.0.1:8000/`.

To deploy the application to production, ensure that the Heroku CLI has been downloaded on your machine. Visit https://devcenter.heroku.com/articles/heroku-cli for installation instructions and an easy-to-use installer.  
To deploy to heroku, ensure that the latest changes have been pushed to the main branch, then run:
```sh
$ git push heroku main
```
Site will be located at http://wildlife-tagger.herokuapp.com/ upon successful build.

To change site domain or heroku deployment configurations, contact apramod3@gatech.edu. 

## Troubleshooting:
- If you see `pip: command not found` when installing dependencies, ensure that python 3.9 has been installed and that you are using `pip3` rather than `pip`. 
- If static images are not rendering on the deployed website, ensure that those static images are within the existing /static directory OR add the new directory of static images in `settings.py`.
- Pushing the updated project to the main branch of Github will NOT automatically update the production site. Reference the "Testing and Deployment" section for more information on how to deploy to Heroku.
- Heroku failed to detect set buildpack-this means that the project structure was changed in a way that makes it incompatible with Heroku. Ensure that the following are in the ROOT folder of the repository: `Procfile`, `atlwildin` (primary project folder), `requirements.txt`, and `runtime.txt`.
- "Bad Request" when attempting to view site after changing domain name: add new domain to `ALLOWED_HOSTS` list in `settings.py`.
