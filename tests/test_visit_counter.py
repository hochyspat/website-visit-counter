from unittest.mock import MagicMock, patch

import pytest
from aiohttp import web

from src.visit_counter import VisitCounter


@pytest.fixture
def mock_request() -> MagicMock:
    req = MagicMock()
    req.remote = "127.0.0.1"
    return req


@pytest.fixture
def visit_counter() -> VisitCounter:
    return VisitCounter()


@patch("src.visit_counter.VisitCounter.save_log")
@patch("src.api_manager.ApiManager.api_visits_all", return_value=12)
@pytest.mark.asyncio
async def test_handle_request(
    mock_api_visits_all: MagicMock,
    mock_save_log: MagicMock,
    visit_counter: VisitCounter,
    mock_request: MagicMock,
) -> None:
    response = await visit_counter.handle(mock_request)

    mock_save_log.assert_called_once()
    mock_api_visits_all.assert_called_once()

    assert isinstance(response, web.Response)
    assert response.text == "Сайт посетили 12 раз(а)"
