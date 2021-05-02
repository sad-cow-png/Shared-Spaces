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

#### Tagging Spaces Background:
Proprietors can tag their spaces by one or however many long words/phrases
separated by commas on create space and update space forms. Tags can be added and removed in
any order, thanks to django-taggit. Tags are first cleared, then added back in 
with duplicate checking in update_space. In create_space, tags are manually added
after the space has been saved. 

##### Create space tagging tests
Tested adding tags and not adding tags as it is not required.
```
python manage.py test sharedspaces.tests.CreateSpaceTagTests
```
##### Update space tagging tests
Tested adding, removing one tag, removing all tags and making sure
tags appear on user account page.
```
python manage.py test sharedspaces.tests.UpdateSpaceTagTests
```

##### Tagged Spaces
Users can click on badges for each tag to go to its page which displays
all spaces that have the tag. 
##### Tagged spaces tests
```
python manage.py test sharedspaces.tests.TaggedSpacesTests
```

<br>

#### Reserve Space
Only clients may access page to reserve a time slot for a space. Each space page
has a reserve page with two selection boxes. Once the date is selected the time slot for
that date will show up. Since each date and time slot are from the same object, there will be
duplicate dates showing up in the reserve date box. Using ajax, once the date is selected, it is used to
determine the SpaceDateTime object pk to display the time slot through ``load_times`` in views.py.
String formatting for date and time slot displayed in selection boxes is done in forms.py <br><br>
Once a client clicks on the reserve button, it sends them back to account page where they can see the spaces
they have reserved.

##### Reserve space testing:
Created a simple test for making sure the reservation goes through. Will possibly add more later.
<br>
```
python manage.py test sharedspaces.tests.ReserveFormSeleniumTests
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

<br>

#### Space Address Background:
Given that each location has to be shown on the map. We need to store their addresses. So, this feature focused on
implementing that into the space model. This required removing all the old migrations as it would require a default.
But we want there to be no spaces in the database without dates. So we deleted the database, reset the migrations, and
will do the same for the Heroku Database. Overall, changed up everywhere the space model was used and fixed up all the
test for the model, and it's uses.

##### Space Address Testing:
The main test added was to make sure the address was saved correctly into the database and that the forms were working
correctly. So I mainly added to the create space tests. I also edited the space close tests, space reuse test, list
space tests, and space date and time tests.
```
./manage.py test sharedspaces.tests.CreateSpaceTests
./manage.py test sharedspaces.tests.TestSpaceDateTime
./manage.py test sharedspaces.tests.ListSpacesTest
./manage.py test sharedspaces.tests.SpaceReuseTest
./manage.py test sharedspaces.tests.SpaceCloseTest
```

<br>

#### Search Bar Background:
The search bar is located on the main/home page of the Shared Spaces site. Search functionality works directly with the 
spaces and space date/time models so that users can directly search for spaces by name, description, and specific dates
for reservation. Users are able to filter search using a search toggle to the side of the search bar to narrow search.
Search results conditionally on a separate page based on filter selctions as individual cards with space details and a 
button that will allow clients to make a reservation. The search results page also includes a home button to return to the home page.

#### Search Testing:
Search testing covers the usage of querysets that extract search results from the space and space date/time models and 
check that the appropriate object is retrieved based off the search criteria.
```
py manage.py test sharedspaces.tests.SearchBarTests
```

<br>

#### Client Reserved Spaces Listings
Once a client reserves a time slot from a space reserve page. Each time instance
appears in their account page as a card.

##### Reserved Spaces Testing (Selenium):
```test_client_reservation_appears``` requires manual reset of reservation time slots
after running the test once. 
```
python manage.py test sharedspaces.tests.ClientReservedListingTests
```
<br>

#### Date/Time Edit Access Decorator Background:
We were missing a decorator that used the date and time id to determine if the proprietor is allowed to edit the form
that updates date and time for specific space. So, that was added to allow only owner of the space to edit 
the status of their date and time.

#### Date/Time Edit Access Decorator Testing:
The test consists of three unittests that make sure that only the owner of the space whose space id is stored
in the data and time model can access the view that redirects the user to the edit page. 

```
./manage.py test sharedspaces.tests.IsDateOwnerDecoratorTest
```

<br>

#### Proprietor Form Styling Background:
The main purpose behind this feature was to make the user interface much more appealing when it comes to all the forms
used by the proprietor. So, a nav bar was added to all the pages with only a few links that made sense available on 
the nav bar. Also, fixed up styling for the spaces that show up on the account page. Also, revamped the date and time 
page to look more appealing and fixed up the date and time cards.

#### Proprietor Form Styling Testing:
The main test done was the redirection changes. When a space is created the user is redirected to the account rather 
than to the page to create new date and time. All the other stuff was styling changes that just added or made the 
interface more appealing so nothing could be tested automatically. We did end up testing if the nav bar was being used
in when the specific pages were called.

```
./manage.py test sharedspaces.tests.FormsStylingTest
```

