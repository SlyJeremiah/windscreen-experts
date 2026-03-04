# Windscreen Experts – Django Web Application

## Tech Stack
| Category | Technology |
|---|---|
| Backend | Django 4.2 |
| Database | PostgreSQL (dj-database-url) |
| Frontend | Bootstrap 5 + Bootstrap Icons |
| Hosting | Vercel |
| Storage | Backblaze B2 (django-storages + boto3) |
| Email | Gmail SMTP |
| Analytics | Google Analytics 4 |

---

## Project Structure
```
windscreen_experts/
├── apps/
│   ├── core/           # Home, About, Contact, Admin Panel views
│   ├── bookings/       # Booking form + model
│   ├── gallery/        # Before/after gallery
│   ├── services/       # Services & pricing
│   └── inquiries/      # Contact inquiries
├── templates/
│   ├── base.html       # Public base (navbar, footer)
│   ├── core/           # Home, About, Contact
│   ├── bookings/
│   ├── gallery/
│   ├── services/
│   ├── inquiries/
│   └── admin_panel/    # Custom admin dashboard
├── static/
├── windscreen_experts/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
├── vercel.json
└── build_files.sh
```

---

## Local Setup

### 1. Clone and create virtual environment
```bash
git clone https://github.com/your-org/windscreen-experts.git
cd windscreen_experts
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env with your values
```

Add to `windscreen_experts/settings.py` top (or use python-dotenv):
```python
from dotenv import load_dotenv
load_dotenv()
```

### 4. Run migrations and create superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Load initial data (optional)
```bash
python manage.py loaddata initial_services.json
```

### 6. Run development server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000  
Admin panel: http://127.0.0.1:8000/admin-panel/

---

## Pages

| URL | Page |
|---|---|
| `/` | Home |
| `/about/` | About Us |
| `/contact/` | Contact |
| `/services/` | Services & Pricing |
| `/gallery/` | Photo Gallery |
| `/bookings/` | Book a Service |
| `/inquiries/` | Send an Inquiry |
| `/admin-panel/` | Custom Admin Dashboard |

---

## Admin Panel Features
- **Dashboard** – booking stats, recent bookings, new inquiries
- **Bookings** – list, filter, update status, admin notes
- **Gallery** – upload before/after photos, manage items
- **Services & Pricing** – add/edit/delete services and price tiers
- **Inquiries** – read, reply via email/WhatsApp
- **Customers** – view all unique customers by booking count

---

## Deploying to Vercel

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-org/windscreen-experts.git
git push -u origin main
```

### 2. Connect to Vercel
- Go to vercel.com → New Project → Import from GitHub
- Set **Root Directory** to `/`
- Add all environment variables from `.env.example`

### 3. Set up PostgreSQL
- Use **Vercel Postgres** or **Supabase** free tier
- Copy the `DATABASE_URL` connection string to Vercel env vars

### 4. Backblaze B2 Setup
- Create a B2 bucket (set to public)
- Create an application key with read/write access
- Add credentials to Vercel env vars
- Set `USE_BACKBLAZE=True`

### 5. Gmail SMTP
- Enable 2FA on your Gmail account
- Create an App Password: Google Account → Security → App Passwords
- Use the 16-character app password as `EMAIL_HOST_PASSWORD`

---

## Initial Data – Seed Services
Run this in Django shell (`python manage.py shell`):
```python
from apps.services.models import Service, ServicePricing
from django.utils.text import slugify

services_data = [
    {
        'name': 'Windscreen Repair',
        'slug': 'windscreen-repair',
        'short_description': 'Chips, cracks, and fractures fixed using industry-leading resin injection.',
        'description': 'Our windscreen repair service uses professional-grade resin injection technology to fix chips and cracks fast. Most repairs take under an hour.',
        'icon': 'bi-tools',
        'pricing': [
            {'label': 'Chip Repair', 'price': 10},
            {'label': 'Crack Repair', 'price': 20},
            {'label': 'Full Replacement', 'price': 80},
        ]
    },
    {
        'name': 'Headlight Restoration',
        'slug': 'headlight-restoration',
        'short_description': 'Restore clarity and brightness to yellowed, hazy headlights.',
        'description': 'We sand, polish and seal your headlights back to factory condition, improving safety and aesthetics significantly.',
        'icon': 'bi-lightbulb',
        'pricing': [{'label': 'Per Pair', 'price': 30}]
    },
    {
        'name': 'Ceramic Tint Installation',
        'slug': 'ceramic-tint',
        'short_description': 'Premium ceramic film for UV protection, heat reduction and privacy.',
        'description': 'Ceramic window film blocks UV rays, reduces cabin heat, and provides excellent privacy without interfering with electronics.',
        'icon': 'bi-shield-shaded',
        'pricing': [
            {'label': '', 'vehicle_type': 'compact', 'price': 20},
            {'label': '', 'vehicle_type': 'sedan', 'price': 50},
            {'label': '', 'vehicle_type': 'suv', 'price': 100},
            {'label': '', 'vehicle_type': 'van', 'price': 200},
        ]
    },
    {
        'name': 'Smart Tint Installation',
        'slug': 'smart-tint',
        'short_description': 'Switchable smart tint — control your privacy at the touch of a button.',
        'description': 'Smart (PDLC) tint switches from clear to opaque instantly, giving you complete privacy control.',
        'icon': 'bi-toggle-on',
        'pricing': [{'label': 'Consultation required', 'price': 60}]
    },
]

for s_data in services_data:
    pricing = s_data.pop('pricing')
    service, _ = Service.objects.get_or_create(slug=s_data['slug'], defaults=s_data)
    for p in pricing:
        ServicePricing.objects.get_or_create(service=service, label=p.get('label',''), defaults={'price': p['price'], 'vehicle_type': p.get('vehicle_type','')})

print("Done!")
```
