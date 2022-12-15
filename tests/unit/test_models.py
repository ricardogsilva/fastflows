import pytest

from fastflows.core.catalog import FlowCatalog
from fastflows.providers.base import BaseProvider

pytestmark = pytest.mark.unit


def test_singletons_work_correctly():
    assert FlowCatalog() != BaseProvider()
