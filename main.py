import sys
import json
import os
import re
from datetime import datetime
from pathlib import Path  # <-- This was the import you added
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, QDate, QTimer
from PySide6.QtWidgets import (QMessageBox, QDialog, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                               QLineEdit, QPushButton, QListWidget, QListWidgetItem,
                               QCheckBox, QLabel, QComboBox, QSpinBox, QTableWidget,
                               QTableWidgetItem, QInputDialog, QRadioButton, QButtonGroup, QTextEdit, QDateEdit, QTabWidget, QScrollArea, QWidget)
from PySide6.QtGui import QIcon, QFont, QColor

# --- NEW IMPORTS ---
from src.managers.database_manager import DatabaseManager
from src.managers.pdf_manager import PDFManager
# -----------------

# Modern Stylesheet - RESTORED
MODERN_STYLESHEET = """
QMainWindow, QDialog, QWidget {
    background-color: #f5f7fa;
}

QLabel {
    color: #2c3e50;
    font-size: 11px;
}

QLineEdit, QTextEdit, QSpinBox {
    background-color: #ffffff;
    border: 2px solid #e1e8ed;
    border-radius: 6px;
    padding: 8px;
    color: #2c3e50;
    font-size: 11px;
    selection-background-color: #3498db;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {
    border: 2px solid #3498db;
    background-color: #f8fbff;
}

QComboBox {
    background-color: #ffffff;
    border: 2px solid #e1e8ed;
    border-radius: 6px;
    padding: 6px;
    color: #2c3e50;
    font-size: 11px;
}

QComboBox:focus {
    border: 2px solid #3498db;
}

QComboBox::drop-down {
    border: none;
    background-color: transparent;
    width: 25px;
}

QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
    font-size: 11px;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #1f618d;
}

QPushButton#filterBtn {
    background-color: #27ae60;
}

QPushButton#filterBtn:hover {
    background-color: #229954;
}

QPushButton#presetsBtn {
    background-color: #e74c3c;
    max-width: 80px;
}

QPushButton#presetsBtn:hover {
    background-color: #c0392b;
}

QCheckBox {
    color: #2c3e50;
    font-size: 11px;
    spacing: 5px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 3px;
}

QCheckBox::indicator:unchecked {
    background-color: #ecf0f1;
    border: 2px solid #bdc3c7;
}

QCheckBox::indicator:checked {
    background-color: #3498db;
    border: 2px solid #3498db;
}

QRadioButton {
    color: #2c3e50;
    font-size: 11px;
    spacing: 5px;
}

QRadioButton::indicator {
    width: 18px;
    height: 18px;
}

QRadioButton::indicator:unchecked {
    background-color: #ecf0f1;
    border: 2px solid #bdc3c7;
    border-radius: 9px;
}

QRadioButton::indicator:checked {
    background-color: #3498db;
    border: 2px solid #3498db;
    border-radius: 9px;
}

QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f8fbff;
    gridline-color: #e1e8ed;
    border: 1px solid #e1e8ed;
    border-radius: 6px;
}

QTableWidget::item {
    padding: 5px;
    color: #2c3e50;
}

QTableWidget::item:selected {
    background-color: #d4e6f1;
}

QHeaderView::section {
    background-color: #34495e;
    color: white;
    padding: 5px;
    border: none;
    font-weight: bold;
    font-size: 10px;
}

QScrollArea {
    border: none;
    background-color: #f5f7fa;
}

QTabWidget::pane {
    border: 1px solid #e1e8ed;
}

QTabBar::tab {
    background-color: #ecf0f1;
    color: #2c3e50;
    padding: 8px 20px;
    margin-right: 2px;
    border: 1px solid #bdc3c7;
    border-bottom: none;
    border-radius: 6px 6px 0 0;
    font-weight: bold;
    font-size: 11px;
}

QTabBar::tab:selected {
    background-color: #3498db;
    color: white;
    border: 1px solid #3498db;
}

QTabBar::tab:hover {
    background-color: #d5dbdb;
}

QMenuBar {
    background-color: #34495e;
    color: white;
    border-bottom: 2px solid #2c3e50;
}

QMenuBar::item:selected {
    background-color: #3498db;
}

QMenu {
    background-color: #ffffff;
    color: #2c3e50;
    border: 1px solid #bdc3c7;
}

QMenu::item:selected {
    background-color: #3498db;
    color: white;
}

QListWidget {
    background-color: #ffffff;
    border: 1px solid #e1e8ed;
    border-radius: 6px;
    color: #2c3e50;
}

QListWidget::item:selected {
    background-color: #3498db;
    color: white;
}

QListWidget::item:hover {
    background-color: #d4e6f1;
}

QScrollBar:vertical {
    background-color: #ecf0f1;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #3498db;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #2980b9;
}

QStatusBar {
    background-color: #34495e;
    color: white;
}

QCalendarWidget QToolButton {
    background-color: #3498db;
    color: white;
    border: 1px solid #2980b9;
    border-radius: 4px;
    padding: 4px;
    font-weight: bold;
}

QCalendarWidget QToolButton:hover {
    background-color: #2980b9;
}

QCalendarWidget QToolButton:pressed {
    background-color: #1f618d;
}
"""


CONFIG_FILE = "config/config.json"
FILTERS_FILE = "settings/filters.json"
REMARKS_FILE = "settings/remarks.json"

class NoWheelComboBox(QComboBox):
    """ComboBox that doesn't change value on mouse wheel scroll"""
    def wheelEvent(self, event):
        event.ignore()

class NavigableLineEdit(QLineEdit):
    """LineEdit with arrow key navigation support"""
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right):
            # Let parent handle arrow keys for table navigation
            self.parent().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

class NavigableComboBox(NoWheelComboBox):
    """ComboBox with arrow key navigation support"""
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Up, Qt.Key_Down) and not self.view().isVisible():
            # If dropdown not open, let parent handle for table navigation
            self.parent().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

class ConfigManager:
    """Manages application settings"""

    DEFAULT_CONFIG = {
        "sessions": ["2024-2025", "2025-2026", "2026-2027", "2027-2028"],
        "default_session": "2025-2026",
        "max_marks_options": [50, 75, 100],
        "default_max_marks": 100,
        "class_defaults": {
            "I": 220, "II": 220, "III": 220, "IV": 220, "V": 220,
            "VI": 240, "VII": 240, "VIII": 240, "IX": 240, "X": 240
        }
    }

    @staticmethod
    def load():
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    # Ensure all default keys exist
                    for key, value in ConfigManager.DEFAULT_CONFIG.items():
                        config.setdefault(key, value)
                    return config
            except:
                return ConfigManager.DEFAULT_CONFIG.copy()
        else:
            ConfigManager.save(ConfigManager.DEFAULT_CONFIG.copy())
            return ConfigManager.DEFAULT_CONFIG.copy()

    @staticmethod
    def save(config):
        # Remove 'subjects' if it exists, as it's now in DB
        config.pop('subjects', None)
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

class FiltersManager:
    """Manages saved subject filters"""

    @staticmethod
    def load():
        if os.path.exists(FILTERS_FILE):
            try:
                with open(FILTERS_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    @staticmethod
    def save(filters):
        try:
            with open(FILTERS_FILE, 'w') as f:
                json.dump(filters, f, indent=2)
            return True
        except:
            return False

class LoginDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.logged_in_user_id = None
        self.setWindowTitle("Login - Report Card System")
        self.setMinimumWidth(350)
        self.setStyleSheet(MODERN_STYLESHEET) # Apply styles

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        layout.addWidget(self.error_label)

        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.attempt_login)
        layout.addWidget(login_button)

        self.username_input.returnPressed.connect(login_button.click)
        self.password_input.returnPressed.connect(login_button.click)

        self.setLayout(layout)
        self.username_input.setFocus()

    def attempt_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            self.error_label.setText("Username and password are required.")
            return
        user_id = self.db_manager.authenticate_user(username, password)
        if user_id:
            self.logged_in_user_id = user_id
            self.accept()
        else:
            self.error_label.setText("Invalid username or password.")
            self.password_input.clear()

