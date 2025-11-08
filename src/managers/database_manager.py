import sqlite3
import os
from pathlib import Path
import hashlib # For basic password hashing (replace with bcrypt later for better security)

class DatabaseManager:
    """Manages all database interactions for the report card system."""

    def __init__(self, db_path="report_system.db"):
        self.db_path = db_path
        # Ensure the database file exists
        if not os.path.exists(self.db_path):
            Path(self.db_path).touch()
            print(f"Created database file at: {self.db_path}")

    def connect(self):
        """Creates and returns a database connection."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row # Allows accessing columns by name
            conn.execute("PRAGMA foreign_keys = ON;") # Enforce foreign keys
            return conn
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None

    def _log_audit(self, cursor, user_id, action, table_name=None, record_id=None, description=None):
        """Helper function to insert an audit log entry."""
        try:
            # In a real app, get IP address here if needed
            ip_address = None # Placeholder for IP address
            cursor.execute(
                """
                INSERT INTO audit_logs (user_id, action, table_name, record_id, description, ip_address)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, action, table_name, record_id, description, ip_address)
            )
        except Exception as log_e:
            # Log the error but don't stop the main operation
            print(f"!!! FAILED TO WRITE AUDIT LOG: {log_e} !!!")

    # --- Hashing function (simple SHA256 for now) ---
    def _hash_password(self, password):
        """Hashes the password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()

    # --- UPDATED: Ensure Default User (Admin Only) ---
    def ensure_default_users(self):
        """Adds the default 'admin' user if it doesn't exist."""
        admin_user = {'username': 'admin', 'password': 'admin', 'role': 'principal'}
        conn = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (admin_user['username'],))
            if not cursor.fetchone():
                hashed_password = self._hash_password(admin_user['password'])
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (admin_user['username'], hashed_password, admin_user['role'])
                )
                print(f"Created default user: {admin_user['username']}")
                conn.commit()
        except Exception as e:
            if conn: conn.rollback()
            print(f"Error ensuring default admin user: {e}")
        finally:
            if conn: conn.close()

    # --- NEW: Get All Users ---
    def get_all_users(self):
        """Fetches all user details (except password) for management."""
        conn = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, username, role, email, is_active FROM users ORDER BY username")
            return cursor.fetchall() # Returns list of Row objects
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []
        finally:
            if conn: conn.close()

    # --- NEW: Add User ---
    def add_user(self, username, password, role, email=None, performed_by_user_id=None): # Added performed_by_user_id
        """Adds a new user to the database."""
        conn = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            hashed_password = self._hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)",
                (username, hashed_password, role, email)
            )
            new_user_id = cursor.lastrowid # Get the ID of the new user

            # --- Log Audit ---
            if performed_by_user_id: # Only log if the action performer is known
                self._log_audit(cursor, performed_by_user_id, "ADD_USER", table_name="users", record_id=new_user_id, description=f"Added user: {username}, Role: {role}")
            # -----------------

            conn.commit()
            return True, f"User '{username}' added successfully."
        except sqlite3.IntegrityError:
            return False, f"Username '{username}' already exists."
        except Exception as e:
            if conn: conn.rollback()
            print(f"Error adding user {username}: {e}")
            return False, f"Error adding user: {e}"
        finally:
            if conn: conn.close()

    # --- NEW: Update User Status ---
    def update_user_status(self, user_id, is_active, performed_by_user_id):
        """Activates or deactivates a user."""
        conn = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET is_active = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?", (is_active, user_id))

            # --- Log Audit ---
            status_desc = "activated" if is_active else "deactivated"
            self._log_audit(cursor, performed_by_user_id, "UPDATE_USER_STATUS", table_name="users", record_id=user_id, description=f"User {status_desc}")
            # -----------------

            conn.commit()
            return True, f"User status updated ({status_desc})."
        except Exception as e:
            if conn: conn.rollback()
            print(f"Error updating user status for ID {user_id}: {e}")
            return False, f"Error updating user status: {e}"
        finally:
            if conn: conn.close()

    # --- NEW: Update User Role ---
    def update_user_role(self, user_id, new_role, performed_by_user_id): # Added performed_by_user_id
        """Updates a user's role."""
        if new_role not in ('teacher', 'principal'):
             return False, "Invalid role specified."
        conn = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET role = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?", (new_role, user_id))

            # --- Log Audit ---
            self._log_audit(cursor, performed_by_user_id, "UPDATE_USER_ROLE", table_name="users", record_id=user_id, description=f"Changed role to {new_role}")
            # -----------------

            conn.commit()
            return True, "User role updated successfully."
        except Exception as e:
            if conn: conn.rollback()
            print(f"Error updating user role for ID {user_id}: {e}")
            return False, f"Error updating user role: {e}"
        finally:
            if conn: conn.close()

    # --- NEW: Update User Password ---
    def update_user_password(self, user_id, new_password, performed_by_user_id): # Added performed_by_user_id
        """Updates a user's password."""
        conn = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            hashed_password = self._hash_password(new_password)
            cursor.execute("UPDATE users SET password = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?", (hashed_password, user_id))

            # --- Log Audit ---
            self._log_audit(cursor, performed_by_user_id, "UPDATE_USER_PASSWORD", table_name="users", record_id=user_id, description="Password reset")
            # -----------------

            conn.commit()
            return True, "User password updated successfully."
        except Exception as e:
            if conn: conn.rollback()
            print(f"Error updating user password for ID {user_id}: {e}")
            return False, f"Error updating user password: {e}"
        finally:
            if conn: conn.close()

    # --- NEW: Delete User ---
    def delete_user(self, user_id, performed_by_user_id): # Added performed_by_user_id
        """Deletes a user from the database."""
        conn = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            if user_id == 1:
                 return False, "Cannot delete the primary admin user."

            # Get username before deleting for logging
            cursor.execute("SELECT username FROM users WHERE user_id = ?", (user_id,))
            user_to_delete = cursor.fetchone()
            username_for_log = user_to_delete['username'] if user_to_delete else f"ID:{user_id}"

            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            rows_affected = cursor.rowcount # Check rows affected *before* logging

            if rows_affected > 0:
                 # --- Log Audit ---
                 self._log_audit(cursor, performed_by_user_id, "DELETE_USER", table_name="users", record_id=user_id, description=f"Deleted user: {username_for_log}")
                 # -----------------
                 conn.commit()
                 return True, "User deleted successfully."
            else:
                 conn.rollback() # No need to commit if nothing changed
                 return False, "User not found or already deleted."
        except sqlite3.IntegrityError as e:
             print(f"Integrity error deleting user ID {user_id}: {e}")
             return False, f"Cannot delete user: They may have associated records (e.g., reports). Consider deactivating instead."
        except Exception as e:
            if conn: conn.rollback()
            print(f"Error deleting user ID {user_id}: {e}")
            return False, f"Error deleting user: {e}"
        finally:
            if conn: conn.close()

    # --- UPDATED: init_database ---
    def init_database(self):
        """
        Initializes the database by creating all tables if they don't exist
        and ensuring the default admin user exists.
        """
        schema = [
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('teacher', 'principal')),
                email TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS teachers (
                teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                teacher_org_id TEXT UNIQUE,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT,
                phone_number TEXT,
                address TEXT,
                appointment_date DATE,
                subject_of_interest TEXT,
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'On Leave', 'Resigned', 'Retired')),
                emergency_contact_name TEXT,
                emergency_contact_phone TEXT,
                additional_info TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS subjects (
                subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_name TEXT UNIQUE NOT NULL,
                type TEXT CHECK(type IN ('Core', 'Non-Core')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                gr_no TEXT UNIQUE NOT NULL,
                student_name TEXT NOT NULL,
                father_name TEXT NOT NULL,
                current_class_sec TEXT,
                current_session TEXT,
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Left', 'Inactive')),
                joining_date DATE,
                left_date DATE,
                left_reason TEXT,
                date_of_birth DATE,
                contact_number TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS student_class_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                class_sec TEXT NOT NULL,
                session TEXT NOT NULL,
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Promoted', 'Detained', 'Left')),
                promoted_to TEXT,
                promotion_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                UNIQUE(student_id, session)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS class_subjects (
                class_subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_sec TEXT NOT NULL,
                subject_id INTEGER NOT NULL,
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
                UNIQUE(class_sec, subject_id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS report_cards (
                report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                session TEXT NOT NULL,
                term TEXT NOT NULL CHECK(term IN ('Mid Year', 'Annual Year')),
                total_days INTEGER,
                days_attended INTEGER,
                days_absent INTEGER,
                rank_in_class TEXT,
                conduct TEXT CHECK(conduct IN ('Good', 'Fair', 'Bad')),
                performance TEXT CHECK(performance IN ('Excellent', 'Good', 'Bad')),
                progress TEXT CHECK(progress IN ('Satisfactory', 'Unsatisfactory')),
                remarks TEXT,
                status TEXT CHECK(status IN ('Passed', 'Promoted with Support', 'Needs Improvement')),
                created_by INTEGER NOT NULL, -- Removed DEFAULT 1
                updated_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                FOREIGN KEY (created_by) REFERENCES users(user_id),
                FOREIGN KEY (updated_by) REFERENCES users(user_id),
                UNIQUE(student_id, session, term)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS marks (
                mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                coursework_marks REAL,
                term_exam_marks REAL,
                max_marks INTEGER,
                obtained_marks REAL,
                percentage REAL,
                grade TEXT,
                is_absent BOOLEAN DEFAULT 0,
                absence_type TEXT CHECK(absence_type IN ('coursework', 'term_exam', 'both', NULL)),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (report_id) REFERENCES report_cards(report_id) ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
                UNIQUE(report_id, subject_id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS audit_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                table_name TEXT,
                record_id INTEGER,
                description TEXT,
                ip_address TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
            """,
            # --- Indices ---
            "CREATE INDEX IF NOT EXISTS idx_students_gr_no ON students(gr_no);",
            "CREATE INDEX IF NOT EXISTS idx_students_current_class ON students(current_class_sec);",
            "CREATE INDEX IF NOT EXISTS idx_student_class_history_student ON student_class_history(student_id);",
            "CREATE INDEX IF NOT EXISTS idx_student_class_history_session ON student_class_history(session);",
            "CREATE INDEX IF NOT EXISTS idx_report_cards_student ON report_cards(student_id);",
            "CREATE INDEX IF NOT EXISTS idx_report_cards_session_term ON report_cards(session, term);",
            "CREATE INDEX IF NOT EXISTS idx_marks_report ON marks(report_id);",
            "CREATE INDEX IF NOT EXISTS idx_audit_logs_user ON audit_logs(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);",
            "CREATE INDEX IF NOT EXISTS idx_teachers_user_id ON teachers(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_teachers_org_id ON teachers(teacher_org_id);"
        ]

        conn = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            for command in schema:
                cursor.execute(command)
            conn.commit()
            print("Database tables initialized successfully.")

            # --- Ensure default admin user exists ---
            self.ensure_default_users()
            # ----------------------------------------

        except Exception as e:
            if conn: conn.rollback()
            print(f"Error initializing database: {e}")
        finally:
            if conn: conn.close()

    # --- User Authentication ---
    def authenticate_user(self, username, password):
        """Checks username and hashed password. Returns user_id or None."""
        conn = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            hashed_password = self._hash_password(password)
            cursor.execute(
                "SELECT user_id FROM users WHERE username = ? AND password = ? AND is_active = 1",
                (username, hashed_password)
            )
            user = cursor.fetchone()
            return user['user_id'] if user else None
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
        finally:
            if conn: conn.close()

    # --- Report Card Saving ---
    def save_report_card(self, data, user_id): # user_id is already passed
        """Saves report card data, linking it to the logged-in user and logging actions."""
        conn = None
        try:
            # --- Define helper function INSIDE the method with proper indentation ---
            def safe_float(value):
                """Converts value to float, handling None, empty strings, and percentage signs."""
                if value is None:
                    return None
                try:
                    # Handle potential percentage strings explicitly
                    str_value = str(value).strip()
                    if not str_value: # Handle empty string
                        return None
                    if '%' in str_value:
                        str_value = str_value.replace('%', '')
                    return float(str_value)
                except (ValueError, TypeError):
                    return None # Return None for invalid conversions
            # -----------------------------------------------------------------------

            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("BEGIN TRANSACTION")

            # --- Pass user_id for potential logging ---
            student_id = self.get_or_create_student(
                data['gr_no'], data['student_name'], data['father_name'],
                data['class_sec'], data['session'], user_id # Pass user_id here
            )
            # ----------------------------------------
            if not student_id:
                raise Exception("Failed to get or create student.")

            current_user_id = user_id # Already have this

            cursor.execute(
                "SELECT report_id FROM report_cards WHERE student_id = ? AND session = ? AND term = ?",
                (student_id, data['session'], data['term'])
            )
            existing_report = cursor.fetchone()

            report_log_action = None
            report_log_desc = None
            report_id = None

            if existing_report:
                report_id = existing_report['report_id']
                cursor.execute(
                    """UPDATE report_cards SET
                        total_days = ?, days_attended = ?, days_absent = ?, rank_in_class = ?,
                        conduct = ?, performance = ?, progress = ?, remarks = ?, status = ?,
                        updated_by = ?, updated_at = CURRENT_TIMESTAMP
                       WHERE report_id = ?""",
                    (data['total_days'], data['days_attended'], data['days_absent'], data['rank'],
                     data['conduct'], data['performance'], data['progress'], data['remarks'],
                     data['status'], current_user_id, report_id)
                )
                cursor.execute("DELETE FROM marks WHERE report_id = ?", (report_id,)) # Clear old marks before insert
                report_log_action = "UPDATE_REPORT_CARD"
                report_log_desc = f"Updated report card for Student ID:{student_id}, Session:{data['session']}, Term:{data['term']}"

            else:
                cursor.execute(
                    """INSERT INTO report_cards (student_id, session, term, total_days, days_attended, days_absent,
                                               rank_in_class, conduct, performance, progress, remarks, status, created_by)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (student_id, data['session'], data['term'], data['total_days'], data['days_attended'], data['days_absent'],
                     data['rank'], data['conduct'], data['performance'], data['progress'], data['remarks'], data['status'], current_user_id)
                )
                report_id = cursor.lastrowid
                report_log_action = "ADD_REPORT_CARD"
                report_log_desc = f"Added report card for Student ID:{student_id}, Session:{data['session']}, Term:{data['term']}"

            # --- Log Report Card Action ---
            if report_log_action:
                 self._log_audit(cursor, current_user_id, report_log_action, table_name="report_cards", record_id=report_id, description=report_log_desc)
            # ----------------------------

            marks_saved_count = 0
            for subject_name, marks in data['marks_data'].items():
                subject_id = self.get_subject_id(subject_name)
                if not subject_id:
                    print(f"Warning: Skipping unknown subject '{subject_name}'")
                    continue

                is_absent = marks.get('is_fully_absent', False)
                absence_type = None
                if is_absent: absence_type = 'both'
                elif marks.get('is_cw_absent', False): absence_type = 'coursework'
                elif marks.get('is_te_absent', False): absence_type = 'term_exam'

                # Use the correctly defined safe_float
                cw_marks = None if marks.get('is_cw_absent') else safe_float(marks['coursework'])
                te_marks = None if marks.get('is_te_absent') else safe_float(marks['termexam'])
                max_m = safe_float(marks['maxmarks'])
                obt_m = None if is_absent else safe_float(marks['obt'])
                pct_m = None if is_absent else safe_float(marks['pct']) # safe_float now handles '%'

                cursor.execute(
                    """INSERT INTO marks (report_id, subject_id, coursework_marks, term_exam_marks,
                                       max_marks, obtained_marks, percentage, grade, is_absent, absence_type)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (report_id, subject_id, cw_marks, te_marks, max_m, obt_m, pct_m, marks['grade'], is_absent, absence_type)
                )
                marks_saved_count += 1

            # --- Log Marks Action (Summary) ---
            if marks_saved_count > 0:
                 self._log_audit(cursor, current_user_id, "SAVE_MARKS", table_name="marks", record_id=report_id, description=f"Saved/Updated {marks_saved_count} marks entries for Report ID:{report_id}")
            # ----------------------------------

            conn.commit()
            return True, "Report card saved successfully!"

        except Exception as e:
            if conn: conn.rollback()
            error_message = f"Error saving report card: {e}"
            print(error_message) # Print detailed error to console
            return False, error_message # Return detailed error
        finally:
            if conn: conn.close()
    # --- Helper: Get or Create Student ---
    def get_or_create_student(self, gr_no, student_name, father_name, class_sec, session, performed_by_user_id): # Added performed_by_user_id
        """
        Finds a student by GR No. If not found, creates a new one. Logs action.
        Updates existing student's class/session if different.
        Returns the student_id.
        """
        conn = None
        try:
            conn = self.connect()
            cursor = conn.cursor()

            cursor.execute("SELECT student_id, student_name, father_name, current_class_sec, current_session FROM students WHERE gr_no = ?", (gr_no,))
            student = cursor.fetchone()

            log_action = None
            log_desc = None
            student_id = None

            if student:
                student_id = student['student_id']
                # Check if relevant details changed for update log
                if (student['student_name'] != student_name or
                    student['father_name'] != father_name or
                    student['current_class_sec'] != class_sec or
                    student['current_session'] != session):
                    cursor.execute(
                        "UPDATE students SET student_name = ?, father_name = ?, current_class_sec = ?, current_session = ?, status = 'Active', updated_at = CURRENT_TIMESTAMP WHERE student_id = ?",
                        (student_name, father_name, class_sec, session, student_id)
                    )
                    log_action = "UPDATE_STUDENT"
                    log_desc = f"Updated student GR:{gr_no} details (Name/Father/Class/Session)"

            else:
                cursor.execute(
                    """INSERT INTO students (gr_no, student_name, father_name, current_class_sec, current_session, joining_date, status)
                       VALUES (?, ?, ?, ?, ?, DATE('now'), 'Active')""",
                    (gr_no, student_name, father_name, class_sec, session)
                )
                student_id = cursor.lastrowid
                log_action = "ADD_STUDENT"
                log_desc = f"Added student: {student_name}, GR:{gr_no}"

            # --- Log Audit (if action occurred) ---
            if log_action:
                self._log_audit(cursor, performed_by_user_id, log_action, table_name="students", record_id=student_id, description=log_desc)
            # ------------------------------------

            conn.commit()
            return student_id
        except Exception as e:
            if conn: conn.rollback()
            print(f"Error in get_or_create_student: {e}")
            return None
        finally:
            if conn: conn.close()

    # --- Helper: Get Subject ID ---
    def get_subject_id(self, subject_name):
        conn = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT subject_id FROM subjects WHERE subject_name = ?", (subject_name,))
            result = cursor.fetchone()
            return result['subject_id'] if result else None
        except Exception as e:
            print(f"Error getting subject ID for '{subject_name}': {e}")
            return None
        finally:
            if conn: conn.close()

    # --- Subject Management Methods (unchanged from previous version) ---
    def get_subjects_with_details(self):
        conn = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT subject_id, subject_name, type FROM subjects ORDER BY subject_name")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting subjects: {e}")
            return []
        finally:
            if conn: conn.close()

    def add_subject(self, subject_name, subject_type, performed_by_user_id): # Added performed_by_user_id
        """Adds a new subject to the database."""
        conn = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO subjects (subject_name, type) VALUES (?, ?)",
                (subject_name, subject_type)
            )
            new_subject_id = cursor.lastrowid

            # --- Log Audit ---
            self._log_audit(cursor, performed_by_user_id, "ADD_SUBJECT", table_name="subjects", record_id=new_subject_id, description=f"Added subject: {subject_name} ({subject_type})")
            # -----------------

            conn.commit()
            return True, f"Subject '{subject_name}' added."
        except sqlite3.IntegrityError:
             return False, f"Subject '{subject_name}' already exists."
        except Exception as e:
            if conn: conn.rollback()
            return False, f"Error adding subject: {e}"
        finally:
            if conn: conn.close()

    def remove_subject(self, subject_id, performed_by_user_id): # Added performed_by_user_id
        """Removes a subject by its ID."""
        conn = None
        try:
            conn = self.connect()
            cursor = conn.cursor()

            # Get name before deleting for logging
            cursor.execute("SELECT subject_name FROM subjects WHERE subject_id = ?", (subject_id,))
            subject_to_delete = cursor.fetchone()
            name_for_log = subject_to_delete['subject_name'] if subject_to_delete else f"ID:{subject_id}"

            cursor.execute("DELETE FROM subjects WHERE subject_id = ?", (subject_id,))
            rows_affected = cursor.rowcount

            if rows_affected > 0:
                 # --- Log Audit ---
                 self._log_audit(cursor, performed_by_user_id, "DELETE_SUBJECT", table_name="subjects", record_id=subject_id, description=f"Deleted subject: {name_for_log}")
                 # -----------------
                 conn.commit()
                 return True, "Subject deleted."
            else:
                 conn.rollback()
                 return False, "Subject not found or already deleted."
        except Exception as e:
            if conn: conn.rollback()
            return False, f"Error deleting subject: {e}"
        finally:
            if conn: conn.close()
