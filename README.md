# Django_Template_Blog

Recently updated to work with Django Version 1.11.5

This is a template Django blog with template functions. 
Some of them are there to provide functionality with openLdap (e.g. add a new user).

All passwords are "default" so change them if you ever try to use this in production.

I reccomend you to "pull request" more functionality, or frontend beauty as it has none, and then use it for your own Django tutorial.

## How to use

Let's start with a virtualenv installation.

``` sudo apt install python-pip
pip install virtualenv
mkdir ~/.virtualenv
sudo(?) easy_install virtualenv
virtualenv --no-source-packages .virtualenv
source .virtualenv/bin/activate
```

Now that we are inside the virtualenv it is time to install our needed python modules.

```pip install Django
pip install python-ldap
pip install django-auth-ldap```

If you get an error while installing django-auth-ldap, like the " Modules/LDAPObject.c:18:18: fatal error: sasl.h: No such file or directory" I got, it could be solved by installing some dev packages to your main system.

For me ```sudo apt install libsasl2-dev``` did the trick.

