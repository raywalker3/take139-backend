"""IMAGO PDF report generator.

Renders the IMAGO report from a scored ImagoResult into a PDF via WeasyPrint.
"""
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from imago_report_data import get_report_data
from imago_scoring import ImagoResult


_HERE = os.path.dirname(os.path.abspath(__file__))
_TEMPLATE_DIR = os.path.join(_HERE, "templates")

def _ordinal(n):
    """Return the ordinal suffix for an integer (1st, 2nd, 3rd, 4th, ...)."""
    n = int(n)
    if 10 <= (n % 100) <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), autoescape=False)
_env.filters["ordinal"] = _ordinal
_template = _env.get_template("imago_report.html")


def generate_imago_pdf(result: ImagoResult, name: str, pair_code: str) -> bytes:
    """Generate an IMAGO PDF report as bytes.

    Args:
        result: A scored ImagoResult.
        name: The respondent's name.
        pair_code: The respondent's pair code.

    Returns:
        PDF document as bytes.
    """
    data = get_report_data(result, name=name, pair_code=pair_code)
    html_str = _template.render(**data)
    pdf_bytes = HTML(string=html_str).write_pdf()
    return pdf_bytes


def generate_imago_html(result: ImagoResult, name: str, pair_code: str) -> str:
    """Generate the HTML for the IMAGO report (useful for debugging/preview)."""
    data = get_report_data(result, name=name, pair_code=pair_code)
    return _template.render(**data)


if __name__ == "__main__":
    # End-to-end test: generate a PDF from a realistic profile
    from imago_items import ITEMS
    from imago_scoring import score_imago

    # A Shepherd-like profile
    answers = {}
    for item in ITEMS:
        code = item["aspect_code"]
        direction = item["direction"]
        if code in ("G1", "G2"):
            answers[item["item_id"]] = 5 if direction == "FORWARD" else 1
        elif code in ("O1", "O2"):
            answers[item["item_id"]] = 1 if direction == "FORWARD" else 5
        elif code == "A1":
            answers[item["item_id"]] = 4 if direction == "FORWARD" else 2
        else:
            answers[item["item_id"]] = 3

    result = score_imago(answers, ITEMS)
    pdf = generate_imago_pdf(result, name="Test Friend", pair_code="GRACE-1234")
    out_path = "/tmp/imago_test.pdf"
    with open(out_path, "wb") as f:
        f.write(pdf)
    print(f"Wrote {len(pdf)} bytes to {out_path}")
    print(f"Profile: {result.letter_type} · The {result.soul_shape} · The {result.archetype}")
