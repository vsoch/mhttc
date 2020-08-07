"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from mhttc.apps.main.models import Project, FormTemplate, Training, TrainingParticipant
from bootstrap_datepicker_plus import DatePickerInput
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
        fields = ("name", "description", "contact", "image_url")

    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class CertificateForm(forms.ModelForm):
    class Meta:
        model = TrainingParticipant
        fields = ("name", "email")

    def __init__(self, *args, **kwargs):
        super(CertificateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class FormTemplateForm(forms.ModelForm):
    """A form to populate a project template. Commented out fields are
       not required for stage 1
    """

    stage = 1

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
            "target_audience_who",
            "target_audience_disciplines",
            "target_audience_roles",
            "target_audience_across_orgs",
            "target_audience_within_org",
            "target_audience_teams_across_orgs",
            "implement_strategy_description",
            "consider_system_factors",
            "consider_org_factors",
            "consider_clinical_factors",
            "consider_sustainment_strategy",  # Only required for stage3
            "outcome_reach",
            "outcome_effectiveness",
            "outcome_adoption",
            "outcome_quality",
            "outcome_cost",
            "outcome_maintenance",  # Only required for stage3
            "outcome_other",
            "implementation_recruited",
            "implementation_participants",  # # enrolled, only after stage 1
            "implementation_enrolled",  # Only required after stage 1
            "implementation_completing_half",  # Only required for stage 3
            "implementation_completing_majority",  # Only required for stage 3
            "results_reach",  # Only required after stage 1
            "results_effectiveness",  # Only required after stage 1
            "results_adoption",  # Only required after stage 1
            "results_quality",  # Only required after stage 1
            "results_cost",  # Only required after stage 1
            "results_maintenance",  # Only required for stage 3
            "results_other",
        )

    def clean(self):
        cleaned_data = super().clean()

        # Required attributes for stage 2 and 3
        if self.stage > 1:
            print(cleaned_data)
            for field in [
                "results_reach",
                "results_effectiveness",
                "results_adoption",
                "results_quality",
                "results_cost",
                "implementation_enrolled",
                "implementation_participants",
            ]:
                if field not in cleaned_data or cleaned_data.get(field) == None:
                    raise forms.ValidationError(
                        f"{field} is required for this stage of the template."
                    )

        # Required attributes for just stage 3
        if self.stage > 2:
            for field in [
                "outcome_maintenance",
                "consider_sustainment_strategy",
                "results_maintenance",
                "implementation_completing_half",
                "implementation_completing_majority",
            ]:
                if field not in cleaned_data or cleaned_data.get(field) == None:
                    raise forms.ValidationError(
                        f"{field} is required for this stage of the template."
                    )

    def __init__(self, *args, **kwargs):
        super(FormTemplateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

        # make subset of fields not required
        for field in [
            "consider_sustainment_strategy",
            "outcome_maintenance",
            "implementation_participants",
            "implementation_enrolled",
            "implementation_completing_half",
            "implementation_completing_majority",
            "results_reach",
            "results_effectiveness",
            "results_adoption",
            "results_quality",
            "results_cost",
            "results_maintenance",
        ]:
            self.fields[field].required = False
