import os
import sys
from unittest.mock import patch

import pytest

# Add the root of the project to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(autouse=True)
def patch_exports_dir(tmp_path):
    with (
        patch("plugins.csv_plugin.EXPORTS_DIR", str(tmp_path)),
        patch("plugins.github_plugin.EXPORTS_DIR", str(tmp_path)),
        patch("api.main.TEMP_DIR", str(tmp_path)),
        patch("api.main.FRONTEND_BUILD", str(tmp_path)),
    ):
        yield
