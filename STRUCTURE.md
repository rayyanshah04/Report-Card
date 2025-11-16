# Report Card System - Folder Structure

```
Report-Card/
├── main.py                          # Entry point - minimal code, just launches app
├── requirements.txt
├── config/
│   └── config.json
├── settings/
│   ├── filters.json
│   └── remarks.json
├── templates/
│   ├── report_card.html
│   ├── styles.css
│   └── fonts/
├── output/
├── src/
│   ├── __init__.py
│   ├── styles/
│   │   ├── __init__.py
│   │   └── stylesheet.py          # All Qt stylesheets
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py              # Utility functions (date formatting, etc)
│   ├── managers/
│   │   ├── __init__.py
│   │   ├── config_manager.py       # Config management
│   │   ├── pdf_manager.py          # PDF generation
│   │   └── filters_manager.py      # Filters management
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── widgets/
│   │   │   ├── __init__.py
│   │   │   └── custom_widgets.py   # NoWheelComboBox, NavigableComboBox
│   │   ├── dialogs/
│   │   │   ├── __init__.py
│   │   │   ├── login_dialog.py     # Login screen
│   │   │   ├── settings_dialog.py  # Settings popup
│   │   │   ├── subject_filter_dialog.py
│   │   │   ├── remarks_dialog.py
│   │   │   └── student_details_dialog.py  # Single student view popup
│   │   ├── screens/
│   │   │   ├── __init__.py
│   │   │   ├── result_screen.py    # Report card generation screen
│   │   │   └── student_view_screen.py  # Student management screen
│   │   └── main_window.py          # Main window with tabs
│   └── database/
│       ├── __init__.py
│       └── db_manager.py           # Database operations
```

## File Descriptions:

### main.py (Entry Point)
- Minimal code
- Just initializes app and shows login/main window

### src/styles/stylesheet.py
- All Qt stylesheets in one place
- MODERN_STYLESHEET constant

### src/utils/helpers.py  
- Date formatting functions
- Common utility functions

### src/managers/
- config_manager.py: ConfigManager class
- pdf_manager.py: PDFManager class
- filters_manager.py: FiltersManager class

### src/ui/widgets/custom_widgets.py
- NoWheelComboBox
- NavigableComboBox
- Other custom widgets

### src/ui/dialogs/
- login_dialog.py: LoginDialog class
- settings_dialog.py: SettingsDialog class
- subject_filter_dialog.py: SubjectFilterDialog class
- remarks_dialog.py: RemarksDialog class
- student_details_dialog.py: Student detail view popup

### src/ui/screens/
- result_screen.py: ReportCardScreen class (entire result/report generation tab)
- student_view_screen.py: StudentViewScreen class (entire student management tab)

### src/ui/main_window.py
- MainWindow class
- Creates tabs
- Manages navigation

### src/database/db_manager.py
- All database operations
- Student CRUD
- Queries
```
