# Use Python 3.9.1
FROM python:3.9.1-slim AS development

# Build arguments to set non-root user
ARG USER_ID=1001
ARG GROUP_ID=1001

# Environment variables to configure FastAPI
ENV API_HOST="0.0.0.0" \
    API_PORT="5000" \
    API_GROUP="fastapi" \
    API_USER="fastapi" \
    API_DIR="/usr/src/api" \
    FASTAPI_ENV="development" \
    FASTAPI_APP="api.py"

# Work directory inside container
WORKDIR ${API_DIR}

# Install Debian Slim packages
ADD packages.txt .
RUN apt-get update -y -qq && xargs -ra packages.txt apt-get install -y -qq

# Install Python packages
ADD requirements.txt .
RUN pip install -r requirements.txt

# Add all other files to the container
ADD . .

# Create non-root user fastapi and give appropriate permissions
RUN groupadd -g ${GROUP_ID} ${API_GROUP} \
  && useradd -u ${USER_ID} -g ${API_GROUP} ${API_USER} \
  && chown ${USER_ID}:${GROUP_ID} ${API_DIR}

# Set non-root user fastapi to run FastAPI
USER ${USER_ID}:${GROUP_ID}

# Expose FastAPI to outside the container
EXPOSE ${API_PORT}

# By default, execute FastAPI
CMD uvicorn api:app --host ${API_HOST} --port ${API_PORT} --reload
