"""
Populate every section of the site with realistic demo content.

Usage
-----
  python manage.py seed_content            # insert (skip existing)
  python manage.py seed_content --flush    # wipe section data then re-seed
  python manage.py seed_content --section hero
  python manage.py seed_content --section services --flush

  # Production-safe: sync curated tech stack / Nepali testimonials & clients
  python manage.py seed_content --section techstack
  python manage.py seed_content --section testimonials
  python manage.py seed_content --section clients

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
    "stats_projects_completed": 15,
    "stats_happy_clients": 8,
    "stats_years_experience": 1,
    "stats_team_members": 6,
    "stats_client_satisfaction_rate": 98,
    "stats_awards_count": 3,
    # About
    "about_section_label": "About Proxy Soft",
    "about_section_heading": "Built for Real Work, Not Just Demos",
    "about_vision_quote": (
        "Proxy Soft designs and delivers custom digital products and automation — "
        "from focused tools for growing teams to enterprise-grade systems that run around the clock."
    ),
    "about_owner_name": "Shekhar Dhakal",
    "about_body": (
        "Established in 2026 and based in Nepal, we help businesses replace fragile, "
        "manual processes with software that is clear, reliable, and easy to own. "
        "Whether you need a custom-designed web or mobile experience, a workflow automation "
        "across your existing tools, or a full platform built for scale, we stay close "
        "from discovery through launch — with 24/7 support when something needs attention."
    ),
    "about_bullets": "Custom Design, Small to Enterprise Automation, 24/7 Support, Nepal-based Delivery",
    "about_core_values_heading": "What Guides Us",
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
        "Custom design and automation solutions for teams of every size — "
        "backed by responsive, 24/7 support."
    ),
    "establishment_year": "2026",
    "company_registration_number": "387235/82/83",
    "pan_number": "623565535",
    "footer_copyright": "Proxy Soft Pvt. Ltd. All Rights Reserved. | Designed for Global Growth.",
    "nav_get_started_text": "Get Started",
}

SERVICES_DATA = [
    {
        "order": 1,
        "title": "Web/App Development",
        "description": (
            "End-to-end product engineering across backend, frontend, mobile, and desktop — "
            "built to scale with your business and ship with confidence."
        ),
        "details": (
            "We design and build full-stack web and application products from discovery through launch "
            "and ongoing improvement.\n\n"
            "What we cover:\n"
            "• Backend APIs and business logic with Django, Node.js, and related frameworks\n"
            "• Modern frontend experiences with React, Next.js, and accessible UI patterns\n"
            "• Mobile apps for iOS and Android using Flutter and React Native\n"
            "• Desktop tooling when your workflow needs a native-feeling app\n\n"
            "You get clear milestones, maintainable code, and a product your team can grow without "
            "starting over every year."
        ),
        "icon_class": "fa-solid fa-laptop-code",
        "icon_style": "blue",
        "tags": "Backend, Frontend, Mobile, Desktop",
        "is_cta": False,
    },
    {
        "order": 2,
        "title": "Robotic Process Automation",
        "description": (
            "Automate repetitive work with agentic workflows, n8n, Robocorp, and Playwright — "
            "so your team spends time on decisions, not copy-paste."
        ),
        "details": (
            "We help you identify high-friction processes and replace them with reliable automation "
            "that fits the tools you already use.\n\n"
            "Typical outcomes:\n"
            "• Agentic assistants that gather context and complete multi-step tasks\n"
            "• n8n workflows that connect CRMs, emails, sheets, and internal APIs\n"
            "• Robocorp bots for structured back-office and ERP-style operations\n"
            "• Playwright-powered browser automation for portals that lack clean APIs\n\n"
            "We focus on auditability, error handling, and handoff documentation so automations "
            "stay trustworthy after go-live."
        ),
        "icon_class": "fa-solid fa-robot",
        "icon_style": "violet",
        "tags": "Agentic, n8n, Robocorp, Playwright",
        "is_cta": False,
    },
    {
        "order": 3,
        "title": "Project Outsourcing",
        "description": (
            "Extend your capacity with a dedicated Proxy Soft team — transparent communication, "
            "agile delivery, and ownership from kickoff to handoff."
        ),
        "details": (
            "When deadlines are tight or your in-house bench is full, we plug in as an extension of "
            "your product and engineering organization.\n\n"
            "Engagement models:\n"
            "• Dedicated squads for product builds and feature roadmaps\n"
            "• Staff augmentation for backend, frontend, QA, and DevOps roles\n"
            "• Fixed-scope delivery for MVPs, migrations, and internal tools\n\n"
            "You keep visibility through weekly demos, shared boards, and a single point of contact. "
            "We optimize for long-term maintainability — not short-term shortcuts."
        ),
        "icon_class": "fa-solid fa-people-group",
        "icon_style": "cyan",
        "tags": "Agile, Dedicated Team, Remote, Delivery",
        "is_cta": False,
    },
    {
        "order": 4,
        "title": "IT Consultation",
        "description": (
            "Practical technology guidance for architecture, cloud, security, and digital "
            "transformation — aligned to business outcomes, not buzzwords."
        ),
        "details": (
            "We partner with founders and IT leaders who need a clear path through complex "
            "technology decisions.\n\n"
            "How we help:\n"
            "• Architecture reviews and technology selection for new or existing products\n"
            "• Cloud readiness, cost control, and migration planning\n"
            "• Security and compliance baselines that match your risk profile\n"
            "• Roadmaps that balance quick wins with sustainable scale\n\n"
            "You leave with prioritized recommendations, estimated effort, and an implementation "
            "plan your team can execute — with or without us."
        ),
        "icon_class": "fa-solid fa-comments",
        "icon_style": "orange",
        "tags": "Strategy, Cloud, Security, Architecture",
        "is_cta": False,
    },
    {
        "order": 5,
        "title": "Need a Custom Solution?",
        "description": (
            "Have a unique workflow, industry constraint, or product idea that doesn’t fit a "
            "standard package? We’ll shape a tailored solution around your goals."
        ),
        "details": (
            "Not every challenge fits neatly into a catalog service — and that’s okay.\n\n"
            "Bring us problems like:\n"
            "• Integrating legacy systems with modern web or mobile fronts\n"
            "• Building internal platforms that connect sales, ops, and finance\n"
            "• Combining automation, AI agents, and custom software into one workflow\n"
            "• Rebuilding an aging product without disrupting day-to-day operations\n\n"
            "We start with a short discovery conversation, map constraints and success metrics, "
            "then propose a scoped approach with timeline and investment options."
        ),
        "icon_class": "fa-solid fa-lightbulb",
        "icon_style": "blue",
        "tags": "Discovery, Tailored Build, Partnership",
        "is_cta": True,
    },
]

CORE_VALUES_DATA = [
    {
        "order": 1,
        "title": "Custom by Default",
        "description": (
            "We don’t force your process into a template. We design interfaces and systems "
            "around how your people actually work."
        ),
    },
    {
        "order": 2,
        "title": "Automation That Scales",
        "description": (
            "From a single workflow for a small team to enterprise-grade automation across "
            "departments — we build solutions that grow with you."
        ),
    },
    {
        "order": 3,
        "title": "Support When You Need It",
        "description": (
            "Production systems don’t wait for office hours. Our team provides 24/7 support "
            "so issues are handled quickly and clearly."
        ),
    },
]

TECH_STACK_DATA = [
    # Combined core + automation — most used / popular only
    {"order": 1, "name": "Python", "icon_class": "fa-brands fa-python", "icon_style": "blue", "category": "core"},
    {"order": 2, "name": "Django", "icon_class": "fa-solid fa-d", "icon_style": "emerald", "category": "core"},
    {"order": 3, "name": "React", "icon_class": "fa-brands fa-react", "icon_style": "cyan", "category": "core"},
    {"order": 4, "name": "Node.js", "icon_class": "fa-brands fa-node-js", "icon_style": "emerald", "category": "core"},
    {"order": 5, "name": "PostgreSQL", "icon_class": "fa-solid fa-database", "icon_style": "blue", "category": "core"},
    {"order": 6, "name": "AWS", "icon_class": "fa-brands fa-aws", "icon_style": "orange", "category": "core"},
    {"order": 7, "name": "Docker", "icon_class": "fa-brands fa-docker", "icon_style": "cyan", "category": "core"},
    {"order": 8, "name": "TypeScript", "icon_class": "fa-solid fa-t", "icon_style": "blue", "category": "core"},
    {"order": 9, "name": "Playwright", "icon_class": "fa-solid fa-masks-theater", "icon_style": "emerald", "category": "core"},
    {"order": 10, "name": "Robocorp", "icon_class": "fa-solid fa-robot", "icon_style": "orange", "category": "core"},
    {"order": 11, "name": "n8n", "icon_class": "fa-solid fa-diagram-project", "icon_style": "violet", "category": "core"},
    {"order": 12, "name": "Selenium", "icon_class": "fa-solid fa-flask-vial", "icon_style": "cyan", "category": "core"},
]

# Names previously seeded / managed by this command (removed items get deleted on sync)
TECH_STACK_MANAGED_NAMES = {
    *(item["name"] for item in TECH_STACK_DATA),
    "Next.js",
    "Flutter",
    "Puppeteer",
    "Cypress",
    "Zapier",
    "Make",
    "Php",
    "PHP",
    "Laravel",
    "Tailwind",
    "Digital Ocean",
    "DigitalOcean",
}

PROJECTS_DATA = [
    {
        "order": 1,
        "category": "E-Commerce",
        "title": "Commerce Platform (React + FastAPI)",
        "description": (
            "A modern online storefront with a React storefront and FastAPI backend — "
            "product catalogs, cart and checkout, order tracking, and an admin panel "
            "built for day-to-day retail operations."
        ),
        "theme": "brand",
        "url": "",
    },
    {
        "order": 2,
        "category": "EdTech",
        "title": "School Management System",
        "description": (
            "An all-in-one school platform covering student attendance, billing, ledgers, "
            "fee schedules, academic records, and parent-facing updates — so offices spend "
            "less time on paperwork and more time with students."
        ),
        "theme": "emerald",
        "url": "",
    },
    {
        "order": 3,
        "category": "RPA / Automation",
        "title": "RPA Orchestration Platform",
        "description": (
            "A control center to monitor robotic process automation at scale — live bot "
            "activity, run history, log monitoring, and process records so teams can spot "
            "failures early and keep automations trustworthy."
        ),
        "theme": "violet",
        "url": "",
    },
    {
        "order": 4,
        "category": "Network Infrastructure",
        "title": "Enterprise Network Management",
        "description": (
            "Manage routers, switches, and firewalls from one place — network monitoring, "
            "VLAN configuration, MAC binding, and device health views built for IT teams "
            "that need clarity across the whole campus or office network."
        ),
        "theme": "orange",
        "url": "",
    },
    {
        "order": 5,
        "category": "Retail / POS",
        "title": "Inventory & Billing for Retail Shops",
        "description": (
            "A retail billing and stock system with VAT calculation, ledger entries, "
            "inventory tracking, and day-end billing — designed for shops that need "
            "accurate books without complicated enterprise software."
        ),
        "theme": "cyan",
        "url": "",
    },
]

TESTIMONIALS_DATA = [
    {
        "order": 1,
        "name": "Sandeep Shrestha",
        "role": "CTO, F1Soft International",
        "avatar": "SS",
        "color": "from-brand-400 to-brand-700",
        "quote": (
            "Proxy Soft rebuilt our payment dashboard from the ground up. "
            "The new platform handles peak festival traffic without a hitch, and our ops team finally has the visibility they needed. "
            "A reliable engineering partner for Nepal's fintech space."
        ),
    },
    {
        "order": 2,
        "name": "Anjali Thapa",
        "role": "Product Manager, LogPoint",
        "avatar": "AT",
        "color": "from-emerald-400 to-teal-700",
        "quote": (
            "Their automation work with Playwright and n8n cut our regression cycle from days to hours. "
            "Clear communication, solid documentation, and delivery that matched what we scoped. "
            "We continue to bring them in for critical releases."
        ),
    },
    {
        "order": 3,
        "name": "Binod Tamang",
        "role": "Founder & CEO, Deerhold",
        "avatar": "BT",
        "color": "from-violet-400 to-purple-700",
        "quote": (
            "We needed a scalable web product for our US clients without growing a huge in-house team. "
            "Proxy Soft plugged in as an extension of our engineering org — quality code, weekly demos, and zero drama. "
            "Exactly the outsourcing experience we wanted from Nepal."
        ),
    },
    {
        "order": 4,
        "name": "Pratima Adhikari",
        "role": "Head of Digital, Nabil Bank",
        "avatar": "PA",
        "color": "from-orange-400 to-red-600",
        "quote": (
            "The cloud migration and Django rewrite were handled with care around compliance and uptime. "
            "Zero unplanned downtime during cutover, and our internal teams were trained properly. "
            "Proxy Soft understands both enterprise constraints and modern delivery."
        ),
    },
]

CLIENTS_DATA = [
    {"order": 1, "name": "F1Soft International", "url": ""},
    {"order": 2, "name": "LogPoint", "url": ""},
    {"order": 3, "name": "Deerhold", "url": ""},
    {"order": 4, "name": "Nabil Bank", "url": ""},
    {"order": 5, "name": "Fusemachines", "url": ""},
    {"order": 6, "name": "CloudFactory", "url": ""},
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
        "title": "Building Reliable Digital Products with Django, Modern Frontends, and Practical Automation",
        "slug": "django-tech-stack-digital-products-automation-proxy-soft",
        "excerpt": (
            "A practical look at how Proxy Soft designs and ships software — from Django and "
            "PostgreSQL backends to React interfaces and automation with n8n, Robocorp, and "
            "Playwright — so teams get systems they can trust and grow."
        ),
        "content": """<p>Most software projects don’t fail because a framework is “wrong.” They fail because the stack, the process, and the business problem never line up. At Proxy Soft, we treat technology as a set of tools with jobs to do — not as a badge of modernity. That is why our day-to-day work sits on a familiar, battle-tested foundation: <strong>Python and Django</strong> for durable backends, <strong>React and TypeScript</strong> for clear interfaces, <strong>PostgreSQL</strong> for data that must stay consistent, and a practical automation layer with <strong>n8n, Robocorp, Playwright, and Selenium</strong> when people should not be doing the same click-and-copy work twice.</p>

