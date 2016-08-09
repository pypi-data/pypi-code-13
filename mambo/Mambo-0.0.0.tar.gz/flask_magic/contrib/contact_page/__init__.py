
"""
Contact Page
"""
from flask_magic import (Magic, page_meta, get_config, flash, abort, get, post,
                         register_app, redirect, request, url_for, models)
from flask_magic.decorators import (set_nav, template, route)
from flask_magic.ext import (mail, recaptcha)
import flask_magic.utils as utils
import logging

register_app(__package__)



def setup(**kwargs):
    """
        - params:
            - recipient
            - return_to
            - page_title
            - success_message
            - failure_message
        - navigation:
            - title
            - order
            - display

    """

    navigation = kwargs.get("navigation", {})
    navigation.setdefault("title", "Contact")
    navigation.setdefault("visible", True)
    navigation.setdefault("order", 100)

    options = kwargs.get("options", {})

    class ContactPage(Magic):
        base_route = "/"
        decorators = kwargs.get("decorators")

        @set_nav(**navigation)
        @route("contact/", methods=["GET", "POST"])
        def index(self):

            # Email to
            email_to = options.get("recipient", get_config("APPLICATION_CONTACT_EMAIL", None))

            if not mail.validated:
                abort("MailmanConfigurationError")
            elif not email_to:
                abort("ContactPageMissingEmailToError")

            if request.method == "POST":
                email = request.form.get("email")
                subject = request.form.get("subject")
                message = request.form.get("message")
                name = request.form.get("name")

                flash_message = options.get("success_message", "Message sent. Thank you!")
                flash_type = "success"

                if recaptcha.verify():

                    if not email or not subject or not message:
                        flash_message = "All fields are required"
                        flash_type = "error"
                    elif not utils.is_email_valid(email):
                        flash_message = "Invalid email address"
                        flash_type = "error"
                    else:
                        try:
                            mail.send(to=email_to,
                                      reply_to=email,
                                      mail_from=email,
                                      mail_subject=subject,
                                      mail_message=message,
                                      mail_name=name,
                                      template="contact-us.txt")
                        except Exception as ex:
                            logging.exception(ex)
                            abort("MailmanConfigurationError")
                else:
                    flash_message = "Security code is invalid"
                    flash_type = "error"

                flash(flash_message, flash_type)

                return redirect(options.get("return_to", None) or self.index)

            page_meta(title=options.get("page_title", "Contact Us"))

            return None

    return ContactPage


