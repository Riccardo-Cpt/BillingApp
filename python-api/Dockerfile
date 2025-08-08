# syntax=docker/dockerfile:1

ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION} AS base

LABEL org.opencontainers.image.source=https://github.com/Riccardo-Cpt/BillingApp

WORKDIR /app

COPY ./app .

ARG UID
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN chown appuser:appuser /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set ownership and permissions for the /app directory
# RESTRICT PERMISSIONS ONCE IN PRODUCTION
RUN chown -R appuser:appuser /app && \
    chmod -R 755 /app

USER appuser

WORKDIR '/app/billing_track/'

#CMD ["python manage.py makemigrations billing_track"]
#CMD ["python manage.py migrate"]
#CMD ["python manage.py runserver 0.0.0.0:8000"] #migrate and run server
