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
     - \_id
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
   - A user has the ability to Upload a Dingbat from their My Dingbats page.
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
2. Verify form is saved correctly to MongoDb Dingbats collection with the following fields created:

- \_id
- contributer_id
- contributer_name
- difficulty
- image
- answer
- likes array
- dislikes array

#### Test: Edit dingbat functionality

- Log in and go to My Dingbats
- Click on Edit button on a dingbat card
- Verify user brought to Edit dingbat page
- Click replace image and verify functionality of cloudinary upload widget
- Change difficulty field
- Change the answer text
- Click Upload button
- Verify User is brought to My Puzzles page and changes to the edited dingbat have been made.

#### Test: Delete dingbat functionality

- Log in and go to My Dingbats
- Click on Delete button on a dingbat card
- Verify page refreshes and the Dingbat is deleted

#### Test My Account and Change Password functionality

- Log in and click on My Account link in navbar
- Verify user is brought to their My Account page with correct username and email values are displayed. These fields are uneditable.
- To change password click on 'Change Password' button
- Verify user is brought to the Reset Password fields
- Verify field validation is active. Trigger field validation errors and verify the error messages are displayed
  1. Passwords must be a minimum of 6 characters
  2. Passwords must match
- Enter 2 new valid passwords and verify user is brought back to My Account page and flash success message is displayed.
- Log out and log back in using old password
- Verify log in is denied
- Log in using new password
- Verify log in access is granted