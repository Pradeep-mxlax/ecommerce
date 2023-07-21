FROM python:3.10.4-slim

ENV PYTHONUNBUFFERD 1

WORKDIR /app/server

ADD . /app/server

ARG DEV=false

COPY . requirements.txt /app/server/

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD [ "python","manage.py","runserver" ,"0.0.0.0:8000"]