from django.contrib import admin
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "show_in_nav", "show_in_footer", "order", "is_published"]
    list_filter = ["is_published", "show_in_nav", "show_in_footer"]
    list_editable = ["order", "show_in_nav", "show_in_footer", "is_published"]
    search_fields = ["title", "slug", "content"]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "content")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
        ("Placement", {"fields": ("show_in_nav", "show_in_footer", "order", "is_published")}),
    )
