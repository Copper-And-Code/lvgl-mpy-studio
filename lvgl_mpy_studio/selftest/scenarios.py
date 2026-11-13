"""The scenarios of the self-test. Each one starts from a new window and an empty folder."""

from PySide6.QtCore import Qt

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


def touch_runs(ide, x, y, line, what):
    """Touch the simulator and wait for the line the code prints."""
    before = ide.output().count(line)
    ide.tap(x, y)
    ide.wait(lambda: ide.output().count(line) > before, f"“{line}” in the Output panel after touching {what}")


def placed_button(ide, text, y=30):
    """A wide button near the top left corner, easy to touch; return its name."""
    button = ide.add_widget("button", 60, y + 10)
    ide.select(button)
    for name, value in (("x", 40), ("y", y), ("width", 200), ("height", 80), ("text", text)):
        ide.set_property(name, value)
    return button


def write_handler(ide, widget, event, code):
    """Create the handler from the Events tab and type its code."""
    if widget in [item.name for item in ide.designer().designer_scene.page.widgets if ide.drawn(item.name)]:
        ide.select(widget)
    else:
        ide.click_tree(widget)
    handler = ide.open_handler(event)
    ide.type_code(code)
    ide.equal(ide.project.code.handlers[handler].body, code, f"code stored for {handler}")
    return handler


@scenario("pages", "Pages: add, rename, navigate, delete")
def pages(ide):
    with ide.step("Create a new project with a button on the first page"):
        ide.choose(ide.window.new_action)
        first = ide.project.pages[0]
        go = placed_button(ide, "Go")
    with ide.step("Add a page: it gets a tab and an entry in the project tree"):
        ide.choose(ide.window.add_page_action)
        ide.equal(len(ide.project.pages), 2, "pages of the project")
        second = ide.project.pages[1]
        ide.check(second.id in ide.window.designers, "the new page has no tab")
        ide.tree_item(second.name)
    with ide.step("Rename the page from the project tree"):
        ide.click_tree(second.name)
        ide.check(ide.designer().designer_scene.page_id == second.id, "clicking the page in the tree did not open it")
        ide.answer_input("Details")
        ide.choose(ide.window.rename_page_action)
        ide.equal(ide.project.pages[1].name, "Details", "name of the page")
        ide.equal(ide.window.tabs.tabText(ide.window.tabs.indexOf(ide.designer())), "Details", "text of the tab")
    with ide.step("Put a button on the second page"):
        back = placed_button(ide, "Back", 200)
        ide.check(ide.project.find_widget(back) in ide.project.pages[1].widgets, "the button went to another page")
    with ide.step("Write the handlers that go from one page to the other"):
        write_handler(ide, back, "CLICKED", f'ui.load_page(ui.PAGE_{first.name.upper()})\nprint("SELFTEST back")')
        ide.click_tree(first.name)
        write_handler(ide, go, "CLICKED", 'ui.load_page(ui.PAGE_DETAILS)\nprint("SELFTEST go")')
    with ide.step("Save and start the simulator"):
        ide.save_as(ide.directory / "pages.json")
        ide.run()
    with ide.step("Touch Go, then Back: each handler runs on its own page"):
        home = ide.frame()
        touch_runs(ide, 140, 70, "SELFTEST go", "Go")
        ide.wait(lambda: ide.frame() != home, "the second page on the screen")
        ide.tap(140, 70)  # where Go was: on the second page nothing is there
        ide.equal(ide.output().count("SELFTEST go"), 1, "times Go ran")
        touch_runs(ide, 140, 240, "SELFTEST back", "Back")
        ide.wait(lambda: ide.frame() == home, "the first page on the screen again")
        ide.check(not ide.errors(), f"the Errors panel says: {ide.errors()}")
        ide.stop()
    with ide.step("Delete the second page, then undo"):
        ide.click_tree("Details")
        ide.choose(ide.window.delete_page_action)
        ide.equal([page.name for page in ide.project.pages], [first.name], "pages after Delete Page")
        ide.equal(ide.window.tabs.indexOf(ide.window.designers.get(second.id, (0, None))[1]) if second.id in ide.window.designers else -1, -1, "tab of the deleted page")
        ide.choose(ide.window.undo_action)
        ide.equal([page.name for page in ide.project.pages], [first.name, "Details"], "pages after Undo")
        ide.check(ide.project.find_widget(back) is not None, "Undo did not bring back the button of the page")


