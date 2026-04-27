"""Blog posts with CKEditor body."""
from django.conf import settings
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=160, unique=True)
    excerpt = models.TextField(blank=True, help_text="Short summary for listing")
    content = RichTextField()
    featured_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
    )
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    is_published = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})
