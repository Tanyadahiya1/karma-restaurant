# Karma Indian Bistro & Restaurant — Website

A full-stack, production-ready Flask website for **Karma Indian Bistro & Restaurant**
(1708 3rd St N, Jacksonville Beach, FL 32250), built in a luxury "Royal Indian Heritage"
theme — Mehndi Green (#0B5D3B) and Royal Gold (#D4AF37) on ivory, with Playfair Display /
Great Vibes / Poppins typography, glassmorphism cards, mandala motifs, parallax hero,
a custom cursor, magnetic buttons, an intro curtain loader, scroll reveal (AOS), and
Swiper carousels.

## Features
- Public site: Home, About, Menu (search + category filters), Gallery (masonry + lightbox),
  Reservations, Order Online (cart + checkout + coupons), Contact (with embedded map).
- **Customer accounts**: register/sign in at `/account/register` and `/account/login`,
  with an account dashboard (`/account/`) showing order and reservation history.
- Full shopping cart stored server-side in the session, with coupon codes (`KARMA10`,
  `WELCOME15`, `JAXBEACH20`) and tax calculation.
- **Stripe Checkout integration** for card payments — see setup below.
- **Email notifications** (via Flask-Mail) — customers get an order/reservation confirmation
  email, and the owner gets notified of every new order and reservation — see setup below.
- Admin panel (`/admin/login`) with dashboard stats, Orders, Reservations, Messages,
  Newsletter subscribers and Menu availability management, CSV export, search, and delete.
- SQLite + SQLAlchemy models, Flask-WTF forms with CSRF protection, Flask-Login (admin) +
  session-based auth (customers).
- SEO: meta tags, Open Graph/Twitter cards, Restaurant JSON-LD schema, `robots.txt`,
  `sitemap.xml`, lazy-loaded images.
- Mobile-first responsive design, dark mode toggle, floating WhatsApp/Call/Back-to-top buttons,
  custom cursor, magnetic buttons, intro curtain loader, and whole-section "swipe up on scroll"
  reveal animations.

## Default Admin Login
- URL: `/admin/login`
- Username: `admin`
- Password: `KarmaAdmin@2026`

**Change these immediately in production** via the `ADMIN_USERNAME` / `ADMIN_PASSWORD`
environment variables, and set a strong `SECRET_KEY`.

## Setting Up Stripe (real card payments)
This project ships with a genuine Stripe Checkout integration — not a fake/simulated one.
Until you add your own keys, the "Pay Online" option will show a friendly message asking
customers to choose "Pay at Counter" or "Cash on Delivery" instead; nothing breaks.

1. Create a free account at https://dashboard.stripe.com and grab your API keys
   (Developers → API keys).
2. Set these environment variables:
   - `STRIPE_SECRET_KEY` — starts with `sk_test_...` (or `sk_live_...` in production)
   - `STRIPE_PUBLISHABLE_KEY` — starts with `pk_test_...` (or `pk_live_...`)
3. For reliable payment confirmation, add a webhook (Developers → Webhooks → Add endpoint):
   - Endpoint URL: `https://yourdomain.com/webhook/stripe`
   - Event to send: `checkout.session.completed`
   - Copy the "Signing secret" into `STRIPE_WEBHOOK_SECRET`
   - Without this secret configured, the webhook endpoint safely refuses all requests
     (returns 400) rather than trusting unverified payloads — the checkout success-page
     redirect still independently verifies payment with Stripe's API either way.
4. Card numbers are **never** handled by this app's own server or database — Stripe's
   hosted Checkout page collects payment details directly, which is the standard,
   PCI-compliant way to accept cards online.

## Setting Up Email (order/reservation confirmations)
Uses Flask-Mail under the hood. Until configured, emails are skipped with a log line —
checkout and reservations still work normally.

Set these environment variables (example values for Gmail SMTP with an App Password):
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
MAIL_DEFAULT_SENDER=Karma Indian Bistro <your-email@gmail.com>
OWNER_NOTIFICATION_EMAIL=owner-inbox@example.com
```
Any standard SMTP provider works (SendGrid, Mailgun, Postmark, your own mail server, etc.) —
just point `MAIL_SERVER` / `MAIL_PORT` / credentials at it.

## Run Locally
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Visit http://localhost:5000 — the SQLite database and menu/admin seed data are created
automatically on first run.

## Environment Variables
| Variable | Purpose | Default |
|---|---|---|
| `SECRET_KEY` | Flask session/CSRF secret | dev key (change in prod) |
| `DATABASE_URL` | SQLAlchemy DB URI | local SQLite file |
| `ADMIN_USERNAME` | Default admin username | `admin` |
| `ADMIN_PASSWORD` | Default admin password | `KarmaAdmin@2026` |
| `FLASK_ENV` | `production` or `development` | `development` |
| `PORT` | Server port | `5000` |
| `STRIPE_SECRET_KEY` | Stripe secret key | *(unset — card payment disabled)* |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key | *(unset)* |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret | *(unset — webhook disabled)* |
| `MAIL_SERVER` / `MAIL_PORT` / `MAIL_USE_TLS` / `MAIL_USERNAME` / `MAIL_PASSWORD` | SMTP settings | *(unset — emails skipped)* |
| `MAIL_DEFAULT_SENDER` | "From" address on outgoing email | Karma noreply address |
| `OWNER_NOTIFICATION_EMAIL` | Where new-order/reservation alerts go | `info@karmabistrojax.com` |

## Deploy on Render
1. Push this project to a GitHub repository.
2. On Render: **New → Web Service**, connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app --workers=3 --bind=0.0.0.0:$PORT` (already in `Procfile`).
5. Add all the environment variables listed above (at minimum `SECRET_KEY`, `ADMIN_USERNAME`,
   `ADMIN_PASSWORD`, `FLASK_ENV=production`; add the Stripe/mail ones once you have them).
6. Optional: attach a Render PostgreSQL database and set `DATABASE_URL` — the app
   auto-converts `postgres://` to `postgresql://` for SQLAlchemy.
7. Deploy. Render will run the app via Gunicorn automatically.

## Project Structure
```
karma-restaurant/
├── app.py                 # App factory, blueprints, error handlers, seeding
├── config.py               # Configuration & real business details
├── models.py                # SQLAlchemy models
├── forms.py                  # Flask-WTF forms
├── extensions.py               # Flask-Login / CSRF singletons
├── seed.py                      # Menu catalog seed data
├── slugify_util.py               # Slug helper
├── requirements.txt
├── Procfile
├── runtime.txt
├── routes/
│   ├── main.py             # Public pages, contact/reservation/newsletter, SEO routes
│   ├── order.py            # Cart, checkout, order confirmation
│   └── admin.py            # Admin auth + CRUD + CSV export
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── images/
└── templates/
    ├── base.html, index.html, about.html, menu.html, gallery.html,
    │   reservation.html, order.html, order_confirmation.html, contact.html,
    │   login.html, admin.html, 404.html, 500.html
```

## A note on imagery
Menu, gallery and hero visuals use free-to-use stock photography (Unsplash) as
placeholders — this project does not copy proprietary photography or the logo file
from any third-party website. To use your own branded photos: drop them into
`static/images/` and swap the `image` values in `seed.py` (menu photos) or the
`<img>` sources in `gallery.html` / `index.html` / `about.html` with no other code changes needed.
