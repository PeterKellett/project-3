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
### Test: Device responsive testing  
This project was tested for display responsiveness using the following screen sizes.
1. Large screen
    - Desktop Chrome
    - Desktop Firefox
    - Desktop Microsoft Edge  
2. Medium screen
    - iPad Pro Safari  
    - Desktop Chrome emulator
3. Small screen  
    - Phone Samsung 7
    - iPhone 6
    - Desktop Chrome emulator  

### Functional Testing  
#### Test: Navbar links  
1. When user logged out verify the navbar contains the following links.
    - Home: Verify user is navigated to the home page.
    - Dingbats: Verify user is navigated to the main Dingbats page.
    - Join: Verify user is brought to the Registration page.
    - Login: Verify user is brought to the login page.
2. When user is logged in verify the navbar contains the following links.
    - Home: Verify user is navigated to the home page.
    - Dingbats: Verify user is navigated to the main Dingbats page.
    - My Dingbats: Verify user is brought to a page showing their own uploaded Dingbat entries and the upload/Edit/Delete buttons are rendered,
    - My Account: Verify user is brought to the My Account page.
    - Logout: Verify user is logged out and is returned to the Home page.

#### Test: Home page buttons 
1. When user logged out verify following page buttons are displayed.
    - Join: Verify user is brought to the Registration page.
    - Login: Verify user is brought to the login page.
    - Browse: Verify user is navigated to the main Dingbats page.
2. When user is logged in verify the only the Browse button is displayed.

#### Test: Dingbat page letter array 
The letter array on the Dingbat page serves as an index to the user by returning only the Dingbats with an answer beginning with the chosen letter.
- Click on each letter in turn and verify only Dingbats with an answer beginning with that letter are returned.

#### Test: Dingbat page Difficulty select button 
- Verify the button dropdown selections contain Easy, Medium, Hard.
- Click on each selection in turn and verify only Dingbats with the selected difficulty are returned.

#### Test: Dingbat Answer buttons 
- Click on each answer button and verify the button/answer is toggled with each click on that Dingbat card only.  

#### Test: Likes/Dislikes 
1. When user is logged out.
    - Verify the thumb icons are disabled and colored blue.
    - Click on a thumb icon and verify a flash message 'You must be logged in to add likes/dislikes' is displayed to user.
    - Verify the total number of the Dingbats likes and dislikes is displayed on the card and are colored green and red respectively.  
2. When user is logged in. 
    - Verify the thumb icons are enabled and colored green and red respectively.  
    - Click on a green 'like' thumb icon and verify the number of likes for that Dingbat entry is incremented by +1 and the thumb icon clicked is now rendered in a larger size. 
    - Click on that same green 'like' thumb icon again and verify the number of likes for that Dingbat entry is decremented by -1 and the thumb icon clicked is now rendered in a normal size. 
    - Click on a red 'dislike' thumb icon and verify the number of dislikes for that Dingbat entry is incremented by +1 and the thumb icon clicked is now rendered in a larger size. 
    - Click on that same red 'dislike' thumb icon again and verify the number of dislikes for that Dingbat entry is decremented by -1 and the thumb icon clicked is now rendered in a normal size.  
3. Testing xor logic on likes/dislikes  
    - Click on a green 'like' thumb icon and verify the number of likes for that Dingbat entry is incremented by +1 and the thumb icon clicked is now rendered in a larger size. 
    - Click on the red 'dislike' thumb icon on the same Dingbat card and verify that the number of likes is decremented by -1 and the green thumb icon is reduced in size and at the same time verify the red dislike number is incremented by +1 and the red thumb icon is increased in size.
    - Click on a red 'dislike' thumb icon and verify the number of dislikes for that Dingbat entry is incremented by +1 and the thumb icon clicked is now rendered in a larger size. 
    - Click on the green 'like' thumb icon on the same Dingbat card and verify that the number of dislikes is decremented by -1 and the red thumb icon is reduced in size and at the same time verify the green like number is incremented by +1 and the green thumb icon is increased in size. 
