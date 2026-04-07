"""
Populate the dynamic website database from the static index.html file.
Run via: python manage.py populate_from_index_html [path/to/index.html]
Or call: from apps.core.populate_from_html import populate_from_index_html; populate_from_index_html('index.html')
"""
import os
import re
from pathlib import Path


def _strip(s):
    """Normalize whitespace and strip."""
    if not s:
        return ""
    return " ".join(s.split()).strip()


def _extract(html, pattern, group=1, default=""):
    """Extract first regex group or return default."""
    m = re.search(pattern, html, re.DOTALL)
    if m:
        return _strip(m.group(group))
    return default


def _extract_all(html, pattern, group=1):
    """Extract all non-overlapping matches for the group."""
    return [_strip(m.group(group)) for m in re.finditer(pattern, html, re.DOTALL)]


def parse_index_html(html_path):
    """
    Parse index.html and return a data dict suitable for SiteConfiguration and related models.
    """
    path = Path(html_path)
    if not path.is_absolute():
        # Assume project root if relative
        base = Path(__file__).resolve().parent.parent.parent
        path = base / html_path
    if not path.exists():
        raise FileNotFoundError(f"HTML file not found: {path}")

    html = path.read_text(encoding="utf-8", errors="replace")

    # Title and SEO (use title as meta_title if no meta description)
    meta_title = _extract(html, r"<title>([^<]+)</title>") or "Proxy Soft Pvt. Ltd. | Leading Tech Solutions"
    site_name = "Proxy Soft"  # from nav
    if "|" in meta_title:
        site_name = meta_title.split("|")[0].strip()

    # Hero
    hero_badge = _extract(html, r"fa-lightbulb[^>]*>\s*([^<]+)</div>")
    hero_full_title = _extract(html, r"<h1[^>]*>([^<]*(?:<[^>]+>[^<]*)*)</h1>")
    hero_title_plain = re.sub(r"<[^>]+>", "", hero_full_title) if hero_full_title else "Securing Your Digital Future"
    hero_highlight = _extract(html, r'<span class="text-proxyCyan">([^<]+)</span>', default="Digital")
    hero_desc = _extract(html, r'<p class="text-lg text-slate-300[^"]*"[^>]*>([^<]+)</p>')
    hero_img = _extract(html, r'<img src="([^"]+)"[^>]*alt="Cyber Security"')
    hero_stat_val = _extract(html, r"text-proxyDark font-bold text-3xl[^>]*>[^<]*</i>\s*([^<]+)</p>")
    hero_stat_label = _extract(html, r"text-proxySilver text-xs uppercase[^>]*>([^<]+)</p>", default="Result Oriented")
    hero_cta_primary = _extract(html, r"#services[^>]*>[^<]*</i>\s*([^<]+)</a>", default="Explore Services")
    hero_cta_secondary = _extract(html, r"#contact[^>]*>[^<]*</i>\s*([^<]+)</a>", default="Contact Us")

    # About
    about_label = _extract(html, r"fa-building-columns[^>]*>\s*</i>\s*([^<]+)</h2>")
    about_heading = _extract(html, r"<h3 class=\"text-4xl font-bold\">([^<]+)</h3>", default="The Proxy Soft Vision")
    about_quote = _extract(html, r'border-l-4 border-proxyBlue[^>]*>\s*"([^"]+)"')
    about_owner = _extract(html, r"Owned by <strong>([^<]+)</strong>")
    about_body = _extract(html, r"</strong>\s*,\s*([^<]+)</p>", default="our company aims to operate as a bridge for foreign projects into Nepal, contributing to local economic growth and employment.")
    about_bullets = _extract_all(html, r"fa-circle-check[^>]*></i>\s*([^<]+)</li>")
    about_core_heading = _extract(html, r">(Our Core Values)</h4>") or "Our Core Values"
    core_value_descs = _extract_all(
        html,
        r'<div class="w-12 h-12 bg-proxyBlue shield-clip[^>]*>[^<]+</div>\s*<p class="text-sm">([^<]+)</p>',
    )

    # Services section
    services_heading = _extract(html, r"fa-layer-group[^>]*></i>\s*([^<]+)</h2>", default="Service Stack")
    services_sub = _extract(html, r"text-proxySilver font-medium\">([^<]+)</p>", default="Expert solutions for every digital need.")
    # Service cards: each has h4 title then p description and icon in a div before h4
    service_blocks = re.findall(
        r'<div class="bg-white p-8 rounded-2xl[^"]*"[^>]*>.*?<i class="([^"]+)[^>]*>.*?</i>\s*</div>\s*<h4[^>]*>([^<]+)</h4>\s*<p[^>]*>([^<]+)</p>',
        html,
        re.DOTALL,
    )
    if not service_blocks:
        service_blocks = [
            ("fa-solid fa-laptop-code text-2xl", "Development", "Web applications, responsive websites, and mobile apps for Android, iOS, and cross-platform environments."),
            ("fa-solid fa-chart-pie text-2xl", "Digital Strategy", "Comprehensive Social Media Marketing, SEO (Technical/On-page), and detailed keyword analytics."),
            ("fa-solid fa-palette text-2xl", "Creative UI/UX", "Expert logo design, branding materials, and user-centric multimedia creatives."),
            ("fa-solid fa-cloud-arrow-up text-2xl", "Enterprise & SaaS", "Enterprise systems, cloud-based dashboards, and custom SaaS platform maintenance."),
            ("fa-solid fa-gears text-2xl", "IT Consultancy", "Technical support, system integration, and technology advisory services."),
        ]

    # Tech stack: span with font-bold contains name, preceding i has icon class
    tech_items = re.findall(
        r'<i class="([^"]+)[^>]*>.*?</i>\s*<span class="font-bold[^"]*">([^<]+)</span>',
        html,
    )
    if not tech_items:
        tech_items = [
            ("fa-brands fa-python text-3xl text-proxyBlue", "Python"),
            ("fa-solid fa-bolt text-2xl text-proxyBlue", "Django"),
            ("fa-solid fa-rocket text-2xl text-proxyCyan", "FastAPI"),
            ("fa-solid fa-database text-2xl text-proxyBlue", "Postgres"),
            ("fa-solid fa-database text-2xl text-proxyBlue", "MySQL"),
            ("fa-brands fa-bootstrap text-2xl text-proxyBlue", "Bootstrap"),
            ("fa-solid fa-wind text-2xl text-proxyCyan", "Tailwind"),
            ("fa-solid fa-code-branch text-2xl text-proxyBlue", "DevOps"),
            ("fa-brands fa-docker text-2xl text-proxyBlue", "Docker"),
            ("fa-solid fa-cloud text-2xl text-proxyCyan", "Cloud Hosting"),
        ]

    # Testimonials from Alpine.js array
    testimonials_raw = _extract(html, r"testimonials:\s*\[(.*?)\]", default="")
    testimonials = []
    if testimonials_raw:
        for m in re.finditer(r"'([^']+)'", testimonials_raw):
            testimonials.append(m.group(1))
    if not testimonials:
        testimonials = [
            "Delivering results that matter for global clients.",
            "Pioneering technical SEO and responsive design in Nepal.",
            "Leading the way in SaaS and enterprise innovation.",
        ]

    # Clients section
    clients_heading = _extract(html, r"fa-handshake[^>]*>\s*</i>\s*([^<]+)</h2>", default="Trusted Partnerships")
    clients_sub = _extract(html, r"Our Valued Clients</h3>\s*<p[^>]*>([^<]+)</p>", default="We are proud to partner with businesses worldwide, delivering solutions that drive growth and innovation.")

    # Contact
    contact_heading = _extract(html, r"<h2 class=\"text-4xl font-bold mb-6\">([^<]+)</h2>", default="Let's Connect")
    contact_intro = _extract(html, r"Let's Connect</h2>\s*<p[^>]*>([^<]+)</p>", default="Generate foreign currency revenue in Nepal with our outsourcing services.")
    address = _extract(html, r"<h4[^>]*>Address</h4>\s*<p[^>]*>([^<]+)</p>", default="Likhu -1, Nuwakot Dhikure, Nepal")
    email = _extract(html, r"<h4[^>]*>Email</h4>\s*<p[^>]*>([^<]+)</p>", default="proxysoft2026@gmail.com")
    phone = _extract(html, r"<h4[^>]*>Phone</h4>\s*<p[^>]*>([^<]+)</p>", default="9840177381")
    contact_options = _extract_all(html, r"<option>([^<]+)</option>")
    if not contact_options:
        contact_options = ["Development", "Digital Marketing", "Outsourcing"]

    # Footer
    footer_tagline = _extract(html, r"Proxy Soft Pvt. Ltd.</span>\s*</div>\s*<p[^>]*>([^<]+)</p>", default="Contributing to economic growth and employment opportunities within Nepal.")
    compliance = _extract(html, r"Compliance</h5>\s*<p[^>]*>([^<]+)</p>", default="Operating under Nepal Citizenship No. 25-01-71-04111")
    year = _extract(html, r"Establishment Year:\s*(\d+)", default="2026")
    footer_copyright = _extract(html, r"&copy;\s*\d+\s*([^<]+)</div>", default="")
    if not footer_copyright:
        footer_copyright = "Proxy Soft Pvt. Ltd. All Rights Reserved. | Designed for Global Growth."

    return {
        "site_name": site_name or "Proxy Soft",
        "meta_title": meta_title,
        "hero_badge_text": hero_badge or "Innovative Tech Solutions",
        "hero_title": hero_title_plain or "Securing Your Digital Future",
        "hero_title_highlight": hero_highlight or "Digital",
        "hero_description": hero_desc or "Proxy Soft Pvt. Ltd. provides scalable, result-oriented solutions in Web, Mobile, and Software Development for international growth.",
        "hero_image_url": hero_img or "",
        "hero_stat_value": hero_stat_val or "100%",
        "hero_stat_label": hero_stat_label or "Result Oriented",
        "hero_cta_primary_text": hero_cta_primary or "Explore Services",
        "hero_cta_secondary_text": hero_cta_secondary or "Contact Us",
        "about_section_label": about_label or "Our Foundation",
        "about_section_heading": about_heading or "The Proxy Soft Vision",
        "about_vision_quote": about_quote or "To establish a technology-driven company providing innovative, scalable, and result-oriented digital solutions.",
        "about_owner_name": about_owner or "Shekhar Dhakal",
        "about_body": about_body or "our company aims to operate as a bridge for foreign projects into Nepal, contributing to local economic growth and employment.",
        "about_bullets": ", ".join(about_bullets) if about_bullets else "International Clients, Tech R&D, Remote Operations, SaaS Platforms",
        "about_core_values_heading": about_core_heading or "Our Core Values",
        "core_value_descriptions": core_value_descs or [
            "Comprehensive Social Media & Content Marketing strategy.",
            "Responsive E-commerce and dynamic platform development.",
            "Collaboration with domestic and international institutions.",
        ],
        "services_section_heading": services_heading or "Service Stack",
        "services_section_subheading": services_sub or "Expert solutions for every digital need.",
        "services": [
            {"icon_class": ic.strip(), "title": t, "description": d}
            for ic, t, d in service_blocks
        ] if service_blocks else None,
        "tech_section_label": "Technologies We Use",
        "tech_section_heading": "The Tech Stack",
        "tech_items": [{"icon_class": ic, "name": name} for ic, name in tech_items] if tech_items else None,
        "testimonials": testimonials,
        "clients_section_label": clients_heading or "Trusted Partnerships",
        "clients_section_heading": "Our Valued Clients",
        "clients_section_subheading": clients_sub or "We are proud to partner with businesses worldwide, delivering solutions that drive growth and innovation.",
        "contact_heading": contact_heading or "Let's Connect",
        "contact_intro": contact_intro or "Generate foreign currency revenue in Nepal with our outsourcing services.",
        "address": address or "Likhu -1, Nuwakot Dhikure, Nepal",
        "email": email or "proxysoft2026@gmail.com",
        "phone": phone or "9840177381",
        "contact_form_subject_choices": ", ".join(contact_options) if contact_options else "Development, Digital Marketing, Outsourcing",
        "footer_tagline": footer_tagline or "Contributing to economic growth and employment opportunities within Nepal.",
        "establishment_year": year or "2026",
        "compliance_number": compliance or "Operating under Nepal Citizenship No. 25-01-71-04111",
        "footer_copyright": footer_copyright or "Proxy Soft Pvt. Ltd. All Rights Reserved. | Designed for Global Growth.",
    }


