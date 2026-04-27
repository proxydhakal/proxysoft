"""Forms for IAM admin dashboard CRUD."""
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from apps.blog.models import BlogPost
from apps.pages.models import Page

from .models import (
    SiteConfiguration,
    Service,
    Client,
    CoreValue,
    Testimonial,
    TechStackItem,
    WhyChooseUsItem,
    HeroBadge,
    ContactSubmission,
)


class IAMLoginForm(forms.Form):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={
        "class": "w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-proxyBlue outline-none transition",
        "placeholder": "Username",
        "autofocus": True,
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-proxyBlue outline-none transition",
        "placeholder": "••••••••",
    }))

    def clean(self):
        data = super().clean()
        username = data.get("username")
        password = data.get("password")
        if username and password:
            self.user = authenticate(self.request, username=username, password=password)
            if self.user is None:
                raise forms.ValidationError("Invalid username or password.")
            if not self.user.is_active:
                raise forms.ValidationError("This account is inactive.")
        return data

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)


class SiteConfigForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        fields = [
            "site_name", "tagline",
            "logo", "logo_url",
            "favicon", "favicon_url",
            "meta_title", "meta_description", "meta_keywords",
            "og_image", "og_image_url",
            "address", "email", "phone",
            "facebook_url", "linkedin_url", "twitter_url", "instagram_url",
            "hero_badge_text", "hero_title", "hero_title_highlight", "hero_description",
            "hero_image_url", "hero_image",
            "hero_cta_primary_text", "hero_cta_secondary_text",
            "hero_stat_value", "hero_stat_label",
            "about_section_label", "about_section_heading", "about_vision_quote",
            "about_owner_name", "about_body", "about_bullets", "about_core_values_heading",
            "services_section_heading", "services_section_subheading",
            "tech_section_label", "tech_section_heading",
            "clients_section_label", "clients_section_heading", "clients_section_subheading",
            "contact_heading", "contact_intro", "contact_form_subject_choices",
            "footer_tagline", "establishment_year",
            "company_registration_number", "pan_number", "compliance_number", "footer_copyright",
            "nav_get_started_text",
            "why_section_label", "why_section_heading", "why_section_body",
            "projects_section_heading", "projects_section_subheading",
        ]
        widgets = {
            "tagline": forms.TextInput(attrs={"class": "w-full px-4 py-2 rounded-lg border border-slate-200"}),
            "logo": forms.ClearableFileInput(attrs={"class": "block w-full text-sm text-slate-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-proxyBlue file:text-white file:font-medium"}),
            "logo_url": forms.URLInput(attrs={"class": "w-full px-4 py-2 rounded-lg border border-slate-200", "placeholder": "https://…"}),
            "favicon": forms.ClearableFileInput(attrs={"class": "block w-full text-sm text-slate-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-proxyBlue file:text-white file:font-medium"}),
            "favicon_url": forms.URLInput(attrs={"class": "w-full px-4 py-2 rounded-lg border border-slate-200", "placeholder": "https://…"}),
            "meta_description": forms.Textarea(attrs={"class": "w-full px-4 py-2 rounded-lg border border-slate-200", "rows": 2}),
            "og_image": forms.ClearableFileInput(attrs={"class": "block w-full text-sm text-slate-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-proxyBlue file:text-white file:font-medium"}),
            "og_image_url": forms.URLInput(attrs={"class": "w-full px-4 py-2 rounded-lg border border-slate-200", "placeholder": "https://…"}),
            "address": forms.Textarea(attrs={"class": "w-full px-4 py-2 rounded-lg border border-slate-200", "rows": 2}),
            "hero_description": forms.Textarea(attrs={"class": "w-full px-4 py-2 rounded-lg border border-slate-200", "rows": 3}),
            "hero_image_url": forms.URLInput(attrs={"class": "w-full px-4 py-2 rounded-lg border border-slate-200", "placeholder": "https://…"}),
            "hero_image": forms.ClearableFileInput(attrs={"class": "block w-full text-sm text-slate-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-proxyBlue file:text-white file:font-medium"}),
            "about_vision_quote": forms.Textarea(attrs={"class": "w-full px-4 py-2 rounded-lg border border-slate-200", "rows": 2}),
            "about_body": forms.Textarea(attrs={"class": "w-full px-4 py-2 rounded-lg border border-slate-200", "rows": 3}),
            "footer_tagline": forms.Textarea(attrs={"class": "w-full px-4 py-2 rounded-lg border border-slate-200", "rows": 2}),
            "why_section_body": forms.Textarea(attrs={"class": "w-full px-4 py-2 rounded-lg border border-slate-200", "rows": 3}),
        }