<p>This article is a longer walk through that approach. If you are a founder, product owner, or IT lead evaluating a custom build, a rewrite, or an outsourcing partnership, it should give you a concrete sense of how we think — and what you can expect when you work with us.</p>

<h2>What “product and solution” really means for us</h2>
<p>Proxy Soft is a Nepal-based team that helps organizations replace fragile manual processes with software that is clear, reliable, and easy to own. Our services are deliberately broad enough to cover a full journey, but focused enough that we do not pretend every engagement is the same:</p>
<ul>
  <li><strong>Web and app development</strong> — backend APIs, modern frontends, mobile and desktop when the workflow needs them</li>
  <li><strong>Robotic process automation</strong> — agentic workflows, n8n integrations, Robocorp bots, and browser automation with Playwright</li>
  <li><strong>Project outsourcing</strong> — dedicated squads or staff augmentation with transparent communication and agile delivery</li>
  <li><strong>IT consultation</strong> — architecture, cloud, security, and roadmaps tied to business outcomes</li>
</ul>
<p>Underneath those offerings is one preference: ship something maintainable. Fancy demos that nobody can operate six months later are not a win. Documentation, error handling, and a stack your team can hire for matter as much as the first release.</p>

<h2>Why Django still earns its place in 2026</h2>
<p>Django is not new, and that is part of the point. When you need authentication, admin tooling, forms, permissions, migrations, and a clear project structure, Django gives you a coherent default instead of a shopping cart of packages glued together late at night.</p>

