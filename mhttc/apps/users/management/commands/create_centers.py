"""

Copyright (C) 2020 Vanessa Sochat.
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.core.management.base import BaseCommand, CommandError
from mhttc.apps.users.models import Center


class Command(BaseCommand):
    """Create centers based on name"""

    help = "Create original set of centers"

    def handle(self, *args, **options):
        print("Creating Centers:\n")
        centers = [
            "MHTTC Network Coordinating Office",
            "National American Indian & Alaska Native MHTTC",
            "National Hispanic & Latino MHTTC",
            "New England MHTTC",
            "Northeast & Caribbean MHTTC",
            "Central East MHTTC",
            "Southeast MHTTC",
            "Great Lakes MHTTC",
            "South Southwest MHTTC",
            "Mid-America MHTTC",
            "Mountain Plains MHTTC",
            "Pacific Southwest MHTTC",
            "Northwest MHTTC",
        ]
        for center in centers:
            print("Creating center %s" % center)
            Center.objects.get_or_create(name=center)
        print("There are a total of %s centers." % Center.objects.count())
