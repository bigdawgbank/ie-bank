# Dockerfile
FROM python:3.10-slim-buster

# Install PostgreSQL development files and other necessary packages
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD gunicorn --workers=4 --bind=0.0.0.0:5000 --timeout=120 --access-logfile=- --error-logfile=- app:app
