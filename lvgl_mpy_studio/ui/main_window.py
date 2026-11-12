import copy
import json

from PySide6.QtCore import QRectF, QSettings, QSize, Qt, QTimer, Signal
from PySide6.QtGui import QAction, QKeySequence, QPainter
from PySide6.QtWidgets import QApplication, QDockWidget, QLabel, QLineEdit, QMainWindow, QMenu, QMessageBox, QPlainTextEdit, QSizePolicy, QTabWidget, QToolBar, QToolButton, QTreeWidget, QWidget

from lvgl_mpy_studio import __version__
from lvgl_mpy_studio.core.boards import ProfileStore, portable_profile, validate_profile
from lvgl_mpy_studio.core.i18n import DEFAULT_LANGUAGE, set_language, tr
from lvgl_mpy_studio.device.service import DeviceSession
from lvgl_mpy_studio.ui.budget import BudgetMonitor, budget_level, budget_text
from lvgl_mpy_studio.ui.code.editor import CodePanel
from lvgl_mpy_studio import mcp_server
from lvgl_mpy_studio.ui.designer.preview import PreviewRenderer, frame_image
from lvgl_mpy_studio.ui.designer.scene import ComponentTray, DesignerView, ToolboxPanel
from lvgl_mpy_studio.ui.device_panel import DeviceConsole
from lvgl_mpy_studio.ui.document import ProjectDocument
from lvgl_mpy_studio.ui.gc_guard import install as install_gc_guard
from lvgl_mpy_studio.ui.language import apply_language
from lvgl_mpy_studio.ui.resolution import ResolutionSelector
from lvgl_mpy_studio.ui.properties.panel import PropertiesPanel
from lvgl_mpy_studio.ui.run_target import SIMULATOR_MICROPYTHON, RunTargetSelector, board_target
from lvgl_mpy_studio.ui.sim_panel import SimPanel
from lvgl_mpy_studio.ui.main_device import LIVE_DELAY_MS, DeviceMixin
from lvgl_mpy_studio.ui.main_tree import ProjectTreeMixin
from lvgl_mpy_studio.ui.main_files import DEFAULTS_KEY, FilesMixin
from lvgl_mpy_studio.ui.main_resolution import ResolutionMixin
from lvgl_mpy_studio.ui.main_run import RunMixin
from lvgl_mpy_studio.ui import theme









