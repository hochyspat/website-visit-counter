from unittest.mock import MagicMock, patch

import pytest
from aiohttp import web

from visit_counter import VisitCounter


@pytest.fixture
def mock_request():
    req = MagicMock()
    req.remote = "127.0.0.1"
    return req


@pytest.fixture
def visit_counter():
    return VisitCounter()


@patch("visit_counter.VisitCounter.save_log")
@patch("visit_counter.ApiManager.api_visits_all", return_value=11)
@pytest.mark.asyncio
async def test_handle_request(
    mock_api_visits_all, mock_save_log, visit_counter, mock_request
):
    response = await visit_counter.handle(mock_request)

    mock_save_log.assert_called_once()
    mock_api_visits_all.assert_called_once()

    assert isinstance(response, web.Response)
    assert response.text == "Сайт посетили 12 раз(а)"
