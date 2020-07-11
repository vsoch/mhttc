"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from mhttc.apps.main.models import Project, FormTemplate, Training
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django import forms


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project

        # Center is associated to the user creating the project
        fields = ("name", "description", "contact")

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training

        # Center is associated to the user creating the training
        fields = ("name", "description", "contact")

    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class FormTemplateForm(forms.ModelForm):
    class Meta:
        model = FormTemplate
        widgets = {
            "start_date": DatePickerInput(),
            "end_date": DatePickerInput(),
        }
        fields = (
            "name",
            "start_date",
            "end_date",
            "target_audience_disciplines",
            "target_audience_roles",
            "target_audience_across_orgs",
            "target_audience_within_org",
            "target_audience_teams_across_orgs",
            "implement_strategy_description",
            "consider_system_factors",
            "consider_org_factors",
            "consider_clinical_factors",
            "consider_sustainment_strategy",
            "outcome_reach",
            "outcome_effectiveness",
            "outcome_adoption",
            "outcome_quality",
            "outcome_cost",
            "outcome_other",
            "implementation_recruited",
            "implementation_participants",
            "implementation_enrolled",
            "implementation_completing_half",
            "implementation_completing_majority",
            "results_reach",
            "results_effectiveness",
            "results_adoption",
            "results_quality",
            "results_cost",
            "results_other",
        )

    def __init__(self, *args, **kwargs):
        super(FormTemplateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
