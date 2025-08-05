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

USER appuser

#to run in interactive mode. TO BE DEACTIVATED ONCE DEVELOPMENT FINISHES 
CMD ["tail", "-f", "/dev/null"]
