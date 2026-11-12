from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any
from uuid import uuid4

from .components import COMPONENTS, block_for, is_component, register_project_blocks
from .events import EVENTS, PAGE_EVENTS, default_event, events_for, handler_name
from .i18n import tr
from .names import allocate_name, validate_name
from lvgl_mpy_studio.gen.identifiers import sanitize_identifier


@dataclass
class Display:
    width: int = 800
    height: int = 480
    colorFormat: str = "RGB565"

    def __post_init__(self):
        if not 1 <= self.width <= 10000 or not 1 <= self.height <= 10000:
            raise ValueError("Invalid display size")
        if self.colorFormat != "RGB565":
            raise ValueError("Only RGB565 is supported")


@dataclass
class Widget:
    type: str
    name: str
    id: str = field(default_factory=lambda: uuid4().hex)
    props: dict[str, Any] = field(default_factory=dict)
    events: dict[str, str] = field(default_factory=dict)
    parentId: str | None = None
    customStyles: dict[str, Any] = field(default_factory=dict)
    animations: list[dict[str, Any]] = field(default_factory=list)
    binding: dict[str, Any] | None = None

    def to_dict(self):
        return {"id": self.id, "name": self.name, "type": self.type, "props": self.props, "events": self.events, **({"parentId": self.parentId} if self.parentId else {}), "customStyles": self.customStyles, "animations": self.animations, **({"binding": self.binding} if self.binding else {})}


@dataclass
class Page:
    name: str
    widgets: list[Widget] = field(default_factory=list)
    canvasSize: tuple[int, int] = (800, 480)
    id: str = field(default_factory=lambda: uuid4().hex)
    designSize: tuple[int, int] | None = None  # resolution the widgets are drawn for, if different from the current one

    def to_dict(self):
        return {"id": self.id, "name": self.name, "canvasSize": list(self.canvasSize), **({"designSize": list(self.designSize)} if self.designSize else {}), "widgets": [widget.to_dict() for widget in self.widgets]}


@dataclass
class Handler:
    widget: str
    event: str
    body: str = ""

    def to_dict(self):
        return {"widget": self.widget, "event": self.event, "body": self.body}


@dataclass
class UserModule:
    """A user .py module: name is the name it is imported with, and the name of the file."""
    name: str
    source: str = ""
    id: str = field(default_factory=lambda: uuid4().hex)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "source": self.source}


@dataclass
class Code:
    module: str = ""
    handlers: dict[str, Handler] = field(default_factory=dict)

    def to_dict(self):
        return {"module": self.module, "handlers": {name: handler.to_dict() for name, handler in self.handlers.items()}}


def _run_target(value):
    """An unreadable run target must not stop the project from opening."""
    if isinstance(value, dict) and value.get("kind") in ("simulator", "board") and value.get("language") in ("micropython", "c"):
        return {"kind": value["kind"], "language": value["language"]}
    return None


SCHEMA_VERSIONS = (1, 2, 3, 4)
VALIDATED_VERSIONS = (2, 3, 4)
MODULES_SCHEMA = 3  # the first version with user modules
BLOCKS_SCHEMA = 4  # the first version with blocks other than the Buzzer
OLD_COMPONENTS = ("buzzer", "timer")  # the components an IDE before blocks knows

RESIZE_MODES = ("keep", "adapt", "stretch")
UNIT_PROPS = (
    "radius", "borderWidth", "lineWidth", "padTop", "padBottom", "padLeft", "padRight", "padRow", "padColumn",
    "tabBarSize", "sidebarWidth", "headerHeight", "majorTickLength", "minorTickLength",
)
UNIT_STYLES = ("border_width", "pad_top", "pad_bottom", "pad_left", "pad_right", "radius", "shadow_width", "shadow_ofs_x", "shadow_ofs_y")


def content_revision(data):
    """Revision of some content: SHA-256 of the bytes, the same on every system."""
    return hashlib.sha256(data).hexdigest()


def file_revision(path):
    """Revision of the file on disk, or None if it does not exist."""
    try:
        return content_revision(Path(path).read_bytes())
    except FileNotFoundError:
        return None


