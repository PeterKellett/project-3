# Peter Kellett - Data Centric Development - Milestone Project 3

## Introduction

The purpose of this project is to demonstrate my ability in the use of a document based database and to perform Create, Read, Update and Delete (CRUD) operations on it.
For this I have constructed a simple Dingbats dictionary where users can view and filter through all the existing entries and be able to upload their own ideas too. Although a user can view all of the users puzzles they only have the ability to edit and delete their own puzzles. I am using MongoDb to store the database documents.

I have also incorporated a 'Likes' and 'Dislikes' functionality as a simple way for different users to show their satisfaction to a particular puzzle. A user must be registered and logged in to avail of this functionality although the number of Likes and Dislikes that each puzzle has are still shown to guest users.  

## Wireframes  
![Site Map](https://res.cloudinary.com/dfboxofas/image/upload/v1600868134/Project-3-readMe%20images/sitemap_vcl8sj.png)

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
- To retain a users indications for future site visits the users id is stored to the respective puzzle MongoDb document likes array or dislikes array.
- To be able to indicate the number of likes or dislikes each puzzle has to all visitors this is the number of entries in the respective puzzle arrays.
- To prevent unwarranted users from repeatedly clicking the like or dislike icon thus racking up indiscriminate values for each.

### Uploading personal ideas

Once a user has registered they then have the ability to upload their own ideas to the Dingbat Dictionary. This is facilitated by the user clicking on the My Puzzles link in the navbar where they can view all their existing entries and a button to take them to the puzzle upload page.

#### The puzzle upload page

The puzzle upload form consists of 3 inputs.

1. A cloudinary image upload widget
2. A select input for selecting the difficulty category
3. A text input for the answer

## User Security

### Passwords

As a website that involves users adding thier own content it is of upmost importance that this content remains secure to that user and is in no way corruptable by others. For this reason a registration/login with password encryption functionality is employed using passlib module from flask.

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



## Gitpod Reminders

To run a frontend (HTML, CSS, Javascript only) application in Gitpod, in the terminal, type:

`python3 -m http.server`

A blue button should appear to click: _Make Public_,

Another blue button should appear to click: _Open Browser_.

To run a backend Python file, type `python3 app.py`, if your Python file is named `app.py` of course.

A blue button should appear to click: _Make Public_,

Another blue button should appear to click: _Open Browser_.

In Gitpod you have superuser security privileges by default. Therefore you do not need to use the `sudo` (superuser do) command in the bash terminal in any of the backend lessons.

## Updates Since The Instructional Video

We continually tweak and adjust this template to help give you the best experience. Here are the updates since the original video was made:

**April 16 2020:** The template now automatically installs MySQL instead of relying on the Gitpod MySQL image. The message about a Python linter not being installed has been dealt with, and the set-up files are now hidden in the Gitpod file explorer.

**April 13 2020:** Added the _Prettier_ code beautifier extension instead of the code formatter built-in to Gitpod.

**February 2020:** The initialisation files now _do not_ auto-delete. They will remain in your project. You can safely ignore them. They just make sure that your workspace is configured correctly each time you open it. It will also prevent the Gitpod configuration popup from appearing.

**December 2019:** Added Eventyret's Bootstrap 4 extension. Type `!bscdn` in a HTML file to add the Bootstrap boilerplate. Check out the <a href="https://github.com/Eventyret/vscode-bcdn" target="_blank">README.md file at the official repo</a> for more options.

---

Happy coding!
