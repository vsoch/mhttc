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


def make_certificate_response(name, center, training_title, image_path=None):
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
        'attachment; filename="MHTTC-training-%s-certificate.pdf"'
        % center.replace(" ", "-").lower()
    )

    c = canvas.Canvas(response, pagesize=landscape(letter))

    # Add image background
    c.setPageSize((960, 540))
    c.drawImage(image_path, 0, 0)

    # Participant Name Text
    c.setFont("Helvetica-Bold", 24, leading=None)
    c.drawCentredString(480, 245, name)

    # More body Text ...
    c.setFont("Helvetica", 20, leading=None)
    c.drawCentredString(480, 150, center + ": " + training_title)
    c.save()
    return response
