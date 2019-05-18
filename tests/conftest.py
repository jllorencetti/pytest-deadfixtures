import pytest

pytest_plugins = "pytester"


@pytest.fixture()
def message_template():
    return "Fixture name: {}, location: {}.py"
