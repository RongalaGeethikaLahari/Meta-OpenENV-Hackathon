FROM python:3.11-slim

# ---------- SETUP ----------
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---------- COPY ----------
COPY . .

# ---------- PYTHON ----------
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Fix imports
ENV PYTHONPATH=/app

# ---------- ONLY EXPOSE UI ----------
EXPOSE 8000

# ---------- RUN BOTH SERVICES ----------
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]