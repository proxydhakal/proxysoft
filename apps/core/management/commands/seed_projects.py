"""
Erase existing featured projects and roll out Proxy Soft major project content.

Usage
-----
  python manage.py seed_projects
  python manage.py seed_projects --dry-run
"""

from django.core.management.base import BaseCommand

from apps.core.models import Project, SiteConfiguration

PROJECTS = [
    {
        "order": 1,
        "category": "E-Commerce",
        "title": "Commerce Platform (React + FastAPI)",
        "description": (
            "A modern online storefront with a React storefront and FastAPI backend — "
            "product catalogs, cart and checkout, order tracking, and an admin panel "
            "built for day-to-day retail operations."
        ),
        "theme": "brand",
        "url": "",
    },
    {
        "order": 2,
        "category": "EdTech",
        "title": "School Management System",
        "description": (
            "An all-in-one school platform covering student attendance, billing, ledgers, "
            "fee schedules, academic records, and parent-facing updates — so offices spend "
            "less time on paperwork and more time with students."
        ),
        "theme": "emerald",
        "url": "",
    },
    {
        "order": 3,
        "category": "RPA / Automation",
        "title": "RPA Orchestration Platform",
        "description": (
            "A control center to monitor robotic process automation at scale — live bot "
            "activity, run history, log monitoring, and process records so teams can spot "
            "failures early and keep automations trustworthy."
        ),
        "theme": "violet",
        "url": "",
    },
    {
        "order": 4,
        "category": "Network Infrastructure",
        "title": "Enterprise Network Management",
        "description": (
            "Manage routers, switches, and firewalls from one place — network monitoring, "
            "VLAN configuration, MAC binding, and device health views built for IT teams "
            "that need clarity across the whole campus or office network."
        ),
        "theme": "orange",
        "url": "",
    },
    {
        "order": 5,
        "category": "Retail / POS",
        "title": "Inventory & Billing for Retail Shops",
        "description": (
            "A retail billing and stock system with VAT calculation, ledger entries, "
            "inventory tracking, and day-end billing — designed for shops that need "
            "accurate books without complicated enterprise software."
        ),
        "theme": "cyan",
        "url": "",
    },
]


class Command(BaseCommand):
    help = "Erase current projects and install Proxy Soft major project showcase content."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be written without changing the database.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        config = SiteConfiguration.load()

        existing = Project.objects.filter(site_config=config).count()
        self.stdout.write(f"Current projects: {existing}")
        self.stdout.write(f"Will install: {len(PROJECTS)} projects")

        if dry_run:
            for item in PROJECTS:
                self.stdout.write(f"  - [{item['order']}] {item['title']} ({item['category']})")
            self.stdout.write(self.style.WARNING("Dry run only — no changes made."))
            return

        deleted, _ = Project.objects.filter(site_config=config).delete()
        self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing project row(s)."))

        config.projects_section_heading = "Featured"
        config.projects_section_subheading = (
            "Selected work across commerce, education, automation, networking, and retail operations."
        )
        config.save(update_fields=["projects_section_heading", "projects_section_subheading"])

        for item in PROJECTS:
            Project.objects.create(site_config=config, **item)
            self.stdout.write(self.style.SUCCESS(f"  + {item['title']}"))

        self.stdout.write(self.style.SUCCESS("Featured projects content rolled out successfully."))
