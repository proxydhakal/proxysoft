from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import BlogPost


def _published_qs():
    now = timezone.now()
    return BlogPost.objects.filter(is_published=True).filter(
        Q(published_at__isnull=True) | Q(published_at__lte=now)
    )


def post_list(request):
    qs = _published_qs().select_related("author").order_by("-published_at", "-created_at")
    return render(request, "blog/post_list.html", {"posts": qs})


def post_detail(request, slug):
    post = get_object_or_404(_published_qs(), slug=slug)
    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "meta_title": post.meta_title or post.title,
            "meta_description": post.meta_description or post.excerpt,
        },
    )
