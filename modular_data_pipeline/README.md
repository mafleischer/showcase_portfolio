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

## Why I Built This
To demonstrate full-stack engineering proficiency across API design, data handling, plugin architecture, secure authentication, DevOps (Docker/Compose), and frontend-backend integration.

## Screenshots <a name="screenshots"></a>

<table>
    <!-- <style>
        th{background-color:#e2fce6;}
        td{background-color:#fff9f3;}
    </style> -->
    <tr>
        <!-- github raw links used so this README is rendered on PyPi too -->
        <th style="background-color: #e2fce6" >Start</th>
        <td style="background-color: #fff9f3" align="center"><img src="https://raw.githubusercontent.com/mafleischer/showcase_portfolio/main/modular_data_pipeline/doc/img/start.png" alt="Start"></img></td>
    </tr>
    <tr>
        <th style="background-color: #e2fce6" >Logged in and ran the plugin for cloning a Github repo, converting all CSVs and getting a download</th>
        <td style="background-color: #fff9f3" align="center"><img src="https://raw.githubusercontent.com/mafleischer/showcase_portfolio/main/modular_data_pipeline/doc/img/logged_in_ran_plugin_git.png" alt="Ran plugin"></img></td>
    </tr>
 </table>

## Tech Stack
| Layer         | Tech Used                             |
|---------------|----------------------------------------|
| API Backend   | FastAPI, OAuth2, SQLAlchemy, PostgreSQL|
| Frontend      | React, Fetch API, FormData             |
| Data Handling | Dagster, Pandas, OpenPyXL, GitPython   |
| Auth          | OAuth2 (JWT), FastAPI Security         |
| DevOps        | Docker, Docker Compose                 |

## Directory Overview
| Path           | Purpose                                               |
|----------------|--------------------------------------------------------|
| `/plugins/`    | Contains plugin implementations (CSV, GitHub)         |
| `/api/`        | Main FastAPI app + auth + endpoints                   |
| `/frontend/`   | React app with auth and plugin execution UI           |
| `/static/exports/` | Generated Excel/ZIP files served via endpoint    |
| `Dockerfile`   | Multi-stage build with frontend + API container       |
| `docker-compose.yml` | Orchestrates backend and Postgres              |

## Setup Instructions
Run in one go:
```bash
```
```bash
docker compose up --build
```
Access UI at `http://localhost:8000/ui`.

or run components separately:\
```bash
docker build -t data-pipeline .
docker run -p 8000:8000 data-pipeline
cd frontend && npm install && npm start
```
Access UI at `http://localhost:3000/ui`

## Login
- Username: `admin`
- Password: `secret`
- Token-based auth via OAuth2 (JWT)

## API Overview
| Endpoint     | Method | Description                 |
|--------------|--------|-----------------------------|
| `/token`     | POST   | Obtain JWT access token     |
| `/run-plugin`| POST   | Execute selected plugin     |
| `/ui`        | GET    | Serve React web interface   |
| `/exports/`  | GET    | Download generated files    |

## Plugin Architecture
Each plugin implements a `BasePlugin` interface and defines a `fetch_data()` method. The system dynamically uses the selected plugin at runtime to fetch and process data.

## Example Use Cases
- Convert uploaded CSV into Excel via web UI.
- Clone a GitHub repo, detect CSVs, convert and bundle as ZIP.
- Automatically log executions to a Postgres database for audit.

## Challenges Tackled
- Secure token-based authentication and session handling.
- Handling large file streams and ZIP creation.
- Managing CORS, static assets, and frontend routing via FastAPI.
- Full CI-like multi-stage Docker build + Compose.

## Potential Enhancements
- Add test coverage (e.g., plugin fetch unit tests)
- Add more plugin types (e.g., API fetch, Excel merge, etc.)
- Role-based user management / login UI
- Hosted version (Render, Railway, etc.)