<p>We reach for Django when clients need:</p>
<ul>
  <li>Business logic that will grow beyond a simple CRUD prototype</li>
  <li>Admin surfaces that non-engineers can use without a separate “ops app”</li>
  <li>Security-conscious defaults for sessions, CSRF protection, and password handling</li>
  <li>A codebase that mid-level engineers can read without a two-week archaeology project</li>
</ul>

<p>Python sits beside Django for good reason. Data work, automation scripts, API clients, and machine-assisted workflows all speak the same language. That reduces handoffs between “the web team” and “the automation team,” which is often where projects quietly leak time.</p>

<h3>What Django is not for</h3>
<p>We are honest about boundaries. If you only need a marketing brochure with almost no backend logic, a lighter CMS or static site may be enough. If you need ultra-specialized real-time event streaming at massive scale from day one, we may layer Node.js services or dedicated workers beside a Django core rather than forcing every concern into one process. The goal is fit, not ideology.</p>

<h2>The frontend people actually use: React and TypeScript</h2>
<p>A strong backend without a usable interface is unfinished work. We build modern frontend experiences with <strong>React</strong>, and we prefer <strong>TypeScript</strong> when the UI has enough moving parts that plain JavaScript starts to hide bugs until production.</p>

<p>In practice that means:</p>
<ul>
  <li>Component patterns that stay consistent across pages</li>
  <li>Accessible forms and navigation, not only polished visuals</li>
  <li>Clear contracts between API responses and UI state</li>
  <li>Performance habits that respect Core Web Vitals instead of shipping megabytes of unused script</li>
