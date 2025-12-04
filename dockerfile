# 1) Base image
FROM python:3.11-slim

# 2) Workdir
WORKDIR /app

# 3) Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy source
COPY api ./api

# 5) Expose port and run app
EXPOSE 8000
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
