from unittest.mock import patch

import pytest

from src.api_manager import ApiManager


@pytest.fixture
def mock_logs():
    return [
        ("127.0.0.1", "2025-04-07"),
        ("127.0.0.2", "2025-04-07"),
        ("127.0.0.1", "2025-04-08"),
        ("127.0.0.1", "2025-04-01"),
        ("192.168.0.1", "2025-03-21"),
    ]


@pytest.fixture
def api_manager(mock_logs):
    with patch("src.api_manager.LoadManager") as MockLoadManager:
        mock_loader_instance = MockLoadManager.return_value
        mock_loader_instance.load_logs.return_value = mock_logs
        api = ApiManager("fake_file.txt")
        return api


def test_total_visits(api_manager):
    assert api_manager.api_visits_all() == 5


def test_visits_day(api_manager):
    assert api_manager.api_visits_day("2025-04-07") == 2


def test_visits_month(api_manager):
    assert api_manager.api_visits_month(r"2025-04-\d{2}") == 4


def test_visits_year(api_manager):
    assert api_manager.api_visits_year(r"2025-\d{2}-\d{2}") == 5


def test_uniq_visits_day(api_manager):
    assert api_manager.api_uniq_visits_day("127.0.0.1", "2025-04-07") == 1


def test_uniq_visits_all(api_manager):
    assert api_manager.api_uniq_visits_all("192.168.0.1") == 1