</ul>

<p><strong>Node.js</strong> shows up when we need API gateways, realtime helpers, build tooling, or services that sit comfortably in the JavaScript ecosystem. We do not force every backend into Node, and we do not force every UI into React. We choose what your team can support after we leave.</p>

<h2>PostgreSQL: the quiet hero of reliable products</h2>
<p>If Django is the application spine, <strong>PostgreSQL</strong> is often the memory that keeps the business honest. Relational integrity, transactions, and mature tooling beat “we’ll fix the data later” almost every time for operational systems.</p>

<p>We design schemas with growth in mind: indexing for the queries you will actually run, constraints that prevent invalid states, and migrations that can be reviewed like any other change. Fancy database choices are interesting. Predictable backups and restore drills are what save weekends.</p>

<h2>Shipping and running it: Docker and AWS</h2>
<p>Code that only works on one laptop is not a product. We containerize with <strong>Docker</strong> so environments stay closer between development, staging, and production. On the cloud side, <strong>AWS</strong> is a common home for our clients — compute, managed databases, object storage, networking, and monitoring — but we size resources to the workload instead of copying a generic enterprise diagram.</p>

<p>Consultation engagements often start here: what do you already run, what is overbuilt, what is under-observed, and what would a sensible next six months look like? Cost control and security baselines are part of that conversation, not an afterthought sold as a separate package.</p>

<h2>Automation that respects how people work</h2>
<p>Custom software is not the only lever. Many organizations already have CRMs, spreadsheets, email inboxes, ERP screens, and partner portals. Connecting those systems — or automating the boring path between them — can unlock more value than a brand-new app.</p>

<p>Our automation toolkit is intentional:</p>
<ul>
  <li><strong>n8n</strong> for visual, maintainable workflows that connect APIs, email, sheets, and internal services</li>
  <li><strong>Robocorp</strong> for structured back-office and ERP-style bots where reliability and audit trails matter</li>
  <li><strong>Playwright</strong> for modern browser automation when a portal has no clean API</li>
  <li><strong>Selenium</strong> when existing suites or legacy environments still need browser coverage</li>
</ul>

<p>We care about failure modes. Automations should retry thoughtfully, log clearly, and escalate to a human when something looks wrong. A silent bot that “usually works” is a liability wearing a productivity costume.</p>

<h2>How these pieces become solutions, not a pile of tools</h2>
<p>Here is a simplified picture of how engagements often land:</p>

<h3>1. Custom web platforms and internal tools</h3>
<p>Django + PostgreSQL power the domain logic. React + TypeScript deliver the day-to-day interface. Docker packages the app. AWS hosts it with monitoring and backups. The result might be a client portal, an operations dashboard, a content-backed marketing site with a real admin, or a multi-tenant SaaS MVP.</p>

<h3>2. Process automation beside the product</h3>
<p>Once the system of record exists, n8n and Robocorp can move data between tools, generate documents, sync statuses, or prepare reports. Playwright steps in when a third-party website is the only interface available. The product and the automation reinforce each other instead of competing.</p>

<h3>3. Outsourcing and dedicated delivery</h3>
<p>Some clients do not need advice about frameworks; they need capacity. We plug in as a dedicated squad or as staff augmentation for backend, frontend, QA, and DevOps roles. You keep visibility through shared boards, demos, and a clear point of contact. The same stack preferences apply: maintainability over clever shortcuts.</p>

<h3>4. Consultation before a big bet</h3>
<p>If you are mid-rewrite, mid-migration, or unsure whether to automate or rebuild, we help you choose. Architecture reviews, cloud readiness, security baselines, and prioritized roadmaps are useful precisely because they reduce expensive thrash later.</p>

