"""
Site configuration (singleton) and dynamic content models.
All editable from admin for a fully dynamic site.
"""
from django.db import models


class SiteConfiguration(models.Model):
    """
    Singleton model: one row for the entire site. Used for SEO, contact, hero, footer, etc.
    """
    # Identity & branding
    site_name = models.CharField(max_length=200, default="Proxy Soft")
    tagline = models.CharField(max_length=255, blank=True, help_text="Short tagline under logo")
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    logo_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Or paste an external logo image URL (used only if no file is uploaded above)",
    )
    favicon = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        help_text="Browser tab icon (.ico or .png, e.g. 32×32). Leave blank to use static/img/favicon.ico or URL below.",
    )
    favicon_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Or external favicon URL (used only if no favicon file is uploaded)",
    )

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    og_image = models.ImageField(upload_to="site/", blank=True, null=True, help_text="Social share image (upload)")
    og_image_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Or paste an external Open Graph image URL (used only if no file is uploaded)",
    )

    # Contact & location
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    # Social links
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    # Hero section
    hero_badge_text = models.CharField(max_length=100, default="Innovative Tech Solutions")
    hero_title = models.CharField(max_length=200, default="Securing Your Digital Future")
    hero_title_highlight = models.CharField(max_length=100, default="Digital", help_text="Word to highlight in hero title")
    hero_description = models.TextField(
        default="Proxy Soft Pvt. Ltd. provides scalable, result-oriented solutions in Web, Mobile, and Software Development for international growth."
    )
    hero_image_url = models.URLField(
        blank=True,
        help_text="External image URL for hero (or leave blank and use hero_image)",
    )
    hero_image = models.ImageField(upload_to="site/", blank=True, null=True)
    hero_cta_primary_text = models.CharField(max_length=80, default="Explore Services")
    hero_cta_secondary_text = models.CharField(max_length=80, default="Contact Us")
    hero_stat_value = models.CharField(max_length=50, default="100%")
    hero_stat_label = models.CharField(max_length=100, default="Result Oriented")

    # About section
    about_section_label = models.CharField(max_length=100, default="Our Foundation")
    about_section_heading = models.CharField(max_length=200, default="The Proxy Soft Vision")
    about_vision_quote = models.TextField(
        default='To establish a technology-driven company providing innovative, scalable, and result-oriented digital solutions.'
    )
    about_owner_name = models.CharField(max_length=200, default="Shekhar Dhakal")
    about_body = models.TextField(
        default="Our company aims to operate as a bridge for foreign projects into Nepal, contributing to local economic growth and employment."
    )
    about_bullets = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated short points, e.g. International Clients, Tech R&D",
    )
    about_core_values_heading = models.CharField(max_length=100, default="Our Core Values")

    # Services section
    services_section_heading = models.CharField(max_length=200, default="Service Stack")
    services_section_subheading = models.CharField(max_length=200, default="Expert solutions for every digital need.")

    # Tech stack section
    tech_section_label = models.CharField(max_length=100, default="Technologies We Use")
    tech_section_heading = models.CharField(max_length=200, default="The Tech Stack")

    # Testimonials section (heading; items in Testimonial model)
    testimonials_heading = models.CharField(max_length=200, blank=True)

    # Clients section
    clients_section_label = models.CharField(max_length=100, default="Trusted Partnerships")
    clients_section_heading = models.CharField(max_length=200, default="Our Valued Clients")
    clients_section_subheading = models.TextField(
        default="We are proud to partner with businesses worldwide, delivering solutions that drive growth and innovation.",
        blank=True,
    )

    # Contact section
    contact_heading = models.CharField(max_length=200, default="Let's Connect")
    contact_intro = models.TextField(
        default="Generate foreign currency revenue in Nepal with our outsourcing services.",
        blank=True,
    )
    contact_form_subject_choices = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated options for subject dropdown, e.g. Development, Digital Marketing",
    )

    # Footer
    footer_tagline = models.TextField(
        default="Contributing to economic growth and employment opportunities within Nepal.",
        blank=True,
    )
    establishment_year = models.CharField(max_length=20, default="2026")
    compliance_number = models.CharField(max_length=200, blank=True)
    company_registration_number = models.CharField(
        max_length=100,
        blank=True,
        default="387235/82/83",
        help_text="Company registration / incorporation number",
    )
    pan_number = models.CharField(
        max_length=50,
        blank=True,
        default="623565535",
        help_text="Permanent Account Number (PAN)",
    )
    footer_copyright = models.CharField(
        max_length=255,
        default="Proxy Soft Pvt. Ltd. All Rights Reserved. | Designed for Global Growth.",
    )
    nav_get_started_text = models.CharField(max_length=50, default="Get Started")

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def save(self, *args, **kwargs):
        # Singleton: only allow one instance
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def about_bullets_list(self):
        if not self.about_bullets:
            return []
        return [s.strip() for s in self.about_bullets.split(",") if s.strip()]

    @property
    def contact_form_subject_list(self):
        if not self.contact_form_subject_choices:
            return []
        return [s.strip() for s in self.contact_form_subject_choices.split(",") if s.strip()]


class CoreValue(models.Model):
    """Core values in the About section (ordered list)."""
    site_config = models.ForeignKey(
        SiteConfiguration, on_delete=models.CASCADE, related_name="core_values", editable=False, default=1
    )
    order = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=500)

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not self.site_config_id:
            self.site_config_id = 1
        super().save(*args, **kwargs)


class Service(models.Model):
    """Services offered (for Services section)."""
    site_config = models.ForeignKey(
        SiteConfiguration, on_delete=models.CASCADE, related_name="services", editable=False, default=1
    )
    order = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-laptop-code",
        help_text="Font Awesome class, e.g. fa-solid fa-laptop-code",
    )
    icon_style = models.CharField(
        max_length=50,
        default="blue",
        help_text="One of: blue, cyan, dark, silver (for Tailwind group hover)",
    )

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not self.site_config_id:
            self.site_config_id = 1
        super().save(*args, **kwargs)


class TechStackItem(models.Model):
    """Technology item (name + icon) for Tech Stack section."""
    site_config = models.ForeignKey(
        SiteConfiguration, on_delete=models.CASCADE, related_name="tech_stack_items", editable=False, default=1
    )
    order = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=100)
    icon_class = models.CharField(
        max_length=100,
        default="fa-brands fa-python",
        help_text="Font Awesome class",
    )
    icon_style = models.CharField(max_length=50, default="blue", help_text="blue or cyan for color")

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not self.site_config_id:
            self.site_config_id = 1
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    """Testimonial quote for the testimonials section."""
    site_config = models.ForeignKey(
        SiteConfiguration, on_delete=models.CASCADE, related_name="testimonials", editable=False, default=1
    )
    order = models.PositiveSmallIntegerField(default=0)
    quote = models.TextField()

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not self.site_config_id:
            self.site_config_id = 1
        super().save(*args, **kwargs)


class Client(models.Model):
    """Client/partner logo or name for Clients section."""
    site_config = models.ForeignKey(
        SiteConfiguration, on_delete=models.CASCADE, related_name="clients", editable=False, default=1
    )
    order = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="clients/", blank=True, null=True)
    url = models.URLField(blank=True)

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not self.site_config_id:
            self.site_config_id = 1
        super().save(*args, **kwargs)


class ContactSubmission(models.Model):
    """Inquiry from the contact form."""
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, blank=True, help_text="Visitor email (for auto-reply)")
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact submission"
        verbose_name_plural = "Contact submissions"
