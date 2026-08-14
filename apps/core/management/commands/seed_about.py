"""
Update About section + core values with realistic Proxy Soft (est. 2026) content.

Usage
-----
  python manage.py seed_about
  python manage.py seed_about --dry-run
"""

from django.core.management.base import BaseCommand

from apps.core.models import CoreValue, SiteConfiguration

ABOUT_CONFIG = {
    "about_section_label": "About Proxy Soft",
    "about_section_heading": "Built for Real Work, Not Just Demos",
    "about_vision_quote": (
        "Proxy Soft designs and delivers custom digital products and automation — "
        "from focused tools for growing teams to enterprise-grade systems that run around the clock."
    ),
    "about_body": (
        "Established in 2026 and based in Nepal, we help businesses replace fragile, "
        "manual processes with software that is clear, reliable, and easy to own. "
        "Whether you need a custom-designed web or mobile experience, a workflow automation "
        "across your existing tools, or a full platform built for scale, we stay close "
        "from discovery through launch — with 24/7 support when something needs attention."
    ),
    "about_owner_name": "Shekhar Dhakal",
    "about_bullets": "Custom Design, Small to Enterprise Automation, 24/7 Support, Nepal-based Delivery",
    "about_core_values_heading": "What Guides Us",
    "establishment_year": "2026",
    # Realistic early-stage numbers for a 2026 company
    "stats_projects_completed": 15,
    "stats_happy_clients": 8,
    "stats_years_experience": 1,
    "stats_team_members": 6,
    "stats_client_satisfaction_rate": 98,
    "footer_tagline": (
        "Custom design and automation solutions for teams of every size — "
        "backed by responsive, 24/7 support."
    ),
}

CORE_VALUES = [
    {
        "order": 1,
        "title": "Custom by Default",
        "description": (
            "We don’t force your process into a template. We design interfaces and systems "
            "around how your people actually work."
        ),
    },
    {
        "order": 2,
        "title": "Automation That Scales",
        "description": (
            "From a single workflow for a small team to enterprise-grade automation across "
            "departments — we build solutions that grow with you."
        ),
    },
    {
        "order": 3,
        "title": "Support When You Need It",
        "description": (
            "Production systems don’t wait for office hours. Our team provides 24/7 support "
            "so issues are handled quickly and clearly."
        ),
    },
]


class Command(BaseCommand):
    help = "Replace About section content and core values with realistic Proxy Soft copy (est. 2026)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview changes without writing to the database.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        config = SiteConfiguration.load()

        self.stdout.write("About config fields to update:")
        for key, value in ABOUT_CONFIG.items():
            preview = value if not isinstance(value, str) else (value[:90] + ("…" if len(value) > 90 else ""))
            self.stdout.write(f"  - {key}: {preview}")

        self.stdout.write(f"Core values to install: {len(CORE_VALUES)}")
        for item in CORE_VALUES:
            self.stdout.write(f"  - [{item['order']}] {item['title']}")

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run only — no changes made."))
            return

        for key, value in ABOUT_CONFIG.items():
            setattr(config, key, value)
        config.save()

        deleted, _ = CoreValue.objects.filter(site_config=config).delete()
        self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing core value row(s)."))

        for item in CORE_VALUES:
            CoreValue.objects.create(site_config=config, **item)
            self.stdout.write(self.style.SUCCESS(f"  + {item['title']}"))

        self.stdout.write(self.style.SUCCESS("About section content rolled out successfully."))
