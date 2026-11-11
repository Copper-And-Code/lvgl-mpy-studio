import copy
from pathlib import Path
from uuid import uuid4

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QUndoCommand, QUndoStack

from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.core.model import Project, file_revision


class ExternalChangeError(Exception):
    """The file changed on disk, or disappeared, after the last open or save."""

    def __init__(self, path, deleted=False):
        super().__init__(str(path))
        self.path = path
        self.deleted = deleted


class SnapshotCommand(QUndoCommand):
    def __init__(self, document, description, mutator, merge_id=-1):
        super().__init__(tr(description))
        self._lvgl_source_text = description
        self.document = document
        self.mutator = mutator
        self.before = copy.deepcopy(document.project.to_dict())
        self.after = None
        self.merge_id = merge_id

    def redo(self):
        if self.after is None:
            self.mutator(self.document.project)
            self.after = copy.deepcopy(self.document.project.to_dict())
        else:
            self.document._restore(self.after)

    def undo(self):
        self.document._restore(self.before)

    def id(self):
        return self.merge_id

    def mergeWith(self, other):
        if self.merge_id < 0 or other.merge_id != self.merge_id or self.after is None:
            return False
        self.after = copy.deepcopy(other.after)
        return True


class ProjectDocument(QObject):
    reset = Signal()
    page_changed = Signal()
    code_changed = Signal()
    path_changed = Signal()
    modified_changed = Signal(bool)

    def __init__(self, project=None):
        super().__init__()
        self.project = project or Project()
        self.path = None
        self.undo_stack = QUndoStack(self)
        self.undo_stack.cleanChanged.connect(self.modified_changed)
        self.read_only = False
        self.clipboard = []
        # Revision of the file as we last read or wrote it; None if there is no file.
        self.disk_revision = None

    @property
    def modified(self):
        return not self.undo_stack.isClean()

    def _restore(self, data):
        project_id = self.project.projectId  # the identity does not follow undo and redo
        self.project = Project.from_dict(copy.deepcopy(data))
        self.project.projectId = project_id
        self.reset.emit()
        self.page_changed.emit()
        self.code_changed.emit()

    def execute(self, description, mutator, merge_id=-1, code_only=False):
        """code_only: only code changes, so canvas and properties are not rebuilt."""
        if self.read_only:
            return False
        command = SnapshotCommand(self, description, mutator, merge_id)
        self.undo_stack.push(command)
        if code_only:
            self.code_changed.emit()
            return True
        self.reset.emit()
        self.page_changed.emit()
        self.code_changed.emit()
        return True

    def new(self, project=None):
        self.path = None
        self.disk_revision = None
        self.project = project or Project()
        self.undo_stack.setClean()
        self.undo_stack.clear()
        self.reset.emit()
        self.path_changed.emit()

    def open(self, path):
        project, revision = Project.load_with_revision(path)
        self.path = Path(path)
        self.disk_revision = revision
        self.project = project
        self.undo_stack.setClean()
        self.undo_stack.clear()
        self.reset.emit()
        self.path_changed.emit()

    def external_change(self):
        """None if the file is as we left it, otherwise "changed" or "deleted".

        A file deleted or moved from outside is a conflict too: saving would make it reappear,
        against the will of whoever removed it. The same bytes written again are not.
        """
        if self.path is None or self.disk_revision is None:
            return None
        current = file_revision(self.path)
        if current is None:
            return "deleted"
        return "changed" if current != self.disk_revision else None

    def reload(self):
        """Read the open file again. If it is not readable raise the error and leave the document as it is."""
        self.open(self.path)

    def save(self, path=None, overwrite_external=False):
        """Save. On the open file refuse to erase an outside change, unless overwrite_external."""
        target = Path(path) if path else self.path
        if not target:
            raise ValueError("Nessun percorso di salvataggio")
        same_file = self.path is not None and target.resolve() == self.path.resolve()
        state = self.external_change() if same_file and not overwrite_external else None
        if state:
            raise ExternalChangeError(target, deleted=state == "deleted")
        previous = self.project.projectId
        if not previous or (self.path is not None and not same_file):
            self.project.projectId = uuid4().hex  # Save As creates a separate project
        try:
            revision = self.project.save(target)
        except Exception:
            self.project.projectId = previous
            raise
        self.path = target
        self.disk_revision = revision
        self.undo_stack.setClean()
        self.path_changed.emit()
        return target
