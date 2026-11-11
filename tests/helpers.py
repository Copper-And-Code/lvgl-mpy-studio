"""Helpers shared by test files."""

import json

from lvgl_mpy_studio import mcp_server


def call(tool, /, **arguments):
    """The result of an MCP tool, called as a client does."""
    return mcp_server.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": tool, "arguments": arguments}})["result"]


def payload(result):
    """The JSON answer of a tool that succeeded."""
    assert not result.get("isError"), result
    return json.loads(result["content"][0]["text"])


def error(result):
    """The message of a tool that failed."""
    assert result.get("isError"), result
    return result["content"][0]["text"]


def find_item(panel, name):
    """The value item of the property name in a properties panel, inside any group."""
    from lvgl_mpy_studio.ui.properties.panel import DESCRIPTOR_ROLE

    def visit(parent):
        for row in range(parent.rowCount()):
            label, value = parent.child(row, 0), parent.child(row, 1)
            if value is not None and (value.data(DESCRIPTOR_ROLE) or {}).get("name") == name:
                return value
            found = visit(label) if label is not None else None
            if found is not None:
                return found
        return None

    return visit(panel.model.invisibleRootItem())
