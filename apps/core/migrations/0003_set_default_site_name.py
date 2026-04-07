# Generated data migration - set default Site display name for admin

from django.db import migrations


def set_site_name(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    site = Site.objects.get(pk=1)
    site.name = "Proxy Soft"
    site.domain = site.domain  # keep domain as-is (e.g. example.com or localhost)
    site.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_add_contact_submission"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.RunPython(set_site_name, noop),
    ]
