"""Scripts of steps for the simulator: touches, waits, checks. Used by simulate and by the visual tests."""

from lvgl_mpy_studio.sim.session import TAP_HOLD, Session, split_tones

MAX_SCRIPT_SECONDS = 30
MAX_VIRTUAL_SECONDS = 600
MAX_REPEAT = 10000
WAIT_UNTIL_MS = 5000


class ScriptError(ValueError):
    pass


def _count(step, key, default):
    value = step.get(key, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        raise ScriptError(f"Step {step!r}: {key} must be a non-negative number")
    return value


ACTIONS = {"wait", "tap", "press", "move", "release", "drag", "key", "reset_redraw", "screenshot", "eval", "exec", "assert", "wait_until", "repeat"}
POINTER_ACTIONS = {"tap", "press", "move", "release", "drag"}


def _check_step(step):
    """Check the shape of a step before running or saving it; widget names are checked later."""
    if not isinstance(step, dict):
        raise ScriptError(f"Each step must be an object, not {step!r}")
    action = step.get("action")
    if action not in ACTIONS:
        raise ScriptError(f"Unknown step action {action!r}")
    suffixes = ("", "_to") if action == "drag" else ("",) if action in POINTER_ACTIONS else ()
    for suffix in suffixes:
        if "widget" + suffix in step:
            if not isinstance(step["widget" + suffix], str):
                raise ScriptError(f"Step {step!r}: widget{suffix} must be a name")
        elif not all(isinstance(step.get(axis + suffix), int) and not isinstance(step.get(axis + suffix), bool) for axis in ("x", "y")):
            raise ScriptError(f"Step {step!r} needs x{suffix}/y{suffix} or widget{suffix}")
    if action == "key" and (isinstance(step.get("code"), bool) or not isinstance(step.get("code"), int)):
        raise ScriptError(f"Step {step!r} needs a numeric code")
    if action in ("eval", "exec"):
        _source(step, "code" if action == "exec" else "expr")
    if action in ("assert", "wait_until"):
        _condition(step)
    if action == "repeat" and not isinstance(step.get("steps", []), list):
        raise ScriptError(f"Step {step!r}: steps must be a list")


def script_seconds(steps):
    """How long the script waits, touches included; checks the shape of every step."""
    if not isinstance(steps, list):
        raise ScriptError("steps must be a list")
    total = 0
    for step in steps:
        _check_step(step)
        action = step.get("action")
        _count(step, "ms", 0)
        if action == "repeat":
            times = _count(step, "times", 1)
            if not isinstance(times, int) or times > MAX_REPEAT:
                raise ScriptError(f"repeat takes a whole number of times, at most {MAX_REPEAT}")
            total += times * (script_seconds(step.get("steps", [])) + 0.001)
        elif action == "drag":
            total += (step.get("ms") or 300) / 1000 + 3 * TAP_HOLD
        elif action in ("tap", "key"):
            total += 2 * TAP_HOLD
        elif action == "wait_until":
            total += step.get("ms", WAIT_UNTIL_MS) / 1000
        else:
            total += step.get("ms", 0) / 1000
        total += 0.001  # a repeat of steps without waiting must not be able to run for ever
    return total


def check_script(steps, clock):
    if clock not in ("virtual", "real"):
        raise ScriptError("clock is virtual or real")
    limit = MAX_VIRTUAL_SECONDS if clock == "virtual" else MAX_SCRIPT_SECONDS
    if script_seconds(steps) > limit:
        raise ScriptError(f"The steps wait more than {limit} s in total with the {clock} clock: split them into shorter runs")


def _widget_center(project, name):
    widget = project.find_widget(name)
    if widget is None:
        raise ScriptError(f"Unknown widget {name!r}. Widgets: {sorted(project.used_names)}")
    x, y = project.screen_position(widget)
    return x + widget.props.get("width", 0) // 2, y + widget.props.get("height", 0) // 2


def _point(project, step, suffix=""):
    if "widget" + suffix in step:
        return _widget_center(project, step["widget" + suffix])
    try:
        return step["x" + suffix], step["y" + suffix]
    except KeyError as exc:
        raise ScriptError(f"Step {step!r} needs x{suffix}/y{suffix} or widget{suffix}") from exc


def _source(step, key):
    source = step.get(key)
    if not isinstance(source, str) or not source.strip():
        raise ScriptError(f"Step {step!r} needs {key}")
    return source


def _condition(step):
    """An expression, or page for the active page: {"page": "End"}."""
    if "page" in step:
        return f"page() == {step['page']!r}"
    return _source(step, "expr")


def _run_steps(session, project, steps, run):
    for step in steps:
        if not session.running or run["failure"]:
            return
        if step.get("action") == "repeat":
            for _time in range(step.get("times", 1)):
                _run_steps(session, project, step.get("steps", []), run)
        else:
            _run_step(session, project, step, run)


def _run_step(session, project, step, run):
    action = step.get("action")
    seconds = step.get("ms", 0) / 1000
    if action == "wait":
        session.wait(seconds)
    elif action == "tap":
        session.tap(*_point(project, step))
    elif action == "press":
        session.press(*_point(project, step))
    elif action == "move":
        session.move(*_point(project, step))
    elif action == "release":
        session.release(*_point(project, step))
    elif action == "drag":
        session.drag(*_point(project, step), *_point(project, step, "_to"), seconds or 0.3)
    elif action == "key":
        session.key(step["code"])
    elif action == "reset_redraw":
        session.reset_redraw()
    elif action == "screenshot":
        run["images"].append((step.get("label", f"screenshot {len(run['images']) + 1}"), session.frame()))
    elif action in ("eval", "exec"):
        source = _source(step, "code" if action == "exec" else "expr")
        succeeded, value = session.probe(action, source)
        if action == "eval":
            run["values"].append({"label": step.get("label", source), "ok": succeeded, "value": value})
        elif not succeeded:
            run["failure"] = {"step": step, "reason": value}
    elif action == "assert":
        succeeded, value = session.probe("eval", _condition(step))
        if not succeeded or not value:
            run["failure"] = {"step": step, "reason": value if not succeeded else f"{_condition(step)} is {value!r}"}
    elif action == "wait_until":
        condition = _condition(step)
        deadline = session.now() + step.get("ms", WAIT_UNTIL_MS)
        while True:
            succeeded, value = session.probe("eval", condition)
            if not succeeded:
                run["failure"] = {"step": step, "reason": value}
                break
            if value:
                break
            if session.now() >= deadline or not session.running:
                run["failure"] = {"step": step, "reason": f"{condition} was still {value!r} after {step.get('ms', WAIT_UNTIL_MS)} ms"}
                break
            session.wait(0.05)
    else:
        raise ScriptError(f"Unknown step action {action!r}")


def play(project, page_index, steps, clock="virtual", seed=None, design_only=False):
    """Run the script and return the report; images is a list of (label, RGB565 pixels)."""
    check_script(steps, clock)
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
        raise ScriptError("seed is a whole number")
    run = {"images": [], "values": [], "failure": None}
    with Session(project, page_index, design_only=design_only, clock=clock, seed=seed) as session:
        _run_steps(session, project, steps, run)
        running = session.running
        redraw = session.redraw()
        exit_code = session.exit_code
        frames = session.frames
        elapsed = session.now()
        run["images"].append(("final", session.frame()))
    console, tones = split_tones(session.console_text)
    traceback = "Traceback (most recent call last)" in console
    return {
        "passed": run["failure"] is None and not traceback and running and all(item["ok"] for item in run["values"]),
        "failure": run["failure"], "values": run["values"], "clock": clock, "seconds": round(elapsed / 1000, 2),
        "running": running, "exitCode": exit_code, "frames": frames, "traceback": traceback, "console": console,
        "tones": tones, "redraw": redraw, "images": run["images"],
    }
