FROM python:3.11-slim
WORKDIR /code
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt
COPY app/ ./app/
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
