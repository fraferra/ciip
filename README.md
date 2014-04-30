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