def _in_builtin_font(char):
    """Montserrat as built into LVGL: printable ASCII, the degree sign, the bullet and the LVGL symbols."""
    code = ord(char)
    return 0x20 <= code <= 0x7E or char in "\n\r\t°•" or 0xF000 <= code <= 0xF8FF


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


@dataclass
class Project:
    projectName: str = "Untitled"
    pages: list[Page] = field(default_factory=lambda: [Page("main")])
    display: Display = field(default_factory=Display)
    code: Code = field(default_factory=Code)
    currentPageId: str | None = None
    schemaVersion: int = 2
    assets: dict[str, Any] = field(default_factory=dict)
    variables: list[dict[str, Any]] = field(default_factory=list)
    extensions: dict[str, Any] = field(default_factory=dict)
    board: dict[str, Any] | None = None
    runTarget: dict[str, str] | None = None
    # Tells the app on the board apart from those of other projects with the same name.
    projectId: str = field(default_factory=lambda: uuid4().hex)
    modules: list[UserModule] = field(default_factory=list)

    def __post_init__(self):
        if not self.pages:
            raise ValueError("The project needs at least one page")
        if self.currentPageId not in {page.id for page in self.pages}:
            self.currentPageId = self.pages[0].id

    def set_display_size(self, width, height):
        self.display.width = width
        self.display.height = height
        self.display.__post_init__()
        for page in self.pages:
            page.canvasSize = (width, height)

    def scale_to(self, width, height, keep_aspect=False):
        """Bring the whole project to a new resolution: adapt (keep_aspect) or stretch."""
        self.resize(width, height, "adapt" if keep_aspect else "stretch")

    def resize(self, width, height, mode="stretch"):
        """Change the resolution, larger or smaller. mode says what to do with the widgets.

        keep: they stay where they are; each page remembers the resolution it is drawn for, to adapt it later.
        stretch: each axis scales on its own, the page stays full but shapes are distorted.
        adapt: sizes and fonts use one factor, so circles and squares stay so, and the position
        follows the anchor deduced from where the widget is.
        """
        if mode not in RESIZE_MODES:
            raise ValueError(f"Unknown mode: {mode}")
        current = (self.display.width, self.display.height)
        for page in self.pages:
            if mode == "keep":
                page.designSize = page.designSize or current
            else:
                self._resize_page(page, page.designSize or current, (width, height), mode == "adapt")
                page.designSize = None  # the widgets are now drawn for the new resolution
            if page.designSize == (width, height):
                page.designSize = None
        self.set_display_size(width, height)

    def adapt_page(self, page, mode="adapt"):
        """Bring to the current resolution a page still drawn for another one."""
        if mode not in ("adapt", "stretch"):
            raise ValueError(f"Unknown mode: {mode}")
        if page.designSize:
            self._resize_page(page, page.designSize, (self.display.width, self.display.height), mode == "adapt")
            page.designSize = None

    def _resize_page(self, page, old_size, new_size, adapt):
        (old_width, old_height), (width, height) = old_size, new_size
        scale_x, scale_y = width / old_width, height / old_height
        unit = min(scale_x, scale_y)
        sizes = self.font_sizes()
        if (scale_x, scale_y) == (1, 1):
            return
        boxes = {widget.id: (widget.props.get("width"), widget.props.get("height")) for widget in page.widgets}
        if adapt:
            self._adapt(page.widgets, old_size, width, height, unit, sizes)
        else:
            for widget in page.widgets:
                props = widget.props
                for key in ("x", "y", "width", "height"):
                    if _is_number(props.get(key)):
                        scaled = round(props[key] * (scale_x if key in ("x", "width") else scale_y))
                        props[key] = max(1, scaled) if key in ("width", "height") else scaled
        for widget in page.widgets:
            props = widget.props
            _scale_points(props, boxes[widget.id])
            for values, keys, font in ((props, UNIT_PROPS, "fontSize"), (widget.customStyles, UNIT_STYLES, "text_font_size")):
                for key in keys:
                    if _is_number(values.get(key)) and values[key]:
                        sign = 1 if values[key] > 0 else -1  # shadow offsets can be negative
                        values[key] = sign * max(1, round(abs(values[key]) * unit))
                if _is_number(values.get(font)):
                    values[font] = min(sizes, key=lambda size: abs(size - values[font] * unit))

    @staticmethod
    def _adapt(widgets, old_size, width, height, unit, sizes):
        """Adapt widgets from containers to children: each follows its container, already adapted.

        The container is the parent or, if there is one, the smallest widget that already encloses
        it on screen and lies under it: a dot drawn on a ring must stay on the ring.
        """
        by_id = {widget.id: widget for widget in widgets}
        frames = {}
        placed = [widget for widget in widgets if all(_is_number(widget.props.get(key)) for key in ("x", "y", "width", "height"))]
        for index, widget in enumerate(placed):
            parent = widget.parentId if widget.parentId in by_id else None
            inside = [other for other in placed[:index] if (other.parentId if other.parentId in by_id else None) == parent and _contains(other.props, widget.props) and other.props["width"] * other.props["height"] > widget.props["width"] * widget.props["height"]]
            frames[widget.id] = (parent, min(inside, key=lambda other: other.props["width"] * other.props["height"]) if inside else None)
        groups = _groups(widgets, frames, old_size)
        old = {None: (0, 0, *old_size)}
        new = {None: (0, 0, width, height)}
        moved = {}
        def depth(widget):
            level, seen = 0, set()
            while widget.parentId in by_id and widget.parentId not in seen:
                seen.add(widget.parentId)
                widget, level = by_id[widget.parentId], level + 1
            return level
        order = {widget.id: index for index, widget in enumerate(widgets)}
        for widget in sorted((widget for widget in widgets if widget.id in frames), key=lambda widget: (depth(widget), order[widget.id])):
            props = widget.props
            parent, frame = frames[widget.id]
            old[widget.id] = (props["x"], props["y"], props["width"], props["height"])
            group = groups.get(widget.id)
            if group is not None:
                # A grid or a row moves as a whole: the anchor applies to the bounding box of the group.
                key = (group, parent, frame.id if frame else None)  # equal groups in different containers are different
                if key not in moved:
                    gx, gy, gw, gh = group
                    if frame is None:
                        (_ox, _oy, old_w, old_h), (nfx, nfy, new_w, new_h) = old[parent], new[parent]
                        fx = fy = nfx = nfy = 0
                    else:
                        (fx, fy, old_w, old_h), (nfx, nfy, new_w, new_h) = old[frame.id], new[frame.id]
                    moved[key] = (nfx + adapt_axis(gx - fx, gw, old_w, new_w, unit)[0], nfy + adapt_axis(gy - fy, gh, old_h, new_h, unit)[0])
                x = moved[key][0] + round((props["x"] - group[0]) * unit)
                y = moved[key][1] + round((props["y"] - group[1]) * unit)
                w, h = max(1, round(props["width"] * unit)), max(1, round(props["height"] * unit))
            elif frame is None:
                (_ox, _oy, old_w, old_h), (_nx, _ny, new_w, new_h) = old[parent], new[parent]
                x, w = adapt_axis(props["x"], props["width"], old_w, new_w, unit)
                y, h = adapt_axis(props["y"], props["height"], old_h, new_h, unit)
            else:
                (fx, fy, fw, fh), (nfx, nfy, nfw, nfh) = old[frame.id], new[frame.id]
                x, w = adapt_axis(props["x"] - fx, props["width"], fw, nfw, unit)
                y, h = adapt_axis(props["y"] - fy, props["height"], fh, nfh, unit)
                x, y = x + nfx, y + nfy
            x, y, w, h = _fit_font(widget, x, y, w, h, unit, sizes)
            _px, _py, parent_w, parent_h = new[parent]
            w, h = min(w, parent_w), min(h, parent_h)
            x = max(0, min(x, parent_w - w)) if w <= parent_w else x  # growth must not leave the container
            y = max(0, min(y, parent_h - h)) if h <= parent_h else y
            props["x"], props["y"], props["width"], props["height"] = x, y, w, h
            new[widget.id] = (x, y, w, h)

    def font_sizes(self):
        """Montserrat sizes text can be drawn in: those of the project's board, or of the simulator."""
        from .boards import profile_fonts

        return profile_fonts(self.board)

    def text_warnings(self):
        """What will not be drawn as asked: font sizes the target lacks and characters outside the built-in font."""
        from .assets import font_warnings, image_warnings, uses_project_font

        sizes = self.font_sizes()
        target = self.board.get("name", self.board.get("id")) if self.board else tr("the simulator")
        warnings = []
        for widget in self.widgets:
            if uses_project_font(self, widget):  # its own font: any size, and the characters it has
                continue
            for values, key in ((widget.props, "fontSize"), (widget.customStyles, "text_font_size")):
                size = values.get(key)
                if _is_number(size) and size and size not in sizes:
                    nearest = min(sizes, key=lambda candidate: abs(candidate - size))
                    warnings.append(tr("{name}: font size {size} is not available on {target}, the text is drawn at {nearest}. Sizes: {sizes}", name=widget.name, size=size, target=target, nearest=nearest, sizes=", ".join(str(item) for item in sizes)))
            missing = sorted({char for value in widget.props.values() if isinstance(value, str) for char in value if not _in_builtin_font(char)})
            if missing and any(key in widget.props for key in ("text", "options", "placeholder")):
                warnings.append(tr("{name}: the built-in font has no glyph for {characters}: they are drawn as empty boxes", name=widget.name, characters=" ".join(f"{char} (U+{ord(char):04X})" for char in missing[:8])))
        return warnings + image_warnings(self) + font_warnings(self)

    def new_page(self, name):
        return Page(name, canvasSize=(self.display.width, self.display.height))

    def resolution_diagnostics(self):
        expected = (self.display.width, self.display.height)
        return [f"pages[{index}].canvasSize: atteso {expected[0]}×{expected[1]}, trovato {page.canvasSize[0]}×{page.canvasSize[1]}" for index, page in enumerate(self.pages) if tuple(page.canvasSize) != expected]

    def screen_position(self, widget):
        """Position on screen: x and y of a widget are relative to its container."""
        by_id = {item.id: item for item in self.widgets}
        x = y = 0
        seen = set()
        while widget is not None and widget.id not in seen:
            seen.add(widget.id)
            x += widget.props.get("x", 0) if _is_number(widget.props.get("x", 0)) else 0
            y += widget.props.get("y", 0) if _is_number(widget.props.get("y", 0)) else 0
            widget = by_id.get(widget.parentId)
        return x, y

    def widgets_outside(self, width=None, height=None):
        width = width or self.display.width
        height = height or self.display.height
        outside = []
        for widget in self.widgets:
            if is_component(widget.type):
                continue
            x, y = self.screen_position(widget)
            size = [widget.props.get(key, 0) if _is_number(widget.props.get(key, 0)) else 0 for key in ("width", "height")]
            if x < 0 or y < 0 or x + size[0] > width or y + size[1] > height:
                outside.append(widget.name)
        return outside

    def initial_page_index(self):
        """The page the app starts from, on the simulator as on the board."""
        return next((index for index, page in enumerate(self.pages) if page.id == self.currentPageId), 0)

    def subtree(self, widget):
        """The widget and everything it contains, in page order."""
        page = next((page for page in self.pages if widget in page.widgets), None)
        if page is None:
            return [widget]
        inside = {widget.id}
        grown = True
        while grown:
            grown = False
            for item in page.widgets:
                if item.parentId in inside and item.id not in inside:
                    inside.add(item.id)
                    grown = True
        return [item for item in page.widgets if item.id in inside]

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Invalid project: no pages")
        version = data.get("schemaVersion", 1)
        if version not in SCHEMA_VERSIONS:
            raise ValueError(f"Unsupported project version: {version}")
        if not isinstance(data.get("pages"), list) or not data["pages"]:
            raise ValueError("Invalid project: no pages")
        register_project_blocks(data)  # a project brings the blocks it uses: it opens where they are not installed
        for index, raw_page in enumerate(data["pages"]):  # version 1 does not go through the full validation
            if not isinstance(raw_page, dict) or not all(isinstance(raw, dict) and isinstance(raw.get("type"), str) for raw in raw_page.get("widgets") or []):
                raise ValueError(f"Invalid project: pages[{index}] must be an object with a list of widgets")
        raw_display = data.get("display") or {}
        first_size = data["pages"][0].get("canvasSize") or {}
        if isinstance(first_size, list):
            first_size = {"width": first_size[0], "height": first_size[1]}
        display = Display(raw_display.get("width", first_size.get("width", 800)), raw_display.get("height", first_size.get("height", 480)), raw_display.get("colorFormat", "RGB565"))
        pages, used_names = [], set()
        for page_index, raw_page in enumerate(data["pages"]):
            size = raw_page.get("canvasSize") or {"width": display.width, "height": display.height}
            if isinstance(size, list): size = {"width": size[0], "height": size[1]}
            page = Page(raw_page.get("name") or f"Pagina {page_index + 1}", id=raw_page.get("id") or f"page_{uuid4().hex}", canvasSize=(size.get("width", 800), size.get("height", 480)))
            design = raw_page.get("designSize")
            if isinstance(design, dict):
                design = [design.get("width"), design.get("height")]
            if isinstance(design, list) and len(design) == 2 and all(isinstance(value, int) and value > 0 for value in design):
                page.designSize = tuple(design)
            for index, raw in enumerate(raw_page.get("widgets") or []):
                name = raw.get("name")
                if version == 1 or validate_name(name, used_names):
                    base = re.sub(r"(?<!^)(?=[A-Z])", "_", raw.get("type", "widget")).lower()
                    candidate = allocate_name(base, used_names) if not name else sanitize_identifier(str(name), raw.get("type", "widget"))
                    number = 2
                    base_candidate = candidate
                    while validate_name(candidate, used_names):
                        candidate = f"{base_candidate}_{number}"
                        number += 1
                    name = candidate
                used_names.add(name)
                events = {}
                if version != 1:  # from version 2 on, events are already handler names
                    events = dict(raw.get("events") or {})
                else:
                    for event in raw.get("events") or []:
                        event_name = str(event.get("type", "")).removeprefix("LV_EVENT_")
                        if event_name in EVENTS:
                            events[event_name] = handler_name(name, event_name)
                page.widgets.append(Widget(raw["type"], name, raw.get("id") or uuid4().hex, dict(raw.get("props") or {}), events, raw.get("parentId"), dict(raw.get("customStyles") or {}), list(raw.get("animations") or []), raw.get("binding")))
            pages.append(page)
        code_data = data.get("code") or {}
        code = Code(str(code_data.get("module") or ""))
        for name, raw in (code_data.get("handlers") or {}).items():
            code.handlers[name] = Handler(raw.get("widget", ""), raw.get("event", ""), str(raw.get("body") or ""))
        if version == 1:
            for page in pages:
                for widget in page.widgets:
                    original = next(raw for raw in data["pages"][pages.index(page)]["widgets"] if raw.get("id") == widget.id)
                    for event in original.get("events") or []:
                        event_name = str(event.get("type", "")).removeprefix("LV_EVENT_")
                        handler = widget.events.get(event_name)
                        if handler and handler not in code.handlers:
                            code.handlers[handler] = Handler(widget.name, event_name, str(event.get("code") or ""))
        known = {"schemaVersion", "projectName", "display", "pages", "code", "currentPageId", "assets", "variables", "board", "runTarget", "projectId", "modules"}
        extensions = {key: value for key, value in data.items() if key not in known}
        board = dict(data["board"]) if isinstance(data.get("board"), dict) else None
        project = cls(str(data.get("projectName") or "Untitled"), pages, display, code, data.get("currentPageId"), assets=dict(data.get("assets") or {}), variables=list(data.get("variables") or []), extensions=extensions, board=board, runTarget=_run_target(data.get("runTarget")))
        project.projectId = str(data.get("projectId") or "")  # empty in files created before the id: it gets one when saved
        raw_modules = data.get("modules") if isinstance(data.get("modules"), list) else []
        for raw in raw_modules:
            if isinstance(raw, dict):
                project.modules.append(UserModule(str(raw.get("name") or ""), str(raw.get("source") or ""), str(raw.get("id") or uuid4().hex)))
        return project

    @classmethod
    def load(cls, path):
        return cls.load_with_revision(path)[0]

    @classmethod
    def load_with_revision(cls, path):
        """The project and the revision of the bytes read: one read, so the two match."""
        raw = Path(path).read_bytes()
        data = json.loads(raw.decode("utf-8"))
        if isinstance(data, dict) and data.get("schemaVersion", 1) in VALIDATED_VERSIONS:
            from .validation import validate_project
            validate_project(data)
        return cls.from_dict(data), content_revision(raw)

    def to_dict(self):
        # Version 3 only when needed: an IDE 0.3 still opens projects without modules and refuses the
        # others, instead of opening them and stopping at start-up with ImportError.
        # Version 4 in the same way: an IDE before blocks would not know what the components are.
        used = {widget.type for widget in self.widgets if is_component(widget.type)}
        version = BLOCKS_SCHEMA if used - set(OLD_COMPONENTS) else MODULES_SCHEMA if self.modules else 2
        # The blocks in use travel with the project, as this IDE knows them now; the standard ones are in every IDE.
        carried = {name: block_for(name).to_dict() for name in sorted(used) if block_for(name) is not None and block_for(name).origin != "standard"}
        assets = {key: value for key, value in self.assets.items() if key != "blocks"} | ({"blocks": carried} if carried else {})
        result = {"schemaVersion": version, "projectName": self.projectName, "display": {"width": self.display.width, "height": self.display.height, "colorFormat": self.display.colorFormat}, "pages": [page.to_dict() for page in self.pages], "code": self.code.to_dict(), "currentPageId": self.currentPageId, "assets": assets, "variables": self.variables}
        if self.projectId:
            result["projectId"] = self.projectId
        if self.board is not None:
            result["board"] = self.board
        if self.runTarget is not None:
            result["runTarget"] = self.runTarget
        if self.modules:
            result["modules"] = [module.to_dict() for module in self.modules]
        result.update(self.extensions)
        return result

    def save(self, path):
        """Write the file atomically and return the revision of what was written."""
        target = Path(path)
        payload = json.dumps(self.to_dict(), ensure_ascii=False, indent=2) + "\n"
        temporary = None
        try:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", dir=target.parent, prefix=f".{target.name}.", suffix=".tmp", delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
            if target.exists():
                os.chmod(temporary, target.stat().st_mode)
            os.replace(temporary, target)
        except Exception:
            if temporary:
                temporary.unlink(missing_ok=True)
            raise
        return content_revision(payload.encode("utf-8"))

    @property
    def widgets(self):
        return [widget for page in self.pages for widget in page.widgets]

    @property
    def used_names(self):
        return {widget.name for widget in self.widgets}

    def find_widget(self, name):
        return next((widget for widget in self.widgets if widget.name == name), None)

    def add_widget(self, page, widget_type, props=None, name=None):
        definitions = {**widget_definitions(), **COMPONENTS}
        if widget_type not in definitions:
            raise ValueError(f"Unknown widget type: {widget_type}")
        name = name or allocate_name(widget_type, self.used_names)
        error = validate_name(name, self.used_names)
        if error: raise ValueError(error)
        merged = dict(definitions[widget_type].get("defaultProps") or {})
        merged.update(props or {})
        widget = Widget(widget_type, name, props=merged)
        page.widgets.append(widget)
        return widget

    def ensure_handler(self, widget_name, event=None):
        widget = self.find_widget(widget_name)
        is_page = widget is None and any(page.name == widget_name for page in self.pages)
        event = event or (default_event(widget.type) if widget else "SCREEN_LOADED" if is_page else "CLICKED")
        if event not in EVENTS: raise ValueError(tr("Unknown event: {event}", event=event))
        allowed = events_for(widget.type) if widget else PAGE_EVENTS if is_page else None
        if allowed is not None and event not in allowed:
            raise ValueError(tr("{name} has no {event} event. Events: {events}", name=widget_name, event=event, events=", ".join(allowed)))
        name = handler_name(widget_name, event)
        handler = self.code.handlers.get(name)
        if handler is None:
            handler = Handler(widget_name, event)
            self.code.handlers[name] = handler
        elif not handler.widget and handler.event == event:
            handler.widget = widget_name
        elif handler.widget != widget_name or handler.event != event:
            raise ValueError(f"Handler {name} already belongs to another object or event")
        if widget: widget.events[event] = name
        return name, handler

    def _code_scopes(self):
        """Every code text of the project, with the name to show in warnings: modules included."""
        return [("modulo (Generale)", self.code.module)] + [(name, handler.body) for name, handler in self.code.handlers.items()] + [(f"{module.name}.py", module.source) for module in self.modules]

    def rename_widget(self, old_name, new_name):
        error = validate_name(new_name, self.used_names - {old_name})
        if error: raise ValueError(error)
        widget = self.find_widget(old_name)
        if not widget: raise KeyError(old_name)
        widget.name = new_name
        replacements = {}
        for event, old_handler in list(widget.events.items()):
            new_handler = handler_name(new_name, event)
            widget.events[event] = new_handler
            replacements[old_handler] = new_handler
        for old, new in replacements.items():
            if old in self.code.handlers:
                self.code.handlers[new] = self.code.handlers.pop(old)
                self.code.handlers[new].widget = new_name
        pattern = re.compile(rf"\b{re.escape(old_name)}\b")
        warnings = []
        for scope, body in self._code_scopes():
            lines = [str(index) for index, line in enumerate(body.splitlines(), 1) if pattern.search(line)]
            if lines: warnings.append(tr("The code still uses {name} in {scope}, lines {lines}: update it by hand", name=old_name, scope=scope, lines=", ".join(lines)))
        return warnings

    def rename_page(self, page, new_name):
        """The handlers of the page refer to it by name: they are renamed with it."""
        old_name = page.name
        if not new_name:
            raise ValueError("The page name is empty")
        if any(page_constant(item.name) == page_constant(new_name) for item in self.pages if item is not page):
            raise ValueError(f"Page {new_name!r} already exists, or has the same constant {page_constant(new_name)}")
        page.name = new_name
        for name, handler in list(self.code.handlers.items()):
            if handler.widget == old_name and handler.event.startswith("SCREEN_"):  # a widget can have the same name as the page
                handler.widget = new_name
                renamed = handler_name(new_name, handler.event)
                self.code.handlers[renamed] = self.code.handlers.pop(name)
        constant = page_constant(old_name)
        warnings = []
        for scope, body in self._code_scopes():
            lines = [str(index) for index, line in enumerate(body.splitlines(), 1) if re.search(rf"\b{constant}\b", line)]
            if lines: warnings.append(tr("The code still uses {name} in {scope}, lines {lines}: update it by hand", name=constant, scope=scope, lines=", ".join(lines)))
        return warnings

    def remove_page(self, page):
        if len(self.pages) == 1:
            raise ValueError(tr("The last page cannot be deleted"))
        for widget in list(page.widgets):
            self.remove_widget(widget.name)
        self.pages.remove(page)
        if self.currentPageId == page.id:
            self.currentPageId = self.pages[0].id

    def remove_widget(self, name):
        """Remove the widget with everything it contains: the children have coordinates relative to it."""
        widget = self.find_widget(name)
        if not widget: return
        removed = self.subtree(widget)
        names = {item.name for item in removed}
        for page in self.pages:
            page.widgets = [item for item in page.widgets if item not in removed]
        for handler in self.code.handlers.values():
            if handler.widget in names: handler.widget = ""

