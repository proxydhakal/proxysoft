"""Main URL configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("", include("apps.core.urls")),
    path("pages/", include("apps.pages.urls")),
    path("blog/", include("apps.blog.urls")),
    path("iamadmin/", include("apps.core.iamadmin_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
