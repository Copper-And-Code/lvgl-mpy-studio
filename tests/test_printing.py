from PySide6.QtCore import QRectF
from PySide6.QtGui import QImage, QKeySequence
from PySide6.QtPrintSupport import QPrinter

from lvgl_mpy_studio.core.model import Handler, Project, UserModule
from lvgl_mpy_studio.ui import printing
from lvgl_mpy_studio.ui.main_window import MainWindow


def project():
    result = Project("Printed")
    result.code.module = "import ui\n\nscore = 0  # points\n"
    result.code.handlers["button1_clicked"] = Handler("button1", "clicked", "global score\nscore += 1\n\nprint(score)")
    result.code.handlers["a_empty"] = Handler("a", "clicked", "")
    result.modules.append(UserModule("helpers", "def twice(value):\n    return value * 2\n", "id1"))
    result.modules.append(UserModule("blank", "\n", "id2"))
    return result


def test_sources_are_the_general_code_the_handlers_and_the_modules(qapp):
    sections = printing.all_sources(project())
    assert [title for title, _text in sections] == ["(General)", "Handlers", "helpers.py"]  # the blank module is left out
    handlers = sections[1][1]
    assert "def a_empty(e):\n    pass\n" in handlers  # a handler without a body is still valid Python
    assert "def button1_clicked(e):\n    global score\n    score += 1\n\n    print(score)\n" in handlers
    compile(handlers, "handlers", "exec")
    current = project()
    assert printing.open_source(current, ("module", "module")) == ("(General)", current.code.module)
    assert printing.open_source(current, ("pymodule", "id1"))[0] == "helpers.py"
    assert printing.open_source(current, ("handler", "button1_clicked"))[1].startswith("def button1_clicked(e):")
    assert printing.open_source(current, ("handler", "gone")) is None


def test_pages_number_lines_wrap_long_ones_and_start_each_source_on_a_new_page(qapp):
    device = QImage(10, 10, QImage.Format_RGB32)
    long_line = "x = '" + "wrap " * 60 + "'"
    text = "\n".join([f"line{index} = {index}" for index in range(1, 201)] + [long_line])
    pages = printing.Pages(device, QRectF(0, 0, 600, 800), "Printed", [("first.py", text), ("second.py", "pass\n")])
    assert len(pages.pages) > 2 and pages.pages[-1][0] == "second.py" and len(pages.pages[-1][1]) == 1
    lines = [entry for title, entries in pages.pages if title == "first.py" for entry in entries]
    numbers = [number for _y, _line, number in lines if number is not None]
    assert numbers == list(range(1, 202))  # one number for each source line
    wrapped = [line for _y, line, number in lines if number is None]
    assert wrapped and all(line.naturalTextWidth() <= 600 - pages.gutter for _y, line, _number in lines)
    for _title, entries in pages.pages:
        assert all(pages.band <= y and y + pages.line_height <= 800 - pages.band for y, _line, _number in entries)
    without = printing.Pages(device, QRectF(0, 0, 600, 800), "Printed", [("first.py", text)], numbers=False)
    assert without.gutter == 0 and without.columns > pages.columns


def test_render_writes_a_pdf_and_honours_the_page_range(qapp, tmp_path):
    text = "\n".join(f"value{index} = {index}" for index in range(400))

    def pdf(name, first=0, last=0):
        printer = printing.new_printer()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(str(tmp_path / name))
        if first:
            printer.setFromTo(first, last)
        count = printing.render(printer, "Printed", [("big.py", text)])
        return count, (tmp_path / name).read_bytes()

    count, whole = pdf("whole.pdf")
    assert count >= 4 and whole.startswith(b"%PDF")
    _count, part = pdf("part.pdf", 2, 2)
    assert whole.count(b"/Type /Page\n") == count and part.count(b"/Type /Page\n") == 1


def test_dialog_offers_the_open_source_or_all_of_them(qtbot, tmp_path, monkeypatch):
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.print_action.shortcut() == QKeySequence(QKeySequence.Print)
    assert window.print_action in window.menuBar().actions()[0].menu().actions()
    window.document.project.code.module = ""
    empty = printing.PrintSourcesDialog(window.document.project, window.code_panel.current, window)
    qtbot.addWidget(empty)
    assert not empty.print_button.isEnabled() and not empty.preview_button.isEnabled()  # nothing to print

    current = project()
    dialog = printing.PrintSourcesDialog(current, ("pymodule", "id1"))
    qtbot.addWidget(dialog)
    assert dialog.open_choice.isChecked() and "helpers.py" in dialog.open_choice.text()
    assert [title for title, _text in dialog.sections()] == ["helpers.py"]
    dialog.all_choice.setChecked(True)
    assert len(dialog.sections()) == 3 and "(3)" in dialog.all_choice.text()
    printer = printing.new_printer()
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName(str(tmp_path / "all.pdf"))
    assert dialog.render(printer) == 3  # each source on its own page