GROUP_GAP = 0.25  # two widgets closer than this, relative to the smaller one, belong to the same group


def _groups(widgets, frames, page_size):
    """Sibling widgets close to each other, like the cells of a grid: {id: bounding box of the group}.

    Only widgets with the same container form a group: parent and widget under them.
    """
    def container(widget):
        parent, frame = frames[widget.id]
        if frame is not None:
            return frame.props["width"], frame.props["height"]
        owner = next((item for item in widgets if item.id == parent), None)
        return (owner.props["width"], owner.props["height"]) if owner else page_size
    def stretches(widget):
        width, height = container(widget)
        return widget.props["width"] >= STRETCH_SHARE * width or widget.props["height"] >= STRETCH_SHARE * height
    loose = [widget for widget in widgets if widget.id in frames and not stretches(widget)]  # a widget that stretches goes on its own
    owner = {widget.id: widget.id for widget in loose}
    def find(item):
        while owner[item] != item:
            owner[item] = owner[owner[item]]
            item = owner[item]
        return item
    for index, first in enumerate(loose):
        for second in loose[index + 1:]:
            if frames[first.id] != frames[second.id]:
                continue
            a, b = first.props, second.props
            gap = max(a["x"] - (b["x"] + b["width"]), b["x"] - (a["x"] + a["width"]), a["y"] - (b["y"] + b["height"]), b["y"] - (a["y"] + a["height"]))
            if gap <= GROUP_GAP * min(a["width"], a["height"], b["width"], b["height"]) and not _contains(a, b) and not _contains(b, a):
                owner[find(first.id)] = find(second.id)
    members = {}
    for widget in loose:
        members.setdefault(find(widget.id), []).append(widget.props)
    result = {}
    for widget in loose:
        group = members[find(widget.id)]
        if len(group) > 1:
            left, top = min(item["x"] for item in group), min(item["y"] for item in group)
            right, bottom = max(item["x"] + item["width"] for item in group), max(item["y"] + item["height"] for item in group)
            result[widget.id] = (left, top, right - left, bottom - top)
    return result