class MainWindow(DeviceMixin, ProjectTreeMixin, FilesMixin, ResolutionMixin, RunMixin, QMainWindow):
    deviceOutput = Signal(str)
    LAYOUT_VERSION = 2    # bottom panels as tabs: layouts saved before are no longer valid

    def __init__(self) -> None:
        super().__init__()
        install_gc_guard()
        theme.install(QApplication.instance()).changed.connect(self._theme_changed)
        self.setContentsMargins(*theme.frame_margins(QApplication.platformName()))
        self.settings = QSettings("CopperAndCode", "LVGL MPY Studio")
        old_settings = QSettings("CopperAndCode", "LVGL IDE")  # the name up to 0.4
        if not self.settings.allKeys():
            for key in old_settings.allKeys():
                self.settings.setValue(key, old_settings.value(key))
        set_language(self.settings.value("language", DEFAULT_LANGUAGE))
        self.profile_store = ProfileStore.tolerant()  # a broken profile file must not stop the start
        self.document = ProjectDocument(self._default_project())
        self.device = DeviceSession()
        self._live_upload_key = None
        self._live_design_key = None
        self._live_page_id = None
        self._live_timer = QTimer(self, singleShot=True, interval=LIVE_DELAY_MS, timeout=self._send_live)
        self._ports = {}
        self.device_app_active = False
        self._worker = None
        self._device_cancel = None
        self._upload_progress = None
        self._device_next = None
        self._building = False
        self._drag_frame_pending = False
        self._device_sourcemap = None
        self._device_trace = ""
        self._device_mapped_traces = set()
        self._sim_trace = ""
        self.deviceOutput.connect(self._device_output)
        self.setWindowTitle("LVGL MPY Studio")
        self.resize(1400, 900)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(False)
        self.setCentralWidget(self.tabs)
        self.designers = {}
        self._make_actions()
        self._make_menus()
        self._make_docks()
        self._make_run_toolbar()
        self._make_device_status()
        self._make_central_tabs()
        self.statusBar().showMessage(tr("Ready"))
        self.document.reset.connect(self._document_changed)
        self.document.code_changed.connect(self._schedule_budget)
        self.document.path_changed.connect(self._update_title)
        self.document.modified_changed.connect(self._update_title)
        self._document_changed()
        self._update_title()
        self._restore_layout()
        self._update_device_actions()
        if self.profile_store.load_error:
            self.append_error(tr("Custom board profiles cannot be read, the built-in ones remain: {error}", error=self.profile_store.load_error))

    def _make_actions(self):
        self.new_action = QAction(tr("New"), self, shortcut=QKeySequence.New, triggered=self.new_project)
        self.open_action = QAction(tr("Open…"), self, shortcut=QKeySequence.Open, triggered=self.open_project_dialog)
        self.save_action = QAction(tr("Save"), self, shortcut=QKeySequence.Save, triggered=self.save_project)
        self.save_as_action = QAction(tr("Save As…"), self, shortcut=QKeySequence.SaveAs, triggered=self.save_project_as)
        self.exit_action = QAction(tr("Exit"), self, shortcut=QKeySequence.Quit, triggered=self.close)
        self.undo_action = self.document.undo_stack.createUndoAction(self, tr("Undo"))
        self.undo_action.setShortcut(QKeySequence.Undo)
        self.redo_action = self.document.undo_stack.createRedoAction(self, tr("Redo"))
        self.redo_action.setShortcut(QKeySequence.Redo)
        self.document.reset.connect(self._update_undo_text)
        self.document.code_changed.connect(self._update_undo_text)
        self.cut_action = QAction(tr("Cut"), self, shortcut=QKeySequence.Cut, triggered=lambda: self._clipboard("cut"))
        self.copy_action = QAction(tr("Copy"), self, shortcut=QKeySequence.Copy, triggered=lambda: self._clipboard("copy"))
        self.paste_action = QAction(tr("Paste"), self, shortcut=QKeySequence.Paste, triggered=lambda: self._clipboard("paste"))
        self.delete_action = QAction(tr("Delete"), self, shortcut=QKeySequence.Delete, triggered=self._delete)
        self.select_all_action = QAction(tr("Select All"), self, shortcut=QKeySequence.SelectAll, triggered=self._select_all)
        self.duplicate_action = QAction(tr("Duplicate"), self, shortcut="Ctrl+D", triggered=lambda: self._on_scene("duplicate_selected"))
        self.align_actions = [
            QAction(tr(text), self, triggered=lambda checked=False, value=side: self._on_scene("align_selected", value))
            for text, side in (("Align Left", "left"), ("Align Center", "center"), ("Align Right", "right"), ("Align Top", "top"), ("Align Middle", "middle"), ("Align Bottom", "bottom"))
        ]
        self.distribute_actions = [
            QAction(tr(text), self, triggered=lambda checked=False, value=axis: self._on_scene("distribute_selected", value))
            for text, axis in (("Distribute Horizontally", "horizontal"), ("Distribute Vertically", "vertical"))
        ]
        self.front_action = QAction(tr("Bring to Front"), self, shortcut="Ctrl+]", triggered=lambda: self._on_scene("change_z", True))
        self.back_action = QAction(tr("Send to Back"), self, shortcut="Ctrl+[", triggered=lambda: self._on_scene("change_z", False))
        self.grid_action = QAction(tr("Grid"), self, checkable=True, triggered=self._toggle_grid)
        self.preview_action = QAction(tr("Real LVGL Preview"), self, checkable=True, triggered=self._toggle_preview)
        self.preview_action.setChecked(self.settings.value("designer/preview", True, bool))
        self.preview_renderer = PreviewRenderer(parent=self)
        self.preview_renderer.rendered.connect(self._preview_rendered)
        self.zoom_in_action = QAction(tr("Zoom In"), self, shortcut=QKeySequence.ZoomIn, triggered=lambda: self._zoom(1.25))
        self.zoom_out_action = QAction(tr("Zoom Out"), self, shortcut=QKeySequence.ZoomOut, triggered=lambda: self._zoom(0.8))
        self.fit_action = QAction(tr("Fit to Window"), self, shortcut="Ctrl+0", triggered=self._fit_canvas)
        self.run_action = QAction(tr("Start"), self, shortcut="F5", triggered=self.run_project)
        self.stop_action = QAction(tr("Stop"), self, shortcut="Shift+F5", triggered=self.stop_simulation)
        self.restart_action = QAction(tr("Restart"), self, triggered=self.restart_project)
        self.build_action = QAction(tr("Build Executable…"), self, triggered=self.build_executable)
        self.single_file_action = QAction(tr("Build Single-File Executable…"), self, triggered=self.build_single_file)
        self.web_action = QAction(tr("Open in Browser"), self, triggered=self.open_in_browser)
        self._web_server = None
        self.export_c_action = QAction(tr("Export C Code…"), self, triggered=self.export_c)
        self.adapt_page_action = QAction(tr("Adapt Page to Resolution…"), self, triggered=self.adapt_current_page)
        self.export_python_action = QAction(tr("Export MicroPython Code…"), self, triggered=self.export_python)
        self.add_page_action = QAction(tr("Add Page"), self, triggered=self.add_page)
        self.rename_page_action = QAction(tr("Rename Page"), self, triggered=self.rename_page)
        self.delete_page_action = QAction(tr("Delete Page"), self, triggered=self.delete_page)
        self.initial_page_action = QAction(tr("Set Initial Page"), self, triggered=self.set_initial_page)
        self.new_module_action = QAction(tr("New Python Module…"), self, triggered=self.new_module)
        self.open_module_action = QAction(tr("Open Module"), self, triggered=lambda: self.open_module(self._selected_module_name()))
        self.rename_module_action = QAction(tr("Rename Module…"), self, triggered=self.rename_module)
        self.delete_module_action = QAction(tr("Delete Module"), self, triggered=self.delete_module)
        self.project_settings_action = QAction(tr("Project Settings…"), self, triggered=self.open_project_settings)
        self.update_profile_action = QAction(tr("Update Project Profile"), self, triggered=self.update_project_profile)
        self.select_device_action = QAction(tr("Change Port…"), self, triggered=self.select_device)
        self.profiles_action = QAction(tr("Manage Board Profiles…"), self, triggered=self.manage_profiles)
        self.connect_action = QAction(tr("Connect"), self, triggered=self.connect_disconnect)
        self.device_info_action = QAction(tr("Device Information"), self, triggered=self.show_device_info)
        self.mcp_action = QAction(tr("MCP Server for AI Agents"), self, checkable=True, triggered=self._toggle_mcp)
        self.mcp_action.setChecked(mcp_server.is_enabled())
        self.mcp_action.setToolTip(tr("Lets an AI agent use the IDE through the lvgl-mpy-studio mcp command, including uploading and running code on the board. Off by default."))
        self.live_action = QAction(tr("Live Editing"), self, checkable=True, triggered=self._toggle_live)
        self.live_action.setChecked(self.settings.value("device/live", True, bool))
        self.upload_action = QAction(tr("Upload Project"), self, triggered=lambda: self.upload_board(False))
        self.upload_run_action = QAction(tr("Upload and Run"), self, triggered=lambda: self.upload_board(True))
        self.device_restart_action = QAction(tr("Restart Interpreter"), self, triggered=self.restart_device)
        self.board_stop_action = QAction(tr("Stop"), self, triggered=self.stop_board)
        self.autostart_install_action = QAction(tr("Install Autostart…"), self, triggered=self.install_autostart)
        self.autostart_remove_action = QAction(tr("Remove Autostart…"), self, triggered=self.remove_autostart)
        self.about_action = QAction(tr("About LVGL MPY Studio"), self, triggered=self.show_about)

    def _make_menus(self):
        file_menu = self.menuBar().addMenu(tr("File"))
        file_menu.addActions((self.new_action, self.open_action, self.save_action, self.save_as_action))
        self.recent_menu = file_menu.addMenu(tr("Recent Files"))
        self.recent_menu.aboutToShow.connect(self._populate_recent)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        edit_menu = self.menuBar().addMenu(tr("Edit"))
        edit_menu.addActions((self.undo_action, self.redo_action))
        edit_menu.addSeparator()
        edit_menu.addActions((self.cut_action, self.copy_action, self.paste_action, self.duplicate_action, self.delete_action))
        edit_menu.addSeparator()
        edit_menu.addAction(self.select_all_action)
        self.view_menu = self.menuBar().addMenu(tr("View"))
        self.view_menu.addActions((self.grid_action, self.preview_action, self.zoom_in_action, self.zoom_out_action, self.fit_action))
        self.arrange_menu = self.menuBar().addMenu(tr("Arrange"))
        self.arrange_menu.addActions(self.align_actions)
        self.arrange_menu.addSeparator()
        self.arrange_menu.addActions(self.distribute_actions)
        self.arrange_menu.addSeparator()
        self.arrange_menu.addActions((self.front_action, self.back_action))
        self.arrange_menu.addSeparator()
        self.arrange_menu.addAction(self.adapt_page_action)
        self.arrange_menu.aboutToShow.connect(self._update_adapt_page_action)
        run_menu = self.menuBar().addMenu(tr("Run"))
        run_menu.addActions((self.run_action, self.stop_action, self.restart_action))
        run_menu.addSeparator()
        run_menu.addActions((self.build_action, self.single_file_action, self.web_action))
        project_menu = self.menuBar().addMenu(tr("Project"))
        project_menu.addActions((self.add_page_action, self.rename_page_action, self.delete_page_action, self.initial_page_action))
        project_menu.addSeparator()
        project_menu.addActions((self.project_settings_action, self.update_profile_action, self.export_c_action, self.export_python_action))
        device_menu = self.menuBar().addMenu(tr("Device"))
        device_menu.addActions((self.select_device_action, self.connect_action, self.device_info_action))
        device_menu.addSeparator()
        device_menu.addAction(self.live_action)
        device_menu.addActions((self.upload_action, self.upload_run_action, self.board_stop_action, self.device_restart_action))
        device_menu.addSeparator()
        device_menu.addActions((self.autostart_install_action, self.autostart_remove_action))
        device_menu.addSeparator()
        device_menu.addAction(self.profiles_action)
        settings_menu = self.menuBar().addMenu(tr("Settings"))
        settings_menu.addAction(self.mcp_action)
        self.language_menu = settings_menu.addMenu(tr("Language"))
        for code, label in (("it", "Italiano"), ("en", "English")):
            action = self.language_menu.addAction(label, lambda checked=False, value=code: self.change_language(value))
            action.setData(code)
        help_menu = self.menuBar().addMenu(tr("Help"))
        help_menu.addAction(self.about_action)
        self._apply_mnemonics()

    def _apply_mnemonics(self):
        """Letters for Alt+key, chosen from what the current language shows."""
        used = set()
        for action in self.menuBar().actions():
            menu = action.menu()
            if menu.property("_lvgl_source_title") is None:
                menu.setProperty("_lvgl_source_title", menu.title())
            title = menu.title().replace("&", "")
            position = next((index for index, letter in enumerate(title) if letter.isalpha() and letter.lower() not in used), None)
            if position is None:
                menu.setTitle(title)
                continue
            used.add(title[position].lower())
            menu.setTitle(f"{title[:position]}&{title[position:]}")

    def _make_run_toolbar(self):
        toolbar = QToolBar(tr("Run toolbar"), self)
        toolbar.setObjectName("runToolBar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(20, 20))
        toolbar.addActions((self.new_action, self.open_action, self.save_action))
        toolbar.addSeparator()
        toolbar.addActions((self.undo_action, self.redo_action))
        toolbar.addSeparator()
        toolbar.addActions((self.grid_action, self.zoom_out_action, self.zoom_in_action, self.fit_action))
        self.resolution_selector = ResolutionSelector(lambda: (self.document.project.display.width, self.document.project.display.height), self.profile_store.profiles, toolbar)
        self.resolution_selector.sizeSelected.connect(self.change_resolution)
        self.resolution_selector.customRequested.connect(self._custom_resolution)
        toolbar.addWidget(self.resolution_selector)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)
        self.run_selector = RunTargetSelector(self._board_entries, lambda: self.run_target, lambda: bool(self.settings.value(DEFAULTS_KEY, "")), toolbar)
        self.run_selector.targetSelected.connect(self.select_run_target)
        self.run_selector.changePortRequested.connect(self.select_device)
        self.run_selector.manageProfilesRequested.connect(self.manage_profiles)
        self.run_selector.saveDefaultRequested.connect(self.save_new_project_defaults)
        self.run_selector.clearDefaultRequested.connect(self.clear_new_project_defaults)
        toolbar.addWidget(self.run_selector)
        self.run_button = QToolButton()
        self.run_button.setObjectName("runButton")
        self.run_button.setDefaultAction(self.run_action)
        self.run_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        toolbar.addWidget(self.run_button)
        toolbar.addAction(self.stop_action)
        self.addToolBar(toolbar)
        self._apply_icons()

    def _apply_icons(self):
        actions = {
            self.new_action: "file-plus-outline", self.open_action: "folder-open-outline", self.save_action: "content-save-outline",
            self.undo_action: "undo", self.redo_action: "redo", self.grid_action: "grid",
            self.zoom_out_action: "magnify-minus-outline", self.zoom_in_action: "magnify-plus-outline",
            self.fit_action: "fit-to-screen-outline", self.stop_action: "stop", self.restart_action: "restart",
            self.build_action: "package-variant-closed", self.single_file_action: "file-outline", self.web_action: "web", self.export_c_action: "export", self.export_python_action: "export",
        }
        for action, name in actions.items():
            action.setIcon(theme.icon(name))
        self.run_action.setIcon(theme.icon("play", "#FFFFFF"))

    def _theme_changed(self):
        self._apply_icons()
        self.toolbox.populate()
        self.toolbox_panel.toolbox.filter(self.toolbox_panel.search.text())
        self.component_tray.rebuild()
        self.code_panel.editor.highlighter.apply_colors(theme.code_colors())
        self.code_panel.apply_error_color()
        self.properties.apply_error_color()
        for _index, view in self.designers.values():
            view.designer_scene.update()
        self.code_panel.helper.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.contentsMargins().left():
            painter = QPainter(self)
            painter.setPen(self.palette().dark().color())
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.rect().adjusted(0, -1, -1, -1))

    def _make_device_status(self):
        self.budget_label = QLabel()
        self._budget = None
        self.budget_monitor = BudgetMonitor(parent=self)
        self.budget_monitor.updated.connect(self._budget_updated)
        self.statusBar().addPermanentWidget(self.budget_label)
        self.device_status = QLabel()
        self.disconnect_button = QToolButton()
        self.disconnect_button.setDefaultAction(self.connect_action)
        self.disconnect_button.setAutoRaise(True)
        self.statusBar().addPermanentWidget(self.device_status)
        self.statusBar().addPermanentWidget(self.disconnect_button)

    def _dock(self, title, widget, area, object_name):
        dock = QDockWidget(title, self)
        dock.setObjectName(object_name)
        dock.setWidget(widget)
        self.addDockWidget(area, dock)
        self.view_menu.addAction(dock.toggleViewAction())
        return dock

    def _make_docks(self):
        self.toolbox_panel = ToolboxPanel()
        self.toolbox = self.toolbox_panel.toolbox
        self._dock("Toolbox", self.toolbox_panel, Qt.LeftDockWidgetArea, "toolboxDock")
        self.project_tree = QTreeWidget()
        self.project_tree.setHeaderHidden(True)
        self.project_tree.itemSelectionChanged.connect(self._tree_selection)
        self.project_tree.itemDoubleClicked.connect(self._tree_activated)
        self.project_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_tree.customContextMenuRequested.connect(self._project_context_menu)
        self._dock(tr("Project"), self.project_tree, Qt.LeftDockWidgetArea, "projectDock")
        self.properties = PropertiesPanel(self.document)
        self.properties.handlerRequested.connect(self.open_handler)
        self._dock(tr("Properties"), self.properties, Qt.RightDockWidgetArea, "propertiesDock")
        self.component_tray = ComponentTray(self.document)
        self.component_tray.selectionChangedTo.connect(self.properties.set_selection)
        self.component_tray.activated_.connect(self._component_activated)
        self._dock(tr("Components"), self.component_tray, Qt.BottomDockWidgetArea, "componentsDock")
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setMaximumBlockCount(5000)
        self._dock("Output", self.output, Qt.BottomDockWidgetArea, "outputDock")
        self.errors = QTreeWidget()
        self.errors.setHeaderLabels((tr("File"), tr("Line"), tr("Message")))
        self.errors.itemActivated.connect(self._error_activated)
        self._dock(tr("Errors"), self.errors, Qt.BottomDockWidgetArea, "errorsDock")
        self.device_console = DeviceConsole()
        self.device_console.commandRequested.connect(self.evaluate_repl)
        self.device_console.interruptRequested.connect(self.cancel_device_operation)
        console_dock = self._dock(tr("Device Console"), self.device_console, Qt.BottomDockWidgetArea, "deviceConsoleDock")
        docks = {dock.objectName(): dock for dock in self.findChildren(QDockWidget)}
        for name in ("errorsDock", "componentsDock"):
            self.tabifyDockWidget(docks["outputDock"], docks[name])
        self.tabifyDockWidget(docks["outputDock"], console_dock)
        docks["outputDock"].raise_()
        self.resizeDocks([docks["outputDock"]], [170], Qt.Vertical)

    def _make_central_tabs(self):
        self.sim_panel = SimPanel(self.document)
        self.sim_panel.started.connect(lambda: self._running_changed(True))
        self.sim_panel.stopped.connect(lambda: self._running_changed(False))
        self.sim_panel.frameReady.connect(self._first_frame)
        self.sim_panel.output.connect(self._sim_output)
        self.sim_panel.error.connect(self.append_error)
        self.code_panel = CodePanel(self.document)
        self.code_panel.stopRequested.connect(self.stop_simulation)
        self._sync_designers()
        self.code_tab_index = self.tabs.addTab(self.code_panel, tr("Code"))
        self.sim_tab_index = self.tabs.addTab(self.sim_panel, tr("Simulator"))
        self.tabs.currentChanged.connect(self._request_preview)
        self.tabs.currentChanged.connect(self._schedule_live)

    def _sync_designers(self):
        pages = self.document.project.pages
        ids = {page.id for page in pages}
        for page_id, (index, view) in list(self.designers.items()):
            if page_id not in ids:
                self.tabs.removeTab(self.tabs.indexOf(view))
                del self.designers[page_id]
        for position, page in enumerate(pages):
            if page.id not in self.designers:
                view = DesignerView(self.document, page.id)
                view.designer_scene.selectionNamesChanged.connect(self.properties.set_selection)
                view.designer_scene.widgetActivated.connect(self.open_handler)
                view.setProperty("_lvgl_dynamic_tab", True)
                view.designer_scene.show_preview = self.preview_action.isChecked()
                view.designer_scene.widgetsReshaped.connect(self._preview_drag)
                view.designer_scene.contextMenuRequested.connect(self._canvas_menu)
                self.designers[page.id] = (position, view)
                self.tabs.insertTab(min(position, self.tabs.count()), view, page.name)
            else:
                view = self.designers[page.id][1]
                self.designers[page.id] = (position, view)
                self.tabs.setTabText(self.tabs.indexOf(view), page.name)
                view.designer_scene.set_page(page.id)

    def _board_limits(self):
        board = self.document.project.board
        saved = self.settings.value(f"device/memory/{board['id']}", "") if board else ""
        return json.loads(saved) if saved else {}

    def _remember_board_memory(self, info):
        board = self.document.project.board
        if board and info.get("memoryFree") is not None:
            self.settings.setValue(f"device/memory/{board['id']}", json.dumps({"ram": info["memoryFree"], "flash": info.get("filesystemFree"), "mpy": info.get("mpy")}))

    def _budget_updated(self, budget):
        self._budget = budget
        self._show_budget()

    def _show_budget(self):
        limits = self._board_limits()
        self.budget_label.setText(budget_text(self._budget, limits))
        level = budget_level(self._budget, limits) if self._budget else 0
        self.budget_label.setStyleSheet({0: "", 1: f"color: {theme.WARNING}", 2: f"color: {theme.error_color()}; font-weight: bold"}[level])
        tip = tr("Flash: files that would go on the board. RAM: measured in the 64-bit simulator, so an overestimate, without video buffers.")
        if limits:
            tip += "\n" + tr("Limits are the free memory read from the board at the last connection.")
        else:
            tip += "\n" + tr("Connect the board to compare these values with the available memory.")
        self.budget_label.setToolTip(tip)

    def _schedule_budget(self):
        if hasattr(self, "budget_monitor"):
            self.budget_monitor.schedule(self.document.project, self._board_limits().get("mpy"))

    def _document_changed(self):
        if hasattr(self, "resolution_selector"):
            self.resolution_selector.rebuild()
        self._sync_device_session()
        self._schedule_budget()
        self._sync_designers()
        self.rebuild_project_tree()
        self._update_title()
        self._update_device_actions()
        self._request_preview()
        self._schedule_live()

    def _toggle_mcp(self, enabled):
        try:
            mcp_server.set_enabled(enabled)
        except OSError as exc:
            self.mcp_action.setChecked(not enabled)
            self.append_error(str(exc))
            return
        self.statusBar().showMessage(tr("MCP server on: agents can use lvgl-mpy-studio mcp.") if enabled else tr("MCP server off."), 5000)

    def _on_scene(self, method, *arguments):
        view = self._active_designer()
        if view is not None:
            getattr(view.designer_scene, method)(*arguments)

    def _select_all(self):
        text = self._focused_text()
        if text is not None:
            text.selectAll()
        else:
            self._on_scene("select_all")

    def _canvas_menu(self, position):
        menu = QMenu(self)
        menu.addActions((self.cut_action, self.copy_action, self.paste_action, self.duplicate_action, self.delete_action))
        menu.addSeparator()
        menu.addAction(self.arrange_menu.menuAction())
        menu.addAction(self.select_all_action)
        menu.exec(position)

    def _active_designer(self):
        widget = self.tabs.currentWidget()
        return widget if isinstance(widget, DesignerView) else None

    @staticmethod
    def _focused_text():
        widget = QApplication.focusWidget()
        return widget if isinstance(widget, (QLineEdit, QPlainTextEdit)) else None

    def _clipboard(self, operation):
        text = self._focused_text()
        if text is not None:
            getattr(text, operation)()
            return
        view = self._active_designer()
        if view is not None:
            scene = view.designer_scene
            scene.paste() if operation == "paste" else scene.copy_selected(cut=operation == "cut")

    def _delete(self):
        text = self._focused_text()
        if isinstance(text, QPlainTextEdit):
            if not text.isReadOnly():
                text.textCursor().removeSelectedText()
        elif text is not None:
            text.del_()
        elif self._active_designer() is not None:
            self._active_designer().designer_scene.delete_selected()

    def _toggle_preview(self, enabled):
        self.settings.setValue("designer/preview", enabled)
        self.preview_renderer.forget()
        for _index, view in self.designers.values():
            view.designer_scene.set_preview(enabled)
        self._request_preview()

    def _request_preview(self, *_ignored):
        view = self.tabs.currentWidget()
        if not self.preview_action.isChecked() or not isinstance(view, DesignerView):
            return
        pages = self.document.project.pages
        page_id = view.designer_scene.page_id
        index = next((position for position, page in enumerate(pages) if page.id == page_id), None)
        if index is not None:
            self.preview_renderer.request(self.document.project, page_id, index)

    def _preview_drag(self):
        """While dragging the real frame follows the widget, without duplicates."""
        view = self._active_designer()
        if view is None or not self.preview_action.isChecked():
            return
        if self.preview_renderer.busy:
            self._drag_frame_pending = True
            return
        scene = view.designer_scene
        pages = self.document.project.pages
        index = next((position for position, page in enumerate(pages) if page.id == scene.page_id), None)
        pending = scene.pending_geometry()
        if index is None or not pending:
            return
        project = copy.deepcopy(self.document.project)
        for widget in project.widgets:
            if widget.id in pending:
                widget.props.update(pending[widget.id])
        self.preview_renderer.request(project, scene.page_id, index, immediate=True)

    def _preview_rendered(self, page_id, pixels, width, height):
        entry = self.designers.get(page_id)
        if entry and self.preview_action.isChecked():
            entry[1].designer_scene.set_preview(True, frame_image(pixels, width, height) if pixels else None)
        if self._drag_frame_pending:
            self._drag_frame_pending = False
            self._preview_drag()

    def _toggle_grid(self, enabled):
        for _index, view in self.designers.values():
            view.designer_scene.show_grid = enabled
            view.designer_scene.grid_size = 8 if enabled else 1
            view.designer_scene.update()

    def _zoom(self, factor):
        view = self._active_designer()
        if view is None:
            return
        zoom = view.transform().m11() * factor
        if 0.5 <= zoom <= 4:
            view.scale(factor, factor)

    def _fit_canvas(self):
        view = self._active_designer()
        if view is not None:
            display = self.document.project.display
            view.fitInView(QRectF(-8, -8, display.width + 16, display.height + 16), Qt.KeepAspectRatio)

    def _update_undo_text(self):
        stack = self.document.undo_stack
        index = stack.index()
        self.undo_action.setText(tr("Undo {command}", command=stack.command(index - 1).text()) if index else tr("Undo"))
        self.redo_action.setText(tr("Redo {command}", command=stack.command(index).text()) if index < stack.count() else tr("Redo"))

    def change_language(self, language):
        apply_language(self, language)
        self._apply_mnemonics()
        self.rebuild_project_tree()
        stack = self.document.undo_stack
        for position in range(stack.count()):
            command = stack.command(position)
            source = getattr(command, "_lvgl_source_text", command.text())
            command._lvgl_source_text = source
            command.setText(tr(source))
        self._update_undo_text()
        self.statusBar().showMessage(tr("Ready"))
        self._update_device_actions()

    @property
    def run_target(self):
        project = self.document.project
        saved = project.runTarget or {}
        if saved.get("kind") == "board" and project.board:
            return board_target(project.board["id"])
        return SIMULATOR_MICROPYTHON

    def select_run_target(self, target):
        if target == self.run_target:
            self._update_device_actions()
            return True
        profile = None
        if target.is_board and (self.document.project.board or {}).get("id") != target.profile_id:
            if self.sim_panel.running or self.device_app_active or self._worker is not None:
                self.statusBar().showMessage(tr("Stop the session before changing the resolution or profile."), 5000)
                self._update_device_actions()
                return False
            profile = self.profile_store.get(target.profile_id)
            try:
                validate_profile(profile)
            except ValueError as exc:
                self.append_error(str(exc))
                self._update_device_actions()
                return False
            mode = self._resize_mode((profile["logicalWidth"], profile["logicalHeight"]))
            if mode is None:
                self._update_device_actions()
                return False
        def mutate(project):
            project.runTarget = None if target == SIMULATOR_MICROPYTHON else {"kind": target.kind, "language": "micropython"}
            if profile:
                project.board = portable_profile(profile)
                project.resize(profile["logicalWidth"], profile["logicalHeight"], mode)
        if not self.document.execute(tr("Change run target"), mutate):
            self.statusBar().showMessage(tr("Stop the session before changing the resolution or profile."), 5000)
            self._update_device_actions()
            return False
        if profile:
            self._report_outside(profile["logicalWidth"], profile["logicalHeight"])
        return True

    def show_about(self):
        info = getattr(self, "_device_info", None) or {}
        missing = tr("Version not detected") if self.device.port else tr("Board not connected")
        micro_version = info.get("implementationVersion")
        if isinstance(micro_version, (list, tuple)):
            micro_version = ".".join(str(part) for part in micro_version if str(part))
        micro_version = micro_version or missing
        lvgl_version = info.get("lvglVersion") or missing
        QMessageBox.about(
            self,
            tr("About LVGL MPY Studio"),
            f"<h2>LVGL MPY Studio</h2>"
            f"<p><b>{tr('IDE version')}:</b> {__version__}<br>"
            f"<b>MicroPython:</b> {micro_version}<br>"
            f"<b>LVGL:</b> {lvgl_version}</p>"
            f"<p><b>{tr('Credits')}:</b> Nunzio Raciti (in vibe coding)</p>"
            f"<p>Copyright (c) 2026 Nunzio Raciti<br>{tr('License: GPL-3.0-or-later. Generated code is under the MIT license.')}<br>"
            f"{tr('This program comes with absolutely no warranty. It is free software: you may redistribute and modify it under the terms of the license.')}</p>",
        )

    def _restore_layout(self):
        state = self.settings.value("windowState")
        geometry = self.settings.value("windowGeometry")
        if state:
            self.restoreState(state, self.LAYOUT_VERSION)
        if geometry:
            self.restoreGeometry(geometry)

    def closeEvent(self, event):
        if self._worker is not None:
            self.cancel_device_operation()
            self.statusBar().showMessage(tr("Wait for the device operation to finish."))
            event.ignore()
            return
        if self._building:
            self.statusBar().showMessage(tr("Wait for the executable build to finish."))
            event.ignore()
            return
        if not self._confirm_discard():
            event.ignore()
            return
        self.budget_monitor.stop()
        self.preview_renderer.stop()
        self.sim_panel.shutdown()
        self.device.disconnect()
        if self._web_server is not None:
            self._web_server.shutdown()
            self._web_server = None
        self.settings.setValue("windowState", self.saveState(self.LAYOUT_VERSION))
        self.settings.setValue("windowGeometry", self.saveGeometry())
        event.accept()
