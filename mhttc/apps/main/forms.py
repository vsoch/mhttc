"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from mhttc.apps.main.models import Project, FormTemplate
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


class FormTemplateForm(forms.ModelForm):
    class Meta:
        model = FormTemplate

        # TODO these need custom views for each stage
        # Center is associated to the user creating the project
        fields = (
            "name",
            "start_date",
            "end_date",
        )
