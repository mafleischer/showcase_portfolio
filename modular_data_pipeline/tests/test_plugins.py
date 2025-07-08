import os
from unittest import mock

import pandas as pd
from plugins.csv_plugin import CSVPlugin


def test_csv_plugin(tmp_path):
    sample_csv = tmp_path / "sample.csv"
    sample_csv.write_text("name,age\nAlice,30\nBob,25")
    plugin = CSVPlugin(str(sample_csv))
    result = plugin.fetch_data()

    assert "download_url" in result
    filepath = tmp_path / result["download_url"].split("/")[-1]
    assert os.path.exists(filepath)

    df = pd.read_excel(filepath)
    assert df.shape == (2, 2)
    assert "name" in df.columns
    assert "age" in df.columns
