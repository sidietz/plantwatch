# Use the official Python runtime image
FROM python:alpine

RUN apk add py3-psycopg2 py3-gunicorn-pyc

RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

RUN pip install --upgrade pip 

COPY .  /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN cp /app/plantwatch/plantwatch/settings_dev.py /app/plantwatch/plantwatch/settings.py
EXPOSE 8000

CMD ["python", "plantwatch/manage.py", "runserver", "0.0.0.0:8000"]
