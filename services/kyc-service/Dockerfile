# --- Builder Stage ---
# Installs dependencies
FROM python:3.11-slim as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# --- Final Stage ---
# Copies dependencies and source code
FROM python:3.11-slim

WORKDIR /usr/src/app

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

COPY --from=builder /usr/src/app/wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache /wheels/*

COPY ./app ./app

# Run as non-root user
USER app

# Expose port and run server
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]