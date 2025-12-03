FROM python:3.11.0-slim-bullseye
ENV PYTHONUNBUFFERED 1

ARG FRONT_HOST=http://localhost:3000
ARG DJANGO_DEV_SERVER_PORT=8030

ENV DJANGO_DEV_SERVER_PORT=$DJANGO_DEV_SERVER_PORT\
        FRONT_HOST=$FRONT_HOST

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && apt-get clean

WORKDIR /ekila_website_app
COPY . /ekila_website_app/
RUN pip install --no-cache-dir -r requirements.txt
COPY /containers/dev/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE $DJANGO_DEV_SERVER_PORT
