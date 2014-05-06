CIIP4ME Documentation
----------------------

**Introduction**

  Welcome! If you are reading this it means that you will have the great privilege of maintaining and improving the ciip4me website. This documentation is divided in three section, depending on three different stakeholders: 1- Coders 2-Managing content 3-Admin work
  
===================================================================

SECTION 1 (CODERS):
----------

**WARNING:**
When Liz and I firstly started to work on this we had no previous programming experience. If you have a CS background you might find many redundancies and structural errors, please feel free to change them!

**THE PHILOSOPHY:**
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
**OVERVIEW**

We used a Model–view–controller (MVC) architecture. The structure of every object ( student, manager, university admin etc. ) is defined in /ciip/models.py . /ciip/views.py controls the views and the requests of the users and in /ciip/templates/ciip/ you will find all the templates used. Please familiarize with the template tags used in Django (http://jinja.pocoo.org/docs/templates/ ) in order to understand how we display the info in the templates.

In the folder mysite you will find settings.py ; ciip is the actual Django app.

/ciip/
------

This is actual app, where all the models, the views and the controller are.

**The Models**

  In models.py you will find all the objects used in ciip4me. Eache field describes a property of the object.
  
  **ATTENTION:** If you change a field in models make sure to use South aftward to migrate from your old database schema to your new database structure. Look at the section South in this documentation to see how to do it.

**The Controller**

  In views.py you will find all the logic that handles the different requests. At the moment all the views for the University admin, Manger and Student are in the same file, this should change in the future, in fact it would be best practice to have three different apps for each stakeholder.
  In every method we handle a different requests. Some of the backend logic is then process in functions.py
  
**The Views**

  In /templates/ciip/ you will find all the templates that define the views, familiarize on the way we pass variables from the controller to the view ( we pass a variable, eg. x,  when we render the page and then we use {{ x }} within a template.
  
**Other files**
  
  **Urls.py**
 
  urls.py, as you can guess from the name it's where we link the actual URL of a page to method in our views.py
  
  **Forms.py**
  
  A form in django is used to enter info about an object define in the models. It is used for two main reasons:
  
  1- it's quicker, in fact you don't have to write HTML, you just need to pass the form to the templates
  
  2- It handles user's errors, in fact a form will not validate if, for instance, a user enter a string in a field in which there should be an integer.
  
  In forms.py each class defines a form. You will need to define which object thet form is linked to and the fields that you want to display. You can also style the fields if you define the form fields directly in the form. Have a look at this link for further info about forms: https://docs.djangoproject.com/en/1.5/topics/forms/ 

  **Admin.py**

  admin.py is used to configure the Django Admin interface. You need to edit admin.py if you want to change the informations displayed about the objects in the Django Admin.
  
  **Functions.py**
  
  In this file you will find some recurrent functions used in the backend
  
/mysite/
--------

This is where the settings are, you rarely touch the files in /mysite/.


SOUTH
-----

**OVERVIEW**

South is used to migrate your database anytime you make a change to your models. South is now integrated with Django 1.7 but since we are using Django 1.5.4 you will have some basic commands that you need to do to migrate succssefully the database.

Firstly have a look at this South introduction, http://south.readthedocs.org/en/latest/tutorial/part1.html . 

The Process:

Usually any time I make a change I apply this kind of workflow:

  1.Change a field in my models
  
  2.Create Migration file:
  ```
  $ python manage.py schemamigration ciip --auto
  ```
  
  3.Apply migration on the local postgresql database:
  ```
  $ python manage.py migrate ciip
  ```
  
  4.Push the changes to GitHub and Heroku
  ```
  $ git push origin master
  ```
  ```
  $ git push heroku master
  ```
  
  5.Apply migration on the postgresql database hosted on heroku
  ```
  $ heroku run python manage.py migrate ciip
  ```

========================================================================================
  
SECTION 2 (UPDATING THE CONTENT):
----------------

**Overview**

This webapp does not have a CMS (Content Management System), hence all the changes must be done directly in the templates.

If you have a basic knowledge of HTML then you should be able to change the contents with no problem.

Below there is a short 'map' of the templates and what contents they contain.


**THE CONTENT MAP**

**A.Landing page and open to the public**

* /ciip/templates/ciip/info.html  -- This is the landing page ( https://www.ciip4me.com/ciip/info). Basic info about the program are given and also some other general info.

* /ciip/templates/ciip/faq.html -- This is the FAQ page ( https://www.ciip4me.com/ciip/faq ). I guess you know what it contains...

* /ciip/templates/ciip/contact_us.html --  https://www.ciip4me.com/ciip/contact_us . Contact page