<h2>A human process, not a slide deck</h2>
<p>Tools do not replace conversation. Our delivery rhythm is deliberately plain:</p>
<ol>
  <li><strong>Discovery</strong> — goals, constraints, success metrics, and what “done” should feel like</li>
  <li><strong>Architecture and stack fit</strong> — what to build, what to integrate, what to automate</li>
  <li><strong>Iterative delivery</strong> — working software in short cycles, not a big reveal after months of silence</li>
  <li><strong>Hardening</strong> — tests, accessibility, performance, and security checks that match the risk</li>
  <li><strong>Launch and ownership</strong> — documentation, handoff, and support options including responsive help when production needs attention</li>
</ol>
<p>We are Nepal-based and oriented toward international collaboration. That means overlapping hours where they help, async updates where they do not, and communication habits that treat your product as shared work — not a black box.</p>

<h2>SEO and content systems: why the stack matters beyond “features”</h2>
<p>Many of our clients care about discoverability as much as functionality. A Django-backed site can own clean URLs, structured metadata, sitemaps, and editorial workflows without bolting five plugins onto a fragile theme. Pair that with a fast React experience where interactivity is needed, and you get pages that are both useful to humans and understandable to search engines.</p>
<p>The same discipline applies to blog and knowledge content: clear titles, honest excerpts, readable headings, and internal links to services and contact paths. This article itself is written that way on purpose.</p>

<h2>Common questions we hear</h2>
<h3>Can you work with an existing codebase?</h3>
<p>Yes. Many projects start with a review of what you already have. Sometimes the right move is a careful Django upgrade and cleanup. Sometimes it is extracting an automation layer before touching the core app. We prefer evidence over a rewrite-for-rewrite’s-sake.</p>

<h3>Do you only use Django?</h3>
<p>No. Django is a strong default for many product backends, but Node.js, React, Flutter or React Native for mobile, and automation-first stacks are all in play depending on the problem. The homepage tech stack you see — Python, Django, React, Node.js, PostgreSQL, AWS, Docker, TypeScript, Playwright, Robocorp, n8n, Selenium — is a map of what we use most often, not a prison.</p>

<h3>How do you handle support after launch?</h3>
<p>Production systems do not wait for office hours. We offer support models that match how critical the system is, with clear escalation paths so issues are handled quickly and documented.</p>

<h2>When you should talk to us</h2>
<p>Reach out if any of these sound familiar:</p>
<ul>
  <li>You need a custom web or mobile product and want a team that will still care about the code next year</li>
  <li>Your staff are drowning in repetitive portal work that could be automated safely</li>
  <li>You want an outsourcing partner who communicates like a teammate, not a ticket queue</li>
  <li>You need architecture or cloud advice before committing budget to a rewrite</li>
</ul>
<p>We are glad to start with a short discovery conversation, map constraints and success metrics, then propose a scoped approach with timeline and investment options.</p>

<h2>Closing thought</h2>
<p>Technology choices are easy to romanticize and hard to live with. Django, React, PostgreSQL, Docker, AWS, and a thoughtful automation layer have earned their place in our work because they help real teams ship, sleep, and iterate. If that is the kind of partnership you want, <a href="/#contact">contact Proxy Soft</a> and tell us what you are trying to make more reliable.</p>""",
        "is_published": True,
        "published_at": timezone.now() - timezone.timedelta(days=35),
        "meta_title": "Django Tech Stack & Digital Solutions | Proxy Soft",
        "meta_description": "How Proxy Soft builds digital products with Django, React, PostgreSQL, AWS, and automation using n8n, Robocorp, and Playwright — practical, maintainable solutions.",
    },
    {
        "title": "When to Choose Django for Your Next Web Product (And When Not To)",
        "slug": "when-to-choose-django-for-web-product",
        "excerpt": (
            "Django is powerful, but it is not magic for every brief. Here is how Proxy Soft "
            "decides when Django is the right backbone for a product — and when a lighter or "
            "different approach will serve you better."
        ),
        "content": """<p>Choosing a backend framework can feel like picking a personality for your company. Teams argue about speed, “modern stacks,” and what looks impressive on a hiring post. At Proxy Soft we try to ask a quieter question first: <strong>what must this system still be able to do in eighteen months?</strong></p>

<p><strong>Django</strong> is often our answer for serious web products — not because it is trendy, but because it is coherent. Authentication, admin, forms, migrations, permissions, and a clear project layout arrive as a shared language instead of a pile of disconnected packages.</p>

<h2>Django is a strong fit when…</h2>
<ul>
  <li>You need a real domain model (users, roles, workflows, approvals) that will keep growing</li>
  <li>Non-engineers must manage content or operations through an admin without a second custom CMS</li>
  <li>Security defaults matter: sessions, CSRF protection, password hashing, and predictable permission checks</li>
  <li>You want Python continuity for APIs, scripts, reporting, and later automation work</li>
  <li>You expect multiple developers to join the codebase and understand it without tribal folklore</li>
</ul>

<p>In those cases we typically pair Django with <strong>PostgreSQL</strong>, containerize with <strong>Docker</strong>, and host on <strong>AWS</strong> with monitoring and backups that match the risk of the product.</p>

