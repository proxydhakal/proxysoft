"""Home page and any other public views."""
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

    testimonials_qs = config.testimonials.all()
    testimonials = []
    for t in testimonials_qs:
        quote = (t.quote or "").strip()
        if not quote:
            continue
        testimonials.append(
            {
                "name": (t.name or "").strip() or "Client",
                "role": (t.role or "").strip(),
                "text": quote,
                "avatar": (t.avatar or "").strip() or "PS",
                "color": (t.color or "").strip() or "from-brand-400 to-brand-700",
            }
        )
    if not testimonials:
        testimonials = [
            {
                "name": "Client",
                "role": "",
                "text": "Delivering results that matter for global clients.",
                "avatar": "PS",
                "color": "from-brand-400 to-brand-700",
            },
            {
                "name": "Client",
                "role": "",
                "text": "Pioneering technical SEO and responsive design in Nepal.",
                "avatar": "PS",
                "color": "from-emerald-400 to-teal-700",
            },
            {
                "name": "Client",
                "role": "",
                "text": "Leading the way in SaaS and enterprise innovation.",
                "avatar": "PS",
                "color": "from-violet-400 to-purple-700",
            },
        ]
    return render(
        request,
        "index.html",
        {
            "site_config": config,
            "testimonials_data": testimonials,
        },
    )
