import pathlib
import pytest
from fastflows.core.catalog import FlowCatalog

flows_home_path = pathlib.Path("tests/test_data/flows")

FlowCatalog().set_flows_path(flows_home_path)


def pytest_configure(config):
    config.addinivalue_line("markers", "unit: run only unit tests")


@pytest.fixture
def flows_folder() -> pathlib.Path:
    current_folder = pathlib.Path(__file__).parent
    return current_folder / "test_data" / "flows"
