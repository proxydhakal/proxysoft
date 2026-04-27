from django.shortcuts import get_object_or_404, render
from .models import Page


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(
        request,
        "pages/page_detail.html",
        {
            "page": page,
            "meta_title": page.meta_title or page.title,
            "meta_description": page.meta_description,
        },
    )