<h2>Consider something else when…</h2>
<ul>
  <li>The site is mostly static marketing pages with almost no business logic</li>
  <li>You need an ultra-specialized realtime service that is cleaner as a focused Node.js worker beside a smaller core</li>
  <li>The primary problem is integration between existing tools, not a new system of record — automation with n8n or Robocorp may come first</li>
</ul>

<h2>How we decide with clients</h2>
<p>We start with discovery: users, constraints, compliance, integrations, and what “done” means. Then we propose a stack that your team can hire for and maintain. Sometimes that is Django + React. Sometimes it is Django for the core and Node.js for a narrow service. Sometimes it is automation first, product second.</p>

<p>If you are weighing a rewrite or a greenfield build, <a href="/#contact">talk to Proxy Soft</a>. We would rather help you choose the boring right option than sell you the exciting wrong one.</p>""",
        "is_published": True,
        "published_at": timezone.now() - timezone.timedelta(days=28),
        "meta_title": "When to Choose Django for Your Web Product | Proxy Soft",
        "meta_description": "Practical guidance from Proxy Soft on when Django is the right backend for a web product — and when a lighter or automation-first approach is smarter.",
    },
    {
        "title": "React and TypeScript Frontends That Stay Maintainable",
        "slug": "react-typescript-maintainable-frontends",
        "excerpt": (
            "Pretty interfaces age badly when the component tree becomes a maze. Learn how "
            "Proxy Soft builds React and TypeScript frontends that stay clear, accessible, "
            "and connected cleanly to Django APIs."
        ),
        "content": """<p>A backend can be perfect and still feel broken if the interface fights the people using it. That is why our product work treats the frontend as part of the solution — not a coat of paint applied at the end.</p>

<p>At Proxy Soft we build many client-facing and internal interfaces with <strong>React</strong>, and we reach for <strong>TypeScript</strong> when the UI has enough state and API surface that plain JavaScript starts hiding bugs until a user finds them.</p>

<h2>What “maintainable” looks like in practice</h2>
<ul>
  <li><strong>Consistent components</strong> — buttons, forms, tables, and empty states behave the same across pages</li>
  <li><strong>Typed contracts</strong> — API responses and UI models stay aligned so refactors do not become archaeology</li>
  <li><strong>Accessible defaults</strong> — keyboard flows, labels, contrast, and focus states are not optional polish</li>
  <li><strong>Performance habits</strong> — ship what the page needs; respect Core Web Vitals instead of bundling everything “just in case”</li>
</ul>

<h2>Working with Django backends</h2>
<p>Most of our React apps talk to Django (or Django REST-style APIs) as the system of record. That split keeps business rules close to the data while letting the UI iterate quickly. We document endpoints, error shapes, and auth expectations so frontend and backend work does not drift into conflicting assumptions.</p>

<p><strong>Node.js</strong> still appears where it earns its keep: build tooling, lightweight gateways, or realtime helpers. We do not force every concern into React or every API into Node.</p>

<h2>Mobile and beyond</h2>
<p>When the workflow needs pockets and offline moments, we extend into mobile with approaches like Flutter or React Native — chosen for the product, not for a portfolio checklist. The principle stays the same: clear ownership, readable code, and a handoff your team can live with.</p>

<p>Need a frontend partner who will still care about the component library next year? <a href="/#contact">Start a conversation with Proxy Soft</a>.</p>""",
        "is_published": True,
        "published_at": timezone.now() - timezone.timedelta(days=21),
        "meta_title": "Maintainable React & TypeScript Frontends | Proxy Soft",
        "meta_description": "How Proxy Soft designs React and TypeScript frontends that stay accessible, performant, and cleanly integrated with Django-powered products.",
    },
    {
        "title": "Practical RPA: n8n, Robocorp, and Playwright Without the Hype",
        "slug": "practical-rpa-n8n-robocorp-playwright",
        "excerpt": (
            "Automation should save hours, not create a second job babysitting bots. "
            "Here is how Proxy Soft uses n8n, Robocorp, Playwright, and Selenium to "
            "automate real work with audit trails and human fallbacks."
        ),
        "content": """<p>Every company has a process that looks harmless on a whiteboard and expensive in real life: copy from portal A, paste into spreadsheet B, upload to system C, then ping someone on Slack. Robotic process automation is useful when it removes that grind without inventing a fragile robot that only one contractor understands.</p>

<p>Proxy Soft’s automation work is deliberately practical. We match the tool to the problem:</p>
<ul>
  <li><strong>n8n</strong> — visual workflows that connect CRMs, email, sheets, webhooks, and internal APIs</li>
  <li><strong>Robocorp</strong> — structured bots for back-office and ERP-style operations where reliability matters</li>
  <li><strong>Playwright</strong> — modern browser automation when a partner portal has no usable API</li>
  <li><strong>Selenium</strong> — coverage for legacy suites and environments that still depend on it</li>
</ul>

<h2>What we optimize for</h2>
<p>Speed demos are easy. Trust is harder. We design automations with:</p>
<ol>
  <li>Clear inputs and outputs so failures are obvious</li>
  <li>Retries that are thoughtful instead of infinite</li>
  <li>Logs someone can read during an incident</li>
  <li>Escalation to a human when data looks wrong</li>
  <li>Documentation so the bot is not tribal knowledge</li>
</ol>

