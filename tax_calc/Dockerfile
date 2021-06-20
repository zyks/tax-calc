FROM python:3.9-alpine3.13

ENV PYTHONUNBUFFERED=1
ENV PYTHONPYCACHEPREFIX=/tmp/pycache

WORKDIR /code
EXPOSE 8000

RUN apk add --no-cache \
    bash \
    gcc \
    musl-dev \
    'postgresql-dev>=13.3-r0'

COPY requirements/base.txt /tmp/
RUN pip install -r /tmp/base.txt
