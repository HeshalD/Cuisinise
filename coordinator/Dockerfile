FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# If the coordinator has its own requirements.txt in coordinator/
# Otherwise, create one with just what it needs (fastapi, uvicorn, requests, httpx, pydantic, etc.)
COPY src/requirements.txt /app/src/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/src/requirements.txt

# Copy only the coordinator code into the image
# This assumes your FastAPI app is in coordinator/src/coordinator_api.py
COPY . /app

# Expose the coordinator port
EXPOSE 8000

# Start the API
# Note: module path is 'src.coordinator_api:app' because WORKDIR=/app and code is in /app/src/...
CMD ["uvicorn", "src.coordinator_api:app", "--host", "0.0.0.0", "--port", "8000"]