@scenario("resolution", "Resolution: change, adapt, rotate, undo")
def resolution(ide):
    button, label = build_counter(ide)

    def inside(width, height):
        return all(0 <= widget.props["x"] and widget.props["x"] + widget.props["width"] <= width and 0 <= widget.props["y"] and widget.props["y"] + widget.props["height"] <= height for widget in ide.project.pages[0].widgets)

    def size():
        return ide.project.display.width, ide.project.display.height

    with ide.step("A new project is 1024×600, for the STM32H7_CORE, and the toolbar says so"):
        ide.equal(size(), (1024, 600), "resolution of a new project")
        ide.equal(ide.window.resolution_selector.text(), "1024×600", "text of the resolution button")
    with ide.step("Choose 480×480 and adapt the widgets"):
        ide.answer_resize("adapt")
        ide.choose_resolution("480×480")
        ide.equal(size(), (480, 480), "resolution of the project")
        ide.equal(ide.window.resolution_selector.text(), "480×480", "text of the resolution button")
        ide.check(inside(480, 480), "a widget is outside the page after adapting")
    with ide.step("The page is drawn at the new size and fitted to the window"):
        picture = ide.wait_preview()
        ide.equal((picture.width(), picture.height()), (480, 480), "size of the LVGL picture of the page")
        view = ide.designer()
        ide.wait(lambda: view.fitted_size == (480, 480), "the page to be fitted to the window")
        visible = view.mapToScene(view.viewport().rect()).boundingRect()
        ide.check(visible.width() >= 480 and visible.height() >= 480, "the whole page is not visible")
    with ide.step("Choose 1024×600 and stretch: the widgets grow with the page"):
        before = dict(ide.project.find_widget(button).props)
        ide.answer_resize("stretch")
        ide.choose_resolution("1024×600")
        ide.equal(size(), (1024, 600), "resolution of the project")
        after = ide.project.find_widget(button).props
        ide.check(after["width"] > before["width"] and after["height"] > before["height"], f"the button did not grow: {before['width']}×{before['height']} → {after['width']}×{after['height']}")
        ide.check(inside(1024, 600), "a widget is outside the page after stretching")
    with ide.step("Rotate: the sides swap"):
        ide.answer_resize("adapt")
        ide.choose_resolution("Rotate")
        ide.equal(size(), (600, 1024), "resolution after Rotate")
        ide.check(inside(600, 1024), "a widget is outside the page after rotating")
    with ide.step("Undo three times: back to 1024×600 with the widgets where they were"):
        for _ in range(3):
            ide.choose(ide.window.undo_action)
        ide.equal(size(), (1024, 600), "resolution after undoing")
        ide.equal({name: ide.project.find_widget(button).props[name] for name in ("x", "y", "width", "height")}, {"x": 40, "y": 30, "width": 200, "height": 80}, "button after undoing")
    with ide.step("Start the simulator at 480×480: the screen has that size"):
        ide.answer_resize("adapt")
        ide.choose_resolution("480×480")
        ide.save_as(ide.directory / "resolution.json")
        ide.run()
        frame = ide.frame()
        ide.equal((frame.width(), frame.height()), (480, 480), "size of the simulator screen")
        ide.stop()


def test_picture(directory):
    """A small picture made on the spot: the self-test carries no files."""
    from PySide6.QtGui import QColor, QImage, QPainter

    image = QImage(96, 64, QImage.Format_ARGB32)
    image.fill(QColor("#D32F2F"))
    painter = QPainter(image)
    painter.fillRect(16, 16, 64, 32, QColor("#FFEB3B"))
    painter.end()
    path = directory / "picture.png"
    image.save(str(path))
    return path


