# SOURCE: https://github.com/microsoft/playwright/blob/master/utils/docker/Dockerfile.focal

FROM ubuntu:20.04 AS builder-image

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

# Install node14
RUN apt-get update \
    && apt-get install -y curl \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs

# Feature-parity with node.js base images.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git ssh \
    && npm install -g yarn

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    python3.9 python3.9-dev python3.9-venv python3-pip python3-wheel build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# create and activate virtual environment
RUN python3.9 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install pip requirements
COPY ../requirements.txt .
RUN pip3 install --no-cache-dir wheel && pip3 install --no-cache-dir -r requirements.txt

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# 2. Install playwright and then delete the installation.
#    Browsers will remain downloaded in `/ms-playwright`.
#    Note: make sure to set 777 to the registry so that any user can access
#    registry.
RUN mkdir /ms-playwright \
    && npm init -y \
    && npm i playwright && \
    && npx playwright install-deps \
    && chmod -R 777 /ms-playwright

FROM ubuntu:20.04 AS runner-image

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install --no-install-recommends -y python3.9 python3.9-venv \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home appuser \
    && mkdir -p /home/appuser/app \
    && chown appuser:appuser /home/appuser/app

USER appuser

COPY --from=builder-image --chown=appuser:appuser /opt/venv /opt/venv
COPY --from=builder-image --chown=appuser:appuser /ms-playwright /ms-playwright

# activate virtual environment
# Keeps Python from generating .pyc files in the container
# Turns off buffering for easier container logging
ENV VIRTUAL_ENV="/opt/venv" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy user code into application code
COPY --chown=appuser:appuser . /home/appuser/app

WORKDIR /home/appuser/app

# Creds
# ENV EC2_KEY='not defined' K8S_KEY='not defined'

# Default arguments (originally /bin/bash)
# ENTRYPOINT [ "/bin/bash" ]
ENTRYPOINT [ "/opt/venv/bin/python", "cl_auto.py" ]
