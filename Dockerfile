FROM python:3.12-alpine

RUN apk add --no-cache postgresql-client

WORKDIR /app

RUN mkdir -p /backups

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "-u", "main.py"]