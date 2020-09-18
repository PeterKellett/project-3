# Peter Kellett - Data Centric Development - Milestone Project 3

## Introduction 
The purpose of this project is to demonstrate my ability in the use of a document based database and to perform Create, Read, Update and Delete (CRUD) operations on it.
For this I have constructed a simple Dingbats type dictionary where users can view and filter through all the existing entries and be able to upload their own ideas too. Although a user can view all of the users puzzles they only have the ability to edit and delete their own puzzles. I am using MongoDb to store the database documents.  

I have also incorporated a 'Likes' and 'Dislikes' functionality as a simple way for different users to show their satisfaction to a particular puzzle. A user must be registered and logged in to avail of this functionality although the number of Likes and Dislikes that each puzzle has are still shown to guest users.  

## Modules and Source libraries
### Flask
This dynamics of this website is implemented using the Jinja template engine which allows for the use of Jinja templating logic along with the Flask framework in Python which are accessed using the PyPI import modules. 

### Flask Modules used
- render_template: This method is used for delivering the required page from the templates folder and the respective template inheritance and Jinja templating logic.
- redirect: This method is used to redirect users to a different URL than the one  requested as an aid to site navigation. 
- url_for: This is used to generate a URL to a given endpoint and calls the respective Python function to be executed. 
- session: This module is used to store various user session variables and are set when a user either registers or logs in. They are removed when a user logs out or closes their browser thus ending their session. 
- flash: This module provides the ability to display feedback messages to the user. The flash functionality makes it possible to record a message at the end of one request and access it with the next request and only next request. Once flash messages are rendered to the user they are deleted from the flash messages list. 


### Flask PyPI import packages used
- dnspython: This module is a DNS toolkit for Python. It is used for server queries and dynamic updates.
- flask-pymongo: This module is used as the interface with MongoDb for performing database CRUD operations
- flask-wtf: This module is used for the site form controls and replaces the need to use html and javascript form controls.
- flask cloudinary: This module is used as the interface with Cloudinary image manager which is used for storing the relevant puzzle image files with the respective image url being stored in MongoDb.


### Materialize
Materialize CSS styling library is used for the grid layout and various page componants required.  
The componants used from Materialize are:
- Navbar
- Icons
- Cards
- Buttons  

### jQuery/JavaScript
jQuery is used for displaying/hiding the collapsible sidenav menu on small and medium sized devices.  
It is also used for toggling the Answer button on each puzzle card and for manually removing flash messages.



## Gitpod Reminders

To run a frontend (HTML, CSS, Javascript only) application in Gitpod, in the terminal, type:

`python3 -m http.server`

A blue button should appear to click: *Make Public*,

Another blue button should appear to click: *Open Browser*.

To run a backend Python file, type `python3 app.py`, if your Python file is named `app.py` of course.

A blue button should appear to click: *Make Public*,

Another blue button should appear to click: *Open Browser*.

In Gitpod you have superuser security privileges by default. Therefore you do not need to use the `sudo` (superuser do) command in the bash terminal in any of the backend lessons.

## Updates Since The Instructional Video

We continually tweak and adjust this template to help give you the best experience. Here are the updates since the original video was made:

**April 16 2020:** The template now automatically installs MySQL instead of relying on the Gitpod MySQL image. The message about a Python linter not being installed has been dealt with, and the set-up files are now hidden in the Gitpod file explorer.

**April 13 2020:** Added the _Prettier_ code beautifier extension instead of the code formatter built-in to Gitpod.

**February 2020:** The initialisation files now _do not_ auto-delete. They will remain in your project. You can safely ignore them. They just make sure that your workspace is configured correctly each time you open it. It will also prevent the Gitpod configuration popup from appearing.

**December 2019:** Added Eventyret's Bootstrap 4 extension. Type `!bscdn` in a HTML file to add the Bootstrap boilerplate. Check out the <a href="https://github.com/Eventyret/vscode-bcdn" target="_blank">README.md file at the official repo</a> for more options.

--------

Happy coding!
