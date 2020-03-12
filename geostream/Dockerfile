FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /usr/src/app

# dont write pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# dont buffer to stdout/stderr
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/app/requirements.txt

# dependencies
RUN set -eux \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/pip
