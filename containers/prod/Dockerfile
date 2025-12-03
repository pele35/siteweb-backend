FROM python:3.11.0-slim-bullseye AS base

FROM base AS system-deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && apt-get clean \
    && python -m pip install hypercorn \
    && rm -rf /var/lib/apt/lists/*

FROM base AS build
ARG BUILD_ENVIRONMENT=requirements.txt
WORKDIR /build

COPY . .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r ${BUILD_ENVIRONMENT}

FROM base AS final
ARG BUILD_ENVIRONMENT=requirements.txt
ARG APP_HOME=/app
ARG DJANGO_DEV_SERVER_PORT=8030
ARG DJANGO_STATIC_ROOT=/var/www/static
ARG DJANGO_MEDIA_ROOT=/var/www/media

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    BUILD_ENV=${BUILD_ENVIRONMENT}

RUN addgroup --system ekiladm; \
        adduser --system --group ekiladm; \
        mkdir -p ${APP_HOME}; \
        mkdir -p ${DJANGO_STATIC_ROOT} ${DJANGO_MEDIA_ROOT}; \
        chown -R ekiladm:ekiladm /var/www

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        gnupg \
        wget \
        postgresql-client \
        make

WORKDIR ${APP_HOME}

COPY --from=build /wheels /wheels
RUN pip install --no-cache /wheels/*

COPY ./containers/prod/entrypoint.sh ${APP_HOME}/entrypoint.sh
COPY ./ekila/settings_prod_example.py ${APP_HOME}/ekila/settings_prod.py
RUN sed -i 's/\r$//g' ${APP_HOME}/entrypoint.sh && chmod +x ${APP_HOME}/entrypoint.sh

COPY . ${APP_HOME}
RUN chown -R ekiladm:ekiladm ${APP_HOME}
USER ekiladm

ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE ${DJANGO_DEV_SERVER_PORT}
