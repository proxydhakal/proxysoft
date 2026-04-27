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

    # New home design: stat counters (About / Highlights)
    stats_projects_completed = models.PositiveIntegerField(default=150)
    stats_happy_clients = models.PositiveIntegerField(default=80)
    stats_years_experience = models.PositiveIntegerField(default=8)
    stats_team_members = models.PositiveIntegerField(default=25)
    stats_client_satisfaction_rate = models.PositiveIntegerField(default=98, help_text="Percentage without % sign")
    stats_awards_count = models.PositiveIntegerField(default=15)
    watch_story_youtube_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="YouTube URL for the 'Watch Our Story' modal (e.g. https://www.youtube.com/watch?v=XXXX)",
    )

    # Services section
    services_section_heading = models.CharField(max_length=200, default="Service Stack")
    services_section_subheading = models.CharField(max_length=200, default="Expert solutions for every digital need.")

    # Tech stack section
    tech_section_label = models.CharField(max_length=100, default="Technologies We Use")
    tech_section_heading = models.CharField(max_length=200, default="The Tech Stack")

    # Testimonials section (heading; items in Testimonial model)
    testimonials_heading = models.CharField(max_length=200, blank=True)

    # Why Choose Us section
    why_section_label = models.CharField(max_length=100, default="Why Us")
    why_section_heading = models.CharField(max_length=200, default="The Smart Choice for Digital Growth")
    why_section_body = models.TextField(
        default="We combine technical expertise with business acumen to deliver solutions that make a real difference. Here's what sets us apart:",
        blank=True,
    )

    # Projects section
    projects_section_heading = models.CharField(max_length=200, default="Featured Projects")
    projects_section_subheading = models.CharField(
        max_length=300,
        default="A showcase of our best work across industries and technologies.",
        blank=True,
    )

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
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated tech tags shown on the home page, e.g. React, Next.js, Node.js",
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
    name = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=200, blank=True)
    avatar = models.CharField(max_length=10, blank=True, help_text="Initials shown in the avatar, e.g. SJ")
    color = models.CharField(
        max_length=50,
        blank=True,
        help_text="Tailwind gradient classes, e.g. from-brand-400 to-brand-700",
    )
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


class Project(models.Model):
    """Featured project for the home page projects section."""

    site_config = models.ForeignKey(
        SiteConfiguration, on_delete=models.CASCADE, related_name="projects", editable=False, default=1
    )
    order = models.PositiveSmallIntegerField(default=0)
    category = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    theme = models.CharField(
        max_length=30,
        default="brand",
        help_text="Color theme: brand, emerald, violet, orange, cyan (used for gradients in the template)",
    )
    url = models.URLField(blank=True, help_text="Optional link to the project/case study")

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not self.site_config_id:
            self.site_config_id = 1
        super().save(*args, **kwargs)


class WhyChooseUsItem(models.Model):
    """Item in the 'Why Choose Us' section."""
    COLOR_CHOICES = [
        ("blue", "Blue (Brand)"),
        ("emerald", "Emerald (Green)"),
        ("violet", "Violet (Purple)"),
        ("orange", "Orange"),
        ("cyan", "Cyan"),
    ]
    site_config = models.ForeignKey(
        SiteConfiguration, on_delete=models.CASCADE, related_name="why_items", editable=False, default=1
    )
    order = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    color_theme = models.CharField(max_length=50, choices=COLOR_CHOICES, default="blue")
    icon_svg_path = models.TextField(
        blank=True,
        help_text="SVG path d='...' value only. Used inside <path stroke-linecap='round' d='...'>.",
    )

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not self.site_config_id:
            self.site_config_id = 1
        super().save(*args, **kwargs)


class HeroBadge(models.Model):
    """Floating orbiting badge in the hero illustration (max 4, by order)."""
    site_config = models.ForeignKey(
        SiteConfiguration, on_delete=models.CASCADE, related_name="hero_badges", editable=False, default=1
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Position slot: 1=top, 2=right, 3=left, 4=bottom",
    )
    label = models.CharField(max_length=100)
    bg_color = models.CharField(
        max_length=50,
        default="bg-blue-500",
        help_text="Tailwind bg class, e.g. bg-blue-500, bg-emerald-500, bg-violet-500, bg-orange-500",
    )
    icon_svg_path = models.TextField(
        blank=True,
        help_text="SVG path d='...' value only for the small badge icon.",
    )

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
