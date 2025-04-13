import pytest
import os
import sys
import pathlib

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))


@pytest.fixture(scope="session", autouse=True)
def setup_data_dir():
    data_dir = pathlib.Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
