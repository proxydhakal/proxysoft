"""Home page and any other public views."""
import json
import logging

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.urls import reverse

from .mail import send_contact_inquiry_notification, send_contact_thank_you_email
from .models import SiteConfiguration, ContactSubmission

logger = logging.getLogger(__name__)


def home(request):
    """Render the main landing page with dynamic content."""
    config = SiteConfiguration.load()

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email_raw = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()
        if not name or not message:
            messages.error(request, "Please provide your name and message.")
        elif not email_raw:
            messages.error(request, "Please provide your email address so we can reply to you.")
        else:
            try:
                validate_email(email_raw)
            except ValidationError:
                messages.error(request, "Please enter a valid email address.")
            else:
                submission = ContactSubmission.objects.create(
                    name=name,
                    email=email_raw,
                    subject=subject or "Inquiry",
                    message=message,
                )
                sent_ok = False
                try:
                    send_contact_thank_you_email(
                        request,
                        to_email=email_raw,
                        recipient_name=name,
                        site_config=config,
                    )
                    sent_ok = True
                except Exception:
                    logger.exception("Contact thank-you email failed to send for %s", email_raw)
                try:
                    send_contact_inquiry_notification(
                        request,
                        submission=submission,
                        site_config=config,
                    )
                except Exception:
                    logger.exception("Staff inquiry notification failed for submission id=%s", submission.pk)
                if sent_ok:
                    messages.success(
                        request,
                        "Thank you! Your message has been sent. Check your inbox for a confirmation email.",
                    )
                else:
                    messages.success(
                        request,
                        "Thank you! Your message has been received. We could not send a confirmation email "
                        "automatically; please contact us directly if you need a quick response.",
                    )
                return redirect(reverse("core:home") + "#contact")

    raw_quotes = config.testimonials.values_list("quote", flat=True)
    testimonials = [q.strip() for q in raw_quotes if q and str(q).strip()]
    if not testimonials:
        testimonials = [
            "Delivering results that matter for global clients.",
            "Pioneering technical SEO and responsive design in Nepal.",
            "Leading the way in SaaS and enterprise innovation.",
        ]
    return render(
        request,
        "index.html",
        {
            "site_config": config,
            "testimonials_json": json.dumps(testimonials),
        },
    )
