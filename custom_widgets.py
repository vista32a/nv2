from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QMouseEvent

class CustomTextEdit(QTextEdit):
    """
    A custom QTextEdit subclass to handle special events, like those
    needed for the Format Painter feature.
    """
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.format_painter_active = False

    def set_format_painter_active(self, active: bool):
        """Activates or deactivates the format painter mode."""
        self.format_painter_active = active
        # In a more advanced implementation, we would change the mouse cursor here
        # e.g., self.viewport().setCursor(Qt.CursorShape.CrossCursor if active else Qt.CursorShape.IBeamCursor)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """
        Overrides the mouse release event to apply formatting if the
        format painter is active.
        """
        # First, let the default handler run to handle text selection, etc.
        super().mouseReleaseEvent(event)

        # Now, if the painter is active and a selection has been made, apply the format.
        if self.format_painter_active and self.textCursor().hasSelection():
            self.main_window.apply_format()
