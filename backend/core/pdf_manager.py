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
                Returns font size based on text length to prevent line wrapping
                Scales down font size progressively for longer names
                """
                text_len = len(text)
                
                # Short names: full size
                if text_len <= 15:
                    return 20
                # Medium names: slightly reduced
                elif text_len <= 20:
                    return 18
                # Long names: more reduced
                elif text_len <= 25:
                    return 16
                # Very long names: significantly reduced
                elif text_len <= 30:
                    return 14
                # Extremely long names: minimum readable size
                else:
                    return 12

            css_path = PDFManager.TEMPLATES_DIR / 'styles.css'
            with open(css_path, 'r', encoding='utf-8') as handle:
                css_content = handle.read()

            templates_dir_str = str(PDFManager.TEMPLATES_DIR).replace('\\', '/')
            css_content = css_content.replace("url('Revue.ttf')", f"url('file:///{templates_dir_str}/Revue.ttf')")
            css_content = css_content.replace("url('calibri-regular.ttf')", f"url('file:///{templates_dir_str}/calibri-regular.ttf')")
            css_content = css_content.replace("url('calibri-italic.ttf')", f"url('file:///{templates_dir_str}/calibri-italic.ttf')")

            env = Environment(loader=FileSystemLoader(str(PDFManager.TEMPLATES_DIR)))
            template = env.get_template('report_card.html')

            data['css_content'] = css_content
            data['template_dir'] = templates_dir_str

            data['student_name_font_size'] = get_font_size(data.get('student_name', ''))
            data['father_name_font_size'] = get_font_size(data.get('father_name', ''))

            html_content = template.render(**data)
            return html_content

        except Exception as exc:  # pragma: no cover
            raise Exception(f"Error rendering template: {exc}") from exc

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
            html_content = PDFManager.render_template(data)

            temp_html = PDFManager.OUTPUT_DIR / "temp_report.html"
            with open(temp_html, 'w', encoding='utf-8') as handle:
                handle.write(html_content)

            pdf_filename = f"{filename}.pdf"
            pdf_path = PDFManager.OUTPUT_DIR / pdf_filename

            HTML(str(temp_html)).write_pdf(str(pdf_path))
            temp_html.unlink()

            return True, "PDF created successfully!", str(pdf_path)

        except ImportError:
            return False, "WeasyPrint not installed. Run: pip install weasyprint", None
        except Exception as exc:  # pragma: no cover
            return False, f"Error generating PDF: {exc}", None
