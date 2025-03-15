# --- Test Stage ---
FROM python:3.9-slim AS test

WORKDIR /app

# For parsing HTML (ArticleSource)
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends libxml2-dev libxslt-dev && \
#     rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

CMD ["python", "main.py"]