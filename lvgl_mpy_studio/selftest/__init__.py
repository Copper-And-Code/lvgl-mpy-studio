"""Self-test: scenarios that use the IDE as a person does, with a report of what passed.

Started with `lvgl-mpy-studio selftest`. It works from a package too, so it also checks a
package that was just built. It needs no pytest and never touches the user's settings."""

from .report import Report  # noqa: F401
from .runner import main  # noqa: F401
