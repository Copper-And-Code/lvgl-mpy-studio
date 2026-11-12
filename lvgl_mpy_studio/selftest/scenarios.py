"""The scenarios of the self-test. Each one starts from a new window and an empty folder."""

from lvgl_mpy_studio.core.model import Project

SCENARIOS = {}


def scenario(name, title):
    def register(function):
        SCENARIOS[name] = (title, function)
        return function

    return register


def build_counter(ide):
    """A button and a label, placed and set as a person would; return their names."""
    with ide.step("Create a new project"):
        ide.choose(ide.window.new_action)
        ide.equal([len(page.widgets) for page in ide.project.pages], [0], "widgets on the pages of a new project")
    with ide.step("Add a button from the toolbox"):
        button = ide.add_widget("button", 60, 40)
        ide.equal(ide.project.find_widget(button).type, "button", "type of the widget added")
    with ide.step("Add a label from the toolbox"):
        label = ide.add_widget("label", 60, 140)
        ide.equal(ide.project.find_widget(label).type, "label", "type of the widget added")
    with ide.step("The page draws both widgets with LVGL"):
        drawn = ide.wait_preview()
        ide.check(ide.drawn(button) is not None and ide.drawn(label) is not None, "a widget is missing from the page")
    with ide.step("Set the button's properties in the Properties panel"):
        ide.select(button)
        for name, value in (("x", 40), ("y", 30), ("width", 200), ("height", 80), ("text", "Press me")):
            ide.set_property(name, value)
    with ide.step("Set the label's properties in the Properties panel"):
        ide.select(label)
        for name, value in (("x", 40), ("y", 150), ("width", 300), ("text", "Not pressed"), ("fontSize", 24)):
            ide.set_property(name, value)
    with ide.step("The page is drawn again with the new properties"):
        ide.check(ide.wait_preview() != drawn, "the picture of the page did not change")
    with ide.step("Undo and redo the last change"):
        ide.choose(ide.window.undo_action)
        ide.equal(ide.project.find_widget(label).props["fontSize"], 14, "font size after Undo")
        ide.choose(ide.window.redo_action)
        ide.equal(ide.project.find_widget(label).props["fontSize"], 24, "font size after Redo")
    return button, label


@scenario("tour", "Full tour: project, widgets, properties, code, simulator")
def tour(ide):
    button, label = build_counter(ide)
    with ide.step("Create the button's CLICKED handler from the Events tab"):
        ide.select(button)
        handler = ide.open_handler("CLICKED")
        ide.check(handler in ide.project.code.handlers, f"the project has no handler {handler}")
    with ide.step("Type the handler's code in the editor"):
        code = f'ui.{label}.set_text("Pressed")\nprint("SELFTEST handler ran")'
        ide.type_code(code)
        ide.equal(ide.project.code.handlers[handler].body, code, "code stored for the handler")
    with ide.step("Save the project with Save As"):
        ide.save_as(ide.directory / "tour.json")
    with ide.step("Start the simulator"):
        ide.run()
        ide.check("SELFTEST handler ran" not in ide.output(), "the handler ran before any touch")
    with ide.step("Touch the button in the simulator: the handler runs and the screen changes"):
        before = ide.frame()
        ide.tap(140, 70)
        ide.wait(lambda: "SELFTEST handler ran" in ide.output(), "the handler's line in the Output panel")
        ide.wait(lambda: ide.frame() != before, "the screen of the simulator to change")
        ide.check(not ide.window.errors.topLevelItemCount(), "the Errors panel is not empty")
    with ide.step("Stop the simulator"):
        ide.stop()
        ide.check(ide.window.properties.isEnabled(), "the Properties panel stayed disabled after Stop")


@scenario("save", "Save, close and open again")
def save_and_reopen(ide):
    button, label = build_counter(ide)
    path = ide.directory / "saved.json"
    with ide.step("Save the project with Save As"):
        ide.save_as(path)
        ide.check(not ide.window.document.modified, "the project is still marked as changed after saving")
    with ide.step("The file on disk holds what was drawn"):
        stored = Project.load(path)
        ide.equal(stored.find_widget(button).props["text"], "Press me", "text of the button in the file")
        ide.equal({name: stored.find_widget(label).props[name] for name in ("x", "y", "width", "text", "fontSize")}, {"x": 40, "y": 150, "width": 300, "text": "Not pressed", "fontSize": 24}, "label in the file")
    with ide.step("Change a property, then Save"):
        ide.select(label)
        ide.set_property("text", "Changed")
        ide.check(ide.window.document.modified, "the change did not mark the project as changed")
        ide.choose(ide.window.save_action)
        ide.equal(Project.load(path).find_widget(label).props["text"], "Changed", "text of the label in the file")
    with ide.step("New project, then open the saved one from Recent Files"):
        ide.choose(ide.window.new_action)
        ide.equal(ide.window.document.path, None, "path of a new project")
        ide.window.recent_menu.aboutToShow.emit()
        recent = [action for action in ide.window.recent_menu.actions() if str(path) in (action.text(), str(action.data()))]
        ide.check(recent, f"Recent Files does not list {path.name}: " + ", ".join(action.text() for action in ide.window.recent_menu.actions()))
        ide.choose(recent[0])
        ide.equal(str(ide.window.document.path), str(path), "path of the project opened")
    with ide.step("The reopened project is the one saved"):
        ide.equal(sorted(widget.name for widget in ide.project.pages[0].widgets), sorted([button, label]), "widgets of the page")
        ide.equal(ide.project.find_widget(label).props["text"], "Changed", "text of the label")
        ide.check(ide.drawn(label) is not None, "the label is not drawn on the page")
