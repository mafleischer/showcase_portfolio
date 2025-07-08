import os
import tempfile
import uuid
import zipfile

import pandas as pd
from git import Repo

from .base_plugin import EXPORTS_DIR, BasePlugin


class GitHubPlugin(BasePlugin):
    def __init__(self, repo_url: str):
        self.repo_url = repo_url

    def fetch_data(self) -> dict:
        temp_dir = tempfile.mkdtemp()
        Repo.clone_from(self.repo_url, temp_dir)

        export_dir = tempfile.mkdtemp()
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(".csv"):
                    csv_path = os.path.join(root, file)
                    df = pd.read_csv(csv_path)
                    xlsx_path = os.path.join(export_dir, file.replace(".csv", ".xlsx"))
                    df.to_excel(xlsx_path, index=False)

        zip_filename = f"{uuid.uuid4()}.zip"
        zip_path = os.path.join(EXPORTS_DIR, zip_filename)
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file in os.listdir(export_dir):
                zipf.write(os.path.join(export_dir, file), arcname=file)

        return {"download_url": f"/download/{zip_filename}"}
