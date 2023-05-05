FROM python:3
LABEL authors="Khlff"

ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt