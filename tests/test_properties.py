import copy

import pytest

from lvgl_mpy_studio.core.model import widget_definitions
from lvgl_mpy_studio.ui.properties.panel import DESCRIPTOR_ROLE, PropertiesPanel
from lvgl_mpy_studio.ui.document import ProjectDocument


def value_items(model):
    result = []
    def visit(parent):
        for row in range(model.rowCount(parent)):
            label = model.index(row, 0, parent)
            value = model.index(row, 1, parent)
            if value.data(DESCRIPTOR_ROLE):
                result.append(value)
            visit(label)
    visit(model.index(-1, -1)) if False else visit(model.invisibleRootItem().index())
    return result


def test_name_validation_and_rename_updates_handler(qtbot):
    document = ProjectDocument()
    document.project.add_widget(document.project.pages[0], "button")
    document.project.ensure_handler("button1")
    panel = PropertiesPanel(document)
    qtbot.addWidget(panel)
    panel.set_selection(["button1"])
    name = next(item for item in value_items(panel.model) if item.data(DESCRIPTOR_ROLE)["name"] == "Name")
    panel.model.setData(name, "class")
    assert document.project.find_widget("button1")
    assert not panel.error.isHidden()
    name = next(item for item in value_items(panel.model) if item.data(DESCRIPTOR_ROLE)["name"] == "Name")
    panel.model.setData(name, "ok_button")
    assert document.project.find_widget("ok_button")
    assert "ok_button_clicked" in document.project.code.handlers


def test_multiselection_edit_is_one_macro(qtbot):
    document = ProjectDocument()
    document.project.add_widget(document.project.pages[0], "button")
    document.project.add_widget(document.project.pages[0], "button")
    initial = copy.deepcopy(document.project.to_dict())
    panel = PropertiesPanel(document)
    qtbot.addWidget(panel)
    panel.set_selection(["button1", "button2"])
    item = next(item for item in value_items(panel.model) if item.data(DESCRIPTOR_ROLE)["name"] == "x")
    panel.model.setData(item, "77")
    assert [widget.props["x"] for widget in document.project.widgets] == [77, 77]
    document.undo_stack.undo()
    assert document.project.to_dict() == initial


def test_event_double_click_creates_handler(qtbot):
    document = ProjectDocument()
    document.project.add_widget(document.project.pages[0], "button")
    panel = PropertiesPanel(document)
    qtbot.addWidget(panel)
    panel.set_selection(["button1"])
    with qtbot.waitSignal(panel.handlerRequested, timeout=1000) as signal:
        panel._event_activated(panel.events_model.index(0, 0))
    assert signal.args == ["button1", "CLICKED"]
    assert "button1_clicked" in document.project.code.handlers


@pytest.mark.parametrize("kind", list(widget_definitions()))
def test_every_schema_property_can_be_edited(qtbot, kind):
    document = ProjectDocument()
    document.project.add_widget(document.project.pages[0], kind, name=f"{kind}1")
    panel = PropertiesPanel(document)
    qtbot.addWidget(panel)
    panel.set_selection([f"{kind}1"])
    expected = {item["name"] for item in widget_definitions()[kind]["properties"]}
    items = {item.data(DESCRIPTOR_ROLE)["name"]: item for item in value_items(panel.model)}
    assert expected <= set(items)
    for name in list(items):
        if name == "Name":
            continue
        items = {item.data(DESCRIPTOR_ROLE)["name"]: item for item in value_items(panel.model)}
        descriptor = items[name].data(DESCRIPTOR_ROLE)
        value = "2" if descriptor["type"] == "number" else "true" if descriptor["type"] == "boolean" else (descriptor.get("options") or ["prova"])[0]
        panel.model.setData(items[name], value)
        actual = document.project.find_widget(f"{kind}1").props[name]
        assert actual == (2 if descriptor["type"] == "number" else True if descriptor["type"] == "boolean" else value)
        panel.set_selection([f"{kind}1"])
        items = {item.data(DESCRIPTOR_ROLE)["name"]: item for item in value_items(panel.model)}
