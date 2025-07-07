FROM node:18 as frontend-builder
WORKDIR /app
COPY frontend/ ./frontend/
RUN cd frontend && npm install && npm run build

FROM python:3.11-slim
WORKDIR /app
COPY --from=frontend-builder /app/frontend/build ./frontend_build
COPY . .
RUN apt-get update && apt-get install git sqlite3 -y
RUN pip install dagster dagit fastapi uvicorn requests sqlalchemy python-jose[cryptography] pandas gitpython openpyxl python-multipart psycopg2-binary
ENV DAGSTER_HOME=/dagster_home
RUN mkdir -p $DAGSTER_HOME
RUN mkdir exports
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
