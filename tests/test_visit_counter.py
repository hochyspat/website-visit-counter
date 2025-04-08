import pytest
from unittest.mock import patch, MagicMock
from aiohttp import web
from VisitCounter import VisitCounter


@pytest.fixture
def mock_request():
    req = MagicMock()
    req.remote = "127.0.0.1"
    return req


@pytest.fixture
def visit_counter():
    return VisitCounter()


@patch("VisitCounter.VisitCounter.save_log")
@patch("VisitCounter.ApiManager.api_visits_all", return_value=11)
@pytest.mark.asyncio
async def test_handle_request(mock_api_visits_all, mock_save_log, visit_counter, mock_request):
    response = await visit_counter.handle(mock_request)

    mock_save_log.assert_called_once()
    mock_api_visits_all.assert_called_once()

    assert isinstance(response, web.Response)
    assert response.text == "Сайт посетили 12 раз(а)"
