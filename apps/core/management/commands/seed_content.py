"""
Populate every section of the site with realistic demo content.

Usage
-----
  python manage.py seed_content            # insert (skip existing)
  python manage.py seed_content --flush    # wipe section data then re-seed
  python manage.py seed_content --section hero
  python manage.py seed_content --section services --flush

Available sections
------------------
  config | services | corevalues | techstack | projects |
  testimonials | clients | whychooseus | herobadges | blog | all (default)
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.blog.models import BlogPost
from apps.core.models import (
    Client,
    CoreValue,
    HeroBadge,
    Project,
    Service,
    SiteConfiguration,
    TechStackItem,
    Testimonial,
    WhyChooseUsItem,
)

User = get_user_model()

SECTIONS = [
    "config",
    "services",
    "corevalues",
    "techstack",
    "projects",
    "testimonials",
    "clients",
    "whychooseus",
    "herobadges",
    "blog",
]


# ─────────────────────────── seed data ────────────────────────────────────────

SITE_CONFIG_DATA = {
    "site_name": "Proxy Soft",
    "tagline": "Digital Innovation Hub",
    "meta_title": "Proxy Soft – Transforming Ideas into Digital Solutions",
    "meta_description": (
        "Proxy Soft Pvt. Ltd. delivers scalable web, mobile, and software solutions "
        "for international growth — based in Kathmandu, serving the world."
    ),
    "meta_keywords": "web development, digital marketing, IT consulting, software Nepal, outsourcing",
    "address": "Kathmandu, Bagmati Province, Nepal",
    "email": "hello@proxysoft.com.np",
    "phone": "+977 9810000000",
    "facebook_url": "https://facebook.com/proxysoftnepal",
    "linkedin_url": "https://linkedin.com/company/proxysoftnepal",
    "twitter_url": "https://twitter.com/proxysoftnepal",
    "instagram_url": "https://instagram.com/proxysoftnepal",
    # Hero
    "hero_badge_text": "Available for New Projects",
    "hero_title": "Transforming Ideas into Digital Solutions",
    "hero_title_highlight": "Digital",
    "hero_description": (
        "Proxy Soft Pvt. Ltd. delivers scalable, result-oriented solutions in "
        "Web, Mobile, and Software Development — bridging global opportunity with Nepal's talent."
    ),
    "hero_cta_primary_text": "Explore Services",
    "hero_cta_secondary_text": "Contact Us",
    "hero_stat_value": "100%",
    "hero_stat_label": "Result Oriented",
    # Stats
    "stats_projects_completed": 150,
    "stats_happy_clients": 80,
    "stats_years_experience": 8,
    "stats_team_members": 25,
    "stats_client_satisfaction_rate": 98,
    "stats_awards_count": 15,
    # About
    "about_section_label": "Our Foundation",
    "about_section_heading": "We Turn Vision Into Reality",
    "about_vision_quote": (
        "To establish a technology-driven company providing innovative, scalable, and "
        "result-oriented digital solutions that bridge global opportunity with Nepal's talent."
    ),
    "about_owner_name": "Shekhar Dhakal",
    "about_body": (
        "Founded in 2016, Proxy Soft has been at the forefront of digital innovation, "
        "helping businesses of all sizes transform their ideas into powerful digital products. "
        "Our team of passionate engineers, designers, and strategists work together to deliver "
        "exceptional results that drive real business growth."
    ),
    "about_bullets": "International Clients, Tech R&D, Quality Delivery, Agile Teams",
    "about_core_values_heading": "Our Core Values",
    # Services section
    "services_section_heading": "Service Stack",
    "services_section_subheading": "Expert, end-to-end digital solutions for every stage of your growth.",
    # Projects section
    "projects_section_heading": "Featured",
    "projects_section_subheading": "A showcase of our best work across industries and technologies.",
    # Why Choose Us
    "why_section_label": "Why Us",
    "why_section_heading": "The Smart Choice for Digital Growth",
    "why_section_body": (
        "We combine technical expertise with business acumen to deliver solutions that make "
        "a real difference. Here's what sets us apart from the competition:"
    ),
    # Tech stack section
    "tech_section_label": "Technologies We Use",
    "tech_section_heading": "The Tech Stack",
    # Clients section
    "clients_section_label": "Trusted Partnerships",
    "clients_section_heading": "Our Valued Clients",
    "clients_section_subheading": (
        "We are proud to partner with businesses worldwide, delivering solutions that "
        "drive growth and innovation across every industry."
    ),
    # Testimonials
    "testimonials_heading": "What Our Clients Say",
    # Contact
    "contact_heading": "Let's Connect",
    "contact_intro": (
        "Have a project in mind or just want to explore possibilities? "
        "We'd love to hear from you — we respond within 24 hours."
    ),
    "contact_form_subject_choices": "Web Development, Digital Marketing, IT Consulting, Project Outsourcing, General Inquiry",
    # Footer
    "footer_tagline": (
        "Transforming ideas into digital solutions that drive growth and innovation "
        "for businesses worldwide. Contributing to economic growth in Nepal."
    ),
    "establishment_year": "2016",
    "company_registration_number": "387235/82/83",
    "pan_number": "623565535",
    "footer_copyright": "Proxy Soft Pvt. Ltd. All Rights Reserved. | Designed for Global Growth.",
    "nav_get_started_text": "Get Started",
}

SERVICES_DATA = [
    {
        "order": 1,
        "title": "Web Development",
        "description": (
            "Modern, scalable web applications built with React, Next.js, Django, and the latest "
            "frameworks. Fast, accessible, and beautifully crafted to convert visitors into customers."
        ),
        "icon_class": "fa-solid fa-laptop-code",
        "icon_style": "blue",
        "tags": "React, Next.js, Django, Node.js",
    },
    {
        "order": 2,
        "title": "Digital Marketing",
        "description": (
            "Data-driven strategies that boost your online presence, drive quality traffic, "
            "and convert visitors into loyal customers through SEO, SEM, and social campaigns."
        ),
        "icon_class": "fa-solid fa-chart-line",
        "icon_style": "emerald",
        "tags": "SEO, SEM, Social Media, Analytics",
    },
    {
        "order": 3,
        "title": "UI/UX Design",
        "description": (
            "Stunning, intuitive designs that captivate users. From wireframes to pixel-perfect "
            "interfaces — we craft experiences that stand out and convert."
        ),
        "icon_class": "fa-solid fa-pen-ruler",
        "icon_style": "violet",
        "tags": "Figma, UI/UX, Branding, Prototyping",
    },
    {
        "order": 4,
        "title": "IT Consulting",
        "description": (
            "Strategic IT guidance to align technology with your business goals. "
            "Architecture planning, security audits, and end-to-end digital transformation."
        ),
        "icon_class": "fa-solid fa-briefcase",
        "icon_style": "orange",
        "tags": "Strategy, Cloud, Security, Architecture",
    },
    {
        "order": 5,
        "title": "Project Outsourcing",
        "description": (
            "Extend your team with our expert engineers. Flexible engagement models, "
            "transparent communication, and consistent delivery — at Nepal-competitive rates."
        ),
        "icon_class": "fa-solid fa-users",
        "icon_style": "cyan",
        "tags": "Agile, Remote, Scalable, Dedicated Teams",
    },
    {
        "order": 6,
        "title": "Mobile Development",
        "description": (
            "Cross-platform and native mobile apps for iOS and Android. From MVP to "
            "production-grade apps — performant, offline-capable, and beautifully designed."
        ),
        "icon_class": "fa-solid fa-mobile-screen",
        "icon_style": "blue",
        "tags": "React Native, Flutter, iOS, Android",
    },
]

CORE_VALUES_DATA = [
    {
        "order": 1,
        "title": "Innovation First",
        "description": "We stay ahead of industry trends to bring you cutting-edge solutions that give you a competitive edge.",
    },
    {
        "order": 2,
        "title": "Reliability You Can Count On",
        "description": "On-time delivery, transparent communication, and consistent quality — every single project.",
    },
    {
        "order": 3,
        "title": "Client-Centered Approach",
        "description": "Your success is our success. We go the extra mile to understand your business and exceed expectations.",
    },
    {
        "order": 4,
        "title": "Continuous Improvement",
        "description": "We invest in R&D and team development so our solutions stay modern, secure, and ahead of the curve.",
    },
]

TECH_STACK_DATA = [
    {"order": 1, "name": "Python", "icon_class": "fa-brands fa-python", "icon_style": "blue"},
    {"order": 2, "name": "Django", "icon_class": "fa-solid fa-d", "icon_style": "blue"},
    {"order": 3, "name": "React", "icon_class": "fa-brands fa-react", "icon_style": "cyan"},
    {"order": 4, "name": "Next.js", "icon_class": "fa-solid fa-n", "icon_style": "blue"},
    {"order": 5, "name": "Node.js", "icon_class": "fa-brands fa-node-js", "icon_style": "emerald"},
    {"order": 6, "name": "PostgreSQL", "icon_class": "fa-solid fa-database", "icon_style": "blue"},
    {"order": 7, "name": "AWS", "icon_class": "fa-brands fa-aws", "icon_style": "orange"},
    {"order": 8, "name": "Docker", "icon_class": "fa-brands fa-docker", "icon_style": "cyan"},
    {"order": 9, "name": "Flutter", "icon_class": "fa-solid fa-mobile-screen", "icon_style": "blue"},
    {"order": 10, "name": "TypeScript", "icon_class": "fa-solid fa-t", "icon_style": "blue"},
]

PROJECTS_DATA = [
    {
        "order": 1,
        "category": "Web Development",
        "title": "FinanceFlow Dashboard",
        "description": (
            "A comprehensive financial analytics platform for real-time portfolio "
            "management, reporting, and multi-currency support for a German fintech startup."
        ),
        "theme": "brand",
        "url": "",
    },
    {
        "order": 2,
        "category": "Digital Marketing",
        "title": "GreenLeaf E-Commerce",
        "description": (
            "Boosted organic traffic by 320% in 4 months with a targeted SEO and "
            "content marketing campaign for an Australian e-commerce brand."
        ),
        "theme": "emerald",
        "url": "",
    },
    {
        "order": 3,
        "category": "UI/UX Design",
        "title": "MediCare Patient Portal",
        "description": (
            "Redesigned patient-doctor interaction portal reducing booking friction by 60% "
            "and improving overall satisfaction scores for a UK healthcare provider."
        ),
        "theme": "violet",
        "url": "",
    },
    {
        "order": 4,
        "category": "IT Consulting",
        "title": "RetailMax Cloud Migration",
        "description": (
            "Complete AWS cloud migration cutting infrastructure costs by 45% with zero "
            "downtime for a 12-store retail chain operating across Southeast Asia."
        ),
        "theme": "orange",
        "url": "",
    },
    {
        "order": 5,
        "category": "Project Outsourcing",
        "title": "TalentBridge HR Platform",
        "description": (
            "Full-stack HR management platform built for a Berlin-based startup — "
            "delivered in 4 months with a 6-developer team, fully tested and deployed."
        ),
        "theme": "cyan",
        "url": "",
    },
]

TESTIMONIALS_DATA = [
    {
        "order": 1,
        "name": "Sarah Johnson",
        "role": "CEO, TechVenture Inc.",
        "avatar": "SJ",
        "color": "from-brand-400 to-brand-700",
        "quote": (
            "Proxy Soft delivered our platform 2 weeks ahead of schedule with exceptional quality. "
            "The team was responsive, professional, and truly understood our vision. "
            "I couldn't recommend them more highly for any complex project."
        ),
    },
    {
        "order": 2,
        "name": "Marcus Chen",
        "role": "CTO, FinanceFlow",
        "avatar": "MC",
        "color": "from-emerald-400 to-teal-700",
        "quote": (
            "The digital marketing strategy they implemented tripled our organic traffic in just 4 months. "
            "Their data-driven approach and constant optimisation made all the difference "
            "for our startup's early growth."
        ),
    },
    {
        "order": 3,
        "name": "Amelia Rodriguez",
        "role": "Founder, StyleCraft",
        "avatar": "AR",
        "color": "from-violet-400 to-purple-700",
        "quote": (
            "Our e-commerce redesign saw a 78% boost in conversions within 6 weeks. "
            "The UI/UX team at Proxy Soft has an incredible eye for detail and user experience. "
            "Best investment we've made this year."
        ),
    },
    {
        "order": 4,
        "name": "David Kim",
        "role": "VP Engineering, RetailMax",
        "avatar": "DK",
        "color": "from-orange-400 to-red-600",
        "quote": (
            "The cloud migration project was flawless — zero downtime, 45% cost reduction, "
            "and our team was fully productive on day one. Proxy Soft exceeded every benchmark we set."
        ),
    },
]

CLIENTS_DATA = [
    {"order": 1, "name": "TechVenture Inc.", "url": ""},
    {"order": 2, "name": "FinanceFlow GmbH", "url": ""},
    {"order": 3, "name": "StyleCraft", "url": ""},
    {"order": 4, "name": "RetailMax Asia", "url": ""},
    {"order": 5, "name": "TalentBridge", "url": ""},
    {"order": 6, "name": "GreenLeaf AU", "url": ""},
]

WHY_CHOOSE_US_DATA = [
    {
        "order": 1,
        "title": "Lightning-Fast Performance",
        "description": "Sub-second load times and optimised user experiences delivered as a baseline, not an afterthought.",
        "color_theme": "blue",
        "icon_svg_path": "M13 10V3L4 14h7v7l9-11h-7z",
    },
    {
        "order": 2,
        "title": "Infinite Scalability",
        "description": "Cloud-native architectures designed to grow seamlessly with your user base and business demands.",
        "color_theme": "emerald",
        "icon_svg_path": "M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12",
    },
    {
        "order": 3,
        "title": "Enterprise-Grade Security",
        "description": "Security-first development practices, regular audits, and proactive vulnerability management.",
        "color_theme": "violet",
        "icon_svg_path": "M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z",
    },
    {
        "order": 4,
        "title": "24/7 Dedicated Support",
        "description": "Round-the-clock monitoring and rapid incident response for mission-critical systems.",
        "color_theme": "orange",
        "icon_svg_path": "M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z",
    },
    {
        "order": 5,
        "title": "Transparent Pricing",
        "description": "No hidden fees. Fixed-price projects or flexible retainer models — you always know what you're paying for.",
        "color_theme": "cyan",
        "icon_svg_path": "M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
    },
]

HERO_BADGES_DATA = [
    {
        "order": 1,
        "label": "Web Dev",
        "bg_color": "bg-blue-500",
        "icon_svg_path": "M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5",
    },
    {
        "order": 2,
        "label": "Marketing",
        "bg_color": "bg-emerald-500",
        "icon_svg_path": "M13 10V3L4 14h7v7l9-11h-7z",
    },
    {
        "order": 3,
        "label": "IT Consult",
        "bg_color": "bg-violet-500",
        "icon_svg_path": "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z",
    },
    {
        "order": 4,
        "label": "Quality",
        "bg_color": "bg-orange-500",
        "icon_svg_path": (
            "M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 "
            "3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 "
            "3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 "
            "3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 "
            "3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 "
            "3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"
        ),
    },
]

BLOG_POSTS_DATA = [
    {
        "title": "How We Cut Cloud Infrastructure Costs by 45% for a Retail Client",
        "slug": "cut-cloud-costs-retail-client",
        "excerpt": (
            "When RetailMax approached us with ballooning AWS bills, we developed a systematic "
            "rightsizing and reserved instance strategy that slashed their monthly spend nearly in half "
            "— with zero downtime during the migration."
        ),
        "content": """<h2>The Challenge</h2>
