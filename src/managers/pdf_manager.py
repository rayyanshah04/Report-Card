"""
PDF Manager - Handles PDF generation from HTML templates
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class PDFManager:
    """Manages PDF generation using Jinja2 templates and WeasyPrint"""

    PROJECT_ROOT = Path(__file__).parent.parent.parent
    TEMPLATES_DIR = PROJECT_ROOT / "templates"
    OUTPUT_DIR = PROJECT_ROOT / "output"

    @staticmethod
    def ensure_output_dir():
        """Create output directory if it doesn't exist"""
        PDFManager.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def render_template(data):
        """
        Render HTML template with student data using Jinja2

        Args:
            data (dict): Dictionary containing all student/marks data

        Returns:
            str: Rendered HTML content
        """
        try:
            def get_font_size(text):
                """
                Returns font size based on text length
                Normal: 20px (for short names)
                Small: 14px (for long names)
                """
                if len(text) <= 19:
                    return 20
                else:
                    return 14
            # Read CSS file and fix font paths
            css_path = PDFManager.TEMPLATES_DIR / 'styles.css'
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()

            # Replace relative font paths with absolute paths for WeasyPrint
            templates_dir_str = str(PDFManager.TEMPLATES_DIR).replace('\\', '/')
            css_content = css_content.replace("url('Revue.ttf')", f"url('file:///{templates_dir_str}/Revue.ttf')")
            css_content = css_content.replace("url('calibri-regular.ttf')", f"url('file:///{templates_dir_str}/calibri-regular.ttf')")
            css_content = css_content.replace("url('calibri-italic.ttf')", f"url('file:///{templates_dir_str}/calibri-italic.ttf')")

            # Setup Jinja2
            env = Environment(loader=FileSystemLoader(str(PDFManager.TEMPLATES_DIR)))
            template = env.get_template('report_card.html')

            # Pass CSS content and template directory to template
            data['css_content'] = css_content
            data['template_dir'] = templates_dir_str

            data['student_name_font_size'] = get_font_size(data.get('student_name', ''))
            data['father_name_font_size'] = get_font_size(data.get('father_name', ''))

            # Render with data
            html_content = template.render(**data)
            return html_content

        except Exception as e:
            raise Exception(f"Error rendering template: {e}")

    @staticmethod
    def generate_pdf(filename, data):
        """
        Generate PDF from HTML template

        Args:
            filename (str): Name for PDF file (e.g., "StudentName_ReportCard_2025-2026")
            data (dict): Dictionary with all student/marks data

        Returns:
            tuple: (success: bool, message: str, pdf_path: str or None)
        """
        try:
            from weasyprint import HTML

            PDFManager.ensure_output_dir()

            # Render HTML
            html_content = PDFManager.render_template(data)

            # Create temporary HTML file
            temp_html = PDFManager.OUTPUT_DIR / "temp_report.html"
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Create PDF filename
            pdf_filename = f"{filename}.pdf"
            pdf_path = PDFManager.OUTPUT_DIR / pdf_filename

            # Convert HTML to PDF using WeasyPrint
            HTML(str(temp_html)).write_pdf(str(pdf_path))

            # Clean up temp file
            temp_html.unlink()

            return True, f"PDF created successfully!", str(pdf_path)

        except ImportError:
            return False, "WeasyPrint not installed. Run: pip install weasyprint", None
        except Exception as e:
            return False, f"Error generating PDF: {str(e)}", None
