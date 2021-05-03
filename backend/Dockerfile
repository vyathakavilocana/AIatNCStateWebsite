FROM python:3.7

# python envs
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# python dependencies
COPY ./requirements.txt /
RUN pip install -r ./requirements.txt

# upload scripts
COPY ./scripts/entrypoint.sh ./scripts/start.sh ./scripts/gunicorn.sh ./scripts/celery.sh ./scripts/celery-beat.sh\
     ./scripts/test.sh /

# Fix windows docker bug, convert CRLF to LF
RUN sed -i 's/\r$//g' /start.sh && chmod +x /start.sh && sed -i 's/\r$//g' /entrypoint.sh && chmod +x /entrypoint.sh &&\
    sed -i 's/\r$//g' /gunicorn.sh && chmod +x /gunicorn.sh && sed -i 's/\r$//g' /celery.sh && chmod +x /celery.sh &&\
    sed -i 's/\r$//g' /celery-beat.sh && chmod +x /celery-beat.sh && sed -i 's/\r$//g' /test.sh && chmod +x /test.sh

# Create new directory for celery beat schedule and set its permissions
RUN mkdir /var/web
RUN chmod -R 755 /var/web

WORKDIR /app