- These tests were also double checked by verifying in MongoDb that the correct user ObjectId's were being correctly pushed and pulled from the respective Mongo document arrays.  


#### Test: Verify Dingbat Contributer links
- Click on a contributers name and verify user is brought to page showing that contributers entries. 

#### Test: Verify Upload/Edit/Delete buttons hidden if contributers id != the session id variable
Clicking on the contributer name on a Dingbat card will bring a user to the Dingbat page for that contributer so a user can view all of that contributers Dingbat entries. By using logic and comparing the contributers ObjectId to the ObjectId stored in the session variables, we can use logic to prevent access to the upload/edit/delete functionality when these variables do not match thus providing read only access and stopping unauthorised access to others to prevent malicious tampering of Dingbat entries.  

- Log in as a user with Dingbats uploaded. 
- Click on the name of any other contributer. Verify the Dingbats are displayed but the Upload/Edit/Delete buttons are not rendered.
- Repeat for many different contributers.
- Now click on your own name on a Dingbat uploaded by the user you logged in as.
- Verify the Upload/Edit/Delete buttons are rendered as the contributers id of the Dingbat selected will be the same as that stored in the session id variable so the Jinja logic will now permit the user access to these editors rights.
- Repeat the above as a logged out user and verify these buttons are again not rendered for any contributer whatsoever.

#### Test: Register
1. Field validation test  
    Username:  
    - Verify this field must fail if less than 4 characters are entered.  
    - Verify validation fail message is displayed for failed attempts.
    - Message "Username must be at least 4 characters long."

    Email:  
    - Verify this field must fail if the input is not of email format.
    - Verify validation fail message is displayed for failed attempts.
    - Message "Email supplied is not of the correct format."

    Password:
    - Verify this field must fail if less than 6 characters are entered.
    - Verify input charaters are blobbed out for user confidentiality.
    - Verify validation fail message is displayed for failed attempts. 
    - Message "Passwords must have a minimum of 6 characters" 

    Repeat Password:
    - Verify this field must fail if this field does not match the Password field.
    - Verify input charaters are blobbed out for user confidentiality.
    - Verify validation fail message is displayed for failed attempts.
    - Message "Passwords must match"  

2. MongoDb Users document
    - Register a new user and verify the a new MongoDb Users document was created with the following fields submitted.  
        - _id
        - username
        - email
        - password

3. Password encryption method  
    - Register as user and verify backend in MongoDb that the password for the new users password is in an encrypted format.  


#### Test: Login / Logout
1. Field validation test 
    Email:  
    - Verify this field must fail if the input is not of email format.
    - Verify validation fail message is displayed for failed attempts.
    - Message "Email supplied is not of the correct format."  
    Password:
    - Verify this field must fail if less than 6 characters are entered.
    - Verify input charaters are blobbed out for user confidentiality.
    - Verify validation fail message is displayed for failed attempts. 
    - Message "Passwords must have a minimum of 6 characters"  
2. Login functionality   
    Login and verify the following changes to the site.
    - The Navbar links should now be for:
        - Home
        - Dingbats
        - My Dingbats
        - My Account
        - Logout
    - The correct username should be displayed in the Welcome header on the Home page.
    - The 'Like' and 'Dislike' functionality is now enabled. 
    - A user has the ability to Upload a Dingbat from their My Puzzles page.  
3. Logout functionality  
    Click on 'Logout' link in navbar and verify all session variables have been deleted all logged in functionality is disabled.

#### Test: Upload functionality
1. Cloudinary upload widget  
    - Verify Cloudinary upload widget opens and closes without error.
    - Verify user can upload an image from all sources.
        - Local 
        - Web address
        - google Drive
        - Dropbox
        - Facebook
        - instagram
        - Shutterstock
    - 