def populate_from_index_html(html_path="index.html", clear_related=True):
    """
    Parse the given index.html and populate SiteConfiguration and related models.

    Args:
        html_path: Path to index.html (relative to project root or absolute).
        clear_related: If True (default), delete existing Services, CoreValues, TechStackItems,
                      Testimonials, and Clients before creating from HTML so the DB matches the file.

    Returns:
        The SiteConfiguration instance that was created/updated.
    """
    import django

    if not django.apps.apps.ready:
        django.setup()

    from apps.core.models import (
        SiteConfiguration,
        CoreValue,
        Service,
        TechStackItem,
        Testimonial,
        Client,
    )

    data = parse_index_html(html_path)

    config, _ = SiteConfiguration.objects.get_or_create(pk=1)
    config.site_name = data["site_name"]
    config.meta_title = data["meta_title"]
    config.hero_badge_text = data["hero_badge_text"]
    config.hero_title = data["hero_title"]
    config.hero_title_highlight = data["hero_title_highlight"]
    config.hero_description = data["hero_description"]
    config.hero_image_url = data.get("hero_image_url") or ""
    config.hero_stat_value = data["hero_stat_value"]
    config.hero_stat_label = data["hero_stat_label"]
    config.hero_cta_primary_text = data["hero_cta_primary_text"]
    config.hero_cta_secondary_text = data["hero_cta_secondary_text"]
    config.about_section_label = data["about_section_label"]
    config.about_section_heading = data["about_section_heading"]
    config.about_vision_quote = data["about_vision_quote"]
    config.about_owner_name = data["about_owner_name"]
    config.about_body = data["about_body"]
    config.about_bullets = data["about_bullets"]
    config.about_core_values_heading = data["about_core_values_heading"]
    config.services_section_heading = data["services_section_heading"]
    config.services_section_subheading = data["services_section_subheading"]
    config.tech_section_label = data["tech_section_label"]
    config.tech_section_heading = data["tech_section_heading"]
    config.clients_section_label = data["clients_section_label"]
    config.clients_section_heading = data["clients_section_heading"]
    config.clients_section_subheading = data["clients_section_subheading"]
    config.contact_heading = data["contact_heading"]
    config.contact_intro = data["contact_intro"]
    config.address = data["address"]
    config.email = data["email"]
    config.phone = data["phone"]
    config.contact_form_subject_choices = data["contact_form_subject_choices"]
    config.footer_tagline = data["footer_tagline"]
    config.establishment_year = data["establishment_year"]
    config.compliance_number = data["compliance_number"]
    config.footer_copyright = data["footer_copyright"]
    config.save()

    if clear_related:
        config.core_values.all().delete()
        config.services.all().delete()
        config.tech_stack_items.all().delete()
        config.testimonials.all().delete()
        config.clients.all().delete()

    # Core values
    for i, desc in enumerate(data.get("core_value_descriptions") or []):
        CoreValue.objects.create(
            site_config=config,
            order=i,
            description=desc[:500],
            title="",
        )

    # Services
    if data.get("services"):
        for i, svc in enumerate(data["services"]):
            icon = (svc.get("icon_class") or "fa-solid fa-laptop-code").strip()
            if "text-2xl" not in icon and "text-3xl" not in icon:
                icon = f"{icon} text-2xl"
            Service.objects.create(
                site_config=config,
                order=i,
                title=svc.get("title", "Service"),
                description=svc.get("description", ""),
                icon_class=icon,
            )

    # Tech stack (clear_related already deleted above)
    if data.get("tech_items"):
        for i, item in enumerate(data["tech_items"]):
            TechStackItem.objects.create(
                site_config=config,
                order=i,
                name=item.get("name", ""),
                icon_class=item.get("icon_class", "fa-solid fa-code"),
            )

    # Testimonials
    if data.get("testimonials"):
        for i, quote in enumerate(data["testimonials"]):
            Testimonial.objects.create(site_config=config, order=i, quote=quote)

    # Clients (HTML has 4 placeholders "Client")
    for i in range(4):
        Client.objects.create(site_config=config, order=i, name="Client")

    return config
