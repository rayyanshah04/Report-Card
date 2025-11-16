"""
Database operations manager
"""
import sqlite3


class DatabaseManager:
    """Handles all database operations"""
    
    def __init__(self, db_path="report_system.db"):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    # Student operations
    def get_all_students(self):
        """Get all students"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT gr_no, student_name, father_name, 
                   current_class_sec, current_session, status, contact_number_resident, address
            FROM students
            ORDER BY gr_no
        """)
        students = cursor.fetchall()
        conn.close()
        return students
    
    def get_student_by_gr_no(self, gr_no):
        """Get student details by GR number"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT student_id, gr_no, student_name, father_name, current_class_sec, current_session, 
                   status, joining_date, left_date, left_reason, date_of_birth, 
                   contact_number_resident, contact_number_neighbour, contact_number_relative,
                   contact_number_other1, contact_number_other2, contact_number_other3,
                   contact_number_other4, address, created_at, updated_at
            FROM students WHERE gr_no = ?
        """, (gr_no,))
        student = cursor.fetchone()
        conn.close()
        return student
    
    def delete_student(self, gr_no):
        """Delete student by GR number"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE gr_no = ?", (gr_no,))
        conn.commit()
        conn.close()
    
    def get_student_stats(self):
        """Get student statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM students")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM students WHERE status = 'Active'")
        active = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM students WHERE status != 'Active'")
        inactive = cursor.fetchone()[0]
        
        conn.close()
        return total, active, inactive
    
    def get_unique_classes(self):
        """Get list of unique classes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT current_class_sec FROM students WHERE current_class_sec IS NOT NULL ORDER BY current_class_sec")
        classes = cursor.fetchall()
        conn.close()
        return [cls[0] for cls in classes if cls[0]]
    
    def import_students_from_excel(self, records):
        """Import multiple students from Excel data
        
        Args:
            records: List of tuples (gr_no, student_name, current_class_sec, address, 
                                    contact_resident, contact_neighbour, contact_relative,
                                    contact_other1-4, dob, joining_date)
        
        Returns:
            tuple: (success_count, errors_list)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        success_count = 0
        errors = []
        
        for idx, record in enumerate(records):
            try:
                cursor.execute("""
                    INSERT INTO students (
                        gr_no, student_name, current_class_sec, address,
                        contact_number_resident, contact_number_neighbour, contact_number_relative,
                        contact_number_other1, contact_number_other2, contact_number_other3, 
                        contact_number_other4, date_of_birth, joining_date
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, record)
                success_count += 1
            except sqlite3.IntegrityError:
                errors.append(f"Row {idx + 2}: G.R No {record[0]} already exists")
            except Exception as e:
                errors.append(f"Row {idx + 2}: {str(e)}")
        
        conn.commit()
        conn.close()
        return success_count, errors
    
    # Subject operations
    def load_subjects_from_db(self):
        """Load all subjects"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT subject_name, type FROM subjects ORDER BY subject_name")
        subjects = cursor.fetchall()
        conn.close()
        return subjects
