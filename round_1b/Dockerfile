# Use Python 3.10 slim for AMD64 platform (suitable for Windows AMD64 Docker Desktop)
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8

CMD ["python", "main.py", \
     "--input_dir", "/app/input", \
     "--outlines_dir", "/app/outlines", \
     "--output_file", "/app/output/results.json", \
     "--persona", "Investment Analyst", \
     "--job_to_be_done", "Analyze revenue trends and market positioning strategies"]
