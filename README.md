# Shared-Spaces
## CMSC 447 Web development project.

As restrictions related to the COVID-19 pandemic begin to relax, the demand for publicly accessible,
socially-distant spaces will increase for individuals with various needs. The Shared Spaces web
application allows users to list, search for, and reserve spaces based on specific criteria such as
maximum occupancy, noise level allowance, wifi availability, etc. Listed spaces will be enhanced with
client ratings and reviews based on their experiences so that other users can identify new and exciting
spaces to explore. The platform will offer user-friendly maps and geolocation services that allow all
users to locate their intended space intuitively.

Shared Spaces services the needs of a post-pandemic world, available on desktop and mobile devices.

### **For Developers**:

#### Create Space Background:

Creating a space for each proprietor involves entering data to a form that will save entries into a Space
model or table so that each shared spaces listed space will exist as its own entry that can be associated to individual
accounts. The spaces can be both created and modified once created. As of now, the only way to get to the creation page
is to use the direct link to the page. The link is as follows: http://127.0.0.1:8000/create_space/. Similarly, in order
to modify the spaces, you would use a similar link along with the id of the space to edit it. The id is just the primary
key of the space in the database. The link is as follows: http://127.0.0.1:8000/update_space/<id>. Later on as the
account pages for the proprietor is completed, these pages will be accessible through buttons on the account page.

##### Testing Creation and modification of spaces:
The command to run the tests are as follows. There are still a few issues with selenium testing. For now the test is
commented out and not included in the repo until a better solution is found.
```
./manage.py test sharedspaces.tests.CreateSpaceTests
```

<br>

#### User Login Background:
When a user uses a signup form, it sets the flags ```is_client``` or ```is_proprietor```
to true depending on which account type they are signing up for. The signup and login forms built off of django contains 
username and password validation. The main signup page allows users to select which account type
they are and takes them to the client/proprietor signup page.

URLs:
<br>
http://127.0.0.1:8000/sign_up/ <br>
http://127.0.0.1:8000/sign_up/proprietor/ <br>
http://127.0.0.1:8000/sign_up/client/ <br>

After successfully logging in, the page redirects to account. Account page displays account type
and username, with logout and space links in header. Accessing the account page while not logged in will redirect to login page.
<br>
http://127.0.0.1:8000/login/ <br>
http://127.0.0.1:8000/account/ <br>
http://127.0.0.1:8000/logout/  <br>
<br>

##### Testing proprietor signup:
```
python manage.py test sharedspaces.tests.ProprietorSignUpTest
```
##### Testing login:
```
python manage.py test sharedspaces.tests.LoginTest
```
<br>


#### Interactive Map Background:
The Google Maps JavaScript API embeds an interactive map centered over UMBC within a
Django HTML template. As of current, the Spaces model does not yet have a location
field, so the JavaScript functionality is not yet integrated with the SQL database.

Current map functionality includes the ability to navigate and adjust the positioning
of the map as well as the placement of markers.

##### Testing the interactive map
There are not tests for the map due to it just being a front end and no backend has been set up yet.

<br>

### Selenium tests for authentication
Before running tests, please _**runserver**_ and _**read comments**_
on each test. User and space variables are adjustable depending on every developer's needs.

```
python manage.py runserver
```

#### Creating new users for tests
```
python manage.py test sharedspaces.tests.CreateUsers
```
#### Creating new spaces for tests
```
python manage.py test sharedspaces.tests.CreateSpaces
```
**Note:** If creating new users somehow breaks, change username and password in
setUp for tests below using users you have created already. 

#### Tests for proprietor_required decorated views
Protect views only accessible to proprietors.
```
python manage.py test sharedspaces.tests.ProprietorRequiredTests
```
#### Tests for user_is_space_owner decorated views
Prevents miscellaneous users from editing spaces they did not create.
```
python manage.py test sharedspaces.tests.SpaceOwnerTests
```
<br>

#### Template Tests
Simple checks for correct template usage and if certain major elements are present on page.
```
python manage.py test sharedspaces.tests.PageTemplateTests
```
<br>

#### Date and time Background:
The date and time of availability for the spaces required a little planning and working with three different tables.
Below is the image of what was planned when it comes to the back end. <br>
![Table Planning](https://cdn.discordapp.com/attachments/808745673280323644/832413159347847228/unknown.png) <br>
This was a diagram create by Sharlet, and the overall design of how the user account, space, and date/time table would be 
related. This shows how a user who is a proprietor can own spaces. A proprietor can own many spaces, so we have a one to
many relationships there. Similarly, the space can have multiple time and date availability. So, spaces have a one to 
many relationships with the time/date table. 

##### Date and time Testing:
Most of the test were done for the form and the model. The integration testing will be done once the space reuse story
is completed as that is what will connect all the tables together and have a working system.
```
python manage.py test sharedspaces.tests.TestSpaceDateTime
```
<br>

#### List spaces Background:
List out the spaces in the user account was mostly already complete but what was needed to be added were a few buttons.
So, a few buttons were added and with that the ability to edit and add time/date for the space. 

##### List spaces Testing:
The test mainly checks that the functionality required for the card is working correctly. This involves making sure
that the space connected to the user can be retrieved easily. The testing for actual front end is not added.
```
python manage.py test sharedspaces.tests.ListSpacesTest
```

<br>

#### Space Reuse Background:
Reuse consisted of making sure that the space had different times that could be signed up for. This consisted of 
connecting a lot that had already been completed. Fixing up the buttons done for the card set up in account
to redirect to the list of dates and time was one of them. It also consisted of making sure new dates could be added
or deactivated and much more. 

##### Space Reuse Testing:
The testing mainly consists of making sure that the spaces created can have dates linked to them and that nothing goes
wrong in the database when they are being connected using the foreign key. 
```
python manage.py test sharedspaces.tests.SpaceReuseTest
```

<br>

#### Deactivate Space Background:
When we deactivate a space, we change the status of the model to not open and there is a text printed on the card that
lets the user know that the space is not active. This mainly affects the proprietors account.

##### Deactivate Space Testing:
The main testing here consisted of making sure that when the space is set to in active, and we access it from a user's
space it still hold the value that it is closed. This is the main process used to change the status of the space.
```
python manage.py test sharedspaces.tests.SpaceCloseTest
```
