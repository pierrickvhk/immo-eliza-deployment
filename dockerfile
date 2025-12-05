# 1) Use a small Python base image
FROM python:3.11-slim

# 2) Set working directory inside the container
WORKDIR /app

# 3) Install basic system dependencies (needed for some Python wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# 4) Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5) Copy only the API code and model artifacts
COPY api ./api

# 6) Expose the port and run the FastAPI app
EXPOSE 8000
# WHY: Render sets port dynamically, so we respect their binding requirements
ENV PORT=8000
CMD ["sh", "-c", "uvicorn api.app:app --host 0.0.0.0 --port $PORT"]

