Requirements
============

MySQL Community Server
----------------------

**GRAB THE FREAKING 64 BIT VERSION. NOT THE 32! I WILL END YOU!**

* Download the Mac OS X (x86, 64-bit), DMG from mysql.com and install the pkg

* Add MySQL to your path:

```$ echo 'export PATH=/usr/local/mysql/bin:$PATH' >> ~/.bash_profile```

* set root password to something personally secret:

```$ mysqladmin -u root password```

* Create a local database:

```mysql
$ mysql -u root -p
mysql> CREATE DATABASE IF NOT EXISTS chopstix;
mysql> CREATE USER 'chop_user'@'localhost' IDENTIFIED BY 'chopstixRock$';
mysql> GRANT ALL ON chopstix.* TO 'chop_user'@'localhost';
mysql> flush privileges;
```



Python
------

Make sure you're running python 2.7: http://www.python.org/download


Git
---

* Get github.com access to the repo if you need to commit.
* Clone Chopstix git repo:

```
$ mkdir ~/projects
$ mkdir ~/projects/testive
$ cd ~/projects
$ git clone git@github.com:tsorensen23/chopstix.git
```


Virtual Env
-----------

```
$ sudo easy_install pip
$ sudo pip install virtualenv
```

* Install a new virtual environment in the directory where the project will live.

```
virtualenv --no-site-packages ~/projects/chopstix/venv
```

Install Requirements
====================

pip
---

* Install back-end packages and dependencies

```
$ cd ~/projects/chopstix
$ pip install -r requirements
```

bower
-----

* Install front-end packages and dependencies

```
$ cd ~/projects/chopstix/chopstix
$ bower install
```


Configure Settings
==================

Flask Settings File
-------------------

* Make a local.py settings file by copying the template file

```
$ cp ~/projects/chopstix/chopstix/settings/local-template.py ~/projects/chopstix/chopstix/settings/local.py
```

* Walk through the settings file and configure it as necessary for your local environment


Build Schema
============

* Create a database framework if you don't have one already

```
$ cd ~/projects/chopstix/chopstix
$ python
>>> from chopstix import db
>>> db.create_all()
```

Running Locally
===============

* Load virtual environment

```
$ cd ~/projects/chopstix
$ source venv/bin/activate
```

* Run a server

```
$ cd ~/projects/chopstix/chopstix
$ python chopstix.py
```

* Open a web browser and go to http://127.0.0.1:5000/


Running on Heroku
=================

* Create a Heroku stack

```
$ heroku create
```

* Configure Heroku Python Buildpack

```
$ heroku config:set BUILDPACK_URL=https://github.com/heroku/heroku-buildpack-python
```

* Push to Heroku

```
$ git push heroku master
```

* Open heroku in a web browser to experience the magic:

```
$ heroku open
```

You're done :)
==============

Nailed it!
