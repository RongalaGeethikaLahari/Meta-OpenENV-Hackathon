FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    curl \
    socat \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

# HF expects 7860
EXPOSE 7860

# Map 7860 → 8000 using socat
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]