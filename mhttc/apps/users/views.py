"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from mhttc.apps.users.models import Center, User
from mhttc.apps.users.decorators import user_agree_terms
from mhttc.apps.users.utils import generate_random_password, send_email
from mhttc.settings import (
    VIEW_RATE_LIMIT as rl_rate,
    VIEW_RATE_LIMIT_BLOCK as rl_block,
)

from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from ratelimit.decorators import ratelimit
from social_core.exceptions import AuthForbidden
from django.utils import timezone

## Centers


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@user_agree_terms
def center_details(request, uuid):
    """Return a project, or 404.
    """
    try:
        center = Center.objects.get(id=uuid)
        return render(
            request, "centers/center_details.html", context={"center": center}
        )
    except Center.DoesNotExist:
        raise Http404


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def user_center(request):
    """Return a user listing of projects
    """
    if request.user.center:
        return redirect("center_details", request.user.center.id)
    messages.warning(request, "You do not belong to a center.")
    return redirect("index")


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def all_centers(request, centers=None):
    if centers is None:
        centers = Center.objects.all().order_by("name")
    return render(request, "centers/all_centers.html", context={"centers": centers})


## Users
@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def invited_user(request):
    """The view for an invited user to set their password and enable account.
    """
    # TODO need to write this view
    # ask user to re-set password
    # make user active
    # confirm uuid is matching
    pass


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def invite_users(request):
    """Create new users based on email, and invite them to their accounts.
    """
    if not request.user.is_superuser:
        messages.warning(request, "You are not allowed to perform this action")
        redirect("index")

    if request.method == "POST":
        emails = request.POST.get("emails")
        resend_invite = request.POST.get("resend_invite") == "on"
        for email in emails.split("\n"):

            # Any weird newlines
            email = email.strip()

            # We create users with emails as username
            user, created = User.objects.get_or_create(username=email, email=email)

            # If we resend an invite, we generate a new password
            if created and resend_invite or not created:
                user.active = False
                password = generate_random_password()
                user.set_password(password)
                user.save()
                url = reverse("invited_user", args=[user.uuid])
                message = (
                    "You've been invited to join the Mental Health Technology Transfer Network!\n"
                    "You can login with the following username and password at %s:\n\nUsername: %s\nPassword: %s\n\n"
                    "If this message was in error, please respond to this email and let us know."
                    % (url, user.username, password)
                )

                message = send_email(
                    email_to=email,
                    message=message,
                    subject="[MHTTC] Your are invited to join the Mental Health Technology Transfer Network",
                )
                messages.info(request, message)

    return render(request, "users/invite_users.html")


## Account Creation and Manamgent


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def view_profile(request, username=None, form=None):
    """view a user's profile
    """
    message = "You must select a user or be logged in to view a profile."
    if not username:
        if not request.user:
            messages.info(request, message)
            return redirect("index")
        user = request.user
    else:
        user = get_object_or_404(User, username=username)

    if form is None:
        form = PasswordChangeForm(request.user)
    context = {"profile": user, "passwordform": form}
    return render(request, "users/profile.html", context)


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
def delete_account(request):
    """delete a user's account"""
    if not request.user or request.user.is_anonymous:
        messages.info(request, "This action is not prohibited.")
        return redirect("index")

    # Log the user out
    auth_logout(request)
    request.user.is_active = False
    messages.info(request, "Thank you for using MHTTC")
    return redirect("index")


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
        else:
            messages.error(request, "Please correct the error below.")
        return view_profile(request, form=form)
    return redirect("index")


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
def agree_terms(request):
    """ajax view for the user to agree"""
    if request.method == "POST":
        request.user.agree_terms = True
        request.user.agree_terms_date = timezone.now()
        request.user.save()
        response_data = {"status": request.user.agree_terms}
        return JsonResponse(response_data)

    return JsonResponse(
        {"Unicorn poop cookies...": "I will never understand the allure."}
    )


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
def login(request):
    """login is bootstrapped here to show the user a usage agreement first, in the
       case that he or she has not agreed to the terms.
    """
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    context = {}
    if request.user.is_authenticated:
        if not request.user.agree_terms:
            return render(request, "terms/usage_agreement_login.html", context)
    else:
        context["form"] = AuthenticationForm()

    return render(request, "social/login.html", context)


@login_required
def logout(request):
    """log the user out, first trying to remove the user_id in the request session
       skip if it doesn't exist
    """
    try:
        del request.session["user_id"]
    except KeyError:
        pass
    auth_logout(request)

    return redirect("/")
