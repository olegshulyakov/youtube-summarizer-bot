# --- Test Stage ---
FROM python:3.9-slim AS test

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# For parsing HTML (ArticleSource)
RUN apt-get update && \
    apt-get install -y --no-install-recommends libxml2-dev libxslt-dev && \
    rm -rf /var/lib/apt/lists/*

# Run the tests
CMD ["pytest", "tests/"]


# --- Final Image Stage ---
FROM python:3.9-slim

WORKDIR /app

# Copy *only* the necessary files from the test stage (not the tests!)
COPY --from=test /app /app
COPY --from=test /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

CMD ["python", "src/main.py"]