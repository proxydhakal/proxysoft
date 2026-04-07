"""Views for /iamadmin dashboard: login, overview, and CRUD for site content."""
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

from apps.accounts.models import UserProfile
from .models import (
    SiteConfiguration,
    Service,
    Client,
    CoreValue,
    Testimonial,
    TechStackItem,
    ContactSubmission,
)
from apps.blog.models import BlogPost
from apps.pages.models import Page

from .iamadmin_forms import (
    IAMLoginForm,
    SiteConfigForm,
    ServiceForm,
    ClientForm,
    CoreValueForm,
    TestimonialForm,
    TechStackItemForm,
    PageForm,
    BlogPostForm,
)


def _dashboard_context(request, active_tab="overview"):
    user = request.user
    if hasattr(user, "profile") and user.profile.full_name:
        user_display = user.profile.full_name
    else:
        user_display = user.get_full_name() or user.username
    return {
        "active_tab": active_tab,
        "user_display": user_display,
    }


# ---------- Login / Logout ----------
@require_http_methods(["GET", "POST"])
@csrf_protect
def iam_login(request):
    if request.user.is_authenticated:
        return redirect("/iamadmin/")
    if request.method == "POST":
        form = IAMLoginForm(request=request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            next_url = request.GET.get("next") or "/iamadmin/"
            return redirect(next_url)
    else:
        form = IAMLoginForm(request=request)
    return render(request, "iamadmin/login.html", {"form": form})


@login_required(login_url="/iamadmin/login/")
def iam_logout(request):
    auth_logout(request)
    return redirect("/iamadmin/login/")


# ---------- Dashboard Overview ----------
@login_required(login_url="/iamadmin/login/")
def iam_dashboard(request):
    config = SiteConfiguration.load()
    recent = ContactSubmission.objects.all()[:10]
    stats = {
        "total_submissions": ContactSubmission.objects.count(),
        "services_count": config.services.count(),
        "clients_count": config.clients.count(),
    }
    return render(request, "iamadmin/overview.html", {
        **_dashboard_context(request, "overview"),
        "recent_submissions": recent,
        "stats": stats,
        "config": config,
    })


# ---------- Site Configuration ----------
@login_required(login_url="/iamadmin/login/")
@require_http_methods(["GET", "POST"])
def iam_site_config(request):
    config = SiteConfiguration.load()
    if request.method == "POST":
        form = SiteConfigForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Site configuration saved.")
            return redirect("iamadmin:site_config")
    else:
        form = SiteConfigForm(instance=config)
    return render(request, "iamadmin/site_config.html", {
        **_dashboard_context(request, "site-config"),
        "form": form,
    })


# ---------- Services ----------
@login_required(login_url="/iamadmin/login/")
def iam_service_list(request):
    config = SiteConfiguration.load()
    return render(request, "iamadmin/service_list.html", {
        **_dashboard_context(request, "services"),
        "services": config.services.all(),
    })


@login_required(login_url="/iamadmin/login/")
@require_http_methods(["GET", "POST"])
def iam_service_form(request, pk=None):
    config = SiteConfiguration.load()
    instance = get_object_or_404(Service, pk=pk, site_config=config) if pk else None
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.site_config_id = 1
            obj.save()
            messages.success(request, "Service saved.")
            return redirect("iamadmin:service_list")
    else:
        form = ServiceForm(instance=instance)
    return render(request, "iamadmin/service_form.html", {
        **_dashboard_context(request, "services"),
        "form": form,
        "instance": instance,
    })


@login_required(login_url="/iamadmin/login/")
@require_http_methods(["POST"])
def iam_service_delete(request, pk):
    config = SiteConfiguration.load()
    obj = get_object_or_404(Service, pk=pk, site_config=config)
    obj.delete()
    messages.success(request, "Service deleted.")
    return redirect("iamadmin:service_list")


# ---------- Clients ----------
@login_required(login_url="/iamadmin/login/")
def iam_client_list(request):
    config = SiteConfiguration.load()
    return render(request, "iamadmin/client_list.html", {
        **_dashboard_context(request, "clients"),
        "clients": config.clients.all(),
    })


@login_required(login_url="/iamadmin/login/")
@require_http_methods(["GET", "POST"])
def iam_client_form(request, pk=None):
    config = SiteConfiguration.load()
    instance = get_object_or_404(Client, pk=pk, site_config=config) if pk else None
    if request.method == "POST":
        form = ClientForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.site_config_id = 1
            obj.save()
            messages.success(request, "Client saved.")
            return redirect("iamadmin:client_list")
    else:
        form = ClientForm(instance=instance)
    return render(request, "iamadmin/client_form.html", {
        **_dashboard_context(request, "clients"),
        "form": form,
        "instance": instance,
    })


@login_required(login_url="/iamadmin/login/")
@require_http_methods(["POST"])
def iam_client_delete(request, pk):
    config = SiteConfiguration.load()
    obj = get_object_or_404(Client, pk=pk, site_config=config)
    obj.delete()
    messages.success(request, "Client deleted.")
    return redirect("iamadmin:client_list")


# ---------- Core Values ----------
@login_required(login_url="/iamadmin/login/")
def iam_corevalue_list(request):
    config = SiteConfiguration.load()
    return render(request, "iamadmin/corevalue_list.html", {
        **_dashboard_context(request, "core-values"),
        "items": config.core_values.all(),
    })


@login_required(login_url="/iamadmin/login/")
@require_http_methods(["GET", "POST"])
def iam_corevalue_form(request, pk=None):
    config = SiteConfiguration.load()
    instance = get_object_or_404(CoreValue, pk=pk, site_config=config) if pk else None
    if request.method == "POST":
        form = CoreValueForm(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.site_config_id = 1
            obj.save()
            messages.success(request, "Core value saved.")
            return redirect("iamadmin:corevalue_list")
    else:
        form = CoreValueForm(instance=instance)
    return render(request, "iamadmin/corevalue_form.html", {
        **_dashboard_context(request, "core-values"),
        "form": form,
        "instance": instance,
    })


@login_required(login_url="/iamadmin/login/")
@require_http_methods(["POST"])
def iam_corevalue_delete(request, pk):
    config = SiteConfiguration.load()
    obj = get_object_or_404(CoreValue, pk=pk, site_config=config)
    obj.delete()
    messages.success(request, "Core value deleted.")
    return redirect("iamadmin:corevalue_list")


# ---------- Testimonials ----------
@login_required(login_url="/iamadmin/login/")
def iam_testimonial_list(request):
    config = SiteConfiguration.load()
    return render(request, "iamadmin/testimonial_list.html", {
        **_dashboard_context(request, "testimonials"),
        "items": config.testimonials.all(),
    })


@login_required(login_url="/iamadmin/login/")
@require_http_methods(["GET", "POST"])
def iam_testimonial_form(request, pk=None):
    config = SiteConfiguration.load()
    instance = get_object_or_404(Testimonial, pk=pk, site_config=config) if pk else None
    if request.method == "POST":
        form = TestimonialForm(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.site_config_id = 1
            obj.save()
            messages.success(request, "Testimonial saved.")
            return redirect("iamadmin:testimonial_list")
    else:
        form = TestimonialForm(instance=instance)
    return render(request, "iamadmin/testimonial_form.html", {
        **_dashboard_context(request, "testimonials"),
        "form": form,
        "instance": instance,
    })


@login_required(login_url="/iamadmin/login/")
@require_http_methods(["POST"])
def iam_testimonial_delete(request, pk):
    config = SiteConfiguration.load()
    obj = get_object_or_404(Testimonial, pk=pk, site_config=config)
    obj.delete()
    messages.success(request, "Testimonial deleted.")
    return redirect("iamadmin:testimonial_list")


# ---------- Tech Stack ----------
@login_required(login_url="/iamadmin/login/")
def iam_techstack_list(request):
    config = SiteConfiguration.load()
    return render(request, "iamadmin/techstack_list.html", {
        **_dashboard_context(request, "tech-stack"),
        "items": config.tech_stack_items.all(),
    })


@login_required(login_url="/iamadmin/login/")
@require_http_methods(["GET", "POST"])
def iam_techstack_form(request, pk=None):
    config = SiteConfiguration.load()
    instance = get_object_or_404(TechStackItem, pk=pk, site_config=config) if pk else None
    if request.method == "POST":
        form = TechStackItemForm(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.site_config_id = 1
            obj.save()
            messages.success(request, "Tech stack item saved.")
            return redirect("iamadmin:techstack_list")
    else:
        form = TechStackItemForm(instance=instance)
    return render(request, "iamadmin/techstack_form.html", {
        **_dashboard_context(request, "tech-stack"),
        "form": form,
        "instance": instance,
    })


@login_required(login_url="/iamadmin/login/")
@require_http_methods(["POST"])
def iam_techstack_delete(request, pk):
    config = SiteConfiguration.load()
    obj = get_object_or_404(TechStackItem, pk=pk, site_config=config)
    obj.delete()
    messages.success(request, "Tech stack item deleted.")
    return redirect("iamadmin:techstack_list")


# ---------- CMS pages (footer / nav) ----------
@login_required(login_url="/iamadmin/login/")
def iam_page_list(request):
    pages = Page.objects.all()
    return render(
        request,
        "iamadmin/page_list.html",
        {**_dashboard_context(request, "pages-cms"), "pages": pages},
    )


@login_required(login_url="/iamadmin/login/")
@require_http_methods(["GET", "POST"])
def iam_page_form(request, pk=None):
    instance = get_object_or_404(Page, pk=pk) if pk else None
    if request.method == "POST":
        form = PageForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Page saved.")
            return redirect("iamadmin:page_list")
    else:
        form = PageForm(instance=instance)
    return render(
        request,
        "iamadmin/page_form.html",
        {**_dashboard_context(request, "pages-cms"), "form": form, "instance": instance},
    )


@login_required(login_url="/iamadmin/login/")
@require_http_methods(["POST"])
def iam_page_delete(request, pk):
    obj = get_object_or_404(Page, pk=pk)
    obj.delete()
    messages.success(request, "Page deleted.")
    return redirect("iamadmin:page_list")


# ---------- Blog ----------
@login_required(login_url="/iamadmin/login/")
def iam_blog_list(request):
    posts = BlogPost.objects.all().select_related("author").order_by("-published_at", "-created_at")
    return render(
        request,
        "iamadmin/blog_list.html",
        {**_dashboard_context(request, "blog"), "posts": posts},
    )


@login_required(login_url="/iamadmin/login/")
@require_http_methods(["GET", "POST"])
def iam_blog_form(request, pk=None):
    instance = get_object_or_404(BlogPost, pk=pk) if pk else None
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            post = form.save(commit=False)
            if not post.author_id:
                post.author = request.user
            post.save()
            messages.success(request, "Blog post saved.")
            return redirect("iamadmin:blog_list")
    else:
        initial = {}
        if not instance:
            initial["author"] = request.user
        form = BlogPostForm(instance=instance, initial=initial)
    return render(
        request,
        "iamadmin/blog_form.html",
        {**_dashboard_context(request, "blog"), "form": form, "instance": instance},
    )


@login_required(login_url="/iamadmin/login/")
@require_http_methods(["POST"])
def iam_blog_delete(request, pk):
    obj = get_object_or_404(BlogPost, pk=pk)
    obj.delete()
    messages.success(request, "Blog post deleted.")
    return redirect("iamadmin:blog_list")


# ---------- Contact Submissions ----------
@login_required(login_url="/iamadmin/login/")
def iam_submissions_list(request):
    items = ContactSubmission.objects.all()
    return render(request, "iamadmin/submissions_list.html", {
        **_dashboard_context(request, "submissions"),
        "items": items,
    })


@login_required(login_url="/iamadmin/login/")
@require_http_methods(["POST"])
def iam_submission_delete(request, pk):
    obj = get_object_or_404(ContactSubmission, pk=pk)
    obj.delete()
    messages.success(request, "Submission deleted.")
    return redirect("iamadmin:submissions_list")


# ---------- My Profile (full_name) ----------
@login_required(login_url="/iamadmin/login/")
@require_http_methods(["GET", "POST"])
def iam_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user, defaults={"full_name": ""})
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        profile.full_name = full_name
        profile.save()
        messages.success(request, "Profile updated.")
        return redirect("iamadmin:profile")
    return render(request, "iamadmin/profile.html", {
        **_dashboard_context(request, "profile"),
        "profile": profile,
    })