<h2>Automation beside custom software</h2>
<p>Often the best answer is both: a Django or Node-backed system of record, plus n8n/Robocorp flows that move status, documents, and notifications between tools your team already uses. That combination tends to beat “rip everything out and rebuild” for mid-sized operations teams.</p>

<h2>A simple discovery checklist</h2>
<ul>
  <li>How often does the process run, and what is the cost of a mistake?</li>
  <li>Is there an API, or only a browser UI?</li>
  <li>Who owns the process after go-live?</li>
  <li>What should happen when the third-party site changes overnight?</li>
</ul>

<p>If your team is drowning in repetitive portal work, <a href="/#contact">tell us about the workflow</a>. We will help you decide what to automate, what to rebuild, and what to leave alone.</p>""",
        "is_published": True,
        "published_at": timezone.now() - timezone.timedelta(days=14),
        "meta_title": "Practical RPA with n8n, Robocorp & Playwright | Proxy Soft",
        "meta_description": "Proxy Soft’s practical approach to RPA using n8n, Robocorp, Playwright, and Selenium — reliable automation with logs, retries, and human fallbacks.",
    },
    {
        "title": "Project Outsourcing That Feels Like an Extension of Your Team",
        "slug": "project-outsourcing-dedicated-team-proxy-soft",
        "excerpt": (
            "Outsourcing fails when communication becomes a ticket queue. See how Proxy Soft "
            "runs dedicated squads and staff augmentation with agile delivery, shared boards, "
            "and ownership from kickoff to handoff."
        ),
        "content": """<p>“Outsourcing” has earned a mixed reputation — sometimes deserved. Black-box vendors, timezone silence, and surprise rewrites can make leaders swear they will never try again. Our view at Proxy Soft is simpler: <strong>remote delivery works when it behaves like teamwork</strong>.</p>

<h2>Engagement models we offer</h2>
<ul>
  <li><strong>Dedicated squads</strong> for product builds and feature roadmaps</li>
  <li><strong>Staff augmentation</strong> for backend, frontend, QA, and DevOps roles</li>
  <li><strong>Fixed-scope delivery</strong> for MVPs, migrations, and internal tools</li>
</ul>

<p>You keep visibility through weekly demos, shared boards, and a single point of contact. We optimize for long-term maintainability — not short-term shortcuts that look fast in month one and expensive in month six.</p>

<h2>How we collaborate day to day</h2>
<p>We are Nepal-based and oriented toward international clients. That means overlapping hours where they help, async updates where they do not, and habits that make progress inspectable: pull requests, written decisions, and demos of working software.</p>

<p>Technically, outsourcing engagements still sit on the same stack preferences you see across our work — Django and Python for durable backends, React and TypeScript for interfaces, PostgreSQL for data integrity, Docker and AWS for deployable environments, plus automation tools when process work should not stay manual.</p>

<h2>What good handoff looks like</h2>
<p>When a phase ends, you should own more than a zip file. Architecture notes, environment setup, admin guides, and a clear map of what is automated versus what is custom code are part of delivery. If you want us to stay for support, we can. If you want your internal team to take over, we plan for that from the start.</p>

<p>If your roadmap is full and your bench is not, <a href="/#contact">explore an outsourcing partnership with Proxy Soft</a>.</p>""",
        "is_published": True,
        "published_at": timezone.now() - timezone.timedelta(days=7),
        "meta_title": "Software Project Outsourcing & Dedicated Teams | Proxy Soft",
        "meta_description": "How Proxy Soft delivers project outsourcing with dedicated squads, staff augmentation, agile demos, and maintainable Django and React codebases.",
    },
    {
        "title": "IT Consultation That Prioritizes Outcomes Over Buzzwords",
        "slug": "it-consultation-architecture-cloud-security",
        "excerpt": (
            "Need clarity before a rewrite, cloud move, or security push? Proxy Soft’s "
            "IT consultation pairs architecture reviews with practical roadmaps — cloud, "
            "cost, and risk included — so you invest with eyes open."
        ),
        "content": """<p>Technology advice is cheap when it is vague. “Move to the cloud,” “add AI,” and “microservices everything” sound decisive in a meeting and expensive in a budget. Proxy Soft’s consultation work is built for founders and IT leaders who need a path they can execute — with or without us building the whole thing.</p>

<h2>Where we typically help</h2>
<ul>
  <li><strong>Architecture reviews</strong> for new products or aging systems that feel brittle</li>
  <li><strong>Technology selection</strong> — when Django, Node.js, React, or an automation-first approach is the better bet</li>
  <li><strong>Cloud readiness and cost control</strong> on platforms like AWS</li>
  <li><strong>Security and compliance baselines</strong> matched to your actual risk, not a generic checklist printout</li>
  <li><strong>Roadmaps</strong> that balance quick wins with sustainable scale</li>
</ul>

<h2>What you leave with</h2>
<p>A useful consultation ends with prioritized recommendations, estimated effort, and an implementation sequence. Sometimes that means stabilize PostgreSQL backups before rewriting the UI. Sometimes it means extract an n8n workflow before touching the monolith. Sometimes it means Dockerize what you have so staging stops lying to you.</p>

<h2>Consultation into delivery</h2>
<p>Many clients start with advice and continue into build: web/app development, RPA, or a dedicated outsourcing squad. That continuity helps because the people who mapped the constraints are not strangers to the people writing the code. Still, you are never locked in — the point of good consultation is optionality.</p>

