# Proxy Soft – Django Site

Dynamic, responsive company website powered by Django with an admin dashboard to manage all content.

## Project structure

- **`config/`** – Django configuration
  - **`config/settings/`** – `base.py`, `development.py`, `production.py` (env-based)
- **`apps/`** – Django apps
  - **`apps/core/`** – Site content: `SiteConfiguration` (singleton), Services, Testimonials, Clients, etc.
- **`templates/`** – Base templates (e.g. `index.html`)
- **`static/`** – Static assets (CSS, JS, images)
- **`media/`** – User-uploaded files (logos, client images)

## Setup

### 1. Environment

```bash
# Copy env example and edit if needed
copy .env.example .env

# Install dependencies (use a venv in production)
pip install -r requirements.txt
```

### 2. Database

- **Local:** SQLite (default). No extra DB config.
- **Production:** Set `DJANGO_ENV=production` and in `.env` set:
  - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 3. Run

```bash
python manage.py runserver
```

- Site: http://127.0.0.1:8000/
- **Admin dashboard:** http://127.0.0.1:8000/iamadmin/ (login with the superuser username and password)

The default Django admin at `/admin/` is disabled. All content is managed from **/iamadmin/**.

## IAM Admin dashboard (/iamadmin)

Log in with **username** and **password** (the superuser you created). The dashboard includes:

- **Overview** – stats and recent contact submissions
- **Site Config** – edit the singleton site configuration (SEO, contact, hero, about, footer, etc.)
- **Services** – add/edit/delete services
- **Clients** – add/edit/delete clients
- **Core Values** – add/edit/delete about section core values
- **Testimonials** – add/edit/delete testimonial quotes
- **Tech Stack** – add/edit/delete tech stack items
- **Submissions** – view and delete contact form submissions
- **My Profile** – set your full name (displayed in the header instead of first/last name)

User display name uses **full name** from **My Profile** (apps.accounts.UserProfile). If not set, the username is shown.

## Admin – dynamic content (via /iamadmin)

From **IAM Admin** you can edit:

- **Branding:** site name, tagline, logo  
- **SEO:** meta title, description, keywords, OG image  
- **Contact:** address, email, phone  
- **Social:** Facebook, LinkedIn, Twitter, Instagram URLs  
- **Hero:** badge, title, description, image, CTAs, stat  
- **About:** vision quote, owner name, body, bullets, core values (inline)  
- **Services section:** heading + inline Services (title, description, icon)  
- **Tech stack section:** heading + inline Tech stack items  
- **Testimonials:** inline quotes  
- **Clients:** inline clients (name, logo, link)  
- **Contact:** heading, intro, subject dropdown options  
- **Footer:** tagline, year, compliance, copyright  

Contact form submissions are stored and listed under **Contact submissions**.

## Production checklist

- Set `DJANGO_ENV=production`.
- In `.env`: strong `SECRET_KEY`, `ALLOWED_HOSTS`, MySQL `DB_*` variables.
- Run `python manage.py collectstatic` and serve static/media with your web server (e.g. Nginx) or WhiteNoise.
- Use HTTPS and consider `SECURE_SSL_REDIRECT=True` in production settings.
