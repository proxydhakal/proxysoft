from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "published_at", "is_published"]
    list_filter = ["is_published", "published_at"]
    list_editable = ["is_published"]
    search_fields = ["title", "slug", "excerpt", "content"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    fieldsets = (
        (None, {"fields": ("title", "slug", "excerpt", "content", "featured_image")}),
        ("Publishing", {"fields": ("author", "published_at", "is_published")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
    )
