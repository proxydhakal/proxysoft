"""
Export / load site database content for copying data to production (or another environment).

Usage (local / source)::

  python manage.py site_data export
  python manage.py site_data export -o backups/my_site.json
  python manage.py site_data export --skip-auth   # content only, no users

Copy the JSON file (and sync the ``media/`` folder for uploaded images) to the server, then
on production (after ``migrate``)::

  python manage.py site_data load backups/my_site.json

Requires the correct ``DJANGO_ENV`` / settings for each environment.
"""
import os

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

# Models/apps to include (omit sessions, admin logs, permissions noise).
_DEFAULT_LABELS = (
    "sites",
    "auth.user",
    "auth.group",
    "accounts",
    "core",
    "pages",
    "blog",
)

_CONTENT_LABELS = (
    "sites",
    "core",
    "pages",
    "blog",
)

_EXCLUDE = (
    "sessions",
    "admin.logentry",
    "auth.permission",
)


class Command(BaseCommand):
    help = "Export current DB to JSON or load JSON into DB (for production / cloning)."

    def add_arguments(self, parser):
        sub = parser.add_subparsers(dest="subcommand", required=True)

        p_export = sub.add_parser(
            "export",
            help="Dump site data to a JSON fixture file.",
        )
        p_export.add_argument(
            "-o",
            "--output",
            default="site_data_export.json",
            help="Output file path (default: site_data_export.json in cwd).",
        )
        p_export.add_argument(
            "--skip-auth",
            action="store_true",
            help="Exclude users, groups, and account profiles (site content only).",
        )

        p_load = sub.add_parser(
            "load",
            help="Load a fixture file produced by site_data export.",
        )
        p_load.add_argument(
            "fixture",
            help="Path to the JSON file from site_data export.",
        )
        p_load.add_argument(
            "--database",
            default="default",
            help='Django database alias (default: "default").',
        )

    def handle(self, *args, **options):
        sub = options["subcommand"]
        if sub == "export":
            self._export(options)
        elif sub == "load":
            self._load(options)
        else:
            raise CommandError(f"Unknown subcommand: {sub}")

    def _export(self, options):
        out = options["output"]
        skip_auth = options["skip_auth"]
        labels = _CONTENT_LABELS if skip_auth else _DEFAULT_LABELS

        abs_out = os.path.abspath(out)
        self.stdout.write(f"Exporting to {abs_out} ...")

        call_command(
            "dumpdata",
            *labels,
            exclude=list(_EXCLUDE),
            natural_foreign=True,
            natural_primary=True,
            indent=2,
            output=out,
        )

        self.stdout.write(self.style.SUCCESS(f"Wrote {abs_out}"))
        self.stdout.write(
            "Copy this file to the server. If you use uploaded images (logo, hero, blog, etc.), "
            "sync MEDIA_ROOT (e.g. rsync media/) so file paths in the DB resolve."
        )
        if skip_auth:
            self.stdout.write(
                self.style.WARNING(
                    "Exported without auth: create a superuser on production if needed "
                    "(python manage.py createsuperuser)."
                )
            )

    def _load(self, options):
        path = options["fixture"]
        database = options["database"]

        if not os.path.isfile(path):
            raise CommandError(f"Fixture not found: {path}")

        abs_path = os.path.abspath(path)
        self.stdout.write(f"Loading {abs_path} into database {database!r} ...")

        call_command(
            "loaddata",
            abs_path,
            database=database,
            ignore=True,
        )

        self.stdout.write(self.style.SUCCESS("Load complete."))
