FROM python:3.9-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir sentence-transformers
RUN pip install --no-cache-dir langchain-huggingface

COPY . .

RUN chmod +x entrypoint.sh

CMD ["sh", "-c", "./entrypoint.sh"]
