"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.conf import settings


def domain_processor(request):
    return {"domain": settings.DOMAIN_NAME}


def social_processor(request):
    return {
        "TWITTER_USERNAME": settings.TWITTER_USERNAME,
        "FACEBOOK_USERNAME": settings.FACEBOOK_USERNAME,
        "INSTAGRAM_USERNAME": settings.INSTAGRAM_USERNAME,
        "GOOGLE_ANALYTICS_ID": settings.GOOGLE_ANALYTICS_ID,
    }
