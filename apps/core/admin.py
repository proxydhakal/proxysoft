"""Admin for site configuration and dynamic content."""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteConfiguration,
    CoreValue,
    Service,
    TechStackItem,
    Testimonial,
    Client,
    ContactSubmission,
)


class CoreValueInline(admin.TabularInline):
    model = CoreValue
    extra = 0
    ordering = ["order"]


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0
    ordering = ["order"]


class TechStackItemInline(admin.TabularInline):
    model = TechStackItem
    extra = 0
    ordering = ["order"]


class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 0
    ordering = ["order"]


class ClientInline(admin.TabularInline):
    model = Client
    extra = 0
    ordering = ["order"]


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ["site_name", "email", "phone"]
    inlines = [
        CoreValueInline,
        ServiceInline,
        TechStackItemInline,
        TestimonialInline,
        ClientInline,
    ]

    fieldsets = (
        ("Branding", {"fields": ("site_name", "tagline", "logo", "logo_url")}),
        (
            "SEO",
            {
                "fields": (
                    "meta_title",
                    "meta_description",
                    "meta_keywords",
                    "og_image",
                    "og_image_url",
                )
            },
        ),
        ("Contact & Location", {"fields": ("address", "email", "phone")}),
        ("Social Links", {"fields": ("facebook_url", "linkedin_url", "twitter_url", "instagram_url")}),
        (
            "Hero",
            {
                "fields": (
                    "hero_badge_text",
                    "hero_title",
                    "hero_title_highlight",
                    "hero_description",
                    "hero_image_url",
                    "hero_image",
                    "hero_cta_primary_text",
                    "hero_cta_secondary_text",
                    "hero_stat_value",
                    "hero_stat_label",
                )
            },
        ),
        (
            "About",
            {
                "fields": (
                    "about_section_label",
                    "about_section_heading",
                    "about_vision_quote",
                    "about_owner_name",
                    "about_body",
                    "about_bullets",
                    "about_core_values_heading",
                )
            },
        ),
        ("Services Section", {"fields": ("services_section_heading", "services_section_subheading")}),
        ("Tech Stack Section", {"fields": ("tech_section_label", "tech_section_heading")}),
        ("Testimonials", {"fields": ("testimonials_heading",)}),
        (
            "Clients Section",
            {"fields": ("clients_section_label", "clients_section_heading", "clients_section_subheading")},
        ),
        (
            "Contact",
            {"fields": ("contact_heading", "contact_intro", "contact_form_subject_choices")},
        ),
        (
            "Footer",
            {
                "fields": (
                    "footer_tagline",
                    "establishment_year",
                    "company_registration_number",
                    "pan_number",
                    "compliance_number",
                    "footer_copyright",
                    "nav_get_started_text",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "subject", "message"]
    readonly_fields = ["name", "subject", "message", "created_at"]
