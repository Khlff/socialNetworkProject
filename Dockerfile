FROM python:3.10
LABEL authors="Khlff"

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

RUN python manage.py migrate

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
