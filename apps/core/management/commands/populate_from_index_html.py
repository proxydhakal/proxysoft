"""Management command: python manage.py populate_from_index_html [path/to/index.html]"""
from django.core.management.base import BaseCommand

from apps.core.populate_from_html import populate_from_index_html


class Command(BaseCommand):
    help = "Populate SiteConfiguration and related models from the static index.html file."

    def add_arguments(self, parser):
        parser.add_argument(
            "html_path",
            nargs="?",
            default="index.html",
            help="Path to index.html (default: index.html in project root)",
        )
        parser.add_argument(
            "--no-clear",
            action="store_true",
            help="Do not clear existing Services, CoreValues, TechStack, Testimonials, Clients before populating (merge instead of replace).",
        )

    def handle(self, *args, **options):
        path = options["html_path"]
        clear_related = not options["no_clear"]
        try:
            config = populate_from_index_html(html_path=path, clear_related=clear_related)
            self.stdout.write(self.style.SUCCESS(f"Successfully populated from {path}. Site: {config.site_name}"))
        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(str(e)))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
            raise
