"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.shortcuts import render
from django.http import Http404
from ratelimit.decorators import ratelimit

from django.contrib.auth.decorators import login_required
from mhttc.apps.users.decorators import user_agree_terms

from mhttc.apps.main.models import Project
from mhttc.settings import VIEW_RATE_LIMIT as rl_rate, VIEW_RATE_LIMIT_BLOCK as rl_block
from mhttc.apps.main.forms import ProjectForm

import os


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def project_details(request, uuid):
    """Return a project, or 404.
    """
    try:
        project = Project.objects.get(uuid=uuid)
        return render(
            request, "projects/project_details.html", context={"project": project}
        )
    except Project.DoesNotExist:
        raise Http404


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def user_projects(request):
    """Return a user listing of projects
    """
    projects = None
    if request.user.center is not None:
        projects = Project.objects.filter(center=request.user.center)
    return all_projects(request, projects)


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def all_projects(request, projects=None):
    """Return a project, or 404.
    """
    if projects is None:
        projects = Project.objects.all()
    return render(request, "projects/all_projects.html", context={"projects": projects})


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def new_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.center = request.user.center
            project.save()
            return redirect("project_detail", uuid=project.uuid)
    else:
        form = ProjectForm()
    return render(request, "projects/new_project.html", {"form": form})
