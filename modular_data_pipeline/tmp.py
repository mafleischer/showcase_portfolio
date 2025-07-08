### Project: Modular Open Data Pipeline Platform

# Updated: Includes OAuth2 Authentication, CSV Plugin, DB Logging, and Full React UI

# File: plugins/base_plugin.py
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @abstractmethod
    def fetch_data(self) -> dict:
        pass


# File: plugins/github_plugin.py
import requests
from .base_plugin import BasePlugin

class GitHubPlugin(BasePlugin):
    def fetch_data(self) -> dict:
        response = requests.get("https://api.github.com/repos/dagster-io/dagster")
        return response.json()


# File: plugins/csv_plugin.py
import csv
from .base_plugin import BasePlugin

class CSVPlugin(BasePlugin):
    def fetch_data(self) -> dict:
        with open('data/sample.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return {"data": [row for row in reader]}


# File: models.py
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///pipeline_logs.db')
Session = sessionmaker(bind=engine)

class PipelineLog(Base):
    __tablename__ = 'pipeline_logs'
    id = Column(Integer, primary_key=True)
    plugin_name = Column(String)
    result_data = Column(JSON)

Base.metadata.create_all(engine)


# File: dagster_pipelines/pipelines.py
from dagster import job, op
from plugins.github_plugin import GitHubPlugin
from plugins.csv_plugin import CSVPlugin
from models import PipelineLog, Session

@op(config_schema={"plugin": str})
def fetch_data_op(context):
    plugin_name = context.op_config["plugin"]
    plugin_class = GitHubPlugin if plugin_name == "github" else CSVPlugin
    plugin = plugin_class()
    data = plugin.fetch_data()

    session = Session()
    log = PipelineLog(plugin_name=plugin_name, result_data=data)
    session.add(log)
    session.commit()

    return data

@op
def print_data_op(data: dict):
    print("Fetched Data:", data)

@job(config={"ops": {"fetch_data_op": {"config": {"plugin": "github"}}}})
def data_pipeline():
    print_data_op(fetch_data_op())


# File: api/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": "secret"  # Ideally use hashed password in production
    }
}

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or user["hashed_password"] != password:
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


# File: api/main.py
from fastapi import FastAPI, Depends
from dagster import execute_job
from dagster_pipelines.pipelines import data_pipeline
from api.auth import authenticate_user, create_access_token, get_current_user
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/run-pipeline")
def run_pipeline(user: str = Depends(get_current_user)):
    result = execute_job(data_pipeline)
    return {"success": result.success}


# File: frontend/src/App.js
import React, { useState } from 'react';

function App() {
  const [token, setToken] = useState(null);
  const [output, setOutput] = useState(null);

  const login = async () => {
    const response = await fetch('http://localhost:8000/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        username: 'admin',
        password: 'secret',
      })
    });
    const data = await response.json();
    setToken(data.access_token);
  };

  const runPipeline = async () => {
    const response = await fetch('http://localhost:8000/run-pipeline', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    const data = await response.json();
    setOutput(data);
  };

  return (
    <div className="App">
      <h1>Run Data Pipeline</h1>
      <button onClick={login}>Login</button>
      <button onClick={runPipeline} disabled={!token}>Run Pipeline</button>
      <pre>{output && JSON.stringify(output, null, 2)}</pre>
    </div>
  );
}

export default App;


# File: frontend/package.json
{
  "name": "pipeline-ui",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "react-scripts": "5.0.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  }
}


# File: Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install dagster dagit fastapi uvicorn requests sqlalchemy python-jose[cryptography]
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]


# File: README.md
# Modular Open Data Pipeline Platform

## Features
- Dagster-powered data pipeline
- Plugin system (GitHub + CSV plugins)
- FastAPI + OAuth2 Auth
- React UI to trigger pipeline
- Database logging via SQLAlchemy (SQLite)

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

