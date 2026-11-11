
# Ipswich Retail - Docker deployment
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . ./

# Prepare CSS, JavaScript and images
RUN DJANGO_DEBUG=true python manage.py collectstatic --noinput

EXPOSE 8000

# Initialise the demo database and run the web server
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py seed_products && exec gunicorn retail_site.wsgi:application --bind 0.0.0.0:8000"]
