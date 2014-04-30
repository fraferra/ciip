CIIP4ME Documentation
----------------------

Introduction:

  Welcome! If you are reading this it means that you will have the great privilege of maintaining and improving the ciip4me website. This documentation is divided in three section, depending on three different stakeholders: 1- Coders 2-Managing content 3-Admin work
  
===================================================================

SECTION 1:
----------

WARNING:
When Liz and I firstly started to work on this we had no previous programming experience. If you have a CS background you might find many redundancies and structural errors, please feel free to change them!

THE PHILOSOPHY:
During last year developing something quickly was the most important thing to achive, for this reason we built the app using as a framework Django and hosting the website on Heroku for a quick hosting. If you have never used Django please follow the tutorial at https://docs.djangoproject.com/en/1.5/intro/tutorial01/ . The Django version used here is 1.5.4

The OS we suggest is Ubuntu 12.04 and all the following instructions that you will see assume that you are using Ubuntu 12.04. We choose Ubunut because since we are working with open source software it's often much easier to install it on Ubunut rather than using Windows or Mac.

1.The Set-Up:
-------------
Firstly let's setup our enviroment in order to have Django ready.

a. Install pip
```
$ sudo apt-get install python-pip
```
b. Install Django
```
$ pip install Django   (May require: $ sudo pip install Django)
```

c. Install PostgreSQL
```
$ apt-get install postgresql-9.3
```

d. Install the psycopg2 driver for PostgreSQL
```
$ sudo easy_install psycopg2
```
2.Familiarazing with Django 1.5.4
--------
OVERVIEW

We used a Model–view–controller (MVC) architecture. The structure of every object ( student, manager, university admin etc. ) is defined in /ciip/models.py . /ciip/views.py controls the views and the requests of the users and in /ciip/templates/ciip/ you will find all the templates used. Please familiarize with the template tags used in Django (http://jinja.pocoo.org/docs/templates/ ) in order to understand how we display the info in the templates.

In the folder mysite you will find settings.py ; ciip is the actual Django app.

The Models

  In models.py you will find all the objects used in ciip4me. Eache field describes a property of the object.
  
  ATTENTION: If you change a field in models make sure to use South aftward to migrate from your old database schema to your new database structure. Look at the section South in this documentation to see how to do it.



SOUTH
-----

OVERVIEW

South is used to migrate your database anytime you make a change to your models. South is now integrated with Django 1.7 but since we are using Django 1.5.4 you will have some basic commands that you need to do to migrate succssefully the database.

Firstly have a look at this South introduction, http://south.readthedocs.org/en/latest/tutorial/part1.html . 

The Process:

Usually any time I make a change I apply this kind of workflow:

  1.Change a field in my models
  
  2.Run this command:
  ```
  $ python manage.py schemamigration ciip --auto
  ```
  















