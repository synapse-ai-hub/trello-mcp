import pytest

from trello_mcp.tools.checklists import (
    add_checklist_item,
    get_checklist,
    update_checklist_item,
)


@pytest.mark.asyncio
async def test_get_checklist_returns_items_with_state(httpx_mock):
    httpx_mock.add_response(
        json={
            "id": "cl1",
            "name": "Tasks",
            "idCard": "c1",
            "checkItems": [
                {"id": "ci1", "name": "Do thing", "state": "complete", "pos": 1},
                {"id": "ci2", "name": "Other", "state": "incomplete", "pos": 2},
            ],
        }
    )
    result = await get_checklist("cl1")
    assert result["id"] == "cl1"
    assert result["name"] == "Tasks"
    assert result["card_id"] == "c1"
    assert len(result["items"]) == 2
    assert result["items"][0]["id"] == "ci1"
    assert result["items"][0]["state"] == "complete"
    assert result["items"][1]["id"] == "ci2"
    assert result["items"][1]["state"] == "incomplete"


@pytest.mark.asyncio
async def test_update_checklist_item_marks_complete(httpx_mock):
    httpx_mock.add_response(
        json={"id": "ci1", "name": "Do thing", "state": "complete"}
    )
    result = await update_checklist_item("c1", "ci1", checked=True)
    assert result["id"] == "ci1"
    assert result["state"] == "complete"
    request = httpx_mock.get_request()
    assert request.method == "PUT"
    assert "/cards/c1/checkItem/ci1" in str(request.url)
    assert "state=complete" in str(request.url)


@pytest.mark.asyncio
async def test_update_checklist_item_marks_incomplete(httpx_mock):
    httpx_mock.add_response(
        json={"id": "ci1", "name": "Do thing", "state": "incomplete"}
    )
    result = await update_checklist_item("c1", "ci1", checked=False)
    assert result["state"] == "incomplete"
    request = httpx_mock.get_request()
    assert "state=incomplete" in str(request.url)