<p>RetailMax, a 12-store retail chain operating across Southeast Asia, was spending over $18,000/month on AWS infrastructure that had grown organically over five years. Resources were over-provisioned, environments weren't separated cleanly, and there was no tagging strategy — making cost attribution nearly impossible.</p>

<h2>Our Approach</h2>
<p>We began with a two-week discovery phase, using AWS Cost Explorer and Trusted Advisor to identify waste:</p>
<ul>
  <li>Over 60% of EC2 instances were running at under 15% CPU utilisation</li>
  <li>Multiple development databases were running production-grade Multi-AZ RDS instances</li>
  <li>S3 lifecycle rules were absent, leaving terabytes of infrequently accessed data in Standard storage</li>
  <li>No use of Savings Plans or Reserved Instances despite predictable baseline workloads</li>
</ul>

<h2>The Solution</h2>
<p>We delivered a phased migration plan across six weeks:</p>
<ol>
  <li><strong>Rightsizing:</strong> Downgraded 34 EC2 instances to appropriate sizes, saving $3,800/month immediately.</li>
  <li><strong>Reserved Instances:</strong> Converted baseline workloads to 1-year Convertible RIs, locking in a 40% discount.</li>
  <li><strong>S3 Intelligent Tiering:</strong> Enabled lifecycle rules moving objects to Glacier after 30 days of inactivity.</li>
  <li><strong>Dev/Staging separation:</strong> Moved non-production RDS to Single-AZ and scaled down instance classes.</li>
  <li><strong>Tagging strategy:</strong> Implemented a mandatory cost-centre tagging policy enforced via AWS Config rules.</li>
