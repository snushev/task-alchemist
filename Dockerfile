FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src . 

RUN ENCRYPTION_KEY=m8PYZzpdEZOGgl5hZAOM4GgKI8pxZBB5_OF_okc-t98= python manage.py collectstatic --noinput

ENV PYTHONPATH=/app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "config.wsgi:application"]
