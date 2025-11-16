"""
Custom widget classes
"""
from PySide6.QtWidgets import QComboBox
from PySide6.QtCore import Qt


class NoWheelComboBox(QComboBox):
    """ComboBox that doesn't change value on mouse wheel scroll"""
    def wheelEvent(self, event):
        event.ignore()


class NavigableComboBox(NoWheelComboBox):
    """ComboBox with arrow key navigation support"""
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Up, Qt.Key_Down):
            # If dropdown not open, let parent handle for table navigation
            if not self.view().isVisible():
                event.ignore()
                return
        super().keyPressEvent(event)
