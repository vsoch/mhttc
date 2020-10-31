"""

Copyright (C) 2020 Vanessa Sochat.
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.core.management.base import BaseCommand
from mhttc.apps.users.models import Center


class Command(BaseCommand):
    """Create centers based on name"""

    help = "Create original set of centers"

    def handle(self, *args, **options):
        print("Creating Centers:\n")
        centers = [
            ["MHTTC Network Coordinating Office", "networkoffice@mhttcnetwork.org"],
            ["National American Indian & Alaska Native MHTTC", None],
            ["National Hispanic & Latino MHTTC", "hispaniclatinomhttc@uccaribe.edu"],
            ["New England MHTTC", None],
            ["Northeast & Caribbean MHTTC", "northeastcaribbean@mhttcnetwork.org"],
            ["Central East MHTTC", None],
            ["Southeast MHTTC", None],
            ["Great Lakes MHTTC", "greatlakes.events@chess.wisc.edu"],
            ["South Southwest MHTTC", "southsouthwest@mhttcnetwork.org"],
            ["Mid-America MHTTC", "midamerica@mhttcnetwork.org"],
            ["Mountain Plains MHTTC", None],
            ["Pacific Southwest MHTTC", "pacificsouthwest@mhttcnetwork.org"],
            ["Northwest MHTTC", None],
        ]

        # The listing above is the 13 that should have full access
        for center, email in centers:
            print("Creating center %s" % center)
            instance, _ = Center.objects.get_or_create(name=center)
            if email is not None:
                instance.email = email
            instance.full_access = True
            instance.save()
        print("There are a total of %s centers." % Center.objects.count())
