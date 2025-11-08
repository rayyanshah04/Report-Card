# GEMINI.md

## Project Overview

This project is a desktop application for managing and generating student report cards for the "Faizan Academy". It is built using Python with the PySide6 framework for the graphical user interface. The application allows users to input student information, record marks for various subjects, and generate professional-looking PDF report cards.

**Key Technologies:**

*   **GUI:** PySide6 (the official Python bindings for Qt)
*   **PDF Generation:** WeasyPrint, which renders HTML and CSS into PDFs.
*   **Templating:** Jinja2 is used to create dynamic HTML templates for the report cards.
*   **Database:** SQLite is used for data storage, managed via the `sqlite3` module.
*   **Image Processing:** Pillow is listed as a dependency, likely for handling images such as the school logo.

**Architecture:**

The application follows a clear, modular structure:

*   **`main.py`**: The main entry point and core of the application. It defines the main window, all dialogs (for settings, user management, etc.), and handles user interactions and event-driven logic.
*   **`src/managers/`**: A directory containing specialized manager classes to handle distinct responsibilities:
    *   **`database_manager.py`**: Encapsulates all database operations. It defines the schema and provides methods for user authentication, data storage (students, subjects, reports), and retrieval. It also includes an audit log for tracking important user actions.
    *   **`pdf_manager.py`**: Manages the creation of PDF report cards. It uses Jinja2 to render an HTML template with student data and then converts the resulting HTML to a PDF using WeasyPrint.
    *   **`config_manager.py`**: (Defined in `main.py`) Handles loading and saving application settings from a `config.json` file.
*   **`templates/`**: This directory stores the assets for PDF generation, including the `report_card.html` Jinja2 template, a `styles.css` file for styling, and font files.
*   **`output/`**: The default directory where generated PDF report cards are saved.
*   **`report_system.db`**: The SQLite database file.

## Building and Running

This is a Python application that can be run directly from the source code.

**1. Setup a Virtual Environment (Recommended):**

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

**2. Install Dependencies:**

The required Python packages are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

**3. Run the Application:**

Execute the `main.py` script to start the GUI application.

```bash
python main.py
```

The application will first present a login screen. A default user is created on the first run:
*   **Username:** `admin`
*   **Password:** `admin`

## Development Conventions

*   **GUI:** The application is built with PySide6 and uses a modern, clean stylesheet defined directly in `main.py`.
*   **Database:** All database interactions are centralized in the `DatabaseManager` class. The schema is comprehensive, including tables for users, students, subjects, report cards, marks, and an audit log. Foreign key constraints are used to maintain data integrity.
*   **Configuration:** Application settings are stored in JSON files (`config/config.json`, `settings/filters.json`, `settings/remarks.json`), making them easy to view and modify.
*   **PDF Generation:** PDF creation is a two-step process: first, a dynamic HTML file is rendered from a Jinja2 template, and then WeasyPrint converts this HTML to a PDF. This approach separates the data, structure (HTML), and presentation (CSS) of the report card.
*   **Error Handling:** The code includes `try...except` blocks to handle potential errors during file I/O, database operations, and PDF generation, often displaying user-friendly error messages via `QMessageBox`.
*   **Security:** The application includes a login system and an audit trail to log significant user actions. Passwords are a basic `hashlib.sha256` hash.
