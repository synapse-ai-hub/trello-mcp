import pytest

from trello_mcp.tools.cards import (
    archive_card,
    create_card,
    get_card,
    get_list_cards,
    move_card,
    update_card,
)

SAMPLE_CARD = {
    "id": "c1",
    "name": "My Card",
    "desc": "Card description",
    "url": "https://trello.com/c/c1",
    "closed": False,
    "idList": "list1",
    "idBoard": "board1",
    "pos": 16384,
    "due": None,
    "dueComplete": False,
    "labels": [{"id": "lb1", "name": "Bug", "color": "red"}],
}


@pytest.mark.asyncio
async def test_get_list_cards(httpx_mock):
    httpx_mock.add_response(json=[SAMPLE_CARD])
    result = await get_list_cards("list1")
    assert len(result) == 1
    assert result[0]["id"] == "c1"
    assert result[0]["name"] == "My Card"
    assert result[0]["list_id"] == "list1"
    assert result[0]["labels"][0]["name"] == "Bug"


@pytest.mark.asyncio
async def test_get_card(httpx_mock):
    """get_card returns core fields; new fields default to empty/None when not in API response."""
    httpx_mock.add_response(json=SAMPLE_CARD)
    result = await get_card("c1")
    assert result["id"] == "c1"
    assert result["description"] == "Card description"
    assert result["board_id"] == "board1"
    assert result["idChecklists"] == []
    assert result["idMembers"] == []


@pytest.mark.asyncio
async def test_create_card(httpx_mock):
    httpx_mock.add_response(json=SAMPLE_CARD)
    result = await create_card("list1", "My Card", description="Card description")
    assert result["id"] == "c1"
    assert result["name"] == "My Card"
    request = httpx_mock.get_request()
    assert "name=My+Card" in str(request.url) or "name=My%20Card" in str(request.url)


@pytest.mark.asyncio
async def test_update_card(httpx_mock):
    updated = {**SAMPLE_CARD, "name": "Updated Card"}
    httpx_mock.add_response(json=updated)
    result = await update_card("c1", name="Updated Card")
    assert result["name"] == "Updated Card"


@pytest.mark.asyncio
async def test_move_card(httpx_mock):
    moved = {**SAMPLE_CARD, "idList": "list2"}
    httpx_mock.add_response(json=moved)
    result = await move_card("c1", "list2")
    assert result["list_id"] == "list2"


@pytest.mark.asyncio
async def test_archive_card(httpx_mock):
    archived = {**SAMPLE_CARD, "closed": True}
    httpx_mock.add_response(json=archived)
    result = await archive_card("c1")
    assert result["closed"] is True


@pytest.mark.asyncio
async def test_get_card_sends_checklists_param_to_api(httpx_mock):
    """get_card requests checklists from the API so the response includes idChecklists."""
    httpx_mock.add_response(json=SAMPLE_CARD)
    await get_card("c1")
    request = httpx_mock.get_request()
    assert "checklists=all" in str(request.url) or "checklists%3Dall" in str(request.url)


@pytest.mark.asyncio
async def test_get_card_includes_id_checklists_id_members_badges_and_metadata(httpx_mock):
    """get_card returns idChecklists, idMembers, badges, idAttachmentCover, id_short, short_url, date_last_activity when the API provides them."""
    full_card = {
        **SAMPLE_CARD,
        "idChecklists": ["cl1", "cl2"],
        "idMembers": ["m1"],
        "idAttachmentCover": "att1",
        "idShort": 42,
        "shortUrl": "https://trello.com/c/abc",
        "dateLastActivity": "2025-01-15T10:30:00.000Z",
        "badges": {
            "comments": 2,
            "attachments": 1,
            "checkItemsChecked": 1,
            "checkItems": 3,
        },
    }
    httpx_mock.add_response(json=full_card)
    result = await get_card("c1")
    assert result["idChecklists"] == ["cl1", "cl2"]
    assert result["idMembers"] == ["m1"]
    assert result["idAttachmentCover"] == "att1"
    assert result["id_short"] == 42
    assert result["short_url"] == "https://trello.com/c/abc"
    assert result["date_last_activity"] == "2025-01-15T10:30:00.000Z"
    assert result["badges"]["comments"] == 2
    assert result["badges"]["attachments"] == 1
    assert result["badges"]["checkItemsChecked"] == 1
    assert result["badges"]["checkItems"] == 3
