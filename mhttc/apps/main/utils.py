"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from mhttc.settings import DOMAIN_NAME
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
import os

import PIL
import requests
from io import BytesIO


def make_certificate_response(name, training, image_path=None):
    """Make a certificate (PDF) to return to a user in the browser
    """
    image_path = (
        image_path or "%s/static/templates/MHTTC-Certificate-Template.png" % DOMAIN_NAME
    )

    if not os.path.exists(image_path):
        response = requests.get(image_path)
        image_path = PIL.Image.open(BytesIO(response.content))
        image_path = ImageReader(image_path)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        'attachment; filename="MHTTC-event-%s-certificate.pdf"'
        % training.center.name.replace(" ", "-").lower()
    )

    c = canvas.Canvas(response, pagesize=landscape(letter))

    # Add image background
    c.setPageSize((960, 540))
    c.drawImage(image_path, 0, 0)

    # Participant Name Text
    c.setFont("Helvetica-Bold", 24, leading=None)
    c.drawCentredString(480, 300, name)

    # More body Text ...
    c.setFont("Helvetica", 20, leading=None)
    c.drawCentredString(480, 200, training.name)

    # If we have dates of event and duration, add to bottom left
    c.setFont("Helvetica", 12, leading=None)
    if training.dates:
        c.drawCentredString(480, 30, "Date of Event: %s" % training.dates)
    if training.duration:
        c.drawCentredString(480, 20, "Duration: %s hours" % training.duration)

    c.save()
    return response
