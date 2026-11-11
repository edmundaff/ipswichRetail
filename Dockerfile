# Ipswich Retail — local container proof of concept (not a production server)
# Python 3.12 runs the project's supported Django 5.2 dependency.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Keep dependency installation in a separate cacheable layer.
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 8000

# Compose overrides this command to migrate and seed demo data before starting.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
