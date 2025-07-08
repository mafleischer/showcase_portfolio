import os
from pathlib import Path
import shutil
import sys
from contextlib import asynccontextmanager
from datetime import timedelta
from uuid import uuid4

from api.auth import authenticate_user, create_access_token, get_current_user
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from models import PipelineLog, Session
from plugins.csv_plugin import CSVPlugin
from plugins.github_plugin import GitHubPlugin

sys.path.append("..")

from plugins.base_plugin import EXPORTS_DIR

TEMP_DIR = "temp"
FRONTEND_BUILD = "frontend_build"


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)
    yield
    shutil.rmtree(TEMP_DIR)
    shutil.rmtree(EXPORTS_DIR)


app = FastAPI(lifespan=lifespan)


app.mount("/exports", StaticFiles(directory=EXPORTS_DIR), name="exports")

# Frontend served in the container:
if Path(FRONTEND_BUILD).exists():
    app.mount("/ui", StaticFiles(directory=FRONTEND_BUILD, html=True), name="frontend")

origins = ["http://localhost:3000", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root_redirect():
    return RedirectResponse(url="/ui")


@app.get("/ui")
def serve_root():
    return FileResponse(f"{FRONTEND_BUILD}/index.html")


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/run-plugin")
def run_plugin(
    plugin_type: str = Form(...),
    repo_url: str = Form(None),
    file: UploadFile = File(None),
    user: str = Depends(get_current_user),
):
    if plugin_type == "github":
        plugin = GitHubPlugin(repo_url)
    elif plugin_type == "csv":
        filename = f"{TEMP_DIR}/{uuid4()}_{file.filename}"
        with open(filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        plugin = CSVPlugin(filename)
    else:
        raise HTTPException(status_code=400, detail="Unknown plugin")

    result = plugin.fetch_data()

    # Log to database
    session = Session()
    log_entry = PipelineLog(username=user, plugin_name=plugin_type, result_data=result)
    session.add(log_entry)
    session.commit()

    return {"success": True, "download_url": result["download_url"]}


@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join("exports", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
