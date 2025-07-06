FROM python:3.10-slim

WORKDIR /app

COPY . .

# Install dependencies including prometheus_client
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir prometheus_client

EXPOSE 5001

CMD ["python", "app.py"]
