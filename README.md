# Peter Kellett - Data Centric Development - Milestone Project 3

## Introduction

The purpose of this project is to demonstrate my ability in the use of a document based database and to perform Create, Read, Update and Delete (CRUD) operations on it.
For this I have constructed a simple Dingbats dictionary where users can view and filter through all the existing entries and be able to upload their own ideas too. Although a user can view all of the users puzzles they only have the ability to edit and delete their own puzzles. I am using MongoDb to store the database documents.

I have also incorporated a 'Likes' and 'Dislikes' functionality as a simple way for different users to show their satisfaction to a particular puzzle. A user must be registered and logged in to avail of this functionality although the number of Likes and Dislikes that each puzzle has are still shown to guest users.

## Sitemap

![Site Map](https://res.cloudinary.com/dfboxofas/image/upload/v1600962101/Project-3-readMe%20images/sitemap_o22eng.png)

## Modules and Source libraries

### Flask

This dynamics of this website is implemented using the Jinja template engine which allows for the use of Jinja templating logic along with the Flask framework in Python which are accessed using the PyPI import modules.

### Flask Modules used

- render_template: This method is used for delivering the required page from the templates folder and the respective template inheritance and Jinja templating logic.
- redirect: This method is used to redirect users to a different URL than the one requested as an aid to site navigation.
- url_for: This is used to generate a URL to a given endpoint and calls the respective Python function to be executed.
- session: This module is used to store various user session variables and are set when a user either registers or logs in. They are removed when a user logs out or closes their browser thus ending their session.
- flash: This module provides the ability to display feedback messages to the user. The flash functionality makes it possible to record a message at the end of one request and access it with the next request and only next request. Once flash messages are rendered to the user they are deleted from the flash messages list.
- passlib: This module enables the sha256_crypt encryption method any passwords provided to keep users passwords safe and confidential.

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

## User Experience (UX)

### Navbar

A fixed navbar is used in the website design as some of the page content can vary depending on which filters the user has applied. By applying a fixed navbar this will allow the user to navigate to other pages without the need to scroll the page to the top.

### Index array

As this is a dictionary/glossary of dingbat definitions the user experience comes with being able to filter through the definitions in a concise controlled way. With this in mind an alphabet array index is provided for the user which will return all items with an answer beginning with the indexed letter.

### Filtering by Difficulty

A user is able to filter by the difficulty category, this is provided via a dropdown menu button.

### Filtering by Contributer

A user is able to view all of a particular contributers entries by clicking the contributer name in each puzzle.

### Likes/dislikes

To provide an element of interaction to users a user also has the ability to express their satisfaction of each entry. This is provided by way of thumbs up and thumbs down icons on each puzzle card. A user must be registered and logged in to be able to indicate a like or dislike as the user id is required. The user id is required for the following reasons:

1. To retain a users indications for future site visits the users id is stored to the respective puzzle MongoDb document likes array or dislikes array.
2. To be able to indicate the number of likes or dislikes each puzzle has to all visitors this is the number of entries in the respective puzzle arrays.
3. To prevent unwarranted users from repeatedly clicking the like or dislike icon thus racking up indiscriminate values for each.

### Uploading personal ideas

Once a user has registered they then have the ability to upload their own ideas to the Dingbat Dictionary. This is facilitated by the user clicking on the My Puzzles link in the navbar where they can view all their existing entries and a button to take them to the puzzle upload page.

#### The puzzle upload page

The puzzle upload form consists of 3 inputs.

1. A cloudinary image upload widget
2. A select input for selecting the difficulty category
3. A text input for the answer

## User Security

### Passwords

As a website that involves users adding their own content it is of upmost importance that this content remains secure to that user and is in no way corruptable by others. For this reason a registration/login with password encryption functionality is employed using passlib module from flask.

### Logged in Session variables

This website uses the flask session module to allow the use of storing unique user variables on the server-side as key: value pairs and are used alongside Jinja Templating Logic to allow us to control which content is displayed to users dependant on whether they are logged in or not. It is used to control access to modifying personal account details such as My Puzzles and the change password functionality. They are set when a user either registers or logs in and are deleted when a user either logs out or closes the browser tab.
The session variables being stored in this case are:

- ["id"]: users mongoDb ObjectId
- ["user"]: users mongoDb username

#### session["id"]

session["id"] = users.ObjectId  
The users unique ObjectId is stored to the session variable on login. This is required to authenticate the user when updating the users password to ensure the correct users password is updated.
The users ObjectId also used to set the contributer_id field in the puzzle document when a user uploads a new puzzle. This allows us to securely return all the puzzle documents relating only to this user when they click on the My Puzzles link.
The session["id"] variable is also used to control whether the upload/edit/delete puzzle buttons are displayed to the user when a user views another contributers puzzles. If the puzzle.contributer_id value equals the session{"id"] value then we know the user is viewing their own puzzle entries and thus can render the upload/edit/delete buttons to the user. If a user is viewing a contributers puzzles where the contributer_id value does not equal the session["id"] value then the upload/edit/delete buttons for the puzzles are not rendered to the user thus making the puzzles read only.
The session["id"] variable also serves as the user identifier which is pushed/pulled to the likes/dislikes arrays in the puzzle documents. This allows us to retain which puzzles a user has liked or disliked so can render their previous selections on future and subsequent visits to the site.

#### session["user"]

session["user"] = users.username  
The users username as supplied when registering is stored as a session variable upon subsequent logins. This allows us to provide a personal touch and good user feedback by dynamically displaying it to the user in page content.

## Database Schema

### Users collection

| Field    | Data Type      | Form Validation Type | Required Field |
| -------- | -------------- | -------------------- | -------------- |
| \_id     | ObjectId       | Auto generated       | Yes            |
| email    | String         | Email                | Yes            |
| username | String         | Text                 | Yes            |
| password | Text encrypted | Text                 | Yes            |

---

### Difficulty_categories collection

| Field      | Data Type | Form Validation Type | Required Field |
| ---------- | --------- | -------------------- | -------------- |
| \_id       | ObjectId  | Auto generated       | Yes            |
| difficulty | String    | None                 | Yes            |

---

### Puzzles collection

| Field            | Data Type                        | Form Validation Type | Required Field |
| ---------------- | -------------------------------- | -------------------- | -------------- |
| \_id             | ObjectId                         | Auto generated       | Yes            |
| image            | String (URL)                     | None                 | Yes            |
| answer           | String                           | Text                 | Yes            |
| difficulty       | difficulty_categories.difficulty | None                 | Yes            |
| contributer_name | users.username                   | None                 | Yes            |
| contributer_id   | users.\_id                       | None                 | Yes            |
| likes            | Array [users._id]                | None                 | No             |
| dislikes         | Array [users._id]                | None                 | No             |

## Testing  
### Features tested  
1. Screen responsiveness  
2. Site navigation links
3. Register a user
4. Login / Logout
5. Password encryption and site Security
6. Uploading a new dingbat entry
7. Editing and deleting dingbat entries
8. Initiating likes and dislikes xor functionality
Full details on testing and procedures can be seen in [testing.md](./testing.md).  

## Deployment Procedures

This projects repository is held in GitHub and is hosted with Heroku Apps.
Deployment to Heroku Apps is done from the GitHub master branch.

- GitHub repository: https://github.com/PeterKellett/project-3

#### Deployment procedure to implement new functionality

1. Go to project repository above and create a new upstream branch or raise an issue, this will also create an upstream branch.
2. Open this branch or issue in code editor. For this project GitPod was used.
3. Add and commit code to this branch until satisfied code can be merged with the main branch.
4. Send a pull request to GitHub requesting the branch can be merged.
5. If there are no conflicts raised this branch or issue can then be closed by performing a merge onto the main branch. A merge can also be performed from GitPod.
6. This GitHub repository master branch is automatically connected to Heroku through Heroku settings so any merges to the GitHub master branch are automatically deployed and built in Heroku.

#### Deployment procedure to clone this project

1. Go to project repository above and click 'Code' button
2. Copy the url (see image below and for full instructions see https://docs.github.com/en/enterprise/2.13/user/articles/cloning-a-repository)
   ![Screenshot](https://res.cloudinary.com/dfboxofas/image/upload/v1601037183/Project-3-readMe%20images/clone_screenshot_i5mgip.png)
3. In your code editor have the following installed:

   - Git
   - pip3
   - dnspython
   - flask
   - flask-pymongo
   - flask-wtf
   - flask cloudinary

   These are installed from the Python Package Index (PyPI) repository.

4. Install the cloned repository by running the code snippet copied above.
5. Create a requirements.txt file by running:  
   pip3 freeze --local > requirements.txt

#### Connect to MongoDb

1. In MongoDb click on the connect button on the cluster you wish to connect to and copy the connection string provided.
2. Create an env.py file to contain the MONGO_URI connection string. Correct the 'dbname' and 'password' values in the connection string to the correct values.
3. Add this env.py file to .gitignore.
4. This program can now be run locally by running the command:
   - python3 run.py

#### To connect to Heroku

1. Create a Procfile to initiate the Heroku web dyno.
   echo web: python3 run.py > Procfile
2. In your Heroku App go to Settings and Reveal Config Vars.
3. Configure the variables as:  
   | KEY | VALUE |  
   | -------- | -------------- |  
   | IP | 0.0.0.0 |  
   | PORT | 5000 |  
   | MONGO_URI | mongodb+srv://root:<password>@myfirstcluster.jraod.mongodb.net/<dbname>?retryWrites=true&w=majority |
   | SECRET_KEY | <secret_key> |

#### To deploy to Heroku from GitHub master branch
1. In your Heroku App go to Deploy tab.
2. Choose the deployment method, choose GitHub.
3. Enter the repository name and GitHub password.
4. Click deploy from master branch.
5. This setting can be automated so any new merges to the GitHub master branch will automatically redeploy and build on Heroku Apps.

## Bugs and troubleshooting
During the course of this project I encountered many, many minor issues. Most were to do with setting and passing the relevant variables from one function to another. These were mainly identified using the built in python debug tool, the browser developer tools and printing values and types of variables to the console for further examination and using online documentation. 
Examples of such were:  
- Working with ObjectId's 
- PyMongo curser objects
- Pushing and pulling ObjectId's to arrays 
- Password encryption 
- Jinja templating logic

## Online References used 
Flask:  
https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/  
https://pythonprogramming.net/practical-flask-introduction/  
Materialize:  
https://materializecss.com/about.html  
Cloudinary:  
https://cloudinary.com/documentation/cloudinary_guides  
MongoDb:  
https://docs.mongodb.com/manual/reference/method/  
HTML CSS JavaScript:
https://www.w3schools.com/  
Other resources:  
https://stackoverflow.com/  
https://www.favicon.cc/  