def _input_class():
    return "w-full px-4 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-proxyBlue outline-none"


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["order", "title", "description", "icon_class", "icon_style", "tags"]
        widgets = {
            "order": forms.NumberInput(attrs={"class": _input_class(), "min": 0}),
            "title": forms.TextInput(attrs={"class": _input_class()}),
            "description": forms.Textarea(attrs={"class": _input_class(), "rows": 3}),
            "icon_class": forms.TextInput(attrs={"class": _input_class(), "placeholder": "fa-solid fa-laptop-code"}),
            "icon_style": forms.Select(choices=[("blue","Blue (Brand)"),("emerald","Emerald"),("violet","Violet"),("orange","Orange"),("cyan","Cyan")], attrs={"class": _input_class()}),
            "tags": forms.TextInput(attrs={"class": _input_class(), "placeholder": "React, Node.js, AWS"}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["order", "name", "logo", "url"]
        widgets = {
            "order": forms.NumberInput(attrs={"class": _input_class(), "min": 0}),
            "name": forms.TextInput(attrs={"class": _input_class()}),
            "url": forms.URLInput(attrs={"class": _input_class()}),
        }


class CoreValueForm(forms.ModelForm):
    class Meta:
        model = CoreValue
        fields = ["order", "title", "description"]
        widgets = {
            "order": forms.NumberInput(attrs={"class": _input_class(), "min": 0}),
            "title": forms.TextInput(attrs={"class": _input_class()}),
            "description": forms.TextInput(attrs={"class": _input_class()}),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["order", "quote"]
        widgets = {
            "order": forms.NumberInput(attrs={"class": _input_class(), "min": 0}),
            "quote": forms.Textarea(attrs={"class": _input_class(), "rows": 3}),
        }


class TechStackItemForm(forms.ModelForm):
    class Meta:
        model = TechStackItem
        fields = ["order", "name", "icon_class", "icon_style"]
        widgets = {
            "order": forms.NumberInput(attrs={"class": _input_class(), "min": 0}),
            "name": forms.TextInput(attrs={"class": _input_class()}),
            "icon_class": forms.TextInput(attrs={"class": _input_class()}),
            "icon_style": forms.TextInput(attrs={"class": _input_class()}),
        }


class PageForm(forms.ModelForm):
    """CMS pages (nav/footer); body uses CKEditor."""

    class Meta:
        model = Page
        fields = [
            "title",
            "slug",
            "content",
            "meta_title",
            "meta_description",
            "show_in_nav",
            "show_in_footer",
            "order",
            "is_published",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": _input_class()}),
            "slug": forms.TextInput(attrs={"class": _input_class(), "placeholder": "e.g. privacy-policy"}),
            "meta_title": forms.TextInput(attrs={"class": _input_class()}),
            "meta_description": forms.Textarea(attrs={"class": _input_class(), "rows": 2}),
            "order": forms.NumberInput(attrs={"class": _input_class(), "min": 0}),
        }


class BlogPostForm(forms.ModelForm):
    """Blog posts; body uses CKEditor."""

    class Meta:
        model = BlogPost
        fields = [
            "title",
            "slug",
            "excerpt",
            "content",
            "featured_image",
            "author",
            "published_at",
            "is_published",
            "meta_title",
            "meta_description",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": _input_class()}),
            "slug": forms.TextInput(attrs={"class": _input_class()}),
            "excerpt": forms.Textarea(attrs={"class": _input_class(), "rows": 3}),
            "meta_title": forms.TextInput(attrs={"class": _input_class()}),
            "meta_description": forms.Textarea(attrs={"class": _input_class(), "rows": 2}),
            "published_at": forms.DateTimeInput(attrs={"class": _input_class()}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        User = get_user_model()
        self.fields["author"].queryset = User.objects.filter(is_staff=True).order_by("username")
        self.fields["author"].required = False
        self.fields["excerpt"].required = False


class WhyChooseUsItemForm(forms.ModelForm):
    class Meta:
        model = WhyChooseUsItem
        fields = ["order", "title", "description", "color_theme", "icon_svg_path"]
        widgets = {
            "order": forms.NumberInput(attrs={"class": _input_class(), "min": 0}),
            "title": forms.TextInput(attrs={"class": _input_class()}),
            "description": forms.TextInput(attrs={"class": _input_class()}),
            "color_theme": forms.Select(attrs={"class": _input_class()}),
            "icon_svg_path": forms.Textarea(attrs={"class": _input_class(), "rows": 2, "placeholder": "M13 10V3L4 14h7v7l9-11h-7z"}),
        }


class HeroBadgeForm(forms.ModelForm):
    class Meta:
        model = HeroBadge
        fields = ["order", "label", "bg_color", "icon_svg_path"]
        widgets = {
            "order": forms.NumberInput(attrs={"class": _input_class(), "min": 1, "max": 4}),
            "label": forms.TextInput(attrs={"class": _input_class(), "placeholder": "Web Dev"}),
            "bg_color": forms.Select(choices=[
                ("bg-blue-500","Blue"),("bg-emerald-500","Emerald"),
                ("bg-violet-500","Violet"),("bg-orange-500","Orange"),("bg-cyan-500","Cyan"),
            ], attrs={"class": _input_class()}),
            "icon_svg_path": forms.Textarea(attrs={"class": _input_class(), "rows": 2, "placeholder": "M12 2L2 7l10 5 10-5-10-5z..."}),
        }
