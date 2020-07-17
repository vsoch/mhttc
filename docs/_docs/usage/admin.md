---
title: Admin Pages
description: MHTTC administrative views
---

# Admin Pages

When you've added a user as staff or a superuser, he or she can access the 
admin views at `/admin`. By default, a regular or non-authenticated user cannot view the admin pages.

![admin-login.png]({{ site.baseurl }}/docs/usage/img/admin-login.png)

To view the admin pages, you'll first need to add the admin user to the
database from the command line. Since this is deployed on App Engine,
this typically needs to be done by the developer.

```bash
$ python manage.py createsuperuser
$ python manage.py add_superuser myusernamejustadded
```

And then login in to the admin home:

![admin-home.png]({{ site.baseurl }}/docs/usage/img/admin-home.png)

This is where you can add new centers, and update user metadata.
This is also where you would add a new user, and also associate them to
a center.

 - [Adding a User](#add-a-user)

<a id="adding-a-user">
## 1. Adding a User

When you browse to the `/admin` url (and there is also a link to it in your
user profile) you first want to make sure that the Center for the user
exists. If it doesn't, click the green ➕️ symbol under Users -> Center to add it
first. Then when you are ready, click the green ➕️ under Users -> Users.
You'll be taken to a list of users, and then you can click "Add User"
to add a new one. You'll see a form like the following:

![admin-add-user.png]({{ site.baseurl }}/docs/usage/img/admin-add-user.png)

The only required fields are:

 - username (should be input as the email address)
 - password
 - center

and you are suggested to also enter the email address under the email address field.

And then the user can change his or her password on first login (and you should
encourage them to).
