FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir requests pyyaml

COPY fetch_jobs.py /app/fetch_jobs.py

CMD ["python", "/app/fetch_jobs.py"]
