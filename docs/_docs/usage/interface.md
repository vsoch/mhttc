---
title: Interacting with MHTTC
description: A typical user might want to browse projects
---

# Interface

The front page of the interface currently shows limited information, but
gives the anonymous user access to social media links. There is a prominent
login form.

<br>

![interface-index.png]({{ site.baseurl }}/docs/usage/img/interface-index.png)


## Accounts

By default, a user cannot make their own account. An administrative user
should go to their Profile and under Admin settings, enter a list of emails
to send invitations to:

![interface-invite.png]({{ site.baseurl }}/docs/usage/img/interface-invite.png)

The users are then notified via email with an email login and temporary password.
By way of doing this via email we also verify the email address.

![interface-invite-email.png]({{ site.baseurl }}/docs/usage/img/interface-invite-email.png)

And then the users are required to login at the custom link for them, and also provide
a new password. 

![interface-invite-login.png]({{ site.baseurl }}/docs/usage/img/interface-invite-login.png)

At the onset of logging in, the user is first asked to agree to the privacy policy
and terms of service. 

<br>

![interface-terms.png]({{ site.baseurl }}/docs/usage/img/interface-terms.png)

<br>

These terms are always available via a link in the footer. The content itself
is maintained in a Google Document so updating it doesn't require updating the 
site itself.

![interface-terms-full.png]({{ site.baseurl }}/docs/usage/img/interface-terms-full.png)

<br>

Once the user has logged in, the login panel changes to a user settings panel.

<br>

![interface-login.png]({{ site.baseurl }}/docs/usage/img/interface-login.png)


## Users

The user profile looks like this:

<br>

![interface-profile.png]({{ site.baseurl }}/docs/usage/img/interface-profile.png)

<br>


From the profile the user can change their password, or delete their account.
This action cannot be undone.

## Search

For an unathenticated user, the search goes to the public search on [https://mhttcnetwork.org/](https://mhttcnetwork.org/).
When logged in, it searches across projects.

![interface-search.png]({{ site.baseurl }}/docs/usage/img/interface-search.png)

## Centers

There is a main listing of centers, which doesn't serve much use other than to
show what exists:

<br>

![interface-centers.png]({{ site.baseurl }}/docs/usage/img/interface-centers.png)

<br>


Each center has a basic page with information (what might be useful to add here?)

<br>

![interface-center.png]({{ site.baseurl }}/docs/usage/img/interface-center.png)

<br>

and easy access to projects and trainings

<br>

![interface-center-projects.png]({{ site.baseurl }}/docs/usage/img/interface-center-projects.png)

<br>

## Training

Each center can have one or more training events (these events are the ones
that have associated certificates for participants to download). In fact, when creating
a new training, the creator can provide an image URL to generate from:

<br>

![interface-new-training.png]({{ site.baseurl }}/docs/usage/img/interface-new-training.png)

<br>

A center member can then add people to the training (based on email address) and mark
them as complete when it's completed.

![interface-training-details.png]({{ site.baseurl }}/docs/usage/img/interface-training-details.png)

Upon being marked as completed, the participant then receives an email, and can enter his or her email address and name
to generate a certificate:

![interface-download-certificate.png]({{ site.baseurl }}/docs/usage/img/interface-download-certificate.png)

An example is shown below. This is the default, in the case that no custom png URL is provided.

![certificate-example.png]({{ site.baseurl }}/docs/usage/img/certificate-example.png)


## Information

### Contact

A contact form is driven by Formspree to easily contact the site main contact:

<br>

![interface-contact.png]({{ site.baseurl }}/docs/usage/img/interface-contact.png)


### About

The about page has basic links to the software and documentation. This page would
do well to have more information about MHTTC.

<br>

![interface-about.png]({{ site.baseurl }}/docs/usage/img/interface-about.png)


Other interfaces are under development.

## Projects

So far, we have a basic page to create a new project.

<br>

![interface-new-project.png]({{ site.baseurl }}/docs/usage/img/interface-new-project.png)


<br>

and then view the project details. Note that each project has an associated form
template:

![interface-project.png]({{ site.baseurl }}/docs/usage/img/interface-project.png)

Which the user should move through in stages:

![interface-form-template.png]({{ site.baseurl }}/docs/usage/img/interface-form-template.png)

## Training

Trainings are associated with centers. Any center member can create a training on behalf
of their center.
