# tests/conftest.py
import pytest
from wireup import DependencyContainer

from wireup.integration.fastapi import get_container

from crypto_tracker.configs.settings import Settings
from tests.utils import get_source_file_from_root


@pytest.fixture
def container(app) -> DependencyContainer:
    return get_container(app)

@pytest.fixture
def settings() -> Settings:
    return Settings(_env_file=get_source_file_from_root("/test.env"), _env_file_encoding='utf-8')