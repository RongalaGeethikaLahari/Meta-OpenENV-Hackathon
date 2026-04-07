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
CMD ["sh", "-c", "\
    apt-get update && apt-get install -y socat && \
    uvicorn server.app:app --host 0.0.0.0 --port 8000 & \
    socat TCP-LISTEN:7860,fork TCP:localhost:8000 \
"]