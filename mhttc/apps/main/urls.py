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
    path("project/<int:uuid>/?", views.project_details, name="project_details"),
]

# urlpatterns = [
#    path('', views.IndexView.as_view(), name='index'),
#    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
#    path('<int:question_id>/vote/', views.vote, name='vote'),
# ]
