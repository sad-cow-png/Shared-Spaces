# Shared-Spaces
CMSC 447 Web development project.

As restrictions related to the COVID-19 pandemic begin to relax, the demand for publicly accessible,
socially-distant spaces will increase for individuals with various needs. The Shared Spaces web 
application allows users to list, search for, and reserve spaces based on specific criteria such as
maximum occupancy, noise level allowance, wifi availability, etc. Listed spaces will be enhanced with
client ratings and reviews based on their experiences so that other users can identify new and exciting
spaces to explore. The platform will offer user-friendly maps and geolocation services that allow all
users to locate their intended space intuitively.

Shared Spaces services the needs of a post-pandemic world, available on desktop and mobile devices. 

























<br>

### Proprietor Login Background:

When a user uses a signup form, it sets the flags ```is_client``` or ```is_proprietor```
to true depending on which account type they are signing up for. The signup and login forms built off of django contains 
username and password validation. The main signup/login page allows users to select which account type
they are and takes them to the client/proprietor signup/login pages.

URLs:
<br>
http://127.0.0.1:8000/sign_up/ <br>
http://127.0.0.1:8000/sign_up/proprietor/ <br>
http://127.0.0.1:8000/login/ <br>

After successfully logging in as a proprietor, the page redirects to account. Account page displays account type
and username, with logout and home links below. Accessing the account page while not logged in will redirect to main login page.
<br>
http://127.0.0.1:8000/login/proprietor/ <br>
http://127.0.0.1:8000/account/ <br>
http://127.0.0.1:8000/logout/  <br>
<br>

##### Testing proprietor signup:
```
python manage.py test sharedspaces.tests.ProprietorSignUpTest
```
##### Testing proprietor login:
```
python manage.py test sharedspaces.tests.ProprietorLoginTest
```
<br>