# Generated manually for Service details modal + CTA card

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_siteconfiguration_watch_story_youtube_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="details",
            field=models.TextField(
                blank=True,
                help_text="Full service details shown in the popup modal (supports multiple paragraphs).",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="is_cta",
            field=models.BooleanField(
                default=False,
                help_text="If checked, render as the highlighted 'Custom Solutions' call-to-action card.",
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="description",
            field=models.TextField(help_text="Short card summary shown on the homepage grid."),
        ),
        migrations.AlterField(
            model_name="service",
            name="icon_style",
            field=models.CharField(
                default="blue",
                help_text="One of: blue, emerald, violet, orange, cyan",
                max_length=50,
            ),
        ),
    ]
