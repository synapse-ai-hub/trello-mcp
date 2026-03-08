import json
from typing import Annotated, Any

from mcp import types
from mcp.server.fastmcp import FastMCP

from trello_mcp.exceptions import TrelloError
from trello_mcp.tools import attachments, boards, cards, checklists, labels, lists, members, search

mcp = FastMCP("trello")


def _format(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)


def _ok(data: Any) -> types.CallToolResult:
    return types.CallToolResult(
        content=[types.TextContent(type="text", text=_format(data))],
        structured_content=data,
    )


def _error(exc: TrelloError) -> types.CallToolResult:
    data = {"error": str(exc), "status_code": exc.status_code}
    return types.CallToolResult(
        content=[types.TextContent(type="text", text=_format(data))],
        structured_content=data,
        is_error=True,
    )


# ── Boards ───────────────────────────────────────────────────────────────────


@mcp.tool()
async def list_my_boards() -> types.CallToolResult:
    """List all boards for the authenticated Trello user."""
    try:
        result = await boards.list_my_boards()
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def get_board(
    board_id: Annotated[str, "The ID of the board"],
) -> types.CallToolResult:
    """Get details of a single Trello board."""
    try:
        result = await boards.get_board(board_id)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


# ── Lists ────────────────────────────────────────────────────────────────────


@mcp.tool()
async def get_board_lists(
    board_id: Annotated[str, "The ID of the board"],
) -> types.CallToolResult:
    """Get all lists on a Trello board."""
    try:
        result = await lists.get_board_lists(board_id)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def create_list(
    board_id: Annotated[str, "The ID of the board"],
    name: Annotated[str, "Name for the new list"],
    position: Annotated[str, "Position: top, bottom, or a positive number"] = "bottom",
) -> types.CallToolResult:
    """Create a new list on a Trello board."""
    try:
        result = await lists.create_list(board_id, name, position)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


# ── Cards ────────────────────────────────────────────────────────────────────


@mcp.tool()
async def get_list_cards(
    list_id: Annotated[str, "The ID of the list"],
) -> types.CallToolResult:
    """Get all cards in a Trello list."""
    try:
        result = await cards.get_list_cards(list_id)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def get_board_cards(
    board_id: Annotated[str, "The ID of the board"],
) -> types.CallToolResult:
    """Get all cards on a Trello board."""
    try:
        result = await cards.get_board_cards(board_id)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def get_card(
    card_id: Annotated[str, "The ID of the card"],
) -> types.CallToolResult:
    """Get details of a single Trello card."""
    try:
        result = await cards.get_card(card_id)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def create_card(
    list_id: Annotated[str, "The ID of the list to add the card to"],
    name: Annotated[str, "Card title"],
    description: Annotated[str, "Card description (Markdown supported)"] = "",
    position: Annotated[str, "Position: top, bottom, or a positive number"] = "bottom",
    due: Annotated[str | None, "Due date in ISO 8601 format (e.g. 2025-12-31T12:00:00Z)"] = None,
    label_ids: Annotated[list[str] | None, "List of label IDs to attach"] = None,
    member_ids: Annotated[list[str] | None, "List of member IDs to assign"] = None,
) -> types.CallToolResult:
    """Create a new card in a Trello list."""
    try:
        result = await cards.create_card(
            list_id, name, description, position, due, label_ids, member_ids
        )
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def update_card(
    card_id: Annotated[str, "The ID of the card to update"],
    name: Annotated[str | None, "New card title"] = None,
    description: Annotated[str | None, "New description"] = None,
    closed: Annotated[bool | None, "True to archive, False to unarchive"] = None,
    list_id: Annotated[str | None, "Move to this list"] = None,
    board_id: Annotated[str | None, "Move to this board"] = None,
    position: Annotated[str | None, "New position: top, bottom, or a number"] = None,
    due: Annotated[str | None, "Due date in ISO 8601 format"] = None,
    due_complete: Annotated[bool | None, "Mark due date as complete"] = None,
    label_ids: Annotated[list[str] | None, "Replace labels with these IDs"] = None,
    member_ids: Annotated[list[str] | None, "Replace members with these IDs"] = None,
) -> types.CallToolResult:
    """Update one or more fields on a Trello card."""
    try:
        result = await cards.update_card(
            card_id,
            name=name,
            description=description,
            closed=closed,
            list_id=list_id,
            board_id=board_id,
            position=position,
            due=due,
            due_complete=due_complete,
            label_ids=label_ids,
            member_ids=member_ids,
        )
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def move_card(
    card_id: Annotated[str, "The ID of the card to move"],
    list_id: Annotated[str, "The ID of the destination list"],
    board_id: Annotated[str | None, "The ID of the destination board (if cross-board move)"] = None,
) -> types.CallToolResult:
    """Move a Trello card to a different list (and optionally a different board)."""
    try:
        result = await cards.move_card(card_id, list_id, board_id)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def archive_card(
    card_id: Annotated[str, "The ID of the card to archive"],
) -> types.CallToolResult:
    """Archive (close) a Trello card."""
    try:
        result = await cards.archive_card(card_id)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def get_card_comments(
    card_id: Annotated[str, "The ID of the card"],
) -> types.CallToolResult:
    """Get all comments on a Trello card."""
    try:
        result = await cards.get_card_comments(card_id)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def add_card_comment(
    card_id: Annotated[str, "The ID of the card"],
    text: Annotated[str, "The comment text"],
) -> types.CallToolResult:
    """Add a comment to a Trello card."""
    try:
        result = await cards.add_card_comment(card_id, text)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


