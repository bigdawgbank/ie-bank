# Dockerfile
FROM python:3.11

# Install PostgreSQL development files and other necessary packages
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 50505

ENTRYPOINT ["gunicorn", "app:app", "-b", "0.0.0.0:50505"]
