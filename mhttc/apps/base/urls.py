"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.views.generic.base import TemplateView
from django.conf.urls import url
import mhttc.apps.base.views as views

urlpatterns = [
    url(r"^$", views.index_view, name="index"),
    url(r"^about/?$", views.about_view, name="about"),
    url(r"^shared-folder/?$", views.shared_folder_view, name="shared_folder"),
    url(r"^contact/?$", views.contact_view, name="contact"),
    url(r"^terms/?$", views.terms_view, name="terms"),
    url(r"^privacy-policy/?$", views.terms_view, name="privacy-policy"),
    url(r"^search/?$", views.search_view, name="search"),
    url(r"^searching/?$", views.run_search, name="running_search"),
    url(r"^search/(?P<query>.+?)/?$", views.search_view, name="search_query"),
    url(
        r"^robots\.txt/$",
        TemplateView.as_view(
            template_name="base/robots.txt", content_type="text/plain"
        ),
    ),
]
