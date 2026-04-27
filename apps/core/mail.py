"""Send transactional emails (contact form auto-reply)."""
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone

logger = logging.getLogger(__name__)


def build_logo_absolute_url(request, site_config):
    """Absolute URL for logo image in HTML emails."""
    if site_config.logo:
        return request.build_absolute_uri(site_config.logo.url)
    if site_config.logo_url:
        url = site_config.logo_url.strip()
        if url.startswith(("http://", "https://")):
            return url
    path = static("img/logo.png")
    return request.build_absolute_uri(path)


def send_contact_thank_you_email(request, *, to_email: str, recipient_name: str, site_config) -> None:
    """
    Send branded HTML thank-you after a contact form submission.
    Raises on missing configuration; caller may catch and log.
    """
    if not to_email or not to_email.strip():
        return

    logo_url = build_logo_absolute_url(request, site_config)
    site_name = site_config.site_name or "Proxy Soft"

    context = {
        "recipient_name": recipient_name.strip() or "there",
        "site_name": site_name,
        "tagline": (site_config.tagline or "").strip(),
        "logo_url": logo_url,
        "site_email": (site_config.email or "").strip(),
        "primary": "#1e40af",
        "primary_dark": "#0a1d37",
        "accent": "#38bdf8",
        "year": timezone.now().year,
    }

    subject = f"Thank you for contacting {site_name}"
    text_body = render_to_string("emails/contact_thank_you.txt", context)
    html_body = render_to_string("emails/contact_thank_you.html", context)

    from_email = settings.DEFAULT_FROM_EMAIL
    if not from_email:
        raise ValueError("DEFAULT_FROM_EMAIL is not configured")

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=[to_email.strip()],
    )
    reply_to = [site_config.email] if site_config.email else None
    if reply_to:
        msg.reply_to = reply_to
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=False)


def send_contact_inquiry_notification(request, *, submission, site_config) -> None:
    """
    Notify staff that a new contact form inquiry was received.
    Recipients from settings.CONTACT_INQUIRY_NOTIFICATION_EMAILS.
    Reply-To is set to the visitor so you can reply from your mail client.
    """
    recipients = [e.strip() for e in getattr(settings, "CONTACT_INQUIRY_NOTIFICATION_EMAILS", []) if e and str(e).strip()]
    if not recipients:
        return

    site_name = site_config.site_name or "Proxy Soft"
    logo_url = build_logo_absolute_url(request, site_config)
    submissions_url = request.build_absolute_uri(reverse("iamadmin:submissions_list"))

    context = {
        "site_name": site_name,
        "logo_url": logo_url,
        "name": submission.name,
        "email": submission.email,
        "subject": submission.subject,
        "message": submission.message,
        "submissions_url": submissions_url,
        "primary": "#1e40af",
        "primary_dark": "#0a1d37",
        "accent": "#38bdf8",
        "year": timezone.now().year,
    }

    subject = f"{getattr(settings, 'EMAIL_SUBJECT_PREFIX', '')}New inquiry from {submission.name} — please check"
    subject = subject.strip()

    text_body = render_to_string("emails/contact_inquiry_notify.txt", context)
    html_body = render_to_string("emails/contact_inquiry_notify.html", context)

    from_email = settings.DEFAULT_FROM_EMAIL
    if not from_email:
        raise ValueError("DEFAULT_FROM_EMAIL is not configured")

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=recipients,
    )
    visitor = (submission.email or "").strip()
    if visitor:
        msg.reply_to = [visitor]
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=False)