class SettingsDialog(QDialog):
    """Settings dialog for application configuration"""

    def __init__(self, parent=None, user_id=None):
        super().__init__(parent)
        self.logged_in_user_id = user_id
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 600, 500)
        self.config = ConfigManager.load()

        # Get the db_manager from the parent (MainWindow)
        self.db_manager = self.parent().db_manager

        tabs = QTabWidget()

        # Sessions Tab
        tabs.addTab(self.create_sessions_tab(), "Sessions")

        # Subjects Tab
        tabs.addTab(self.create_subjects_tab(), "Subjects")

        # Marks Tab
        tabs.addTab(self.create_marks_tab(), "Marks")

        # Class Defaults Tab
        tabs.addTab(self.create_class_defaults_tab(), "Class Defaults")

        layout = QVBoxLayout()
        layout.addWidget(tabs)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_settings)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def create_sessions_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Available Sessions:"))
        self.sessions_list = QListWidget()
        for session in self.config.get("sessions", []):
            self.sessions_list.addItem(session)
        layout.addWidget(self.sessions_list)

        input_layout = QHBoxLayout()
        self.new_session_input = QLineEdit()
        self.new_session_input.setPlaceholderText("e.g., 2025-2026")
        add_btn = QPushButton("Add Session")
        add_btn.clicked.connect(self.add_session)
        input_layout.addWidget(self.new_session_input)
        input_layout.addWidget(add_btn)
        layout.addLayout(input_layout)

        layout.addWidget(QLabel("Default Session:"))
        self.default_session_combo = NoWheelComboBox()
        self.default_session_combo.addItems(self.config.get("sessions", []))
        self.default_session_combo.setCurrentText(self.config.get("default_session", "2025-2026"))
        layout.addWidget(self.default_session_combo)

        remove_btn = QPushButton("Remove Selected Session")
        remove_btn.clicked.connect(self.remove_session)
        layout.addWidget(remove_btn)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_subjects_tab(self):
        """Create Subjects tab in Settings Dialog"""
        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Subjects in Database:"))

        # Create table instead of list
        self.subjects_table = QTableWidget()
        self.subjects_table.setColumnCount(2)
        self.subjects_table.setHorizontalHeaderLabels(["Subject Name", "Type"])
        self.subjects_table.horizontalHeader().setStretchLastSection(False)
        self.subjects_table.setColumnWidth(0, 250)
        self.subjects_table.setColumnWidth(1, 100)
        self.load_subjects_from_db()
        layout.addWidget(self.subjects_table)

        # Add new subject section
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel("Add New Subject:"))

        input_layout = QHBoxLayout()
        self.new_subject_input = QLineEdit()
        self.new_subject_input.setPlaceholderText("Enter subject name")
        input_layout.addWidget(self.new_subject_input)

        # Type dropdown (Core / Non-Core)
        input_layout.addWidget(QLabel("Type:"))
        self.subject_type_combo = NoWheelComboBox()
        self.subject_type_combo.addItems(["Core", "Non-Core"])
        input_layout.addWidget(self.subject_type_combo)

        add_btn = QPushButton("Add Subject")
        add_btn.clicked.connect(self.add_subject_to_db)
        input_layout.addWidget(add_btn)
        layout.addLayout(input_layout)

        remove_btn = QPushButton("Remove Selected Subject")
        remove_btn.clicked.connect(self.remove_subject_from_db)
        layout.addWidget(remove_btn)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def load_subjects_from_db(self):
        """
        Load all subjects from DatabaseManager into table
        """
        try:
            # Use the manager passed from MainWindow
            subjects = self.db_manager.get_subjects_with_details()

            self.subjects_table.setRowCount(0)
            self.subject_db_ids = {} # Stores {row_index: subject_id}

            for row_idx, subject_row in enumerate(subjects):
                self.subjects_table.insertRow(row_idx)

                # Column 0: Subject Name
                name_item = QTableWidgetItem(subject_row['subject_name'])
                self.subjects_table.setItem(row_idx, 0, name_item)

                # Column 1: Type
                type_item = QTableWidgetItem(subject_row['type'])
                self.subjects_table.setItem(row_idx, 1, type_item)

                # Store DB ID for deletion
                self.subject_db_ids[row_idx] = subject_row['subject_id']

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading subjects: {e}")

    def add_subject_to_db(self):
        """
        Add new subject via DatabaseManager
        """
        subject_name = self.new_subject_input.text().strip()
        subject_type = self.subject_type_combo.currentText()

        if not subject_name:
            QMessageBox.warning(self, "Error", "Subject name cannot be empty!")
            return

        # Use the manager
        success, message = self.db_manager.add_subject(subject_name, subject_type, self.logged_in_user_id)

        if success:
            self.load_subjects_from_db() # Reload table
            self.new_subject_input.clear()
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)

    def remove_subject_from_db(self):
        """
        Remove selected subject via DatabaseManager
        """
        selected_row = self.subjects_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Select a subject to delete!")
            return

        subject_id = self.subject_db_ids.get(selected_row)
        subject_name = self.subjects_table.item(selected_row, 0).text()

        if not subject_id:
            QMessageBox.warning(self, "Error", "Could not find subject ID!")
            return

        reply = QMessageBox.question(
            self, "Confirm Delete", f"Delete '{subject_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.No:
            return

        # Use the manager
        success, message = self.db_manager.remove_subject(subject_id, self.logged_in_user_id)

        if success:
            self.load_subjects_from_db() # Reload table
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)

    def create_marks_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Maximum Marks Options:"))
        self.marks_list = QListWidget()
        for marks in self.config.get("max_marks_options", []):
            self.marks_list.addItem(str(marks))
        layout.addWidget(self.marks_list)

        input_layout = QHBoxLayout()
        self.new_marks_input = QSpinBox()
        self.new_marks_input.setMinimum(1)
        self.new_marks_input.setMaximum(500)
        add_btn = QPushButton("Add Marks Option")
        add_btn.clicked.connect(self.add_marks)
        input_layout.addWidget(self.new_marks_input)
        input_layout.addWidget(add_btn)
        layout.addLayout(input_layout)

        remove_btn = QPushButton("Remove Selected")
        remove_btn.clicked.connect(self.remove_marks)
        layout.addWidget(remove_btn)

        layout.addWidget(QLabel("Default Maximum Marks:"))
        self.default_marks_combo = NoWheelComboBox()
        self.default_marks_combo.addItems([str(m) for m in self.config.get("max_marks_options", [])])
        self.default_marks_combo.setCurrentText(str(self.config.get("default_max_marks", 100)))
        layout.addWidget(self.default_marks_combo)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_class_defaults_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Total School Days by Class:"))

        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        self.class_days_inputs = {}
        for class_name in ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]:
            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(f"Class {class_name}:"))
            spin = QSpinBox()
            spin.setMinimum(0)
            spin.setMaximum(500)
            spin.setValue(self.config.get("class_defaults", {}).get(class_name, 220))
            self.class_days_inputs[class_name] = spin
            h_layout.addWidget(spin)
            scroll_layout.addLayout(h_layout)

        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        widget.setLayout(layout)
        return widget

    def add_session(self):
        text = self.new_session_input.text().strip()
        if text and text not in [self.sessions_list.item(i).text() for i in range(self.sessions_list.count())]:
            self.sessions_list.addItem(text)
            self.new_session_input.clear()
            self.default_session_combo.addItem(text)

    def remove_session(self):
        if self.sessions_list.currentItem():
            self.sessions_list.takeItem(self.sessions_list.row(self.sessions_list.currentItem()))

    def add_marks(self):
        marks = self.new_marks_input.value()
        if str(marks) not in [self.marks_list.item(i).text() for i in range(self.marks_list.count())]:
            self.marks_list.addItem(str(marks))
            self.default_marks_combo.addItem(str(marks))

    def remove_marks(self):
        if self.marks_list.currentItem():
            self.marks_list.takeItem(self.marks_list.row(self.marks_list.currentItem()))

    def save_settings(self):
        """
        Saves only the config.json settings. Subjects are saved live.
        """
        self.config["sessions"] = [self.sessions_list.item(i).text() for i in range(self.sessions_list.count())]
        self.config["default_session"] = self.default_session_combo.currentText()

        self.config["max_marks_options"] = [int(self.marks_list.item(i).text()) for i in range(self.marks_list.count())]
        self.config["default_max_marks"] = int(self.default_marks_combo.currentText())

        if "class_defaults" not in self.config:
            self.config["class_defaults"] = {}
        for class_name, spin in self.class_days_inputs.items():
            self.config["class_defaults"][class_name] = spin.value()

        ConfigManager.save(self.config)
        QMessageBox.information(self, "Success", "Settings saved successfully!")
        self.accept()