</ol>

<h2>The Result</h2>
<p>Monthly AWS spend dropped from $18,200 to $9,900 — a 45.6% reduction — within 8 weeks, with zero production downtime. The new tagging strategy gave RetailMax's finance team per-store cost visibility for the first time.</p>

<blockquote>The cloud migration project was flawless — zero downtime, 45% cost reduction, and our team was fully productive on day one. Proxy Soft exceeded every benchmark we set. — David Kim, VP Engineering</blockquote>

<h2>Key Takeaways</h2>
<p>Cloud cost optimisation isn't a one-time task. We set up monthly Cost Anomaly Detection alerts and quarterly review cadences so RetailMax can stay lean as their infrastructure evolves.</p>""",
        "is_published": True,
        "published_at": timezone.now(),
        "meta_title": "How We Cut Cloud Costs by 45% for a Retail Client | Proxy Soft",
        "meta_description": "A detailed case study on how Proxy Soft reduced AWS infrastructure spend by 45% for a Southeast Asian retail chain — with zero downtime.",
    },
    {
        "title": "Why Nepal Is Becoming a Top Destination for Software Outsourcing",
        "slug": "nepal-software-outsourcing-destination",
        "excerpt": (
            "Cost-competitive talent, strong English proficiency, a growing developer community, "
            "and a time zone that overlaps with both Europe and Asia — here's why more global "
            "companies are choosing Nepal for their technology outsourcing needs."
        ),
        "content": """<h2>The Shifting Landscape of Outsourcing</h2>
<p>For years, India, the Philippines, and Eastern Europe dominated the global software outsourcing market. But the landscape is shifting. Rising salaries in Bangalore, Manila, and Warsaw, combined with a new generation of highly skilled developers in Nepal, are creating a compelling alternative.</p>

<h2>Talent Quality and Availability</h2>
<p>Nepal produces over 8,000 engineering graduates annually, with the majority in computer science and IT disciplines. Institutions like Tribhuvan University, Kathmandu University, and a growing number of private colleges are turning out developers who are fluent in modern stacks — React, Django, Flutter, Node.js, and cloud platforms.</p>

<p>Critically, Nepal's developer community has strong ties to the international tech ecosystem. Many senior engineers have worked remotely for US, UK, German, and Australian companies for years, building communication habits and code quality standards that match global expectations.</p>

<h2>The Cost Advantage</h2>
<p>Senior full-stack developers in Nepal command salaries of $12,000–$24,000/year — a fraction of equivalent talent in Western markets, and still competitive with India and the Philippines when you factor in quality and communication overhead.</p>

<h2>Time Zone Advantages</h2>
<p>Nepal Standard Time (UTC+5:45) offers genuine overlap with:</p>
<ul>
  <li><strong>Europe:</strong> 3–4 hours of shared business hours with the UK and Central Europe</li>
  <li><strong>Australia:</strong> 4–5 hours of overlap with AEDT, making handoffs smooth</li>
  <li><strong>US East Coast:</strong> Async-first with morning handoffs that work well for agile sprints</li>
</ul>

<h2>How Proxy Soft Bridges the Gap</h2>
<p>At Proxy Soft, we've built our processes around international collaboration from day one. We use Jira for sprint management, Slack for communication, GitHub for code review, and Loom for async video updates — ensuring our clients feel as though their Nepal-based team is down the corridor, not across the globe.</p>

<p>If you're considering outsourcing your next project, <a href="/#contact">get in touch</a> — we'd be happy to discuss how we can become your engineering partner.</p>""",
        "is_published": True,
        "published_at": timezone.now(),
        "meta_title": "Why Nepal Is a Top Destination for Software Outsourcing | Proxy Soft",
        "meta_description": "Explore why Nepal is emerging as a premier software outsourcing destination — competitive talent, English proficiency, and a favourable time zone.",
    },
    {
        "title": "From Wireframe to Launch: Our 6-Step Web Development Process",
        "slug": "web-development-process-6-steps",
        "excerpt": (
            "Great websites don't happen by accident. Behind every fast, accessible, and "
            "conversion-optimised site is a disciplined process. Here's exactly how we take "
            "a project from the first conversation to a live, production-ready product."
        ),
        "content": """<h2>Why Process Matters</h2>
<p>We've seen what happens when web projects lack structure: scope creep, missed deadlines, unclear ownership, and products that don't match the original vision. Our 6-step process exists to prevent exactly that — giving clients full visibility at every stage while keeping our team aligned and moving fast.</p>

<h2>Step 1: Discovery & Requirements</h2>
<p>Every project starts with a structured kick-off: we map your business objectives, target audience, competitive landscape, and technical constraints. We use this phase to surface the questions that kill projects later — what does success look like? Who approves decisions? What integrations are non-negotiable?</p>
<p>Deliverable: a <strong>Project Brief</strong> document signed off by both parties.</p>

<h2>Step 2: Information Architecture & Wireframes</h2>
<p>Before a single pixel of design is committed, we map the site's structure, user flows, and content hierarchy. Low-fidelity wireframes let us move quickly and iterate without the cost of changing polished designs.</p>
<p>Deliverable: annotated wireframes in Figma, reviewed and approved by the client.</p>

<h2>Step 3: UI/UX Design</h2>
<p>With structure agreed, our designers bring the wireframes to life. We build a design system (colours, typography, spacing, component library) before designing individual pages — ensuring consistency and making handoff to development frictionless.</p>
<p>Deliverable: high-fidelity Figma prototype with a linked component library.</p>

<h2>Step 4: Development</h2>
<p>We work in two-week sprints, shipping working software at the end of each cycle. Our tech stack defaults — Django/Next.js for most web projects — are chosen for performance, developer productivity, and long-term maintainability, not trends.</p>
<p>Code review is mandatory. Every pull request is reviewed by a senior engineer before merging.</p>

<h2>Step 5: QA & Testing</h2>
<p>Testing isn't a phase at the end — it runs in parallel with development. We write unit and integration tests as we build, and run a dedicated QA cycle before launch covering:</p>
<ul>
  <li>Cross-browser and cross-device testing (Chrome, Firefox, Safari, Edge; iOS and Android)</li>
  <li>Performance profiling (Core Web Vitals, Lighthouse scores)</li>
  <li>Accessibility audit (WCAG 2.1 AA compliance)</li>
  <li>Security scan (OWASP Top 10 checklist)</li>
</ul>

<h2>Step 6: Launch & Handover</h2>
<p>Launch day isn't the end — it's a milestone. We deploy to production with a rollback plan ready, monitor error rates and performance for 48 hours post-launch, and then hand over full documentation: architecture overview, deployment guide, admin manual, and a recorded walkthrough for your team.</p>
<p>Post-launch support is available as a monthly retainer or on an ad-hoc basis.</p>

<h2>Ready to Start?</h2>
<p>If you'd like to discuss your next web project, <a href="/#contact">reach out here</a> — we'll schedule a free 30-minute discovery call to see if we're a good fit.</p>""",
        "is_published": True,
        "published_at": timezone.now(),
        "meta_title": "From Wireframe to Launch: Our 6-Step Process | Proxy Soft",
        "meta_description": "A detailed look at how Proxy Soft takes a web project from discovery through to a live, production-ready product in six structured steps.",
    },
]


