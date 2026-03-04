from typing import Any

from trello_mcp.client import TrelloClient


def _format_card(c: dict[str, Any]) -> dict[str, Any]:
    """Format a raw Trello card API response into a consistent output shape."""
    return {
        "id": c["id"],
        "name": c["name"],
        "description": c.get("desc", ""),
        "url": c.get("url", ""),
        "closed": c.get("closed", False),
        "list_id": c.get("idList", ""),
        "board_id": c.get("idBoard", ""),
        "position": c.get("pos"),
        "due": c.get("due"),
        "due_complete": c.get("dueComplete", False),
        "labels": [
            {"id": lb["id"], "name": lb.get("name", ""), "color": lb.get("color", "")}
            for lb in c.get("labels", [])
        ],
        "idChecklists": c.get("idChecklists", []),
        "idMembers": c.get("idMembers", []),
        "idAttachmentCover": c.get("idAttachmentCover"),
        "id_short": c.get("idShort"),
        "short_url": c.get("shortUrl"),
        "date_last_activity": c.get("dateLastActivity"),
        "badges": c.get("badges"),
    }


async def get_list_cards(list_id: str) -> list[dict[str, Any]]:
    """Return all cards in a list."""
    client = TrelloClient()
    cards = await client.get(f"/lists/{list_id}/cards")
    return [_format_card(c) for c in cards]


async def get_board_cards(board_id: str) -> list[dict[str, Any]]:
    """Return all cards on a board."""
    client = TrelloClient()
    cards = await client.get(f"/boards/{board_id}/cards")
    return [_format_card(c) for c in cards]


async def get_card(card_id: str) -> dict[str, Any]:
    """Return full details of a single card, including checklist IDs, members, badges, and metadata."""
    client = TrelloClient()
    c = await client.get(f"/cards/{card_id}", params={"checklists": "all"})
    return _format_card(c)


async def create_card(
    list_id: str,
    name: str,
    description: str = "",
    position: str = "bottom",
    due: str | None = None,
    label_ids: list[str] | None = None,
    member_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Create a new card in a list."""
    client = TrelloClient()
    params: dict[str, Any] = {
        "idList": list_id,
        "name": name,
        "pos": position,
    }
    if description:
        params["desc"] = description
    if due:
        params["due"] = due
    if label_ids:
        params["idLabels"] = ",".join(label_ids)
    if member_ids:
        params["idMembers"] = ",".join(member_ids)

    c = await client.post("/cards", params=params)
    return _format_card(c)


async def update_card(
    card_id: str,
    name: str | None = None,
    description: str | None = None,
    closed: bool | None = None,
    list_id: str | None = None,
    board_id: str | None = None,
    position: str | None = None,
    due: str | None = None,
    due_complete: bool | None = None,
    label_ids: list[str] | None = None,
    member_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Update fields on a card."""
    client = TrelloClient()
    params: dict[str, Any] = {}
    if name is not None:
        params["name"] = name
    if description is not None:
        params["desc"] = description
    if closed is not None:
        params["closed"] = str(closed).lower()
    if list_id is not None:
        params["idList"] = list_id
    if board_id is not None:
        params["idBoard"] = board_id
    if position is not None:
        params["pos"] = position
    if due is not None:
        params["due"] = due
    if due_complete is not None:
        params["dueComplete"] = str(due_complete).lower()
    if label_ids is not None:
        params["idLabels"] = ",".join(label_ids)
    if member_ids is not None:
        params["idMembers"] = ",".join(member_ids)

    c = await client.put(f"/cards/{card_id}", params=params)
    return _format_card(c)


async def move_card(card_id: str, list_id: str, board_id: str | None = None) -> dict[str, Any]:
    """Move a card to a different list (and optionally a different board)."""
    return await update_card(card_id, list_id=list_id, board_id=board_id)


async def archive_card(card_id: str) -> dict[str, Any]:
    """Archive (close) a card."""
    return await update_card(card_id, closed=True)


def _format_comment(action: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": action["id"],
        "text": action.get("data", {}).get("text", ""),
        "date": action.get("date", ""),
        "member": action.get("memberCreator", {}).get("fullName", ""),
        "username": action.get("memberCreator", {}).get("username", ""),
    }


async def get_card_comments(card_id: str) -> list[dict[str, Any]]:
    """Return all comments on a card."""
    client = TrelloClient()
    actions = await client.get(
        f"/cards/{card_id}/actions", params={"filter": "commentCard"}
    )
    return [_format_comment(a) for a in actions]


async def add_card_comment(card_id: str, text: str) -> dict[str, Any]:
    """Add a comment to a card."""
    client = TrelloClient()
    action = await client.post(
        f"/cards/{card_id}/actions/comments", params={"text": text}
    )
    return _format_comment(action)
