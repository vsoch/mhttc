---
title: Getting Started
tags: 
 - jekyll
 - github
description: Getting started with MHTTC Development
---

# Getting Started

The documentation here will get you started to use the MHTTC interweb, developed
with Python and Django. This is intended for developers. If you want to see
the user documentation, see [the user guide]({{ site.baseurl }}/user-guide/).

### Setup

You will want to follow the instructions [here](https://cloud.google.com/appengine/docs/standard/python3/building-app/writing-web-service)
and:

 - create a Google Cloud Project, you can request one at Stanford [here](https://stanford.service-now.com/it_services?id=sc_cat_item&sys_id=fa9f80bddbf05b401df130cf9d96198b)
 - install the gcloud command line client and Python3+
 - authenticate on the command line with `gcloud auth application-default login`

For example, after I've created my project and I've installed gcloud, I might login and
then set the default project to be my new project:

```bash
$ gcloud auth application-default login
$ gcloud config set project <myproject>
```

Then to work locally (if you are developing) you'll want to clone the project:

```bash
git clone https://github.com/vsoch/mhttc
cd mhttc
```

On the [Google Project Console](https://console.developers.google.com/apis) you'll want to enable
APIs for:

 - Identity and Access Management (IAM) API
 - Google Storage


#### Storage

Since app engine doesn't allow writing to the filesystem, we will use Google Cloud Storage
for file uploads, and use the [django-storages](https://django-storages.readthedocs.io/en/latest/backends/gcloud.html)
library to do this (not yet developed).

### Billing

Under billing, it's good practice to also set up billing alerts - unintended charges to a project that you don't know about can have dire consequences. A small server of this size shouldn't cost more than $55 a  month (this would be a LOT) so I generally would start with a lower monthly limit (possibly $55) with alerts at 25, 50, 75, and 100 percents, and adjust as needed.


### Configuration

The application has a set of configuration variables that are discovered in the environment
via an .env file that you can source before running the application, and these
environment variables are also given to the app engine app.yaml file so they are discovered
on App Engine. When you first start out, you can copy the dummy template provided in
the repository:

```bash
cp .dummy-env .env
```

and then populate the following configuration variables into that file.

#### Secret Key

A secret key is used to secure your server. You can use the [secret key generator](https://djecrety.ir/) to make a new secret key, and also export it as the `DJANGO_SECRET_KEY` in your `.env` file:

```bash
export DJANGO_SECRET_KEY=123455
```

#### Google Analytics

If you want to use [Google Analytics](https://analytics.google.com/analytics/web/) with your application, generate a key and add
it to your application, again in the `.env` file.

```bash
export GOOGLE_ANALYTICS_ID=1111111111111111
```

#### Social Networks

If you want a twitter card / alias embedded in site metadata, export the `TWITTER_USERNAME` in your .env file.
The default is already set for MHTTC.

```bash
export TWITTER_USERNAME=MHTTCNetwork
```

You can also easily link to an instagram or facebook.

```
export FACEBOOK_USERNAME=mhttc
export INSTAGRAM_USERNAME=mhttc
```

These last two are undefined by default and won't show on the site.

#### Authentication 

Since we want to control login via invited email address, we are going to disable having a register form, and users
are required to login with an email and password. An administrator is responsible for adding new users. 
The login flow will be handled by the [python-social-auth](https://github.com/python-social-auth/social-core)
module.

### SendGrid Secrets

To send PDFs (and other emails) from the server, we use SendGrid. This means
that you need to [sign up](https://app.sendgrid.com/) for an account (the basic account with 100 emails
per day is free) and then add the `SENDGRID_API_KEY` to your settings/config.py:

```python
SENDGRID_API_KEY=xxxxxxxxxxxxxxx
```

To create your key:

 1. Go to [SendGrid](https://app.sendgrid.com/) and click on Settings -> Api keys in the left bar
 2. Click the blue button to "Create API key"
 3. Give your key a meaningful name (e.g., freegenes_dev_test)
 4. Choose "Restricted Access" and give "Full Access" to mail send by clicking the bar on the far right circle.
 5. Copy it to a safe place, likely your settings/config.py (it is only shown once!)

If the value is found to be None, emails will not be sent.


### Rate Limits

It's hard to believe that anyone would want to maliciously issue requests to your server,
but it's unfortunately a way of life. For this reason, all views have a rate limit, along
with blocking ip addresses that exceed it (for the duration of the limit, one day). You
can customize this:

```python
VIEW_RATE_LIMIT="50/1d"  # The rate limit for each view, django-ratelimit, "50 per day per ipaddress)
VIEW_RATE_LIMIT_BLOCK=True # Given that someone goes over, are they blocked for the period?
```

And see the [django-ratelimit](https://django-ratelimit.readthedocs.io/en/v1.0.0/usage.html) documentation
for other options. 

### Database

For our database, we use [Stanford managed SQL](https://uit.stanford.edu/service/sql).
We won't need this for local development, for which we will use sqlite (a local file database).
If you ever need to delete and refresh this local testing database, you can do:

```bash
rm db.sqlite3
```

### Development

To develop locally, you'll want to create a local environment and then install
dependencies to it.

```bash
python -m venv env
source env/bin/activate
pip install  -r requirements.txt
```

And always source this environment before you start working.
Then you will want to source your environment file:

```bash
source .env
```

To make migrations we usually might do this:

```bash
python manage.py makemigrations
python manage.py makemigrations main
python manage.py migrate
```

But to make it easier, there is an included Makefile that can be used to make
migrations, and then migrate.

```bash
make migrations
make migrate
```

And then we would typically use the `manage.py` to run the server.

```bash
python manage.py runserver
```

But there is also a make command that is easier to type:

```bash
make run
```

And then you can open up your browser to [http://localhost:8000](http://localhost:8000).

### Deployment

https://cloud.google.com/python/django/appengine#deploying_the_app_to_the_standard_environment_

<hr>
