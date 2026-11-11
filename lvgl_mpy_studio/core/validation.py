from .components import COMPONENTS
from .events import EVENTS
from .modules import validate_module_name
from .names import validate_name


def _dimensions(value, path, errors):
    if isinstance(value, list):
        if len(value) != 2:
            errors.append(f"{path}: width and height are required")
            return
        value = {"width": value[0], "height": value[1]}
    if not isinstance(value, dict):
        errors.append(f"{path}: invalid size")
        return
    for key in ("width", "height"):
        dimension = value.get(key, 800 if key == "width" else 480)
        if isinstance(dimension, bool) or not isinstance(dimension, int) or not 1 <= dimension <= 10000:
            errors.append(f"{path}.{key}: must be a whole number from 1 to 10000")


def validate_project(project):
    from .model import widget_definitions  # model imports this module to validate on load

    data = project.to_dict() if hasattr(project, "to_dict") else project
    errors, warnings = [], []
    if not isinstance(data, dict):
        raise ValueError("Invalid project: the document must be a JSON object")
    if data.get("schemaVersion", 1) not in (2, 3):
        raise ValueError(f"Unsupported project version: {data.get('schemaVersion')}")
    pages = data.get("pages")
    if not isinstance(pages, list) or not pages:
        raise ValueError("Invalid project: no pages")
    _dimensions(data["display"] if "display" in data else {}, "display", errors)
    definitions = {**widget_definitions(), **COMPONENTS}
    identifiers = {}
    used_names = set()
    page_names = set()
    code = data["code"] if "code" in data else {}
    if not isinstance(code, dict):
        errors.append("code: must be an object")
        code = {}
    handlers = code["handlers"] if "handlers" in code else {}
    if not isinstance(handlers, dict):
        errors.append("code.handlers: must be an object")
        handlers = {}

    def register_id(value, path):
        if not isinstance(value, str) or not value:
            errors.append(f"{path}: missing or invalid ID")
        elif value in identifiers:
            errors.append(f"{path}: duplicate ID of {identifiers[value]}")
        else:
            identifiers[value] = path

    for page_index, page in enumerate(pages):
        page_path = f"pages[{page_index}]"
        if not isinstance(page, dict):
            errors.append(f"{page_path}: must be an object")
            continue
        register_id(page.get("id"), f"{page_path}.id")
        page_name = page.get("name")
        if not isinstance(page_name, str) or not page_name:
            errors.append(f"{page_path}.name: missing page name")
        elif page_name in page_names:
            errors.append(f"{page_path}.name: duplicate page name {page_name!r}")
        else:
            page_names.add(page_name)
        size = page["canvasSize"] if "canvasSize" in page else {"width": 800, "height": 480}
        _dimensions(size, f"{page_path}.canvasSize", errors)
        if "designSize" in page:
            _dimensions(page["designSize"], f"{page_path}.designSize", errors)
        widgets = page["widgets"] if "widgets" in page else []
        if not isinstance(widgets, list):
            errors.append(f"{page_path}.widgets: must be a list")
            continue
        widget_ids = set()
        for widget_index, widget in enumerate(widgets):
            widget_path = f"{page_path}.widgets[{widget_index}]"
            if not isinstance(widget, dict):
                errors.append(f"{widget_path}: must be an object")
                continue
            widget_id = widget.get("id")
            register_id(widget_id, f"{widget_path}.id")
            if isinstance(widget_id, str) and widget_id:
                widget_ids.add(widget_id)
            widget_type = widget.get("type")
            if not isinstance(widget_type, str) or widget_type not in definitions:
                errors.append(f"{widget_path}.type: unknown type {widget_type!r}")
                continue
            name = widget.get("name")
            name_error = validate_name(name, used_names)
            if name_error:
                errors.append(f"{widget_path}.name: {name_error}")
            else:
                used_names.add(name)
            props = widget["props"] if "props" in widget else {}
            if not isinstance(props, dict):
                errors.append(f"{widget_path}.props: must be an object")
            else:
                definition = definitions[widget_type]
                supported = {item["name"] for item in definition.get("properties") or []} | set(definition.get("defaultProps") or {})
                for key in props.keys() - supported:
                    warnings.append(f"{widget_path}.props.{key}: unsupported property kept but ignored")
            events = widget["events"] if "events" in widget else {}
            if not isinstance(events, dict):
                errors.append(f"{widget_path}.events: must be an object")
            else:
                for event, handler_name in events.items():
                    event_path = f"{widget_path}.events.{event}"
                    if not isinstance(event, str) or event not in EVENTS:
                        errors.append(f"{event_path}: unknown event")
                    if not isinstance(handler_name, str) or not handler_name:
                        errors.append(f"{event_path}: invalid handler")
                        continue
                    declaration = handlers.get(handler_name)
                    if declaration is None:
                        errors.append(f"{event_path}: missing handler {handler_name!r}")
                    elif isinstance(declaration, dict) and isinstance(name, str):
                        if declaration.get("widget", "") != name or declaration.get("event") != event:
                            errors.append(f"{event_path}: does not match the owner or event of the handler")
        for widget_index, widget in enumerate(widgets):
            if not isinstance(widget, dict):
                continue
            parent = widget.get("parentId")
            if parent and (not isinstance(parent, str) or parent not in widget_ids):
                errors.append(f"{page_path}.widgets[{widget_index}].parentId: parent not found in the page")
        by_id = {widget.get("id"): widget for widget in widgets if isinstance(widget, dict) and isinstance(widget.get("id"), str) and widget.get("id")}
        for widget_index, widget in enumerate(widgets):
            if not isinstance(widget, dict) or not isinstance(widget.get("id"), str):
                continue
            seen = set()
            current = widget
            while current:
                parent = current.get("parentId")
                if not parent or not isinstance(parent, str):
                    break
                current_id = current.get("id")
                if not isinstance(current_id, str):
                    break
                if current_id in seen:
                    errors.append(f"{page_path}.widgets[{widget_index}].parentId: cycle in the containers")
                    break
                seen.add(current_id)
                current = by_id.get(parent)

    page_ids = {page.get("id") for page in pages if isinstance(page, dict) and isinstance(page.get("id"), str)}
    if "currentPageId" in data and (not isinstance(data["currentPageId"], str) or data["currentPageId"] not in page_ids):
        errors.append("currentPageId: initial page not found")
    if "module" in code and not isinstance(code["module"], str):
        errors.append("code.module: must be text")
    widgets_by_name = {
        widget.get("name"): widget
        for page in pages if isinstance(page, dict) and isinstance(page.get("widgets"), list)
        for widget in page["widgets"] if isinstance(widget, dict) and isinstance(widget.get("name"), str)
    }
    for name, handler in handlers.items():
        path = f"code.handlers.{name}"
        if not isinstance(name, str) or not name:
            errors.append(f"{path}: nome invalid handler")
        if not isinstance(handler, dict):
            errors.append(f"{path}: must be an object")
            continue
        event = handler.get("event")
        if not isinstance(event, str) or event not in EVENTS:
            errors.append(f"{path}.event: unknown event {event!r}")
        if "body" in handler and not isinstance(handler["body"], str):
            errors.append(f"{path}.body: must be text")
        owner = handler["widget"] if "widget" in handler else ""
        if not isinstance(owner, str):
            errors.append(f"{path}.widget: invalid reference")
            continue
        widget = widgets_by_name.get(owner)
        widget_events = widget.get("events") if widget else {}
        if widget and isinstance(event, str) and event in EVENTS and isinstance(widget_events, dict) and widget_events.get(event) != name:
            errors.append(f"{path}: does not match the handler declared by the widget")
        elif not widget and owner not in page_names:
            warnings.append(f"{path}: orphan handler kept and not connected")
    _modules(data, handlers, register_id, errors)
    if errors:
        raise ValueError("Invalid project:\n- " + "\n- ".join(errors))
    return warnings


def _modules(data, handlers, register_id, errors):
    if "modules" not in data:
        return
    modules = data["modules"]
    if not isinstance(modules, list):
        errors.append("modules: must be a list")
        return
    names = set()
    for index, module in enumerate(modules):
        path = f"modules[{index}]"
        if not isinstance(module, dict):
            errors.append(f"{path}: must be an object")
            continue
        register_id(module.get("id"), f"{path}.id")
        name = module.get("name")
        error = validate_module_name(name)
        if error:
            errors.append(f"{path}.name: {error}")
        elif name in names:
            errors.append(f"{path}.name: duplicate module {name!r}")
        elif name in handlers:
            errors.append(f"{path}.name: {name!r} is also the name of a handler")
        else:
            names.add(name)
        if not isinstance(module.get("source", ""), str):
            errors.append(f"{path}.source: must be text")
