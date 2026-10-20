from typing import Iterator

import pytest
import requests


@pytest.fixture
def session() -> Iterator[requests.Session]:
    with requests.Session() as sesion:
        yield sesion