<p>If you are mid-decision on a rewrite, migration, or automation program, <a href="/#contact">book a discovery conversation</a>. We will help you spend the next quarter on the work that actually moves the business.</p>""",
        "is_published": True,
        "published_at": timezone.now() - timezone.timedelta(days=2),
        "meta_title": "IT Consultation: Architecture, Cloud & Security | Proxy Soft",
        "meta_description": "Outcome-focused IT consultation from Proxy Soft — architecture reviews, AWS cloud guidance, security baselines, and roadmaps you can actually execute.",
    },
]

# Previous blog slugs managed by this seeder (removed on sync)
BLOG_MANAGED_SLUGS = {
    *(p["slug"] for p in BLOG_POSTS_DATA),
    "cut-cloud-costs-retail-client",
    "nepal-software-outsourcing-destination",
    "web-development-process-6-steps",
}



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
        """
        Sync curated tech stack (core + popular automation in one list).
        Production-safe without --flush: upserts seed items and removes
        obsolete managed names; keeps unknown custom admin-added items.
        """
        label = "Tech Stack"
        seed_names = {item["name"] for item in TECH_STACK_DATA}
        qs = config.tech_stack_items.all()

        if flush:
            qs.delete()

        created = 0
        updated = 0
        for data in TECH_STACK_DATA:
            payload = {**data}
            name = payload.pop("name")
            obj, was_created = TechStackItem.objects.update_or_create(
                site_config=config,
                name=name,
                defaults=payload,
            )
            if was_created:
                created += 1
            else:
                updated += 1

        # Drop old managed items no longer in the curated popular list
        removed, _ = (
            config.tech_stack_items.filter(name__in=TECH_STACK_MANAGED_NAMES)
            .exclude(name__in=seed_names)
            .delete()
        )

        if created:
            self._ok(label, created, "created")
        if updated:
            self._ok(label, updated, "updated")
        if removed:
            self._ok(label, removed, "removed")
        if not created and not updated and not removed:
            self._skip(label, qs.count())

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
        """Upsert testimonials by name so production can refresh Nepali reviews safely."""
        label = "Testimonials"
        qs = config.testimonials.all()
        seed_names = {item["name"] for item in TESTIMONIALS_DATA}
        managed_names = seed_names | {
            "Sarah Johnson",
            "Marcus Chen",
            "Amelia Rodriguez",
            "David Kim",
        }

        if flush:
            qs.delete()

        created = 0
        updated = 0
        for data in TESTIMONIALS_DATA:
            payload = {**data}
            name = payload.pop("name")
            obj, was_created = Testimonial.objects.update_or_create(
                site_config=config,
                name=name,
                defaults=payload,
            )
            if was_created:
                created += 1
            else:
                updated += 1

        removed, _ = (
            config.testimonials.filter(name__in=managed_names)
            .exclude(name__in=seed_names)
            .delete()
        )

        if created:
            self._ok(label, created, "created")
        if updated:
            self._ok(label, updated, "updated")
        if removed:
            self._ok(label, removed, "removed")
        if not created and not updated and not removed:
            self._skip(label, qs.count())

    def _seed_clients(self, config, flush):
        """Upsert clients by name for production-safe Nepal company list."""
        label = "Clients"
        qs = config.clients.all()
        seed_names = {item["name"] for item in CLIENTS_DATA}
        managed_names = seed_names | {
            "TechVenture Inc.",
            "FinanceFlow GmbH",
            "StyleCraft",
            "RetailMax Asia",
            "TalentBridge",
            "GreenLeaf AU",
        }

        if flush:
            qs.delete()

        created = 0
        updated = 0
        for data in CLIENTS_DATA:
            payload = {**data}
            name = payload.pop("name")
            obj, was_created = Client.objects.update_or_create(
                site_config=config,
                name=name,
                defaults=payload,
            )
            if was_created:
                created += 1
            else:
                updated += 1

        removed, _ = (
            config.clients.filter(name__in=managed_names)
            .exclude(name__in=seed_names)
            .delete()
        )

        if created:
            self._ok(label, created, "created")
        if updated:
            self._ok(label, updated, "updated")
        if removed:
            self._ok(label, removed, "removed")
        if not created and not updated and not removed:
            self._skip(label, qs.count())

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
        managed_qs = BlogPost.objects.filter(slug__in=BLOG_MANAGED_SLUGS)
        if flush:
            managed_qs.delete()
        else:
            # Always remove obsolete managed posts so old seed articles disappear
            obsolete = BLOG_MANAGED_SLUGS - {p["slug"] for p in BLOG_POSTS_DATA}
            if obsolete:
                BlogPost.objects.filter(slug__in=obsolete).delete()

        author = User.objects.filter(is_superuser=True).order_by("date_joined").first()
        if not author:
            author = User.objects.filter(is_staff=True).order_by("date_joined").first()

        created = 0
        updated = 0
        for data in BLOG_POSTS_DATA:
            obj, was_created = BlogPost.objects.update_or_create(
                slug=data["slug"],
                defaults={**data, "author": author},
            )
            if was_created:
                created += 1
            else:
                updated += 1

        author_label = author.username if author else "no author (create a superuser)"
        self._ok(label, created + updated, f"created={created} updated={updated}  [author: {author_label}]")
