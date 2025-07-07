# Modular Open Data Pipeline Platform
## Features
- Plugin system (GitHub + CSV plugins)
- FastAPI + OAuth2 Auth
- React UI to trigger plugin actions
- Converts CSV to Excel and serves files
- GitHub repo scanning and ZIP download
- Database logging via SQLAlchemy (optional)

## Run
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
