"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.shortcuts import render, redirect
from django.http import Http404
from ratelimit.decorators import ratelimit

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict
from mhttc.apps.users.decorators import user_agree_terms

from mhttc.apps.main.models import Project, Training
from mhttc.apps.users.models import get_center
from mhttc.settings import VIEW_RATE_LIMIT as rl_rate, VIEW_RATE_LIMIT_BLOCK as rl_block
from mhttc.apps.main.forms import ProjectForm, TrainingForm, FormTemplateForm

import os


## Projects


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
            return redirect("project_details", uuid=project.uuid)
    else:
        form = ProjectForm()
    return render(request, "projects/new_project.html", {"form": form})


## Form Templates


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def edit_form_template(request, uuid, stage=1):
    """edit a form template, meaning entering information for different stages
    """
    try:
        project = Project.objects.get(uuid=uuid)
    except Project.DoesNotExist:
        raise Http404

    if request.method == "POST":

        # Get standard form fields
        form = FormTemplateForm(request.POST)
        form.stage = project.stage

        # Also get strategy_ fields
        strategy = {}
        for key in request.POST:
            if key.startswith("strategy_"):
                strategy[key] = request.POST[key]

        # TODO stopped here, need to parse these custom for validation based on stage
        import pickle

        pickle.dump({"form": form, "strategy": strategy}, open("form.pkl", "wb"))
        if form.is_valid():
            template = form.save(commit=False)

            # If the form already belongs to another center
            if template.center != None and template.center != request.user.center:
                messages.warning(
                    request,
                    "You are not allowed to edit a form not owned by your center.",
                )
                return redirect("index")

            template.center = request.user.center
            template.save()
            return redirect("center_details", uuid=template.center.uuid)

        # Not valid - return to page to populate
        else:
            return render(
                request,
                "projects/edit_form_template.html",
                {"form": form, "project": project},
            )
    else:
        form = FormTemplateForm()
        if project.form is not None:
            form = FormTemplateForm(initial=model_to_dict(project.form))
        form.stage = project.stage
    return render(
        request, "projects/edit_form_template.html", {"form": form, "project": project}
    )


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def view_project_form(request, uuid):
    try:
        project = Project.objects.get(uuid=uuid)
        if project.form == None:
            messages.info(request, "This project does not have a form started yet.")
            return redirect("project_details", project.uuid)
        return render(
            request, "projects/view_project_form.html", context={"project": project}
        )
    except Project.DoesNotExist:
        raise Http404


## Training


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def new_training(request):
    if request.method == "POST":
        form = TrainingForm(request.POST)
        if form.is_valid():
            training = form.save(commit=False)
            training.center = request.user.center
            training.save()
            return redirect("traiing_details", uuid=training.uuid)
    else:
        form = TrainingForm()
    return render(request, "training/new_training.html", {"form": form})


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def center_training(request):
    """Return a listing of training events being held by the center
    """
    if not request.user.center:
        messages.info(request, "You are not part of a center.")
        redirect("index")
    events = Training.objects.filter(center=request.user.center)
    return render(
        request,
        "training/center_training.html",
        {"events": events, "center": request.user.center},
    )


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def training_details(request, uuid):
    try:
        training = Training.objects.get(uuid=uuid)
        return render(
            request, "training/training_details.html", context={"training": training}
        )
    except Training.DoesNotExist:
        raise Http404
