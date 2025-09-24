# syntax=docker/dockerfile:1

ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION} AS base

LABEL org.opencontainers.image.source=https://github.com/Riccardo-Cpt/BillingApp

#install curl module for API calls
RUN apt-get update && apt-get install -y curl ca-certificates

COPY ./embeddings_pipeline ./embeddings_pipeline
COPY ./data ./data
COPY ./app ./app

WORKDIR /app


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