def _scale_points(props, old_box):
    """The points of a line are relative to its box: they follow its new size."""
    old_width, old_height = old_box
    points = props.get("points")
    if not isinstance(points, str) or not _is_number(old_width) or not _is_number(old_height) or not old_width or not old_height:
        return
    scale_x, scale_y = props["width"] / old_width, props["height"] / old_height
    scaled = []
    for pair in points.split():
        try:
            x, y = (float(value) for value in pair.split(","))
        except ValueError:
            return  # an unknown format stays as it is
        scaled.append(f"{round(x * scale_x)},{round(y * scale_y)}")
    props["points"] = " ".join(scaled)


def _contains(outer, inner):
    return outer["x"] <= inner["x"] and outer["y"] <= inner["y"] and inner["x"] + inner["width"] <= outer["x"] + outer["width"] and inner["y"] + inner["height"] <= outer["y"] + outer["height"]


def _fit_font(widget, x, y, width, height, unit, sizes):
    """Fonts come in few sizes: if the chosen one is larger than the scale, the label must grow with it.

    Labels only: buttons and boxes have the size of the drawing, and growing they would overlap.
    """
    if widget.type != "label":
        return x, y, width, height
    for values, key in ((widget.props, "fontSize"), (widget.customStyles, "text_font_size")):
        size = values.get(key)
        if _is_number(size) and size:
            chosen = min(sizes, key=lambda candidate: abs(candidate - size * unit))
            grow = chosen / (size * unit)
            if grow > 1.05:
                new_width, new_height = round(width * grow), round(height * grow)
                return x - (new_width - width) // 2, y - (new_height - height) // 2, new_width, new_height
    return x, y, width, height