# ── Attachments ─────────────────────────────────────────────────────────────


@mcp.tool()
async def get_card_attachments(
    card_id: Annotated[str, "The ID of the card"],
) -> types.CallToolResult:
    """Get all attachments on a Trello card."""
    try:
        result = await attachments.get_card_attachments(card_id)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def add_card_attachment(
    card_id: Annotated[str, "The ID of the card"],
    file_path: Annotated[str, "Absolute path to the file to upload"],
    name: Annotated[str | None, "Display name for the attachment (defaults to filename)"] = None,
) -> types.CallToolResult:
    """Upload a file as an attachment to a Trello card."""
    try:
        result = await attachments.add_card_attachment(card_id, file_path, name)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def add_card_url_attachment(
    card_id: Annotated[str, "The ID of the card"],
    url: Annotated[str, "The URL to attach"],
    name: Annotated[str | None, "Display name for the attachment"] = None,
) -> types.CallToolResult:
    """Attach a URL to a Trello card."""
    try:
        result = await attachments.add_card_url_attachment(card_id, url, name)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def delete_card_attachment(
    card_id: Annotated[str, "The ID of the card"],
    attachment_id: Annotated[str, "The ID of the attachment to delete"],
) -> types.CallToolResult:
    """Delete an attachment from a Trello card."""
    try:
        result = await attachments.delete_card_attachment(card_id, attachment_id)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


# ── Labels ───────────────────────────────────────────────────────────────────


@mcp.tool()
async def get_board_labels(
    board_id: Annotated[str, "The ID of the board"],
) -> types.CallToolResult:
    """Get all labels on a Trello board."""
    try:
        result = await labels.get_board_labels(board_id)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def create_label(
    board_id: Annotated[str, "The ID of the board"],
    name: Annotated[str, "Label name"],
    color: Annotated[
        str,
        "Label color: yellow, purple, blue, red, green, orange, black, sky, pink, lime",
    ] = "blue",
) -> types.CallToolResult:
    """Create a label on a Trello board."""
    try:
        result = await labels.create_label(board_id, name, color)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


# ── Checklists ───────────────────────────────────────────────────────────────


@mcp.tool()
async def get_checklist(
    checklist_id: Annotated[str, "The ID of the checklist"],
) -> types.CallToolResult:
    """Get a checklist and its items."""
    try:
        result = await checklists.get_checklist(checklist_id)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def create_checklist(
    card_id: Annotated[str, "The ID of the card"],
    name: Annotated[str, "Checklist name"],
) -> types.CallToolResult:
    """Create a checklist on a Trello card."""
    try:
        result = await checklists.create_checklist(card_id, name)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def add_checklist_item(
    checklist_id: Annotated[str, "The ID of the checklist"],
    name: Annotated[str, "Item text"],
    checked: Annotated[bool, "Whether the item starts checked"] = False,
) -> types.CallToolResult:
    """Add an item to a Trello checklist."""
    try:
        result = await checklists.add_checklist_item(checklist_id, name, checked)
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


@mcp.tool()
async def update_checklist_item(
    card_id: Annotated[str, "The ID of the card that contains the checklist"],
    check_item_id: Annotated[str, "The ID of the checklist item to update"],
    checked: Annotated[bool, "True to mark as done, False to mark as not done"],
) -> types.CallToolResult:
    """Mark a checklist item as done (checked) or not done (unchecked)."""
    try:
        result = await checklists.update_checklist_item(
            card_id, check_item_id, checked
        )
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


# ── Members ──────────────────────────────────────────────────────────────────


@mcp.tool()
async def get_me() -> types.CallToolResult:
    """Get the authenticated Trello member's profile."""
    try:
        result = await members.get_me()
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


# ── Search ───────────────────────────────────────────────────────────────────


@mcp.tool()
async def search_trello(
    query: Annotated[str, "Search query string"],
    model_types: Annotated[str, "Comma-separated types to search: cards, boards"] = "cards,boards",
    board_ids: Annotated[list[str] | None, "Limit search to these board IDs"] = None,
    cards_limit: Annotated[int, "Max number of cards to return"] = 10,
    boards_limit: Annotated[int, "Max number of boards to return"] = 5,
) -> types.CallToolResult:
    """Search Trello for cards and/or boards matching a query."""
    try:
        result = await search.search_trello(
            query, model_types, board_ids, cards_limit, boards_limit
        )
        return _ok(result)
    except TrelloError as exc:
        return _error(exc)


# ── Entry point ──────────────────────────────────────────────────────────────


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
