
FROM python:3.12-slim
# Set environment variables to prevent writing .pyc files
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]

# FROM python:3.10-slim AS runtime
# ENV PYTHONUNBUFFERED=1
# WORKDIR /app
# COPY --from=build /app /app
# EXPOSE 8000
# CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]