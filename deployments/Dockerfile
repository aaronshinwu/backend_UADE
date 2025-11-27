#PASO 1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONNUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \ 
    libmariadb-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

#PASO 4
COPY Backend/requirements.txt .

#PASO 5
RUN pip install --no-cache-dir -r requirements.txt

#PASO 6
COPY Backend/ .

COPY deployments/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

#PASO 7
RUN mkdir -p /app/media /app/logs /app/staticsfiles

# #PASO 8
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app


#PASO 10
USER appuser

#PASO 11
EXPOSE 8000

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]

#PASO 12
CMD ["production"]

