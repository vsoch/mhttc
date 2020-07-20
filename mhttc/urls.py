"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.contrib import admin
from django.urls import include, path
from mhttc.apps.main import urls as main_urls
from mhttc.apps.base import urls as base_urls
from mhttc.apps.users import urls as user_urls

# Customize admin title, headers
admin.site.site_header = "MHTTC administration"
admin.site.site_title = "MHTTC Admin"
admin.site.index_title = "MHTTC administration"

# Configure custom error pages
handler404 = "mhttc.apps.base.views.handler404"
handler500 = "mhttc.apps.base.views.handler500"

urlpatterns = [
    path("", include(base_urls)),
    path("", include(main_urls)),
    path("", include(user_urls)),
    path("admin/", admin.site.urls),
]
