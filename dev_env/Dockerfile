FROM python:3.13-bookworm

WORKDIR /app

COPY backup_utility/ backup_utility/
COPY config.yaml config.yaml
COPY requirements.txt requirements.txt

RUN apt update && apt install -y mariadb-client postgresql-client nano
RUN pip install --no-cache-dir -r requirements.txt