# ofo. - Online Freizeit Organisator

## 5-Minute-Setup

The deployment of the app is done using Docker. During the build step the Django project is added to the image and the required Python3 packages are installed.
The container is exposing port 8000.

```
# clone repo
git clone https://github.com/herzog-ch/online-freizeit-organisator.git

# build the Docker image
docker build -t ofo_django_app_image .

# run a Docker container
docker run -p 8000:8000 -i -t ofo_django_app_image
```

Open Chrome Browser: http://localhost:8000


## Features

+ User management
+ Sending invitation email notifications
+ Live User Search for inviting people
+ Giving proposals and comments for meetings


## 3rd Party Libs

+ jQuery 3.4.1
+ popper.js 1.16.0
+ Bootstrap 4.4.1
+ Fontawesome Icons


## Project Structure

### Login App

+ Models
    
    For the login application there are no custom models needed, since the "User" model from django.contrib.auth.models can be used.

+ Views
  + Login (\<host\>/login):
    + Template: login/templates/login/login.html
  + Logout (\<host\>/logout)
    + No template -> redirects back to login view 
  + Signup (\<host\>/signup)
    + Template: login/templates/login/signup.html

+ Static Files

    No additional static files (css, js) is needed


### Events App

### Base Templates

All templates extend the template base.html in the project directory /templates.
Header, menue and footer as well as the integration of e.g. bootstrap and jQuery are defined there and therefore never duplicated.