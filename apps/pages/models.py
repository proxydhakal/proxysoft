"""Dynamic pages (CMS) with CKEditor content."""
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class Page(models.Model):
    """A standalone page shown in nav/footer when enabled."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=120, unique=True, help_text="URL segment, e.g. privacy-policy")
    content = RichTextField(help_text="Page body (CKEditor)")
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    show_in_nav = models.BooleanField(default=False, help_text="Show link in main navigation")
    show_in_footer = models.BooleanField(default=False, help_text="Show link in footer Quick Links")
    order = models.PositiveSmallIntegerField(default=0, help_text="Lower numbers appear first")
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("pages:detail", kwargs={"slug": self.slug})
