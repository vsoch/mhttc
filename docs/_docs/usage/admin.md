---
title: Admin Pages
description: FreeGenes administrative views
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

![admin-add-user.png]({{ site.baseurl }}/docs/usage/img/admin-add-user.png)
