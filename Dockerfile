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

CMD gunicorn --bind=0.0.0.0:5000 --access-logfile '-' wallet_api.gunicorn-entry:app
