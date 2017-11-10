# Taxi API Django Rest
[![Build Status](https://travis-ci.org/juniorgerdet/tappsi_test.png)](https://travis-ci.org/juniorgerdet/tappsi_test)

**Great seed - demo of a Full API powerful with all main features of best practices on Django, Python, Django Rest Framework and others for Taxi Apps **

A powerful combination:

* Lettuce BDD
* Django Oauth Toolkit
* CORSHEADERS
* Native Pagination
* Nested Serialize
* Parsers
* Renders
* Continuos Integrations
* Detection of Users Agents
* Swagger Documentation

## Author: Junior Gerdet

You may also want to follow the [author](https://twitter.com/juniorgerdet) on Twitter. My email is juniorgerdet@gmail.com

# Overview

A seed with demo and combination of features powerful django rest for Taxi Apps.

# Requirements

* Python (2.7, 3.2, 3.3, 3.4)
* Django (1.7, 1.8)

#Environment

I recomend virtualenv

    virtualenv name --no-site-packages
    source /path/a/name/bin/activate
    

# Installation of dependencies

Install using `pip`...

    pip install -r requirements.txt

Preparation:

    python manage.py migrate
    python manage.py makemigrations tappsi_api
    python manage.py sqlmigrate tappsi_api 0001 
    python manage.py migrate
    python manage.py createsuperuser
    
For execute the automatized test:

    python manage.py harvest -d tappsi_api/features/


**Note**:   The next step is optional, when you execute the automatized tests, the database is loaded with the credentials.

Step 1: Register an application
To register the app:

  To obtain a valid access_token first we must register an application. DOT has a set of customizable views you can use to CRUD application instances, just point your browser at:

    python manage.py runserver 
    
  Access to url and login with superuser:

    http://127.0.0.1:8000/admin/
    
  Now, access to url:

    http://127.0.0.1:8000/o/applications/
  
Click on the link to create a new application and fill the form with the following data:

* Name: just a name of your choice
* Client Type: confidential
* Authorization Grant Type: Resource owner password-based
* Save your app!

# Documentation & Support

The documentation of API is available at [docs](http://127.0.0.1:8000/api/v1/docs).

For questions, juniorgerdet@gmail.com

## Contact

You may also want to follow the [author](https://twitter.com/juniorgerdet) on Twitter.
