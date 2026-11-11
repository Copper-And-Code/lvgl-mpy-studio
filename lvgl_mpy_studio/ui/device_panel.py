from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget

from lvgl_mpy_studio.core.i18n import tr


class DeviceWorker(QThread):
    succeeded = Signal(object)
    failed = Signal(object)
    progress = Signal(int, int)

    def __init__(self, operation, parent=None):
        super().__init__(parent)
        self.operation = operation

    def run(self):
        try:
            self.succeeded.emit(self.operation())
        except Exception as exc:
            self.failed.emit(exc)


class DeviceConsole(QWidget):
    commandRequested = Signal(str)
    interruptRequested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setMaximumBlockCount(10000)
        layout.addWidget(self.output, 1)
        row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText(tr("MicroPython REPL command"))
        self.send = QPushButton(tr("Send"))
        self.interrupt = QPushButton(tr("Cancel operation"))
        self.interrupt.setEnabled(False)
        row.addWidget(self.input, 1)
        row.addWidget(self.send)
        row.addWidget(self.interrupt)
        layout.addLayout(row)
        self.send.clicked.connect(self.submit)
        self.input.returnPressed.connect(self.submit)
        self.interrupt.clicked.connect(self.interruptRequested)
        self.set_ready(False)

    def set_ready(self, ready):
        self.input.setEnabled(ready)
        self.send.setEnabled(ready)

    def set_busy(self, busy):
        self.interrupt.setEnabled(busy)

    def submit(self):
        source = self.input.text()
        if source.strip():
            self.input.clear()
            self.commandRequested.emit(source)

    def append(self, text):
        if text:
            self.output.insertPlainText(str(text))
            scrollbar = self.output.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())


class SelectDeviceDialog(QDialog):
    def __init__(self, ports, current=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("Select Device"))
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(tr("Explicitly select the port; the board profile is configured in the project.")))
        form = QFormLayout()
        self.port = QComboBox()
        self.port.setEditable(True)
        for device in ports:
            label = f"{device['port']} — {device['description']} ({device['usb']})"
            self.port.addItem(label, device["port"])
        if current:
            index = self.port.findData(current)
            if index >= 0:
                self.port.setCurrentIndex(index)
            else:
                self.port.setEditText(current)
        elif not ports:
            self.port.setEditText("")
        form.addRow(tr("Port"), self.port)
        layout.addLayout(form)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.button(QDialogButtonBox.Ok).setText(tr("Select"))
        self.buttons.button(QDialogButtonBox.Cancel).setText(tr("Cancel"))
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def selected_port(self):
        return self.port.currentData() if self.port.currentIndex() >= 0 and self.port.currentText() == self.port.itemText(self.port.currentIndex()) else self.port.currentText().strip()
