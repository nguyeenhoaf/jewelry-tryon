FROM python:3.10

WORKDIR /app

# 1️⃣ Cài system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libgl1 \
    libglib2.0-0 \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 2️⃣ Copy & install python deps
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 3️⃣ Copy source
COPY app ./app
COPY assets ./assets

ENV INSIGHTFACE_HOME=/app/assets/models

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
