"""
Erase existing services and roll out the production Service Stack content.

Usage
-----
  python manage.py seed_services
  python manage.py seed_services --dry-run
"""

from django.core.management.base import BaseCommand

from apps.core.models import Service, SiteConfiguration

SERVICES = [
    {
        "order": 1,
        "title": "Web/App Development",
        "description": (
            "End-to-end product engineering across backend, frontend, mobile, and desktop — "
            "built to scale with your business and ship with confidence."
        ),
        "details": (
            "We design and build full-stack web and application products from discovery through launch "
            "and ongoing improvement.\n\n"
            "What we cover:\n"
            "• Backend APIs and business logic with Django, Node.js, and related frameworks\n"
            "• Modern frontend experiences with React, Next.js, and accessible UI patterns\n"
            "• Mobile apps for iOS and Android using Flutter and React Native\n"
            "• Desktop tooling when your workflow needs a native-feeling app\n\n"
            "You get clear milestones, maintainable code, and a product your team can grow without "
            "starting over every year."
        ),
        "icon_class": "fa-solid fa-laptop-code",
        "icon_style": "blue",
        "tags": "Backend, Frontend, Mobile, Desktop",
        "is_cta": False,
    },
    {
        "order": 2,
        "title": "Robotic Process Automation",
        "description": (
            "Automate repetitive work with agentic workflows, n8n, Robocorp, and Playwright — "
            "so your team spends time on decisions, not copy-paste."
        ),
        "details": (
            "We help you identify high-friction processes and replace them with reliable automation "
            "that fits the tools you already use.\n\n"
            "Typical outcomes:\n"
            "• Agentic assistants that gather context and complete multi-step tasks\n"
            "• n8n workflows that connect CRMs, emails, sheets, and internal APIs\n"
            "• Robocorp bots for structured back-office and ERP-style operations\n"
            "• Playwright-powered browser automation for portals that lack clean APIs\n\n"
            "We focus on auditability, error handling, and handoff documentation so automations "
            "stay trustworthy after go-live."
        ),
        "icon_class": "fa-solid fa-robot",
        "icon_style": "violet",
        "tags": "Agentic, n8n, Robocorp, Playwright",
        "is_cta": False,
    },
    {
        "order": 3,
        "title": "Project Outsourcing",
        "description": (
            "Extend your capacity with a dedicated Proxy Soft team — transparent communication, "
            "agile delivery, and ownership from kickoff to handoff."
        ),
        "details": (
            "When deadlines are tight or your in-house bench is full, we plug in as an extension of "
            "your product and engineering organization.\n\n"
            "Engagement models:\n"
            "• Dedicated squads for product builds and feature roadmaps\n"
            "• Staff augmentation for backend, frontend, QA, and DevOps roles\n"
            "• Fixed-scope delivery for MVPs, migrations, and internal tools\n\n"
            "You keep visibility through weekly demos, shared boards, and a single point of contact. "
            "We optimize for long-term maintainability — not short-term shortcuts."
        ),
        "icon_class": "fa-solid fa-people-group",
        "icon_style": "cyan",
        "tags": "Agile, Dedicated Team, Remote, Delivery",
        "is_cta": False,
    },
    {
        "order": 4,
        "title": "IT Consultation",
        "description": (
            "Practical technology guidance for architecture, cloud, security, and digital "
            "transformation — aligned to business outcomes, not buzzwords."
        ),
        "details": (
            "We partner with founders and IT leaders who need a clear path through complex "
            "technology decisions.\n\n"
            "How we help:\n"
            "• Architecture reviews and technology selection for new or existing products\n"
            "• Cloud readiness, cost control, and migration planning\n"
            "• Security and compliance baselines that match your risk profile\n"
            "• Roadmaps that balance quick wins with sustainable scale\n\n"
            "You leave with prioritized recommendations, estimated effort, and an implementation "
            "plan your team can execute — with or without us."
        ),
        "icon_class": "fa-solid fa-comments",
        "icon_style": "orange",
        "tags": "Strategy, Cloud, Security, Architecture",
        "is_cta": False,
    },
    {
        "order": 5,
        "title": "Need a Custom Solution?",
        "description": (
            "Have a unique workflow, industry constraint, or product idea that doesn’t fit a "
            "standard package? We’ll shape a tailored solution around your goals."
        ),
        "details": (
            "Not every challenge fits neatly into a catalog service — and that’s okay.\n\n"
            "Bring us problems like:\n"
            "• Integrating legacy systems with modern web or mobile fronts\n"
            "• Building internal platforms that connect sales, ops, and finance\n"
            "• Combining automation, AI agents, and custom software into one workflow\n"
            "• Rebuilding an aging product without disrupting day-to-day operations\n\n"
            "We start with a short discovery conversation, map constraints and success metrics, "
            "then propose a scoped approach with timeline and investment options. "
            "If it is a fit, we move from idea to working software with the same care we bring "
            "to every engagement."
        ),
        "icon_class": "fa-solid fa-lightbulb",
        "icon_style": "blue",
        "tags": "Discovery, Tailored Build, Partnership",
        "is_cta": True,
    },
]


class Command(BaseCommand):
    help = "Erase current services and install the production Service Stack content."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be written without changing the database.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        config = SiteConfiguration.load()

        existing = Service.objects.filter(site_config=config).count()
        self.stdout.write(f"Current services: {existing}")
        self.stdout.write(f"Will install: {len(SERVICES)} services")

        if dry_run:
            for item in SERVICES:
                self.stdout.write(f"  - [{item['order']}] {item['title']} (cta={item['is_cta']})")
            self.stdout.write(self.style.WARNING("Dry run only — no changes made."))
            return

        deleted, _ = Service.objects.filter(site_config=config).delete()
        self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing service row(s)."))

        # Align section headings used on the homepage
        config.services_section_heading = "Service Stack"
        config.services_section_subheading = (
            "Expert, end-to-end digital solutions for every stage of your growth."
        )
        config.save(update_fields=["services_section_heading", "services_section_subheading"])

        for item in SERVICES:
            Service.objects.create(site_config=config, **item)
            self.stdout.write(self.style.SUCCESS(f"  + {item['title']}"))

        self.stdout.write(self.style.SUCCESS("Service Stack content rolled out successfully."))