STRETCH_SHARE = 0.8   # a widget at least this wide, relative to the container, stretches with it
BIG_SHARE = 0.5      # beyond this share of the container a widget does not anchor to the edges
EDGE_SHARE = 0.15     # a widget this close to an edge stays anchored to that edge


def adapt_axis(position, size, old_parent, new_parent, unit):
    """New position and size on one axis, with the anchor deduced from the position.

    Stretched if it fills almost all the container; anchored to the edge if it is close to it;
    otherwise its centre keeps the same proportion, so a row stays evenly spread.
    """
    if old_parent <= 0:
        return position, size
    before, after = position, old_parent - position - size
    if size >= STRETCH_SHARE * old_parent:
        start = round(before * unit)
        return start, max(1, new_parent - start - round(after * unit))
    new_size = max(1, round(size * unit))
    if size >= BIG_SHARE * old_parent:  # a large block looks better centred than resting on an edge
        center = (position + size / 2) * new_parent / old_parent
        return round(center - new_size / 2), new_size
    if before <= EDGE_SHARE * old_parent and before <= after:
        return round(before * unit), new_size
    if after <= EDGE_SHARE * old_parent:
        return new_parent - round(after * unit) - new_size, new_size
    center = (position + size / 2) * new_parent / old_parent
    return round(center - new_size / 2), new_size


def page_constant(name):
    """The ui.PAGE_… constant the code uses for a page: different names can give the same one."""
    return "PAGE_" + re.sub(r"\W", "_", str(name)).upper()


def widget_definitions():
    path = Path(__file__).parents[1] / "gen" / "widgets.json"
    return json.loads(path.read_text(encoding="utf-8"))
