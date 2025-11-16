"""
Application stylesheet constants
"""

MODERN_STYLESHEET = """
QMainWindow, QDialog, QWidget {
    background-color: #f5f7fa;
    color: #2c3e50;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QLineEdit, QTextEdit, QSpinBox {
    background-color: #ffffff;
    border: 2px solid #e1e8ed;
    border-radius: 6px;
    padding: 6px;
    color: #2c3e50;
    font-size: 11px;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {
    border: 2px solid #3498db;
}

QLineEdit:disabled, QTextEdit:disabled, QSpinBox:disabled {
    background-color: #ecf0f1;
    color: #95a5a6;
}

QSpinBox::up-button, QSpinBox::down-button {
    background-color: #3498db;
    border: none;
    width: 20px;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #2980b9;
}

QCheckBox, QRadioButton {
    spacing: 8px;
    color: #2c3e50;
    font-size: 11px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #bdc3c7;
    border-radius: 4px;
    background-color: white;
}

QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    background-color: #3498db;
    border-color: #3498db;
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
    subcontrol-origin: padding;
    subcontrol-position: right center;
    image: url(none);
}

QComboBox::down-arrow {
    image: url(none);
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #000000;
    selection-background-color: #3498db;
    selection-color: #ffffff;
    border: 1px solid #e1e8ed;
    outline: none;
}

QComboBox QAbstractItemView::item {
    color: #000000;
    padding: 5px;
    border: none;
    outline: none;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #3498db;
    color: #ffffff;
    border: none;
    outline: none;
}

QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 11px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #1f618d;
}

QPushButton:disabled {
    background-color: #bdc3c7;
    color: #7f8c8d;
}

QPushButton#generateBtn {
    background-color: #27ae60;
    font-size: 13px;
    padding: 12px 24px;
}

QPushButton#generateBtn:hover {
    background-color: #229954;
}

QLabel {
    color: #2c3e50;
    font-size: 11px;
}

QTableWidget {
    background-color: white;
    alternate-background-color: #f8f9fa;
    gridline-color: #e1e8ed;
    border: 1px solid #e1e8ed;
    border-radius: 6px;
    font-size: 11px;
}

QTableWidget::item {
    padding: 4px;
    color: #2c3e50;
    border: none;
}

QTableWidget::item:selected {
    background-color: #3498db;
    color: white;
}

QHeaderView::section {
    background-color: #34495e;
    color: white;
    padding: 8px;
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
    background-color: #f5f5f5;
    color: #2c3e50;
    border-bottom: 1px solid #e0e0e0;
    padding: 2px;
    font-size: 11px;
}

QMenuBar::item {
    padding: 4px 12px;
    background-color: transparent;
}

QMenuBar::item:selected {
    background-color: #e0e0e0;
    color: #2c3e50;
}

QMenu {
    background-color: white;
    border: 1px solid #e1e8ed;
    padding: 4px;
}

QMenu::item {
    padding: 6px 20px;
    color: #2c3e50;
}

QMenu::item:selected {
    background-color: #3498db;
    color: white;
}

QListWidget {
    background-color: white;
    border: 1px solid #e1e8ed;
    border-radius: 6px;
    padding: 4px;
}

QListWidget::item {
    padding: 8px;
    border-radius: 4px;
}

QListWidget::item:selected {
    background-color: #3498db;
    color: white;
}

QStatusBar {
    background-color: #34495e;
    color: white;
}

QDateEdit {
    background-color: #ffffff;
    border: 2px solid #e1e8ed;
    border-radius: 6px;
    padding: 6px;
    color: #000000;
    font-size: 11px;
}

QDateEdit:focus {
    border: 2px solid #3498db;
}

QDateEdit::drop-down {
    border: none;
    background-color: transparent;
    width: 25px;
    subcontrol-origin: padding;
    subcontrol-position: right center;
    image: url(none);
}

QDateEdit::down-arrow {
    image: url(none);
    width: 12px;
    height: 12px;
}

QCalendarWidget {
    background-color: #ffffff;
    color: #000000;
}

QCalendarWidget QAbstractItemView {
    background-color: #ffffff;
    color: #000000;
    selection-background-color: #3498db;
    selection-color: #ffffff;
}

QCalendarWidget QWidget {
    color: #000000;
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

QCalendarWidget QMenu {
    background-color: #ffffff;
    color: #000000;
}

QCalendarWidget QSpinBox {
    background-color: #ffffff;
    color: #000000;
}
"""
