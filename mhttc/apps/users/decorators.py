"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.shortcuts import render


def user_agree_terms(function):
    """A wrapper to ensure that a user has agreed to terms."""

    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.agree_terms:
                return render(request, "terms/usage_agreement_login.html")
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
