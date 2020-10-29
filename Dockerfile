FROM python:3.7-slim-buster

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt && \
    pip install gunicorn

COPY ./wallet_api /app/wallet_api
COPY ./tools /app/tools

ENV FLASK_APP /app/wallet_api

RUN flask init-db && \
    python /app/tools/adduser.py --database /app/instance/wallet.sqlite --username john --password test --balance 100

ENV PORT 5000
ENV NUM_WORKERS 4
ENV WORKER_CLASS sync

CMD gunicorn \
    --bind=0.0.0.0:$PORT \
    --access-logfile '-' \
    --workers=$NUM_WORKERS \
    --worker-class=$WORKER_CLASS \
    wallet_api.gunicorn-entry:app