# ─────────────────────────── command ──────────────────────────────────────────

class Command(BaseCommand):
    help = "Seed the site with realistic demo content for every section."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            default=False,
            help="Delete existing section data before seeding (default: skip if data exists).",
        )
        parser.add_argument(
            "--section",
            choices=SECTIONS + ["all"],
            default="all",
            help="Only seed a specific section (default: all).",
        )

    def handle(self, *args, **options):
        flush = options["flush"]
        section = options["section"]
        targets = SECTIONS if section == "all" else [section]

        self.stdout.write(self.style.MIGRATE_HEADING("\n  Proxy Soft — Content Seeder"))
        self.stdout.write(f"  Sections : {', '.join(targets)}")
        self.stdout.write(f"  Flush    : {flush}\n")

        config = SiteConfiguration.load()

        runners = {
            "config":       lambda: self._seed_config(config, flush),
            "services":     lambda: self._seed_services(config, flush),
            "corevalues":   lambda: self._seed_corevalues(config, flush),
            "techstack":    lambda: self._seed_techstack(config, flush),
            "projects":     lambda: self._seed_projects(config, flush),
            "testimonials": lambda: self._seed_testimonials(config, flush),
            "clients":      lambda: self._seed_clients(config, flush),
            "whychooseus":  lambda: self._seed_whychooseus(config, flush),
            "herobadges":   lambda: self._seed_herobadges(config, flush),
            "blog":         lambda: self._seed_blog(flush),
        }

        for name in targets:
            runners[name]()

        self.stdout.write(self.style.SUCCESS("\n  Done. Run the dev server and visit the homepage.\n"))

    # ── helpers ──────────────────────────────────────────────────────────────

    def _ok(self, label, count, action="created"):
        self.stdout.write(f"  {self.style.SUCCESS('✓')} {label:<22} {action} {count}")

    def _skip(self, label, count):
        self.stdout.write(f"  {self.style.WARNING('~')} {label:<22} skipped ({count} already exist)")

    # ── sections ─────────────────────────────────────────────────────────────

    def _seed_config(self, config, flush):
        label = "Site Config"
        # Config is a singleton — always update
        for field, value in SITE_CONFIG_DATA.items():
            setattr(config, field, value)
        config.save()
        self._ok(label, 1, "updated")

    def _seed_services(self, config, flush):
        label = "Services"
        qs = config.services.all()
        if qs.exists() and not flush:
            self._skip(label, qs.count())
            return
        if flush:
            deleted, _ = qs.delete()
        created = 0
        for data in SERVICES_DATA:
            Service.objects.create(site_config=config, **data)
            created += 1
        self._ok(label, created)

    def _seed_corevalues(self, config, flush):
        label = "Core Values"
        qs = config.core_values.all()
        if qs.exists() and not flush:
            self._skip(label, qs.count())
            return
        if flush:
            qs.delete()
        created = 0
        for data in CORE_VALUES_DATA:
            CoreValue.objects.create(site_config=config, **data)
            created += 1
        self._ok(label, created)

    def _seed_techstack(self, config, flush):
        label = "Tech Stack"
        qs = config.tech_stack_items.all()
        if qs.exists() and not flush:
            self._skip(label, qs.count())
            return
        if flush:
            qs.delete()
        created = 0
        for data in TECH_STACK_DATA:
            TechStackItem.objects.create(site_config=config, **data)
            created += 1
        self._ok(label, created)

    def _seed_projects(self, config, flush):
        label = "Projects"
        qs = config.projects.all()
        if qs.exists() and not flush:
            self._skip(label, qs.count())
            return
        if flush:
            qs.delete()
        created = 0
        for data in PROJECTS_DATA:
            Project.objects.create(site_config=config, **data)
            created += 1
        self._ok(label, created)

    def _seed_testimonials(self, config, flush):
        label = "Testimonials"
        qs = config.testimonials.all()
        if qs.exists() and not flush:
            self._skip(label, qs.count())
            return
        if flush:
            qs.delete()
        created = 0
        for data in TESTIMONIALS_DATA:
            Testimonial.objects.create(site_config=config, **data)
            created += 1
        self._ok(label, created)

    def _seed_clients(self, config, flush):
        label = "Clients"
        qs = config.clients.all()
        if qs.exists() and not flush:
            self._skip(label, qs.count())
            return
        if flush:
            qs.delete()
        created = 0
        for data in CLIENTS_DATA:
            Client.objects.create(site_config=config, **data)
            created += 1
        self._ok(label, created)

    def _seed_whychooseus(self, config, flush):
        label = "Why Choose Us"
        qs = config.why_items.all()
        if qs.exists() and not flush:
            self._skip(label, qs.count())
            return
        if flush:
            qs.delete()
        created = 0
        for data in WHY_CHOOSE_US_DATA:
            WhyChooseUsItem.objects.create(site_config=config, **data)
            created += 1
        self._ok(label, created)

    def _seed_herobadges(self, config, flush):
        label = "Hero Badges"
        qs = config.hero_badges.all()
        if qs.exists() and not flush:
            self._skip(label, qs.count())
            return
        if flush:
            qs.delete()
        created = 0
        for data in HERO_BADGES_DATA:
            HeroBadge.objects.create(site_config=config, **data)
            created += 1
        self._ok(label, created)

    def _seed_blog(self, flush):
        label = "Blog Posts"
        qs = BlogPost.objects.filter(slug__in=[p["slug"] for p in BLOG_POSTS_DATA])
        if qs.exists() and not flush:
            self._skip(label, qs.count())
            return
        if flush:
            qs.delete()

        # Use first superuser as author if available, otherwise None
        author = User.objects.filter(is_superuser=True).order_by("date_joined").first()
        if not author:
            author = User.objects.filter(is_staff=True).order_by("date_joined").first()

        created = 0
        for data in BLOG_POSTS_DATA:
            BlogPost.objects.create(author=author, **data)
            created += 1

        author_label = author.username if author else "no author (create a superuser)"
        self._ok(label, created, f"created  [author: {author_label}]")
