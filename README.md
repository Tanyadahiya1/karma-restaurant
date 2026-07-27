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
