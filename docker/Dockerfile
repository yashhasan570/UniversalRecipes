###############################################
# Frontend Build
###############################################
FROM node:26@sha256:e18c3ccdf7d71619990b0e85639f506e2028a95410999cab24cc373cbd10e0ac \
    AS frontend-builder

# renovate: datasource=npm depName=pnpm
RUN npm install --global pnpm@12.20.0

WORKDIR /frontend

COPY frontend .

# The lang files import the seeded ingredient unit names, which live with the backend rather
# than in frontend/. Copy them to the same path they occupy in the repo, so the relative import
# in app/lang/locales/*.ts resolves identically here and in local dev.
COPY universalrecipes/repos/seed/resources/units/locales /universalrecipes/repos/seed/resources/units/locales

RUN pnpm clean-install

RUN pnpm generate

###############################################
# Base Image - Python
###############################################
FROM python:3.14-slim@sha256:a2b82f3c48559aa0a8446d9af49826b6e2b2016f4cd2afabfe6013ec53729170 \
    AS python-base

ENV UNIVERSALRECIPES_HOME="/app"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    VENV_PATH="/opt/universalrecipes"

# prepend venv to path
ENV PATH="$VENV_PATH/bin:$PATH"

# create user account
RUN useradd -u 911 -U -d $UNIVERSALRECIPES_HOME -s /bin/bash abc \
    && usermod -G users abc \
    && mkdir $UNIVERSALRECIPES_HOME

###############################################
# Backend Package Build
###############################################
FROM python-base AS backend-builder
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# renovate: datasource=pypi depName=uv
RUN pip install uv==0.13.8

# Install from the committed lockfile; never re-resolve. The rolling
# `exclude-newer` cooling window (pyproject [tool.uv]) would otherwise make
# `uv export` below re-resolve and fail on in-window pins.
ENV UV_FROZEN=1

WORKDIR /universalrecipes

# copy project files here to ensure they will be cached.
COPY uv.lock pyproject.toml ./
COPY universalrecipes ./universalrecipes

# Copy frontend to package it into the wheel
COPY --from=frontend-builder /frontend/dist ./universalrecipes/frontend

# Build the source and binary package
RUN uv build --out-dir dist

# dependencies.txt changes only when uv.lock does, so the venv build can cache
# the install. requirements.txt adds the wheel that was just built, so an
# install from it gets that exact one.
RUN uv export --no-dev --no-editable --no-emit-project --extra pgsql --format requirements-txt --output-file dist/dependencies.txt \
    && cp dist/dependencies.txt dist/requirements.txt \
    && UNIVERSALRECIPES_VERSION=$(python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])") \
    && echo "universalrecipes[pgsql]==${UNIVERSALRECIPES_VERSION} \\" >> dist/requirements.txt \
    && pip hash dist/universalrecipes-${UNIVERSALRECIPES_VERSION}-py3-none-any.whl | tail -n1 | tr -d '\n' >> dist/requirements.txt \
    && echo " \\" >> dist/requirements.txt \
    && pip hash dist/universalrecipes-${UNIVERSALRECIPES_VERSION}.tar.gz | tail -n1 >> dist/requirements.txt

###############################################
# Package Container
# Only role is to hold the packages, or be overridden by a --build-context flag.
###############################################
FROM scratch AS packages
COPY --from=backend-builder /universalrecipes/dist /

###############################################
# Python Virtual Environment Build
###############################################
# Install packages required to build the venv, in parallel to building the wheel
FROM python-base AS venv-builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    libwebp-dev \
    ffmpeg \
    # LDAP Dependencies
    libsasl2-dev libldap2-dev libssl-dev \
    gnupg gnupg2 gnupg1 \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv --upgrade-deps $VENV_PATH

# Install the wheel and all dependencies into the venv
FROM venv-builder-base AS venv-builder

# Cache key is dependencies.txt, so a universalrecipes-only commit reuses this layer.
COPY --from=packages dependencies.txt /dist/dependencies.txt
RUN . $VENV_PATH/bin/activate \
    && pip install --require-hashes -r /dist/dependencies.txt

# Copy built package (wheel) and its dependency requirements
COPY --from=packages * /dist/

# The dependencies are already in place, so pip only installs universalrecipes itself.
RUN . $VENV_PATH/bin/activate \
    && pip install --require-hashes -r /dist/requirements.txt --find-links /dist

###############################################
# Production Image
###############################################
FROM python-base AS production
ENV PRODUCTION=true
ENV TESTING=false

ARG COMMIT
ENV GIT_COMMIT_HASH=$COMMIT

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    ffmpeg \
    gosu \
    iproute2 \
    libldap-common \
    libldap2 \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# create directory used for Docker Secrets
RUN mkdir -p /run/secrets

# Copy venv into image. It contains a fully-installed universalrecipes backend and frontend.
COPY --from=venv-builder $VENV_PATH $VENV_PATH

# install nltk data for the ingredient parser
ENV NLTK_DATA="/nltk_data/"
COPY ./docker/setup_nltk_data.sh $UNIVERSALRECIPES_HOME/setup_nltk_data.sh
RUN chmod +x $UNIVERSALRECIPES_HOME/setup_nltk_data.sh && $UNIVERSALRECIPES_HOME/setup_nltk_data.sh

VOLUME [ "$UNIVERSALRECIPES_HOME/data/" ]
ENV APP_PORT=9000

EXPOSE ${APP_PORT}

COPY ./docker/healthcheck.sh $UNIVERSALRECIPES_HOME/healthcheck.sh
RUN chmod +x $UNIVERSALRECIPES_HOME/healthcheck.sh
HEALTHCHECK CMD $UNIVERSALRECIPES_HOME/healthcheck.sh

ENV HOST=0.0.0.0

EXPOSE ${APP_PORT}
COPY ./docker/entry.sh $UNIVERSALRECIPES_HOME/run.sh

RUN chmod +x $UNIVERSALRECIPES_HOME/run.sh
ENTRYPOINT ["/app/run.sh"]
