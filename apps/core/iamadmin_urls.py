"""URLs for /iamadmin dashboard."""
from django.urls import path
from . import iamadmin_views

app_name = "iamadmin"

urlpatterns = [
    path("login/", iamadmin_views.iam_login, name="login"),
    path("logout/", iamadmin_views.iam_logout, name="logout"),
    path("profile/", iamadmin_views.iam_profile, name="profile"),
    path("", iamadmin_views.iam_dashboard, name="dashboard"),
    path("site-config/", iamadmin_views.iam_site_config, name="site_config"),
    # CMS pages
    path("pages/", iamadmin_views.iam_page_list, name="page_list"),
    path("pages/new/", iamadmin_views.iam_page_form, name="page_create"),
    path("pages/<int:pk>/edit/", iamadmin_views.iam_page_form, name="page_edit"),
    path("pages/<int:pk>/delete/", iamadmin_views.iam_page_delete, name="page_delete"),
    # Blog
    path("blog/", iamadmin_views.iam_blog_list, name="blog_list"),
    path("blog/new/", iamadmin_views.iam_blog_form, name="blog_create"),
    path("blog/<int:pk>/edit/", iamadmin_views.iam_blog_form, name="blog_edit"),
    path("blog/<int:pk>/delete/", iamadmin_views.iam_blog_delete, name="blog_delete"),
    # Services
    path("services/", iamadmin_views.iam_service_list, name="service_list"),
    path("services/new/", iamadmin_views.iam_service_form, name="service_create"),
    path("services/<int:pk>/edit/", iamadmin_views.iam_service_form, name="service_edit"),
    path("services/<int:pk>/delete/", iamadmin_views.iam_service_delete, name="service_delete"),
    # Clients
    path("clients/", iamadmin_views.iam_client_list, name="client_list"),
    path("clients/new/", iamadmin_views.iam_client_form, name="client_create"),
    path("clients/<int:pk>/edit/", iamadmin_views.iam_client_form, name="client_edit"),
    path("clients/<int:pk>/delete/", iamadmin_views.iam_client_delete, name="client_delete"),
    # Core values
    path("core-values/", iamadmin_views.iam_corevalue_list, name="corevalue_list"),
    path("core-values/new/", iamadmin_views.iam_corevalue_form, name="corevalue_create"),
    path("core-values/<int:pk>/edit/", iamadmin_views.iam_corevalue_form, name="corevalue_edit"),
    path("core-values/<int:pk>/delete/", iamadmin_views.iam_corevalue_delete, name="corevalue_delete"),
    # Testimonials
    path("testimonials/", iamadmin_views.iam_testimonial_list, name="testimonial_list"),
    path("testimonials/new/", iamadmin_views.iam_testimonial_form, name="testimonial_create"),
    path("testimonials/<int:pk>/edit/", iamadmin_views.iam_testimonial_form, name="testimonial_edit"),
    path("testimonials/<int:pk>/delete/", iamadmin_views.iam_testimonial_delete, name="testimonial_delete"),
    # Tech stack
    path("tech-stack/", iamadmin_views.iam_techstack_list, name="techstack_list"),
    path("tech-stack/new/", iamadmin_views.iam_techstack_form, name="techstack_create"),
    path("tech-stack/<int:pk>/edit/", iamadmin_views.iam_techstack_form, name="techstack_edit"),
    path("tech-stack/<int:pk>/delete/", iamadmin_views.iam_techstack_delete, name="techstack_delete"),
    # Why Choose Us
    path("why-choose-us/", iamadmin_views.iam_whychooseus_list, name="whychooseus_list"),
    path("why-choose-us/new/", iamadmin_views.iam_whychooseus_form, name="whychooseus_create"),
    path("why-choose-us/<int:pk>/edit/", iamadmin_views.iam_whychooseus_form, name="whychooseus_edit"),
    path("why-choose-us/<int:pk>/delete/", iamadmin_views.iam_whychooseus_delete, name="whychooseus_delete"),
    # Hero Badges
    path("hero-badges/", iamadmin_views.iam_herobadge_list, name="herobadge_list"),
    path("hero-badges/new/", iamadmin_views.iam_herobadge_form, name="herobadge_create"),
    path("hero-badges/<int:pk>/edit/", iamadmin_views.iam_herobadge_form, name="herobadge_edit"),
    path("hero-badges/<int:pk>/delete/", iamadmin_views.iam_herobadge_delete, name="herobadge_delete"),
    # Contact submissions
    path("submissions/", iamadmin_views.iam_submissions_list, name="submissions_list"),
    path("submissions/<int:pk>/delete/", iamadmin_views.iam_submission_delete, name="submission_delete"),
]
