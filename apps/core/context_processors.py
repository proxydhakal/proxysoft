"""Inject site configuration and navigation into every template."""
from .models import SiteConfiguration


def site_config(request):
    """Add `site_config`, dynamic pages for nav/footer, and `is_home`."""
    try:
        config = SiteConfiguration.load()
    except Exception:
        config = None

    nav_pages = []
    footer_pages = []
    try:
        from apps.pages.models import Page

        nav_pages = list(Page.objects.filter(is_published=True, show_in_nav=True).order_by("order", "title"))
        footer_pages = list(Page.objects.filter(is_published=True, show_in_footer=True).order_by("order", "title"))
    except Exception:
        pass

    path = getattr(request, "path", "") or ""
    is_home = path in ("/", "")

    return {
        "site_config": config,
        "nav_pages": nav_pages,
        "footer_pages": footer_pages,
        "is_home": is_home,
    }
