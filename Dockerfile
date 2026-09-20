# Official Python image use karein
# FROM python:3.11-slim
FROM python:3.12-slim

# Working directory set karein
WORKDIR /app

# Environment variables set karein
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# System dependencies install karein (agar psycopg2 ke liye darkar hon)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Requirements file copy karein aur packages install karein
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Poora project copy karein
COPY . /app/

# Port expose karein
EXPOSE 8000

# Server run karne ki command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]