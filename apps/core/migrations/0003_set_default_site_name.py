# Generated data migration - set default Site display name for admin

from django.db import migrations


def set_site_name(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    # pk=1 is expected when SITE_ID = 1, but fresh/empty DBs may have no row yet
    site = Site.objects.filter(pk=1).first()
    if site is None:
        site = Site.objects.order_by("pk").first()
    if site is None:
        Site.objects.create(pk=1, domain="example.com", name="Proxy Soft")
        return
    site.name = "Proxy Soft"
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
