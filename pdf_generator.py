"""PDF generation using Jinja2 + WeasyPrint."""
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


def render_report_html(data: dict) -> str:
    """Render the report template to HTML."""
    template = env.get_template("report.html")
    return template.render(**data)


def render_email_html(data: dict) -> str:
    """Render the email template to HTML."""
    template = env.get_template("email.html")
    return template.render(**data)


def generate_pdf(html_content: str) -> bytes:
    """Convert HTML string to PDF bytes."""
    return HTML(string=html_content).write_pdf()


def generate_report_pdf(data: dict) -> bytes:
    """One-shot: render report HTML and convert to PDF bytes."""
    html = render_report_html(data)
    return generate_pdf(html)
