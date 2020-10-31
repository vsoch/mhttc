"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import string
import random

from mhttc.settings import SENDGRID_API_KEY, SENDGRID_SENDER_EMAIL
from django.contrib import messages

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Email,
    To,
    Content,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)

from python_http_client.exceptions import ForbiddenError
import base64
import os


def send_email(
    email_to,
    message,
    subject,
    email_from=SENDGRID_SENDER_EMAIL,
    attachment=None,
    filetype="application/pdf",
    request=None,
    filename=None,
):
    """given an email, a message, and an attachment, and a SendGrid API key is defined in
    settings, send an attachment to the user. We return a message to print to
    the interface.

    Parameters
    ==========
    email_to: the email to send the message to
    message: the html content for the body
    subject: the email subject
    attachment: the attachment file on the server
    """
    if not SENDGRID_API_KEY or not email_from:
        if request is not None:
            messages.warning(
                request,
                "SendGrid secrets were not found in the environment and you have not provided an email_from that is a validated sender. Please add email_from or see https://vsoch.github.io/mhttc/docs/getting-started/#sendgrid-secrets",
            )
        return False

    mail = create_mail(
        email_to=email_to,
        email_from=email_from,
        subject=subject,
        message=message,
        attachment=attachment,
        filetype=filetype,
        filename=filename,
    )

    try:
        sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.headers)
        return True
    except ForbiddenError as e:
        sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
        mail = create_mail(
            email_to=email_to,
            email_from=SENDGRID_SENDER_EMAIL,
            subject=subject,
            message=message,
            attachment=attachment,
            filetype=filetype,
            filename=filename,
        )
        print(e)
        return False
    except Exception as e:
        print(e.message)
        return False


def request_sender(center, email):
    """Given an email, request sender permission for it

    Parameters
    ==========
    center: the center to request sender permission for
    email: the email address to request permission for
    """
    if not center.email:
        return

    sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
    data = {
        "nickname": center.name,
        "from": {"email": center.email, "name": center.name},
        "reply_to": {"email": center.email, "name": center.name},
        "country": "United States",
    }
    # TODO: this endpoint looks like it's for a different service?
    return sg.client.senders.post(request_body=data)


def create_mail(email_to, email_from, subject, message, attachment, filetype, filename):
    """Create the actual mail object and attachment, if defined"""
    mail = Mail(
        Email(email_from),
        To(email_to),
        subject,
        Content("text/html", message),
    )

    # If the user has provided an attachment, add it
    if attachment:
        mail.attachment = generate_attachment(
            filepath=attachment, filetype=filetype, filename=filename
        )
    return mail


def generate_attachment(filepath, filetype="application/pdf", filename=None):
    """given a filepath, generate an attachment object for SendGrid by reading
    it in and encoding in base64.

    Parameters
    ==========
    filepath: the file path to attach on the server.
    filetype: MIME content type (defaults to application/pdf)
    filename: a filename for the attachment (defaults to basename provided)
    """
    if not os.path.exists(filepath):
        return

    # Read in the attachment, base64 encode it
    with open(filepath, "rb") as filey:
        data = filey.read()

    # The filename can be provided, or the basename of actual file
    if not filename:
        filename = os.path.basename(filepath)

    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType(filetype)
    attachment.file_name = FileName(filename)
    attachment.disposition = Disposition("attachment")
    return attachment


def generate_random_password(length=10):
    """Generate a random password with letters, numbers, and special characters"""
    password_characters = string.ascii_letters + string.digits
    password = "".join(random.choice(password_characters) for i in range(length))
    return password
