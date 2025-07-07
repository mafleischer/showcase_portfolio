# Modular Open Data Pipeline Platform
## Features
- **Plugin System**: Modular design with built-in support for:
  - GitHub repo CSV ingestion (via `GitHubPlugin`)
  - Direct CSV file upload (via `CSVPlugin`)
- **Authentication**: OAuth2 login via FastAPI and JWT tokens
- **Data Processing**: Converts CSVs to Excel files
- **File Export**: Downloads returned as `.xlsx` files or zipped results
- **Logging**: Logs plugin executions to PostgreSQL with user, plugin type, and timestamp
- **Web UI**: React frontend served from `/ui`
- **Fully Containerized**: One-command setup with Docker Compose

## Run
Run in one go:\
```bash
docker compose up --build
```

or run components separately:\
```bash
docker build -t data-pipeline .
docker run -p 8000:8000 data-pipeline
cd frontend && npm install && npm start
```
Visit `http://localhost:3000` to run the pipeline.

## Notes
- Login: `admin` / `secret`
- Token-based auth via OAuth2 (JWT)
- Extend with more plugins and UI features as needed.
