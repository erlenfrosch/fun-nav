import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="Integrationstests ausführen (erfordert laufenden GraphHopper-Service)",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "integration: erfordert laufenden GraphHopper-Service (--integration)",
    )


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--integration"):
        skip = pytest.mark.skip(reason="Nur mit --integration ausführen")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip)