class SubjectFilterDialog(QDialog):
    """Dialog to select subjects for report card"""

    def __init__(self, config, saved_filters=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Subjects")
        self.setGeometry(100, 100, 400, 600)
        self.setMinimumSize(350, 400)
        self.config = config
        self.saved_filters = saved_filters or {}
        self.selected_subjects = []

        # Get the db_manager from the parent (MainWindow)
        self.db_manager = self.parent().db_manager

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Select Subjects to Include:"))

        # Create scroll area for checkboxes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        # Load subjects from database via manager
        self.checkboxes = {}
        subjects = self.load_subjects_from_db() # Updated method

        for subject_row in subjects:
            subject_name = subject_row['subject_name']
            subject_type = subject_row['type']

            cb = QCheckBox(f"{subject_name} ({subject_type})")
            cb.setChecked(True)
            cb.setProperty("subject_name", subject_name)
            self.checkboxes[subject_name] = cb
            scroll_layout.addWidget(cb)

        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel("Saved Filters:"))

        self.filters_combo = NoWheelComboBox()
        self.filters_combo.addItem("-- New Filter --")
        if self.saved_filters:
            self.filters_combo.addItems(self.saved_filters.keys())
        self.filters_combo.currentTextChanged.connect(self.load_filter)
        layout.addWidget(self.filters_combo)

        filter_btn_layout = QHBoxLayout()
        self.save_filter_btn = QPushButton("Save as Filter")
        self.save_filter_btn.clicked.connect(self.save_filter_dialog)
        self.delete_filter_btn = QPushButton("Delete Filter")
        self.delete_filter_btn.clicked.connect(self.delete_filter)
        filter_btn_layout.addWidget(self.save_filter_btn)
        filter_btn_layout.addWidget(self.delete_filter_btn)
        layout.addLayout(filter_btn_layout)

        layout.addStretch()

        btn_layout2 = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout2.addWidget(ok_btn)
        btn_layout2.addWidget(cancel_btn)
        layout.addLayout(btn_layout2)

        self.setLayout(layout)

    def load_subjects_from_db(self):
        """
        Load all subjects from DatabaseManager
        """
        try:
            return self.db_manager.get_subjects_with_details()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading subjects: {e}")
            return []

    def load_filter(self, filter_name):
        if filter_name == "-- New Filter --":
            # Reset all to checked
            for cb in self.checkboxes.values():
                cb.setChecked(True)
            return

        if filter_name in self.saved_filters:
            filter_subjects = self.saved_filters[filter_name]
            # Uncheck all
            for cb in self.checkboxes.values():
                cb.setChecked(False)
            # Check only the ones in filter
            for subject in filter_subjects:
                if subject in self.checkboxes:
                    self.checkboxes[subject].setChecked(True)

    def save_filter_dialog(self):
        filter_name, ok = QtWidgets.QInputDialog.getText(self, "Save Filter", "Filter Name:")
        if ok and filter_name:
            selected = self.get_selected_subjects()
            self.saved_filters[filter_name] = selected
            FiltersManager.save(self.saved_filters)

            # Add to combo if not exists
            if self.filters_combo.findText(filter_name) == -1:
                self.filters_combo.addItem(filter_name)

            QMessageBox.information(self, "Success", f"Filter '{filter_name}' saved!")

    def delete_filter(self):
        current = self.filters_combo.currentText()
        if current == "-- New Filter --":
            QMessageBox.warning(self, "Error", "Cannot delete default filter")
            return

        if current in self.saved_filters:
            reply = QMessageBox.question(self, "Confirm", f"Delete filter '{current}'?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                del self.saved_filters[current]
                FiltersManager.save(self.saved_filters)
                self.filters_combo.removeItem(self.filters_combo.currentIndex())
                QMessageBox.information(self, "Success", "Filter deleted!")

    def get_selected_subjects(self):
        """Return list of selected subject names"""
        return [subject for subject, cb in self.checkboxes.items() if cb.isChecked()]

class UserManagementDialog(QDialog):
    def __init__(self, db_manager, user_id, parent=None): # Added user_id parameter
        super().__init__(parent)
        self.logged_in_user_id = user_id # Store the ID of the user performing actions
        self.db_manager = db_manager
        self.setWindowTitle("User Management")
        self.setMinimumSize(650, 450) # Slightly larger
        self.setStyleSheet(MODERN_STYLESHEET)

        layout = QVBoxLayout(self) # Set layout on self directly

        # --- User Table ---
        layout.addWidget(QLabel("Registered Users:"))
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(5)
        self.user_table.setHorizontalHeaderLabels(["ID", "Username", "Role", "Email", "Status"])
        self.user_table.setEditTriggers(QTableWidget.NoEditTriggers) # Read-only
        self.user_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.user_table.setSelectionMode(QTableWidget.SingleSelection)
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.user_table)

        # --- Action Buttons ---
        button_layout = QHBoxLayout()
        add_button = QPushButton("➕ Add User"); add_button.clicked.connect(self.add_user)
        status_button = QPushButton("🔄 Toggle Status"); status_button.clicked.connect(self.toggle_user_status)
        role_button = QPushButton("🧑‍🏫 Change Role"); role_button.clicked.connect(self.change_user_role)
        reset_pw_button = QPushButton("🔑 Reset Password"); reset_pw_button.clicked.connect(self.reset_password)
        delete_button = QPushButton("🗑️ Delete User"); delete_button.clicked.connect(self.delete_user)

        button_layout.addWidget(add_button); button_layout.addWidget(status_button); button_layout.addWidget(role_button)
        button_layout.addWidget(reset_pw_button); button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        close_button = QPushButton("Close"); close_button.clicked.connect(self.accept)
        layout.addWidget(close_button, alignment=Qt.AlignRight)

        self.populate_user_table() # Initial load

    def populate_user_table(self):
        self.user_table.setRowCount(0)
        users = self.db_manager.get_all_users()
        for row_idx, user_data in enumerate(users):
            self.user_table.insertRow(row_idx)
            # Store user_id in the first item's data role
            id_item = QTableWidgetItem(str(user_data['user_id'])); id_item.setData(Qt.UserRole, user_data['user_id'])
            self.user_table.setItem(row_idx, 0, id_item)
            self.user_table.setItem(row_idx, 1, QTableWidgetItem(user_data['username']))
            self.user_table.setItem(row_idx, 2, QTableWidgetItem(user_data['role']))
            self.user_table.setItem(row_idx, 3, QTableWidgetItem(user_data['email'] or 'N/A'))
            status_text = "Active" if user_data['is_active'] else "Inactive"
            status_item = QTableWidgetItem(status_text)
            status_item.setForeground(Qt.darkGreen if user_data['is_active'] else Qt.red)
            self.user_table.setItem(row_idx, 4, status_item)
        self.user_table.resizeColumnsToContents()
        self.user_table.horizontalHeader().setStretchLastSection(True)

    def get_selected_user_id(self):
        selected_items = self.user_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "Please select a user."); return None
        # Get user ID from the data stored in the first column item
        user_id = self.user_table.item(selected_items[0].row(), 0).data(Qt.UserRole)
        if user_id is None: QMessageBox.critical(self, "Error", "Could not get user ID."); return None
        return int(user_id)

    def add_user(self):
        username, ok1 = QInputDialog.getText(self, "Add User", "Enter Username:")
        if not ok1 or not username.strip(): return
        password, ok2 = QInputDialog.getText(self, "Add User", f"Enter Password for {username}:", QLineEdit.Password)
        if not ok2 or not password: return
        roles = ["teacher", "principal"]; role, ok3 = QInputDialog.getItem(self, "Add User", "Select Role:", roles, 0, False)
        if not ok3: return
        email, ok4 = QInputDialog.getText(self, "Add User", "Enter Email (Optional):")
        # --- Pass performing user ID ---
        success, message = self.db_manager.add_user(
            username.strip(),
            password,
            role,
            email.strip() if ok4 and email.strip() else None,
            performed_by_user_id=self.logged_in_user_id # Pass logged-in user ID
        )
        if success: QMessageBox.information(self, "Success", message); self.populate_user_table()
        else: QMessageBox.warning(self, "Error", message)

    def toggle_user_status(self):
        user_id_to_modify = self.get_selected_user_id();
        if user_id_to_modify is None: return
        selected_row = self.user_table.currentRow(); current_status_item = self.user_table.item(selected_row, 4)
        currently_active = current_status_item.text() == "Active"; new_status = not currently_active
        status_text = "Deactivate" if currently_active else "Activate"; username = self.user_table.item(selected_row, 1).text()
        reply = QMessageBox.question(self, "Confirm", f"Are you sure you want to {status_text} user '{username}'?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No: return
        # --- Pass performing user ID ---
        success, message = self.db_manager.update_user_status(
            user_id_to_modify,
            new_status,
            performed_by_user_id=self.logged_in_user_id # Pass logged-in user ID
        )
        if success: QMessageBox.information(self, "Success", message); self.populate_user_table()
        else: QMessageBox.warning(self, "Error", message)

    def change_user_role(self):
        user_id_to_modify = self.get_selected_user_id();
        if user_id_to_modify is None: return
        selected_row = self.user_table.currentRow(); username = self.user_table.item(selected_row, 1).text(); current_role = self.user_table.item(selected_row, 2).text()
        roles = ["teacher", "principal"]; current_index = roles.index(current_role) if current_role in roles else 0
        new_role, ok = QInputDialog.getItem(self, "Change Role", f"Select new role for '{username}':", roles, current_index, False)
        if not ok or new_role == current_role: return
        # --- Pass performing user ID ---
        success, message = self.db_manager.update_user_role(
            user_id_to_modify,
            new_role,
            performed_by_user_id=self.logged_in_user_id # Pass logged-in user ID
        )
        if success: QMessageBox.information(self, "Success", message); self.populate_user_table()
        else: QMessageBox.warning(self, "Error", message)

    def reset_password(self):
        user_id_to_modify = self.get_selected_user_id();
        if user_id_to_modify is None: return
        username = self.user_table.item(self.user_table.currentRow(), 1).text()
        new_password, ok = QInputDialog.getText(self, "Reset Password", f"Enter new password for '{username}':", QLineEdit.Password)
        if not ok or not new_password: QMessageBox.warning(self, "Input Error", "Password cannot be empty."); return
        reply = QMessageBox.question(self, "Confirm", f"Reset password for '{username}'?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No: return
        # --- Pass performing user ID ---
        success, message = self.db_manager.update_user_password(
            user_id_to_modify,
            new_password,
            performed_by_user_id=self.logged_in_user_id # Pass logged-in user ID
        )
        if success: QMessageBox.information(self, "Success", message)
        else: QMessageBox.warning(self, "Error", message)

    def delete_user(self):
        user_id_to_delete = self.get_selected_user_id();
        if user_id_to_delete is None: return
        username = self.user_table.item(self.user_table.currentRow(), 1).text()
        if user_id_to_delete == 1: QMessageBox.warning(self, "Error", "Cannot delete the primary admin user."); return
        reply = QMessageBox.question(self, "Confirm Deletion", f"DANGER: Delete user '{username}'?\nThis cannot be undone.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No: return
        # --- Pass performing user ID ---
        success, message = self.db_manager.delete_user(
            user_id_to_delete,
            performed_by_user_id=self.logged_in_user_id # Pass logged-in user ID
        )
        if success: QMessageBox.information(self, "Success", message); self.populate_user_table()
        else: QMessageBox.warning(self, "Error", message)

class MarksTableWidget(QWidget):
    """Widget to handle arrow key navigation in marks table"""
    def __init__(self, marks_grid):
        super().__init__()
        self.marks_grid = marks_grid
        self.current_row = 0
        self.current_col = 0
        self.setFocusPolicy(Qt.StrongFocus)  # Enable focus

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            # Tab out of table to next widget
            self.focusNextChild()
            event.accept()
        elif event.key() == Qt.Key_Backtab:
            # Shift+Tab out of table to previous widget
            self.focusPreviousChild()
            event.accept()
        elif event.key() == Qt.Key_Down:
            self.current_row = min(self.current_row + 1, len(self.marks_grid) - 1)
            self.focus_cell()
            event.accept()
        elif event.key() == Qt.Key_Up:
            self.current_row = max(self.current_row - 1, 0)
            self.focus_cell()
            event.accept()
        elif event.key() == Qt.Key_Right:
            self.current_col = min(self.current_col + 1, 4) # 5 columns: 0,1,2,3,4
            self.focus_cell()
            event.accept()
        elif event.key() == Qt.Key_Left:
            self.current_col = max(self.current_col - 1, 0)
            self.focus_cell()
            event.accept()
        else:
            super().keyPressEvent(event)

    def focus_cell(self):
        columns = ["coursework", "absent_cw", "termexam", "absent_te", "maxmarks"]
        self.current_col = min(self.current_col, len(columns) - 1) # Ensure col index is valid
        if self.current_row < len(self.marks_grid):
            cell = self.marks_grid[self.current_row].get(columns[self.current_col])
            if cell:
                cell.setFocus()

class NavigableMainWindow(QtWidgets.QMainWindow):
    """Main window with arrow key navigation"""
    def __init__(self):
        super().__init__()
        self.focused_widget_index = 0
        self.all_widgets = []  # Will be populated after widgets are created

    def register_widgets(self, widgets_list):
        """Register widgets in navigation order"""
        self.all_widgets = widgets_list
        if self.all_widgets:
            self.all_widgets[0].setFocus()
            self.focused_widget_index = 0

    def keyPressEvent(self, event):
        """Handle arrow key navigation"""
        if event.key() == Qt.Key_Down or event.key() == Qt.Key_Right:
            self.move_to_next_widget()
            event.accept()
        elif event.key() == Qt.Key_Up or event.key() == Qt.Key_Left:
            self.move_to_previous_widget()
            event.accept()
        else:
            super().keyPressEvent(event)

    def move_to_next_widget(self):
        """Move focus to next widget"""
        if not self.all_widgets:
            return
        self.focused_widget_index = (self.focused_widget_index + 1) % len(self.all_widgets)
        self.all_widgets[self.focused_widget_index].setFocus()

    def move_to_previous_widget(self):
        """Move focus to previous widget"""
        if not self.all_widgets:
            return
        self.focused_widget_index = (self.focused_widget_index - 1) % len(self.all_widgets)
        self.all_widgets[self.focused_widget_index].setFocus()

# --- MAIN WINDOW ---
class MainWindow(NavigableMainWindow):
    def __init__(self, user_id): # <-- Accepts user_id
        super().__init__()
        self.setWindowTitle("📋 Faizan Academy - Report Card System")
        self.showMaximized()
        self.setStyleSheet(MODERN_STYLESHEET)

        self.logged_in_user_id = user_id # <-- Stores user_id

        self.config = ConfigManager.load()
        self.filters = FiltersManager.load()

        # Initialize the Database Manager
        self.db_manager = DatabaseManager("report_system.db")
        # No need to call init_database() here, it's done before login

        self.selected_subjects = []
        self.marks_grid = []

        self.create_menu() # <-- Ensure this is called BEFORE create_form
        self.create_form()
        self.load_initial_subjects()
        # self.show() is called after successful login in the main block

    def reset_form(self):
        """Clear all form fields"""
        self.student_name_input.clear()
        self.father_name_input.clear()
        self.class_sec_input.clear()
        self.gr_no_input.clear()
        self.term_combo.setCurrentIndex(0)
        self.session_combo.setCurrentText(self.config.get("default_session", "2025-2026"))
        self.rank_combo.setCurrentIndex(0)
        self.total_days_input.setValue(0)
        self.days_attended_input.setValue(0)
        self.days_absent_input.setValue(0)
        self.conduct_combo.setCurrentIndex(0)
        self.performance_combo.setCurrentIndex(0)
        self.progress_combo.setCurrentIndex(0)
        self.remarks_input.clear()
        self.status_group.setExclusive(False)
        for button in self.status_group.buttons():
            button.setChecked(False)
        self.status_group.setExclusive(True)
        self.date_input.setDate(QDate.currentDate())

        # Clear marks table
        if hasattr(self, 'marks_inputs'): # Safety check
            for subject, row in self.marks_inputs.items():
                row["coursework"].clear()
                row["termexam"].clear()
                row["absent_cw"].setChecked(False)
                row["absent_te"].setChecked(False)
                row["coursework"].setEnabled(True)
                row["termexam"].setEnabled(True)
                row["maxmarks"].setEnabled(True)
                # Reset labels to default state
                row["obt"].setText("0")
                row["pct"].setText("0%")
                row["grade"].setText("-")
                row["obt"].setStyleSheet("color: #3498db; font-weight: bold;")
                row["pct"].setStyleSheet("color: #2980b9; font-weight: bold;")
                row["grade"].setStyleSheet("color: #27ae60; font-weight: bold; background-color: #d5f4e6; border-radius: 4px; padding: 2px;")

        self.update_grand_totals()

    def create_menu(self):
        menubar = self.menuBar()

        # --- Settings Menu ---
        settings_menu = menubar.addMenu("Settings")
        settings_action = settings_menu.addAction("Application Settings")
        settings_action.triggered.connect(self.open_settings)

        # --- NEW Users Menu ---
        users_menu = menubar.addMenu("Users")
        manage_users_action = users_menu.addAction("Manage Users")
        manage_users_action.triggered.connect(self.open_user_management) # Connect to new method
        # ----------------------

    def open_settings(self):
        """
        Passes 'self' (MainWindow) as parent, so dialog can access db_manager.
        Also passes the logged_in_user_id for audit logging.
        """
        # --- EDITED LINE ---
        dialog = SettingsDialog(parent=self, user_id=self.logged_in_user_id)
        # -------------------
        if dialog.exec():
            # Reload config in case sessions, etc. changed
            self.config = ConfigManager.load()
            self.update_form_sessions() # Renamed to be specific
            # Subjects are reloaded when filter dialog opens or app restarts

    def open_user_management(self):
        """Opens the User Management dialog, passing the logged-in user ID."""
        # Optional: Add role check here later if needed based on self.logged_in_user_id
        # --- EDITED LINE ---
        dialog = UserManagementDialog(self.db_manager, user_id=self.logged_in_user_id, parent=self)
        # -------------------
        dialog.exec()

    def create_form(self):
        widget = QtWidgets.QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(60, 40, 60, 40)

        # --- Term Selection ---
        h = QHBoxLayout(); h.addWidget(QLabel("Term:")); self.term_combo = NoWheelComboBox(); self.term_combo.addItems(["Mid Year", "Annual Year"]); h.addWidget(self.term_combo); h.addStretch(); layout.addLayout(h)
        # --- Session Selection ---
        h = QHBoxLayout(); h.addWidget(QLabel("Session:")); self.session_combo = NoWheelComboBox(); self.session_combo.addItems(self.config.get("sessions", [])); self.session_combo.setCurrentText(self.config.get("default_session", "2025-2026")); h.addWidget(self.session_combo); h.addStretch(); layout.addLayout(h)
        # --- Student's Name ---
        h = QHBoxLayout(); h.addWidget(QLabel("Student's Name:")); self.student_name_input = QLineEdit(); h.addWidget(self.student_name_input); layout.addLayout(h)
        # --- Father's Name ---
        h = QHBoxLayout(); h.addWidget(QLabel("Father's Name:")); self.father_name_input = QLineEdit(); h.addWidget(self.father_name_input); layout.addLayout(h)
        # --- Class/Sec with Live Validation ---
        h = QHBoxLayout(); h.addWidget(QLabel("Class/Sec:")); self.class_sec_input = QLineEdit(); self.class_sec_input.setPlaceholderText("e.g., I-A, II-B, III-C"); self.class_sec_input.textChanged.connect(self.validate_class_sec_live); h.addWidget(self.class_sec_input); layout.addLayout(h)
        self.class_sec_error = QLabel(""); self.class_sec_error.setStyleSheet("color: #e74c3c; font-size: 9px;"); layout.addWidget(self.class_sec_error)
        # --- G.R No with Live Validation (Numeric Only) ---
        h = QHBoxLayout(); h.addWidget(QLabel("G.R No.:")); self.gr_no_input = QLineEdit(); self.gr_no_input.setPlaceholderText("Numeric only"); self.gr_no_input.textChanged.connect(self.validate_gr_no_live); h.addWidget(self.gr_no_input); layout.addLayout(h)
        # --- Rank in Class ---
        h = QHBoxLayout(); h.addWidget(QLabel("Rank in Class:")); self.rank_combo = NoWheelComboBox(); items = ["N/A"] + [str(i) for i in range(1, 11)]; self.rank_combo.addItems(items); self.rank_combo.setCurrentIndex(0); h.addWidget(self.rank_combo); h.addStretch(); layout.addLayout(h)
        # --- School Days ---
        h = QHBoxLayout(); h.addWidget(QLabel("Total School Days:")); self.total_days_input = QSpinBox(); self.total_days_input.setMaximum(500); self.total_days_input.valueChanged.connect(self.calculate_days_absent); h.addWidget(self.total_days_input); h.addStretch(); layout.addLayout(h)
        h = QHBoxLayout(); h.addWidget(QLabel("Days Attended:")); self.days_attended_input = QSpinBox(); self.days_attended_input.setMaximum(500); self.days_attended_input.valueChanged.connect(self.calculate_days_absent); h.addWidget(self.days_attended_input); h.addStretch(); layout.addLayout(h)
        h = QHBoxLayout(); h.addWidget(QLabel("Days Absent:")); self.days_absent_input = QSpinBox(); self.days_absent_input.setMaximum(500); self.days_absent_input.setReadOnly(True)
        self.days_absent_input.setStyleSheet("""
            QSpinBox {
                background-color: #ecf0f1;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                color: #7f8c8d;
            }
        """)
        h.addWidget(self.days_absent_input); h.addStretch(); layout.addLayout(h)

        # --- Marks Section ---
        marks_header_layout = QHBoxLayout(); marks_label = QLabel("Subject Marks"); marks_label.setFont(QFont("Arial", 12, QFont.Bold)); marks_header_layout.addWidget(marks_label); filter_btn = QPushButton("▼ Select Subjects"); filter_btn.setObjectName("filterBtn"); filter_btn.setMaximumWidth(150); filter_btn.clicked.connect(self.open_subject_filter); marks_header_layout.addWidget(filter_btn); marks_header_layout.addStretch(); layout.addLayout(marks_header_layout)
        self.marks_container = QWidget(); self.marks_layout = QVBoxLayout(); self.marks_layout.setSpacing(5); self.marks_container.setLayout(self.marks_layout); layout.addWidget(self.marks_container) # Ensure marks_layout is created

        # --- Conduct/Performance ---
        layout.addWidget(QLabel("Conduct:")); self.conduct_combo = NoWheelComboBox(); self.conduct_combo.addItems(["Good", "Fair", "Bad"]); layout.addWidget(self.conduct_combo)
        layout.addWidget(QLabel("Daily Performance:")); self.performance_combo = NoWheelComboBox(); self.performance_combo.addItems(["Excellent", "Good", "Bad"]); layout.addWidget(self.performance_combo)
        layout.addWidget(QLabel("Progress:")); self.progress_combo = NoWheelComboBox(); self.progress_combo.addItems(["Satisfactory", "Unsatisfactory"]); layout.addWidget(self.progress_combo)
        # --- Remarks ---
        layout.addWidget(QLabel("Teacher's Remarks:")); remarks_layout = QHBoxLayout(); self.remarks_input = QTextEdit(); self.remarks_input.setMaximumHeight(80); self.remarks_input.setTabChangesFocus(True); remarks_layout.addWidget(self.remarks_input); preset_btn = QPushButton("💬 Presets"); preset_btn.setObjectName("presetsBtn"); preset_btn.clicked.connect(self.show_preset_remarks); remarks_layout.addWidget(preset_btn); layout.addLayout(remarks_layout)
        # --- Status ---
        layout.addWidget(QLabel("Result Status:")); self.status_group = QButtonGroup(); status_layout = QHBoxLayout();
        for i, status in enumerate(["Passed", "Promoted with Support", "Needs Improvement"]): rb = QRadioButton(status); status_layout.addWidget(rb); self.status_group.addButton(rb, i)
        layout.addLayout(status_layout)
        # --- Date ---
        h = QHBoxLayout(); h.addWidget(QLabel("Date:")); self.date_input = QDateEdit(); self.date_input.setDate(QDate.currentDate()); self.date_input.setCalendarPopup(True); self.date_input.setDisplayFormat("dd MMMM yyyy"); h.addWidget(self.date_input); h.addStretch(); layout.addLayout(h)

        # --- Generate Button ---
        generate_btn = QPushButton("✓ Save & Generate PDF"); generate_btn.setObjectName("generateBtn"); generate_btn.setMinimumHeight(45); generate_btn.setFont(QFont("Arial", 12, QFont.Bold))
        generate_btn.setStyleSheet("""
            QPushButton#generateBtn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #27ae60, stop:1 #1e8449);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton#generateBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #229954, stop:1 #186a3b);
            }
            QPushButton#generateBtn:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1e8449, stop:1 #145a32);
            }
        """)
        generate_btn.clicked.connect(self.save_and_generate_pdf); layout.addWidget(generate_btn)

        layout.addStretch(); widget.setLayout(layout)
        scroll = QScrollArea(); scroll.setWidget(widget); scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; }
            QScrollBar:vertical { background-color: #ecf0f1; width: 12px; border-radius: 6px; margin: 0px 0px 0px 0px;}
            QScrollBar::handle:vertical { background-color: #3498db; border-radius: 6px; min-height: 20px; }
            QScrollBar::handle:vertical:hover { background-color: #2980b9; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { border: none; background: none; height: 0px; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
        """)
        self.setCentralWidget(scroll)

        # Base order for navigation
        self.widgets_order_base = [ self.term_combo, self.session_combo, self.student_name_input, self.father_name_input, self.class_sec_input, self.gr_no_input, self.rank_combo, self.total_days_input, self.days_attended_input, ]
        for btn in self.findChildren(QPushButton):
            if "Select Subjects" in btn.text(): self.widgets_order_base.append(btn); break

    # --- ADD THIS METHOD ---
    def setup_complete_navigation_order(self):
        """Finalizes the navigation order after the marks table is populated."""
        widgets_order = self.widgets_order_base.copy()
        if hasattr(self, 'marks_grid'):
            for row in self.marks_grid:
                # Ensure keys exist before appending
                if "coursework" in row: widgets_order.append(row["coursework"])
                if "absent_cw" in row: widgets_order.append(row["absent_cw"])
                if "termexam" in row: widgets_order.append(row["termexam"])
                if "absent_te" in row: widgets_order.append(row["absent_te"])
                if "maxmarks" in row: widgets_order.append(row["maxmarks"])

        widgets_order.extend([
            self.conduct_combo, self.performance_combo, self.progress_combo,
            self.remarks_input,
        ])
        for btn in self.findChildren(QPushButton):
            if "Presets" in btn.text(): widgets_order.append(btn); break
        if self.status_group.buttons(): widgets_order.append(self.status_group.buttons()[0]) # Add first radio button
        widgets_order.append(self.date_input)
        for btn in self.findChildren(QPushButton):
            if btn.objectName() == "generateBtn": widgets_order.append(btn); break
        self.register_widgets(widgets_order)

    def validate_class_sec_live(self):
        text = self.class_sec_input.text().strip().upper(); pattern = r'^(I|II|III|IV|V|VI|VII|VIII|IX|X|\d+)-[A-Z]$'
        if text != self.class_sec_input.text(): self.class_sec_input.blockSignals(True); self.class_sec_input.setText(text); self.class_sec_input.blockSignals(False)
        if not text: self.class_sec_error.setText(""); self.class_sec_input.setStyleSheet(""); return True
        if re.match(pattern, text): self.class_sec_error.setText(""); self.class_sec_input.setStyleSheet("QLineEdit { background-color: #ffffff; border: 2px solid #27ae60; border-radius: 6px; padding: 8px; color: #2c3e50; }"); return True
        else: self.class_sec_error.setText("❌ Format: I-A, II-B, III-C, etc."); self.class_sec_input.setStyleSheet("QLineEdit { background-color: #fff5f5; border: 2px solid #e74c3c; border-radius: 6px; padding: 8px; color: #2c3e50; }"); return False

    def validate_gr_no_live(self):
        text = self.gr_no_input.text(); numeric_text = ''.join(c for c in text if c.isdigit())
        if numeric_text != text: self.gr_no_input.blockSignals(True); self.gr_no_input.setText(numeric_text); self.gr_no_input.blockSignals(False)

    def calculate_days_absent(self):
        total = self.total_days_input.value(); attended = self.days_attended_input.value()
        if attended > total: self.days_attended_input.blockSignals(True); self.days_attended_input.setValue(total); attended = total; self.days_attended_input.blockSignals(False)
        absent = max(0, total - attended); self.days_absent_input.setValue(absent)

    def update_form_sessions(self):
        self.session_combo.clear(); self.session_combo.addItems(self.config.get("sessions", [])); self.session_combo.setCurrentText(self.config.get("default_session", "2025-2026"))

    def open_subject_filter(self):
        dialog = SubjectFilterDialog(self.config, self.filters, self)
        if dialog.exec():
            self.selected_subjects = dialog.get_selected_subjects()
            self.populate_marks_table()

    def load_initial_subjects(self):
        if self.filters: first_filter_name = list(self.filters.keys())[0]; self.selected_subjects = self.filters[first_filter_name]
        else: db_subjects = self.db_manager.get_subjects_with_details(); self.selected_subjects = [s['subject_name'] for s in db_subjects]
        self.populate_marks_table()

    def get_grade(self, percentage):
        try:
            pct = float(percentage)
            if pct >= 80: return "A1"
            elif pct >= 70: return "A"
            elif pct >= 60: return "B"
            elif pct >= 50: return "C"
            elif pct >= 40: return "D"
            else: return "U"
        except: return "-"

    def populate_marks_table(self):
        while self.marks_layout.count() > 0: # Check count > 0 explicitly
            item = self.marks_layout.takeAt(0)
            if item: # Check if item is not None
                 widget = item.widget()
                 if widget:
                      widget.deleteLater()
            else:
                 break # Exit loop if takeAt returns None unexpectedly

        max_marks_options = self.config.get("max_marks_options", [100]); table_container = QWidget(); table_layout = QVBoxLayout(); table_layout.setSpacing(0); table_layout.setContentsMargins(0, 0, 0, 0)
        header_layout = QHBoxLayout(); header_layout.setSpacing(5); header_layout.setContentsMargins(0, 0, 0, 0)
        headers = ["Subject", "Course Work", "Abs CW", "Term Exam", "Abs TE", "Max", "Obt", "%", "Grade"]; widths = [100, 90, 60, 90, 60, 60, 60, 60, 60]
        for header_text, width in zip(headers, widths): header = QLabel(header_text); header.setMinimumWidth(width); header.setMaximumWidth(width); header.setFont(QFont("Arial", 9, QFont.Bold)); header.setAlignment(Qt.AlignCenter); header_layout.addWidget(header)
        header_layout.addStretch(); table_layout.addLayout(header_layout); separator = QtWidgets.QFrame(); separator.setFrameShape(QtWidgets.QFrame.HLine); separator.setFrameShadow(QtWidgets.QFrame.Sunken); separator.setLineWidth(2); table_layout.addWidget(separator)
        self.marks_inputs = {}; self.marks_grid = []; marks_rows_layout = QVBoxLayout(); marks_rows_layout.setSpacing(0); marks_rows_layout.setContentsMargins(0, 0, 0, 0)

        for subject_idx, subject in enumerate(self.selected_subjects):
            row_layout = QHBoxLayout(); row_layout.setSpacing(5); row_layout.setContentsMargins(0, 0, 0, 0); row_data = {}
            label = QLabel(subject); label.setMinimumWidth(100); label.setMaximumWidth(100); label.setFont(QFont("Arial", 9)); row_layout.addWidget(label)
            coursework = NavigableLineEdit(); coursework.setPlaceholderText("0"); coursework.setMinimumWidth(90); coursework.setMaximumWidth(90); coursework.textChanged.connect(lambda text, s=subject: self.validate_marks_sum(s)); row_layout.addWidget(coursework); row_data["coursework"] = coursework
            absent_cw_cb = QCheckBox(); absent_cw_cb.setMinimumWidth(60); absent_cw_cb.setMaximumWidth(60); absent_cw_cb.stateChanged.connect(lambda state, s=subject: self.handle_absent_toggle(s)); row_layout.addWidget(absent_cw_cb); row_data["absent_cw"] = absent_cw_cb
            termexam = NavigableLineEdit(); termexam.setPlaceholderText("0"); termexam.setMinimumWidth(90); termexam.setMaximumWidth(90); termexam.textChanged.connect(lambda text, s=subject: self.validate_marks_sum(s)); row_layout.addWidget(termexam); row_data["termexam"] = termexam
            absent_te_cb = QCheckBox(); absent_te_cb.setMinimumWidth(60); absent_te_cb.setMaximumWidth(60); absent_te_cb.stateChanged.connect(lambda state, s=subject: self.handle_absent_toggle(s)); row_layout.addWidget(absent_te_cb); row_data["absent_te"] = absent_te_cb
            combo = NavigableComboBox(); combo.addItems([str(m) for m in max_marks_options]); combo.setCurrentText(str(self.config.get("default_max_marks", 100))); combo.setMinimumWidth(60); combo.setMaximumWidth(60); combo.currentTextChanged.connect(lambda text, s=subject: self.validate_marks_sum(s)); row_layout.addWidget(combo); row_data["maxmarks"] = combo
            obt_label = QLabel("0"); obt_label.setMinimumWidth(60); obt_label.setMaximumWidth(60); obt_label.setAlignment(Qt.AlignCenter); obt_label.setStyleSheet("color: #3498db; font-weight: bold;"); obt_label.setFocusPolicy(Qt.NoFocus); row_layout.addWidget(obt_label); row_data["obt"] = obt_label
            pct_label = QLabel("0%"); pct_label.setMinimumWidth(60); pct_label.setMaximumWidth(60); pct_label.setAlignment(Qt.AlignCenter); pct_label.setStyleSheet("color: #2980b9; font-weight: bold;"); pct_label.setFocusPolicy(Qt.NoFocus); row_layout.addWidget(pct_label); row_data["pct"] = pct_label
            grade_label = QLabel("-"); grade_label.setMinimumWidth(60); grade_label.setMaximumWidth(60); grade_label.setAlignment(Qt.AlignCenter); grade_label.setStyleSheet("color: #27ae60; font-weight: bold; background-color: #d5f4e6; border-radius: 4px; padding: 2px;"); grade_label.setFocusPolicy(Qt.NoFocus); row_layout.addWidget(grade_label); row_data["grade"] = grade_label
            row_layout.addStretch(); self.marks_inputs[subject] = row_data; self.marks_grid.append(row_data); marks_rows_layout.addLayout(row_layout)

        marks_table_widget = MarksTableWidget(self.marks_grid); marks_table_widget.setLayout(marks_rows_layout); table_layout.addWidget(marks_table_widget); separator2 = QtWidgets.QFrame(); separator2.setFrameShape(QtWidgets.QFrame.HLine); separator2.setFrameShadow(QtWidgets.QFrame.Sunken); separator2.setLineWidth(1); table_layout.addWidget(separator2)
        grand_layout = QHBoxLayout(); grand_layout.setSpacing(5); grand_layout.setContentsMargins(5, 10, 0, 10); grand_label = QLabel("GRAND TOTAL"); grand_label.setMinimumWidth(100); grand_label.setMaximumWidth(100); grand_label.setFont(QFont("Arial", 10, QFont.Bold)); grand_layout.addWidget(grand_label)
        self.grand_cw = QLabel("0"); self.grand_cw.setMinimumWidth(90); self.grand_cw.setMaximumWidth(90); self.grand_cw.setAlignment(Qt.AlignCenter); self.grand_cw.setFont(QFont("Arial", 10, QFont.Bold)); self.grand_cw.setStyleSheet("color: #27ae60; background-color: #d5f4e6; padding: 5px; border-radius: 4px;"); grand_layout.addWidget(self.grand_cw); spacer1 = QLabel(""); spacer1.setMinimumWidth(60); spacer1.setMaximumWidth(60); grand_layout.addWidget(spacer1)
        self.grand_te = QLabel("0"); self.grand_te.setMinimumWidth(90); self.grand_te.setMaximumWidth(90); self.grand_te.setAlignment(Qt.AlignCenter); self.grand_te.setFont(QFont("Arial", 10, QFont.Bold)); self.grand_te.setStyleSheet("color: #27ae60; background-color: #d5f4e6; padding: 5px; border-radius: 4px;"); grand_layout.addWidget(self.grand_te); spacer2 = QLabel(""); spacer2.setMinimumWidth(60); spacer2.setMaximumWidth(60); grand_layout.addWidget(spacer2)
        self.grand_max = QLabel("0"); self.grand_max.setMinimumWidth(60); self.grand_max.setMaximumWidth(60); self.grand_max.setAlignment(Qt.AlignCenter); self.grand_max.setFont(QFont("Arial", 10, QFont.Bold)); self.grand_max.setStyleSheet("color: #27ae60; background-color: #d5f4e6; padding: 5px; border-radius: 4px;"); grand_layout.addWidget(self.grand_max)
        self.grand_obt = QLabel("0"); self.grand_obt.setMinimumWidth(60); self.grand_obt.setMaximumWidth(60); self.grand_obt.setAlignment(Qt.AlignCenter); self.grand_obt.setFont(QFont("Arial", 10, QFont.Bold)); self.grand_obt.setStyleSheet("color: #27ae60; background-color: #d5f4e6; padding: 5px; border-radius: 4px;"); grand_layout.addWidget(self.grand_obt)
        self.grand_pct = QLabel("0%"); self.grand_pct.setMinimumWidth(60); self.grand_pct.setMaximumWidth(60); self.grand_pct.setAlignment(Qt.AlignCenter); self.grand_pct.setFont(QFont("Arial", 10, QFont.Bold)); self.grand_pct.setStyleSheet("color: #fff; background-color: #27ae60; padding: 5px; border-radius: 4px;"); grand_layout.addWidget(self.grand_pct)
        self.grand_grade = QLabel("-"); self.grand_grade.setMinimumWidth(60); self.grand_grade.setMaximumWidth(60); self.grand_grade.setAlignment(Qt.AlignCenter); self.grand_grade.setFont(QFont("Arial", 11, QFont.Bold)); self.grand_grade.setStyleSheet("color: #fff; background-color: #1e8449; padding: 5px; border-radius: 4px;"); grand_layout.addWidget(self.grand_grade); grand_layout.addStretch(); table_layout.addLayout(grand_layout); table_container.setLayout(table_layout); self.marks_layout.addWidget(table_container)

        # --- Setup navigation AFTER table is populated ---
        self.setup_complete_navigation_order()
        # ---

    def handle_absent_toggle(self, subject):
        if subject not in self.marks_inputs: return; row = self.marks_inputs[subject]; is_cw_absent = row["absent_cw"].isChecked(); is_te_absent = row["absent_te"].isChecked()
        if is_cw_absent: row["coursework"].setEnabled(False); row["coursework"].clear(); row["coursework"].setStyleSheet("QLineEdit { background-color: #ffe6e6; border: 2px solid #e74c3c; border-radius: 6px; padding: 8px; color: #999; }")
        else: row["coursework"].setEnabled(True); row["coursework"].setStyleSheet("QLineEdit { background-color: #ffffff; border: 2px solid #e1e8ed; border-radius: 6px; padding: 8px; color: #2c3e50; }")
        if is_te_absent: row["termexam"].setEnabled(False); row["termexam"].clear(); row["termexam"].setStyleSheet("QLineEdit { background-color: #ffe6e6; border: 2px solid #e74c3c; border-radius: 6px; padding: 8px; color: #999; }")
        else: row["termexam"].setEnabled(True); row["termexam"].setStyleSheet("QLineEdit { background-color: #ffffff; border: 2px solid #e1e8ed; border-radius: 6px; padding: 8px; color: #2c3e50; }")
        if is_cw_absent and is_te_absent:
            # row["maxmarks"].setEnabled(False) # Let's keep max marks combo enabled visually
            row["obt"].setText("Absent"); row["pct"].setText("Absent"); row["grade"].setText("Absent")
            row["obt"].setStyleSheet("color: #e74c3c; font-weight: bold; font-style: italic;"); row["pct"].setStyleSheet("color: #e74c3c; font-weight: bold; font-style: italic;"); row["grade"].setStyleSheet("color: #e74c3c; font-weight: bold; font-style: italic; background-color: #ffe6e6; border-radius: 4px; padding: 2px;")
        else:
             # row["maxmarks"].setEnabled(True) # Ensure enabled if not fully absent
             self.validate_marks_sum(subject)
        self.update_grand_totals()

    def validate_marks_sum(self, subject):
        if subject not in self.marks_inputs: return; row = self.marks_inputs[subject]; is_cw_absent = row["absent_cw"].isChecked(); is_te_absent = row["absent_te"].isChecked()
        if is_cw_absent and is_te_absent: row["obt"].setText("Absent"); row["pct"].setText("Absent"); row["grade"].setText("Absent"); row["obt"].setStyleSheet("color: #e74c3c; font-weight: bold; font-style: italic;"); row["pct"].setStyleSheet("color: #e74c3c; font-weight: bold; font-style: italic;"); row["grade"].setStyleSheet("color: #e74c3c; font-weight: bold; font-style: italic; background-color: #ffe6e6; border-radius: 4px; padding: 2px;"); self.update_grand_totals(); return
        try:
            cw = 0 if is_cw_absent else float(row["coursework"].text() or 0); te = 0 if is_te_absent else float(row["termexam"].text() or 0); max_marks = float(row["maxmarks"].currentText()); obt = cw + te
            row["obt"].setText(str(int(obt))); pct = (obt / max_marks * 100) if max_marks > 0 else 0; row["pct"].setText(f"{pct:.1f}%"); grade = self.get_grade(pct); row["grade"].setText(grade)
            row["obt"].setStyleSheet("color: #3498db; font-weight: bold;"); row["pct"].setStyleSheet("color: #2980b9; font-weight: bold;"); row["grade"].setStyleSheet("color: #27ae60; font-weight: bold; background-color: #d5f4e6; border-radius: 4px; padding: 2px;")
            if obt > max_marks:
                if not is_cw_absent: row["coursework"].setStyleSheet("QLineEdit { background-color: #fff5f5; border: 2px solid #e74c3c; border-radius: 6px; padding: 8px; color: #2c3e50; }")
                if not is_te_absent: row["termexam"].setStyleSheet("QLineEdit { background-color: #fff5f5; border: 2px solid #e74c3c; border-radius: 6px; padding: 8px; color: #2c3e50; }")
                row["obt"].setStyleSheet("color: #e74c3c; font-weight: bold; background-color: #ffe6e6; padding: 2px; border-radius: 2px;"); row["pct"].setStyleSheet("color: #e74c3c; font-weight: bold;")
            self.update_grand_totals()
        except ValueError: pass # Ignore conversion errors temporarily

    def update_grand_totals(self):
        if not hasattr(self, 'marks_inputs') or not hasattr(self, 'grand_cw'): return # More safety checks
        try:
            total_cw = 0; total_te = 0; total_max = 0; total_obt = 0
            for subject, row in self.marks_inputs.items():
                is_cw_absent = row["absent_cw"].isChecked(); is_te_absent = row["absent_te"].isChecked()
                try: max_m = float(row["maxmarks"].currentText()); total_max += max_m
                except ValueError: pass
                if is_cw_absent and is_te_absent: continue
                cw = 0 if is_cw_absent else float(row["coursework"].text() or 0); te = 0 if is_te_absent else float(row["termexam"].text() or 0)
                total_cw += cw; total_te += te; total_obt += cw + te
            self.grand_cw.setText(str(int(total_cw))); self.grand_te.setText(str(int(total_te))); self.grand_max.setText(str(int(total_max))); self.grand_obt.setText(str(int(total_obt)))
            grand_pct = (total_obt / total_max * 100) if total_max > 0 else 0; self.grand_pct.setText(f"{grand_pct:.1f}%")
            grand_grade = self.get_grade(grand_pct); self.grand_grade.setText(grand_grade)
        except ValueError: pass
        except Exception as e: print(f"Error in update_grand_totals: {e}")

    def show_preset_remarks(self):
        remarks_data = self.load_preset_remarks(); dialog = QDialog(self); dialog.setWindowTitle("Preset Remarks"); dialog.setGeometry(100, 100, 500, 400); layout = QVBoxLayout()
        layout.addWidget(QLabel("Select or manage preset remarks:")); remarks_list = QListWidget();
        for remark in remarks_data.get("presets", []): remarks_list.addItem(remark)
        layout.addWidget(remarks_list); btn_layout = QHBoxLayout()
        def insert_remark():
            if remarks_list.currentItem(): self.remarks_input.insertPlainText(remarks_list.currentItem().text()); dialog.close()
        def add_new_remark():
            text, ok = QInputDialog.getMultiLineText(self, "Add Remark", "Enter new preset remark:")
            if ok and text: remarks_data["presets"].append(text); self.save_preset_remarks(remarks_data); remarks_list.addItem(text)
        def delete_remark():
            if remarks_list.currentItem(): row = remarks_list.row(remarks_list.currentItem()); remarks_data["presets"].pop(row); self.save_preset_remarks(remarks_data); remarks_list.takeItem(row)
        insert_btn = QPushButton("Insert Selected"); insert_btn.clicked.connect(insert_remark); add_btn = QPushButton("Add New"); add_btn.clicked.connect(add_new_remark); delete_btn = QPushButton("Delete"); delete_btn.clicked.connect(delete_remark); close_btn = QPushButton("Close"); close_btn.clicked.connect(dialog.close)
        btn_layout.addWidget(insert_btn); btn_layout.addWidget(add_btn); btn_layout.addWidget(delete_btn); btn_layout.addWidget(close_btn); layout.addLayout(btn_layout); dialog.setLayout(layout); dialog.exec()

    def load_preset_remarks(self):
        if os.path.exists(REMARKS_FILE):
            try:
                with open(REMARKS_FILE, 'r') as f: return json.load(f)
            except: return {"presets": []}
        return {"presets": []}

    def save_preset_remarks(self, remarks_data):
        try:
            os.makedirs(os.path.dirname(REMARKS_FILE), exist_ok=True) # Ensure dir exists
            with open(REMARKS_FILE, 'w') as f: json.dump(remarks_data, f, indent=2)
        except Exception as e: print(f"Error saving remarks: {e}")

    def get_marks_data_for_pdf(self):
        marks_data = {};
        if not hasattr(self, 'marks_inputs'): return {}, {}
        for subject, row in self.marks_inputs.items():
            is_cw_absent = row["absent_cw"].isChecked(); is_te_absent = row["absent_te"].isChecked()
            if is_cw_absent and is_te_absent: marks_data[subject] = {"coursework": "Absent", "termexam": "Absent", "maxmarks": row["maxmarks"].currentText(), "obt": "Absent", "pct": "Absent", "grade": "Absent", "is_cw_absent": True, "is_te_absent": True, "is_fully_absent": True}
            elif is_cw_absent: marks_data[subject] = {"coursework": "Absent", "termexam": row["termexam"].text() or "0", "maxmarks": row["maxmarks"].currentText(), "obt": row["obt"].text(), "pct": row["pct"].text(), "grade": row["grade"].text(), "is_cw_absent": True, "is_te_absent": False, "is_fully_absent": False}
            elif is_te_absent: marks_data[subject] = {"coursework": row["coursework"].text() or "0", "termexam": "Absent", "maxmarks": row["maxmarks"].currentText(), "obt": row["obt"].text(), "pct": row["pct"].text(), "grade": row["grade"].text(), "is_cw_absent": False, "is_te_absent": True, "is_fully_absent": False}
            else: marks_data[subject] = {"coursework": row["coursework"].text() or "0", "termexam": row["termexam"].text() or "0", "maxmarks": row["maxmarks"].currentText(), "obt": row["obt"].text(), "pct": row["pct"].text(), "grade": row["grade"].text(), "is_cw_absent": False, "is_te_absent": False, "is_fully_absent": False}
        grand_totals = {"cw": self.grand_cw.text(), "te": self.grand_te.text(), "max": self.grand_max.text(), "obt": self.grand_obt.text(), "pct": self.grand_pct.text(), "grade": self.grand_grade.text()}; return marks_data, grand_totals

    def save_and_generate_pdf(self):
        try:
            student_name = self.student_name_input.text().strip().title();
            if not student_name: QMessageBox.warning(self, "Error", "Student name required!"); self.student_name_input.setFocus(); return
            class_sec = self.class_sec_input.text().strip().upper();
            if not self.validate_class_sec(class_sec): QMessageBox.warning(self, "Error", "Class/Sec format invalid! Use: I-A, II-B, etc."); self.class_sec_input.setFocus(); return
            gr_no = self.gr_no_input.text().strip();
            if not self.validate_gr_no(gr_no): QMessageBox.warning(self, "Error", "G.R No must be numeric!"); self.gr_no_input.setFocus(); return
            status_btn = self.status_group.checkedButton();
            if not status_btn: QMessageBox.warning(self, "Error", "Please select a Result Status (e.g., Passed)."); return

            marks_data, grand_totals = self.get_marks_data_for_pdf(); date_str = self.date_input.date().toString("dd MMMM yyyy")
            pdf_data = {
                "student_name": student_name, "father_name": self.father_name_input.text().strip().title(), "class_sec": class_sec,
                "session": self.session_combo.currentText(), "gr_no": gr_no, "rank": self.rank_combo.currentText(),
                "total_days": str(self.total_days_input.value()), "days_attended": str(self.days_attended_input.value()), "days_absent": str(self.days_absent_input.value()),
                "term": self.term_combo.currentText(), "marks_data": marks_data, "conduct": self.conduct_combo.currentText(),
                "performance": self.performance_combo.currentText(), "progress": self.progress_combo.currentText(), "remarks": self.remarks_input.toPlainText(),
                "status": status_btn.text(), "date": date_str, "grand_totals": grand_totals, "all_subjects": self.selected_subjects
            }
            success, message = self.db_manager.save_report_card(pdf_data, self.logged_in_user_id) # Pass user ID
            if not success: QMessageBox.critical(self, "Database Error", f"Failed to save report card:\n{message}"); return
            self.create_pdf_report(pdf_data) # Generate PDF after successful save
        except Exception as e: QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}\nCheck console for details."); print(e)

    def validate_class_sec(self, class_sec):
        if not class_sec: return False; pattern = r'^(I|II|III|IV|V|VI|VII|VIII|IX|X|\d+)-[A-Z]$'; return bool(re.match(pattern, class_sec.upper()))

    def validate_gr_no(self, gr_no):
        if not gr_no: return False; return gr_no.isdigit()

    def create_pdf_report(self, data):
        try:
            filename = f"{data['student_name'].replace(' ', '_')}_{data['class_sec']}_ReportCard_{data['session']}"
            success, message, pdf_path = PDFManager.generate_pdf(filename, data)
            if success:
                QMessageBox.information(self, "Success", f"Report card saved and PDF generated!\n\nSaved at: {pdf_path}")
                reply = QMessageBox.question(self, "Open PDF", "Do you want to open the generated PDF?", QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    try: os.startfile(pdf_path) # Windows
                    except AttributeError:
                        try: os.system(f'open "{pdf_path}"') # macOS
                        except: os.system(f'xdg-open "{pdf_path}"') # Linux
                self.reset_form() # Reset form ONLY after successful save AND PDF generation
            else: QMessageBox.critical(self, "PDF Error", f"Report was saved to DB, but PDF generation failed:\n{message}")
        except ImportError:
             QMessageBox.critical(self, "Error", "PDF Generation library (WeasyPrint) not found.\nPlease install it: pip install weasyprint")
        except Exception as e: QMessageBox.critical(self, "PDF Error", f"Error generating PDF: {str(e)}")

# --- Main Application Execution ---
if __name__ == "__main__":

    # Ensure directories exist
    os.makedirs("config", exist_ok=True); os.makedirs("settings", exist_ok=True); os.makedirs("output", exist_ok=True)
    os.makedirs("src/managers", exist_ok=True)
    init_path = "src/__init__.py";
    if not os.path.exists(init_path): Path(init_path).touch()
    init_path_managers = "src/managers/__init__.py";
    if not os.path.exists(init_path_managers): Path(init_path_managers).touch()

    app = QApplication(sys.argv)

    # Initialize DB Manager (creates tables & default admin user)
    db_manager = DatabaseManager("report_system.db")
    db_manager.init_database()

    # Show Login Dialog
    login_dialog = LoginDialog(db_manager)
    if login_dialog.exec() == QDialog.Accepted:
        logged_in_user_id = login_dialog.logged_in_user_id
        window = MainWindow(logged_in_user_id) # Pass user ID to main window
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0) # Exit if login fails or is cancelled
