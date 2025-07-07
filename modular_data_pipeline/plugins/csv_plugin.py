import os
import uuid

import pandas as pd

from .base_plugin import BasePlugin


class CSVPlugin(BasePlugin):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def fetch_data(self) -> dict:
        df = pd.read_csv(self.filepath)
        output_path = f"exports/{uuid.uuid4()}.xlsx"
        df.to_excel(output_path, index=False)
        return {"download_url": f"/download/{os.path.basename(output_path)}"}
