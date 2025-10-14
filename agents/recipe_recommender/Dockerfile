FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# If this service has its own requirements.txt in this folder:
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch \
    && pip install --no-cache-dir -r /app/requirements.txt


# Copy service code
COPY . /app

# Service port (change per service below)
EXPOSE 8004

# Start (change module:app and port per service)
CMD ["uvicorn", "recipe_recommender_api:app", "--host", "0.0.0.0", "--port", "8004"]
