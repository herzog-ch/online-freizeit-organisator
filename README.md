# ofo. - Online Freizeit Organisator

The Online-Freizeit-Organisator is implemented in Python3 using the Django framework.<br>
The deployment can be done easily using Docker. The Django development server is used by purpose to keep the setup effort minimal. In production this method shouldn't be used.

## 5-Minute-Setup

The deployment of the app is done using Docker. During the build step the Django project is added to the image and the required Python3 packages are installed.
The container is exposing port 8000.

```
# clone repo
git clone https://github.com/herzog-ch/online-freizeit-organisator.git

# build the Docker image
cd online-freizeit-organisator
docker build -t ofo_django_app_image .

# run a Docker container
docker run -p 8000:8000 -i -t ofo_django_app_image
```

Open Chrome Browser: http://localhost:8000<br>
Stop the container with CMD+C / CTRL+C<br>
Resume the container with:<br>
```
# list all containers
docker ps -a

# find your stopped container name, e.g. "zealous_hugle"
docker start -ai <container name>
# e.g. docker start -ai zealous_hugle
```


## Features

+ User management
+ Creating new meetings and inviting other users by username
+ Live User Search for inviting people
+ Sending invitation email notifications
+ Giving proposals and comments for meetings
+ Mobile friendly design


## 3rd Party Libs

+ jQuery 3.4.1
+ popper.js 1.16.0
+ Bootstrap 4.4.1
+ Fontawesome Icons


## Project Structure

The Django project is structured in two apps for better reusability.<br>
The Login app is responsible for signing up, login and logout. It provides the forms and templates for these tasks.
The Events App contains everything related to creating and managing events. This comprises database models for events, status, proposals as well as different forms. Django templates as well as static resources (Javascript, CSS) for the event views are also contained in the app.

### Login App

+ Models<br>
    For the login application there are no custom models needed, since the "User" model from django.contrib.auth.models can be used.
+ Views
  + Login (\<host\>/login):
    + Template: login/templates/login/login.html
  + Logout (\<host\>/logout)
    + No template -> redirects back to login view 
  + Signup (\<host\>/signup)
    + Template: login/templates/login/signup.html
+ Forms
  + RegistrationForm
  + LoginForm
+ Static Files<br>
    No additional static file (css, js) is needed in the login app


### Events App

+ Models
  + Status
  + Event
  + Proposal
+ Views
  + detail
    + Templates:
      + events/templates/events/events_detail.html
      + events/templates/events/events_detail_determine_partial.html
      + events/templates/events/events_detail_give_proposal_partial.html    
      + events/templates/events/events_detail_proposal_partial.html           
  + overview
    + Templates:
      + events/templates/events/events_overview.html
      + events/templates/events/events_overview_invited_partial.html
      + events/templates/events/events_overview_organised_partial.html      
  + new_event
    + Templates:
      + events/templates/events/events_new.html  
  + user_search
    + Templates:
      + events/templates/events/search_result_partial.html
    + Javascript: events/static/js/user_search.js
  + delete_event
+ Forms
  + NewEventForm
  + ProposalForm
  + DetermineEventForm
+ Static Files
  + Javascript + CSS in events/static/events/js and events/static/events/css  


### Base Templates

All templates extend the template base.html in the project directory /templates.
Header, menue and footer as well as the integration of e.g. bootstrap and jQuery are defined here and therefore never duplicated.