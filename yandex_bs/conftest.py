import pytest
from django.test import RequestFactory


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()


def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker('django_db')
