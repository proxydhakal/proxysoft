"""Home page and any other public views."""
import json
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import SiteConfiguration, ContactSubmission


def home(request):
    """Render the main landing page with dynamic content."""
    config = SiteConfiguration.load()

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()
        if name and message:
            ContactSubmission.objects.create(name=name, subject=subject or "Inquiry", message=message)
            messages.success(request, "Thank you! Your message has been sent.")
            return redirect(reverse("core:home") + "#contact")
        else:
            messages.error(request, "Please provide your name and message.")

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
