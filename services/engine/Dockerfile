# Multi-arch friendly (build with buildx for linux/amd64 + linux/arm64).
# See docs/08-deployment/deployment-and-portability.md.
FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -e .

EXPOSE 8000
CMD ["python", "-m", "broke_engine"]