def any_font():
    """A TrueType file that is surely there: LVGL's own, one of the system, or the icon font of the IDE."""
    import sys
    from pathlib import Path

    import qtawesome

    from lvgl_mpy_studio.platform import root_dir

    candidates = [root_dir() / ".reference/lvgl-bindings/lvgl/scripts/built_in_font/Montserrat-Medium.ttf", Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"), Path("C:/Windows/Fonts/arial.ttf")]
    candidates += sorted(Path("/usr/share/fonts").rglob("*.ttf"))[:1] if sys.platform.startswith("linux") else []
    candidates += sorted((Path(qtawesome.__file__).parent / "fonts").glob("*.ttf"))
    return next((path for path in candidates if path.exists()), None)


@scenario("assets", "Pictures and fonts of the project")
def assets(ide):
    from lvgl_mpy_studio.core.assets import fonts, images

    with ide.step("Create a new project with an image and a label"):
        ide.choose(ide.window.new_action)
        image = ide.add_widget("image", 120, 120)
        label = ide.add_widget("label", 300, 60)
        ide.select(label)
        for name, value in (("width", 400), ("height", 60), ("text", "0123456789"), ("fontSize", 32)):
            ide.set_property(name, value)
        plain = ide.wait_preview()
    with ide.step("Choose a picture for the image with the “…” button"):
        ide.select(image)
        stored = ide.choose_file_property("src", test_picture(ide.directory))
        ide.equal([item["name"] for item in images(ide.project)], [stored], "pictures stored in the project")
        ide.check("/" not in stored and "\\" not in stored, f"the property holds a path instead of the name in the project: {stored}")
    with ide.step("The page draws the picture"):
        with_picture = ide.wait_preview()
        ide.check(with_picture != plain, "the picture of the page did not change")
    with ide.step("Choose a font for the label with the “…” button"):
        font = any_font()
        ide.check(font is not None, "no TrueType font was found on this computer")
        ide.select(label)
        stored = ide.choose_file_property("font", font)
        ide.equal([item["name"] for item in fonts(ide.project)], [stored], "fonts stored in the project")
    with ide.step("The page draws the text with the new font"):
        ide.check(ide.wait_preview() != with_picture, "the picture of the page did not change")
    with ide.step("Save, open again: the picture and the font are inside the file"):
        path = ide.directory / "assets.json"
        ide.save_as(path)
        ide.choose(ide.window.new_action)
        ide.window.open_project(path)
        ide.equal((len(images(ide.project)), len(fonts(ide.project))), (1, 1), "pictures and fonts after opening again")
    with ide.step("Start the simulator: no error, and the screen is the one of the page"):
        ide.run()
        ide.check(not ide.errors(), f"the Errors panel says: {ide.errors()}")
        ide.check(ide.frame().convertToFormat(with_picture.format()) != plain.convertToFormat(with_picture.format()), "the simulator shows the page without picture and font")
        ide.stop()


@scenario("modules", "Python modules: create, use, rename, delete")
def modules(ide):
    from PySide6.QtWidgets import QMessageBox

    with ide.step("Create a new project with a button"):
        ide.choose(ide.window.new_action)
        button = placed_button(ide, "Greet")
    with ide.step("Create a Python module from the Project menu"):
        ide.answer_input("greetings")
        ide.choose(ide.window.new_module_action)
        ide.equal([module.name for module in ide.project.modules], ["greetings"], "modules of the project")
        ide.check(ide.window.tabs.currentWidget() is ide.window.code_panel and ide.window.code_panel.module() is not None, "the new module was not opened in the editor")
        ide.tree_item("greetings.py")
    with ide.step("Type a function in the module"):
        source = 'COUNT = 0\n\n\ndef greet(name):\n    global COUNT\n    COUNT += 1\n    return "Hello %s %d" % (name, COUNT)'
        ide.type_code(source, replace=True)
        ide.equal(ide.project.modules[0].source, source, "source stored for the module")
        compile(source, "greetings.py", "exec")
    with ide.step("Call the module from the button's handler"):
        ide.click_tree(ide.project.pages[0].name)
        write_handler(ide, button, "CLICKED", 'import greetings\nprint("SELFTEST", greetings.greet("you"))')
    with ide.step("Save, start the simulator and touch the button twice"):
        ide.save_as(ide.directory / "modules.json")
        ide.run()
        touch_runs(ide, 140, 70, "SELFTEST Hello you 1", "the button")
        touch_runs(ide, 140, 70, "SELFTEST Hello you 2", "the button")
        ide.check(not ide.errors(), f"the Errors panel says: {ide.errors()}")
        ide.stop()
    with ide.step("Rename the module: the IDE warns that the handler still imports the old name"):
        ide.click_tree("greetings.py")
        ide.answer_input("salutes")
        ide.answer_message(QMessageBox.Yes)
        ide.choose(ide.window.rename_module_action)
        ide.equal([module.name for module in ide.project.modules], ["salutes"], "modules after renaming")
        ide.check("greetings" in ide.output(), "the Output panel does not mention the import of the old name")
    with ide.step("Start with the old import: the error leads to the handler"):
        ide.choose(ide.window.save_action)
        ide.choose(ide.window.run_action)
        ide.wait(lambda: ide.window.sim_panel.running and ide.window.sim_panel.first_frame_ms is not None, "the first frame of the simulator", 20000)
        ide.tap(140, 70)
        ide.wait(lambda: any("ImportError" in message for _file, _line, message in ide.errors()), "an ImportError in the Errors panel")
        ide.stop()
    with ide.step("Delete the module, then undo"):
        ide.click_tree("salutes.py")
        ide.answer_message(QMessageBox.Yes)
        ide.choose(ide.window.delete_module_action)
        ide.equal(ide.project.modules, [], "modules after deleting")
        ide.choose(ide.window.undo_action)
        ide.equal([module.name for module in ide.project.modules], ["salutes"], "modules after Undo")


@scenario("components", "Components: Timer and Buzzer")
def components(ide):
    with ide.step("Create a new project with a button, a Timer and a Buzzer"):
        ide.choose(ide.window.new_action)
        button = placed_button(ide, "Beep")
        timer = ide.add_widget("timer")
        buzzer = ide.add_widget("buzzer")
        ide.equal((ide.project.find_widget(timer).type, ide.project.find_widget(buzzer).type), ("timer", "buzzer"), "types of the components")
        ide.check(ide.drawn(timer) is None and ide.drawn(buzzer) is None, "a component is drawn on the page")
        ide.tree_item(timer)
        ide.tree_item(buzzer)
    with ide.step("Set the Timer's period from the Properties panel"):
        ide.click_tree(timer)
        ide.equal(ide.window.properties.names, [timer], "selection after clicking the Timer in the tree")
        ide.set_property("period", 200)
    with ide.step("Write the Timer's and the button's handlers"):
        write_handler(ide, timer, "TICK", 'print("SELFTEST tick")')
        ide.click_tree(ide.project.pages[0].name)
        write_handler(ide, button, "CLICKED", f'ui.{buzzer}.beep(880, 50)\nprint("SELFTEST beep")')
    with ide.step("Save and start the simulator: the Timer ticks by itself"):
        ide.save_as(ide.directory / "components.json")
        tones = []
        ide.window.sim_panel.tone.connect(lambda frequency, milliseconds: tones.append((frequency, milliseconds)))
        ide.run()
        ide.wait(lambda: ide.output().count("SELFTEST tick") >= 3, "three ticks of the Timer in the Output panel")
    with ide.step("Touch the button: the Buzzer plays the note"):
        touch_runs(ide, 140, 70, "SELFTEST beep", "the button")
        ide.wait(lambda: (880, 50) in tones, f"the tone 880 Hz for 50 ms from the simulator (heard: {tones})")
        ide.check(not ide.errors(), f"the Errors panel says: {ide.errors()}")
        ide.stop()
    with ide.step("After Stop the Timer no longer ticks"):
        from .driver import sleep

        ticks = ide.output().count("SELFTEST tick")
        sleep(600)
        ide.equal(ide.output().count("SELFTEST tick"), ticks, "ticks after Stop")


@scenario("errors", "Errors: syntax and run time")
def errors(ide):
    with ide.step("Create a new project with a button"):
        ide.choose(ide.window.new_action)
        button = placed_button(ide, "Break")
    with ide.step("A handler with a syntax error: Start refuses and the Errors panel says where"):
        handler = write_handler(ide, button, "CLICKED", 'print("SELFTEST before")\nvalue = (1 +')
        ide.save_as(ide.directory / "errors.json")
        ide.choose(ide.window.run_action)
        ide.wait(lambda: bool(ide.errors()), "a row in the Errors panel")
        ide.check(not ide.window.sim_panel.running, "the simulator started with a syntax error")
        ide.check(any("2" == line for _file, line, _message in ide.errors()), f"no error points to line 2: {ide.errors()}")
    with ide.step("Fix it into an error that happens when running"):
        ide.type_code('print("SELFTEST before")\nvalue = missing_name + 1', replace=True)
        ide.equal(ide.project.code.handlers[handler].body, 'print("SELFTEST before")\nvalue = missing_name + 1', "code stored for the handler")
        ide.run()
        ide.check(not ide.errors(), f"the Errors panel is not empty before any touch: {ide.errors()}")
    with ide.step("Touch the button: the NameError appears with the handler and the line"):
        touch_runs(ide, 140, 70, "SELFTEST before", "the button")
        ide.wait(lambda: any("NameError" in message for _file, _line, message in ide.errors()), "a NameError in the Errors panel")
        item, data = ide.error_data("NameError")
        ide.equal((data.get("handler"), item.text(1)), (handler, "2"), "handler and line of the error")
        ide.check(ide.window.sim_panel.running, "the simulator stopped because of an error in a handler")
    with ide.step("Double-click the error: the editor opens the handler at that line"):
        ide.stop()
        item, _data = ide.error_data("NameError")
        ide.window.tabs.setCurrentIndex(0)
        ide.window.errors.itemActivated.emit(item, 0)
        ide.check(ide.window.tabs.currentWidget() is ide.window.code_panel, "the Code tab did not come to the front")
        ide.equal(ide.window.code_panel.current, ("handler", handler), "source open in the editor")
        ide.equal(ide.window.code_panel.editor.textCursor().blockNumber() + 1, 2, "line of the cursor")


@scenario("blocks", "Hardware blocks: Digital Output and Digital Input")
def blocks(ide):
    with ide.step("Create a new project with a button, a Digital Output and a Digital Input"):
        ide.choose(ide.window.new_action)
        button = placed_button(ide, "Toggle")
        led = ide.add_widget("digital_output")
        key = ide.add_widget("digital_input")
        ide.equal((ide.project.find_widget(led).type, ide.project.find_widget(key).type), ("digital_output", "digital_input"), "types of the components")
        ide.check(ide.drawn(led) is None and ide.drawn(key) is None, "a block is drawn on the page")
    with ide.step("Set their pins from the Properties panel"):
        ide.click_tree(led)
        ide.set_property("pin", 25)
        ide.click_tree(key)
        ide.set_property("pin", 14)
        ide.set_property("debounce", 50)
        ide.equal(ide.project.find_widget(key).props, {"pull": "up", "active_low": True, "debounce": 50, "pin": 14}, "properties of the input")
    with ide.step("The Events tab offers the events of the block, and the editor its methods"):
        from lvgl_mpy_studio.core.events import events_for

        ide.equal(events_for("digital_input"), ["CHANGED", "PRESSED", "RELEASED"], "events of the Digital Input")
        ide.check("CHANGED" not in events_for("button"), "a button offers the event of a block")
        ide.equal(ide.window.code_panel._completions(f"ui.{led}."), ["off", "on", "set", "toggle", "value"], "methods suggested for the output")
        helper = ide.window.code_panel.helper
        helper.rebuild()
        group = next(helper.tree.topLevelItem(row) for row in range(helper.tree.topLevelItemCount()) if helper.tree.topLevelItem(row).text(0).startswith(key))
        offered = [group.child(row).data(0, Qt.UserRole) for row in range(group.childCount())]
        ide.equal(offered, [f"ui.{key}.value()", f"ui.{key}.simulate(§)"], "what “What do you want to do?” offers for the input")
    with ide.step("Write the handlers: the button toggles the output, the input reports its changes"):
        write_handler(ide, key, "PRESSED", 'print("SELFTEST pressed", e.value())')
        write_handler(ide, key, "RELEASED", 'print("SELFTEST released", e.value())')
        ide.click_tree(ide.project.pages[0].name)
        write_handler(ide, button, "CLICKED", f"ui.{led}.toggle()\nui.{key}.simulate(ui.{led}.value())")
    with ide.step("Save: the file is version 4 and opens again"):
        import json

        from lvgl_mpy_studio.core.model import Project

        path = ide.directory / "blocks.json"
        ide.save_as(path)
        ide.equal(json.loads(path.read_text(encoding="utf-8"))["schemaVersion"], 4, "version of the project file")
        ide.equal(Project.load(path).find_widget(led).props["pin"], 25, "pin of the output in the file")
    with ide.step("Start the simulator and touch the button twice"):
        ide.run()
        touch_runs(ide, 140, 70, "SELFTEST pressed True", "the button")
        ide.check(f"{led}: on" in ide.output(), "the simulated output did not say it went on")
        touch_runs(ide, 140, 70, "SELFTEST released False", "the button")
        ide.check(f"{led}: off" in ide.output(), "the simulated output did not say it went off")
        ide.check(not ide.errors(), f"the Errors panel says: {ide.errors()}")
        ide.stop()
