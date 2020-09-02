"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.urls import reverse

from django.db import models

import uuid

################################################################################
# Supporting Functions
################################################################################


def get_instance(uid, Model):
    """get a instance based on UID

       Parameters
       ==========
       uid: the id of the instance
    """
    keyargs = {"id": uid}
    try:
        instance = Model.objects.get(**keyargs)
    except Model.DoesNotExist:
        instance = None
    return instance


def get_center(uid):
    return get_instance(uid, Center)


def get_user(uid):
    return get_instance(uid, User)


class CustomUserManager(BaseUserManager):
    """Create and save a User with the given username, email and password.
    """

    def _create_user(
        self, username, email, password, is_staff, is_superuser, **extra_fields
    ):
        if not username:
            raise ValueError("The given username must be set")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=True,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(
            username, email, password, False, False, **extra_fields
        )

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True, **extra_fields)

    def add_superuser(self, user):
        """ Intended for existing user"""
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def add_staff(self, user):
        """ Intended for existing user"""
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    active = models.BooleanField(default=True)

    # A temporary uuid that allows them to access their personal invitation
    uuid = models.UUIDField(default=uuid.uuid4)

    # A center is required
    center = models.ForeignKey(
        "users.center", on_delete=models.PROTECT, null=True, blank=True
    )

    # has the user agreed to terms?
    agree_terms = models.BooleanField(default=False)
    agree_terms_date = models.DateTimeField(blank=True, default=None, null=True)

    # Participant metadata
    first_name = models.CharField(null=True, blank=True, max_length=255)
    last_name = models.CharField(null=True, blank=True, max_length=255)
    role = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Your position or role in your center",
    )

    # Ensure that we can add staff / superuser and retain on logout
    objects = CustomUserManager()

    def has_full_access(self):
        """Determine if the user has full access to the interweb, meaning they
           can see more than projects
        """
        if not self.center:
            return False
        return self.center.full_access

    class Meta:
        app_label = "users"

    def get_label(self):
        return "users"


class Center(models.Model):
    """A center is a group of users with shared affiliation. It can have
       one or more owners to manage it.
    """

    name = models.CharField(max_length=50, unique=True, default=None)
    owners = models.ManyToManyField(
        User,
        blank=True,
        default=None,
        related_name="center_owners",
        related_query_name="center_owners",
        help_text="Administrators of the center.",
    )
    full_access = models.BooleanField(
        default=False, help_text="The center has full access to the interweb."
    )
    created_at = models.DateTimeField("date of creation", auto_now_add=True)
    updated_at = models.DateTimeField("date of last update", auto_now=True)

    @property
    def uuid(self):
        """Derive a unique id from the center name
        """
        if self.name is not None:
            return self.name.lower().replace(" ", "-")

    def has_edit_permission(self, request):
        """ determine if a user has edit permission for a team.
            1. A superuser has edit permission, always
            2. A global admin has edit permission, always
            3. A user has edit permission if is one of the owners
        """
        # Global edit permission for superuser and staff
        if request.user.is_superuser or request.user.is_staff:
            return True

        # Edit permission to owners given so
        elif request.user in self.owners.all():
            return True

        return False

    def get_absolute_url(self):
        return reverse("center_details", args=[str(self.id)])

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return "%s" % self.name

    def get_label(self):
        return "users"

    class Meta:
        app_label = "users"
