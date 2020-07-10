"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from mhttc.apps.users.models import Center
from django.db import models
from django.urls import reverse
import uuid


class Project(models.Model):
    """A project is owned by a center, and includes one or more form templates.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Why do these fields use time, and others use date (e.g., see ip_check*)
    time_created = models.DateTimeField("date created", auto_now_add=True)
    time_updated = models.DateTimeField("date modified", auto_now=True)
    name = models.CharField(max_length=250, blank=False)
    description = models.CharField(max_length=500, blank=True, null=True)

    # Manage project forms
    form = models.ForeignKey(
        "main.FormTemplate", on_delete=models.CASCADE, blank=True, null=True
    )

    # A project must be owned by a center, and the contact must be a user
    center = models.ForeignKey("users.Center", on_delete=models.PROTECT, blank=False)
    contact = models.ForeignKey("users.User", on_delete=models.PROTECT, blank=False)

    def get_absolute_url(self):
        return reverse("project_details", args=[self.uuid])

    def get_label(self):
        return "project"

    class Meta:
        app_label = "main"


class Strategy(models.Model):
    """An implementation strategy to add to a FormTemplate
    """

    FREQUENCY_CHOICES = [
        ("daily", "daily",),
        ("monthly", "monthly",),
        ("weeky", "weekly",),
        ("yearly", "yearly",),
        ("bi-weeky", "bi-weekly",),
        ("bi-monthly", "bi-monthly",),
    ]
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time_created = models.DateTimeField("date created", auto_now_add=True)
    time_updated = models.DateTimeField("date modified", auto_now=True)

    frequency = models.CharField(
        max_length=250, blank=False, choices=FREQUENCY_CHOICES, help_text="Frequency"
    )
    strategy_format = models.CharField(
        max_length=500, blank=True, null=True, help_text="Format"
    )
    strategy_type = models.CharField(
        max_length=500, blank=True, null=True, help_text="Type"
    )
    planned_number_units = models.PositiveIntegerField(
        help_text="Planned number of units"
    )

    def get_label(self):
        return "strategy"

    class Meta:
        app_label = "main"


class FormTemplate(models.Model):
    """A form template collects basic information about the project. We render
       different information and make it editable for the user depending on their
       role and the project stage.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Create, update (complete) times
    time_created = models.DateTimeField("date created", auto_now_add=True)
    time_updated = models.DateTimeField(
        "date modified", auto_now=True, help_text="Template Updated or completed at."
    )

    # Project start / end date
    start_date = models.DateTimeField("project start date")
    end_date = models.DateTimeField("project end date")

    # 1. Evidence based intervention (what)
    name = models.TextField(
        blank=False,
        help_text="Evidence-Based Intervention/Program/Service Being Implemented (WHAT)",
    )

    # 2. Target audience (WHO)
    target_audience_disciplines = models.TextField(
        blank=False, help_text="Specify discipline(s)"
    )
    target_audience_roles = models.TextField(blank=False, help_text="Specify role(s)")

    target_audience_across_orgs = models.BooleanField(
        default=False, help_text="Multiple individuals across organizations"
    )
    target_audience_within_org = models.BooleanField(
        default=False, help_text="Multiple individuals within an organization"
    )
    target_audience_teams_across_orgs = models.BooleanField(
        default=False, help_text="Multiple individuals or teams across organizations"
    )

    # 3. Implementation strategy
    implement_strategy = models.ManyToManyField(
        "main.Strategy",
        blank=True,
        default=None,
        related_name="form_template1",
        related_query_name="form_template1",
    )

    implement_strategy_description = models.TextField(
        blank=False,
        null=False,
        help_text="Free Text Description (Provide a Description of the Planned Implementation Steps)",
    )

    # 4. Contextual/determinant Considerations
    consider_system_factors = models.TextField(
        help_text="System factors--external to the organization (e.g., financing; mandates, community, culture)"
    )
    consider_org_factors = models.TextField(
        help_text="Organizational factors—internal to the organization (e.g., leadership; readiness)"
    )
    consider_clinical_factors = models.TextField(
        help_text="Individual clinician factors (e.g., alignment with existing practice; complexity)"
    )
    consider_sustainment_strategy = models.TextField(
        help_text="Sustainment strategies applied"
    )  # only form stage 3

    # TODO possibly add checkboxes here in some respect

    # 5. Measures being planned (stage 1)
    outcome_reach = models.TextField(
        help_text="Reach (# or percentage of population, what is the population, and how will you be measuring the outcome?"
    )
    outcome_effectiveness = models.TextField(
        help_text="Effectiveness of Intervention/Program/Services (w/consumers), how will you measure it?"
    )
    outcome_adoption = models.TextField(
        help_text="Number of providers? How will you be measuring it?"
    )
    outcome_quality = models.TextField(
        help_text="Implementation Fidelity/Adherence/Quality. How will you be measuring it?"
    )
    outcome_cost = models.TextField(help_text="Cost. How will you keep track of it?")
    outcome_other = models.TextField(help_text="Any other measures being planned?")

    # 5. Implementation process (stage 2)
    implementation_recruited = models.PositiveIntegerField(
        help_text="How many participants will be recruited?"
    )
    implementation_participants = models.PositiveIntegerField(
        help_text="How many participants are enrolled?"
    )
    implementation_enrolled = models.PositiveIntegerField(
        help_text="# (%) initiating implementation strategy (individuals, teams or organizations"
    )

    # the following are only for (stage 3)
    implementation_completing_half = models.PositiveIntegerField(
        help_text="# (%) completing 50% of implementation strategy activities"
    )
    implementation_completing_majority = models.PositiveIntegerField(
        help_text="# (%) completing 80% or more of implementation strategy activities"
    )

    # 6. Results Available (stage 2)
    results_reach = models.TextField(
        help_text="Reach (# or percentage of population, what is the population, and how will you be measuring the outcome?"
    )
    results_effectiveness = models.TextField(
        help_text="Effectiveness of Intervention/Program/Services (w/consumers), how will you measure it?"
    )
    results_adoption = models.TextField(
        help_text="Results available for number of providers?"
    )
    results_quality = models.TextField(
        help_text="Results available for implementation Fidelity/Adherence/Quality?"
    )
    results_cost = models.TextField(help_text="Results available for cost?")
    results_other = models.TextField(help_text="Results available for other?")

    def get_absolute_url(self):
        return reverse("formtemplate_details", args=[self.uuid])

    def get_label(self):
        return "formtemplate"

    class Meta:
        app_label = "main"
