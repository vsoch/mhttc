"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.urls import path
from mhttc.apps.main import views


urlpatterns = [
    # Projects
    path("projects/", views.all_projects, name="all_projects"),
    path("u/projects/", views.user_projects, name="user_projects"),
    path("projects/new/", views.new_project, name="new_project"),
    path("project/<uuid:uuid>/", views.project_details, name="project_details"),
    path(
        "project/forms/<uuid:uuid>/<int:stage>/edit",
        views.edit_form_template,
        name="edit_form_template",
    ),
    path(
        "project/forms/<uuid:uuid>/", views.view_project_form, name="view_project_form"
    ),
    # Training
    path("training/new/", views.new_training, name="new_training"),
    path("training/<uuid:uuid>/", views.training_details, name="training_details"),
    path("center/training/", views.center_training, name="center_training"),
]
