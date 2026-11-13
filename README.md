# Ipswich Retail — Django e-commerce proof of concept

A real Django **Model–View–Template (MVT)** shopping demo built for the University of Suffolk DevOps Component 2 case-study scenario. The shop is deliberately small: **4 main customer pages** plus Django Admin. The project is intended to be reviewed, customised and understood by the student before it is submitted or extended.

> **Safety:** This is a proof of concept, not a production store. Checkout creates an **example order without taking payment**. Do not use it to collect real customer information. Do not deploy with the development SECRET_KEY, DEBUG=True, or the SQLite development database.

## Site pages and features

| Customer page | Route | Functionality |
|---|---|---|
| Home | `/` | Hero section, featured products, category navigation |
| Shop all | `/shop/` | Database-backed products, text search, category filter, sorting |
| Product details | `/shop/<slug>/` | Product information, stock status and Add to Basket |
| Basket + demo checkout | `/basket/` | Edit quantities, checkout form, saved demo orders and confirmation |
| Admin (excluded from 4 pages) | `/admin/` | Product/category administration, inspect demo orders |
| Monitoring endpoint | `/health/` | JSON: `{"status":"ok","service":"ipswich-retail-demo"}` |

### Technology

- **Python 3.10+** and **Django 5.2 LTS** (officially supported series as of November 2026)
- SQLite for **local development only**
- Django ORM models: `Category`, `Product`, `Order`, `OrderItem`
- Django templates, HTML5, CSS, original SVG product illustrations; minimal JavaScript
- Session-backed basket with CSRF-protected POST forms; server-side stock/price validation
- Unit/integration tests with Django's built-in test runner

## Run on a Mac (simplest option)

1. Unzip the downloaded project.
2. Open Terminal, then go into the folder: `cd /path/to/Ipswich_Retail_Django`.
3. Run `bash START_ON_MAC.command`.
4. Open **http://127.0.0.1:8000/** in your browser.
5. Stop the server with **Ctrl+C**.

You can also double-click the `.command` file if macOS permits opening it; Terminal is more reliable. The first run uses pip to download Django, so you **need internet access on your Mac**.

## Run manually (Mac, Linux or Windows)

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_products
python manage.py runserver
```

Open http://127.0.0.1:8000/ — a fully working local Django shop.

### Admin

Create a local admin account (choose your own credentials):

```bash
python manage.py createsuperuser
```

Then open http://127.0.0.1:8000/admin/ . Never commit real usernames, passwords or secrets. Django stores passwords as hashes, not cleartext.

### Tests

```bash
python manage.py check
python manage.py test shop
python manage.py makemigrations --check --dry-run
```

The test suite covers the home page, product filtering, product details, basket operations, invalid quantities, available stock, demo checkout validation, order persistence and the health endpoint.

### What demo checkout does

1. A user adds one or more products to their basket.
2. The basket stores **product IDs and quantities only** in a signed Django session.
3. At checkout, the backend validates input and current database stock, computes the authoritative total, creates `Order` and `OrderItem` records, decrements inventory and displays a short confirmation code.
4. **No card numbers, payment gateway or real order fulfilment.**

## Project structure

```text
Ipswich_Retail_Django/
├── manage.py                         # Django commands
├── retail_site/                      # Django settings, URL config, ASGI/WSGI
├── shop/
│   ├── models.py                     # MVT: data (products, categories, orders)
│   ├── views.py                      # MVT: request handling/business logic
│   ├── forms.py                      # Checkout validation
│   ├── urls.py                       # Customer routes
│   ├── cart.py                       # Basket session logic
│   ├── admin.py                      # Product/order admin
│   ├── tests.py                      # Automated tests
│   ├── migrations/                   # Database schema migration
│   ├── management/commands/seed_products.py
│   ├── templates/shop/              # MVT: HTML templates
│   └── static/shop/                  # CSS, JS, original SVG artwork
├── docs/preview.html                 # VISUAL PREVIEW ONLY; not a live Django app
├── docs/architecture.md              # Explanation of design
├── requirements.txt
├── .env.example
└── START_ON_MAC.command
```

