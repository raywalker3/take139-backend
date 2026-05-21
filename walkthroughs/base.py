"""Shared infrastructure for all Walkthrough PDFs.

Provides:
    PALETTE constants (warm paper + Fraunces + burnt sienna design system)
    ensure_fonts() — downloads & registers Fraunces + Inter on first use
    make_styles() — paragraph style sheet for headings, body, callouts
    page setup helpers — backgrounds, headers, footers
    common flowables — journal lines, callouts, dividers, question cards
"""
import io
import os
import re
import urllib.request
from pathlib import Path
from typing import List, Optional

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph,
    Spacer, KeepTogether, HRFlowable, Table, TableStyle, NextPageTemplate,
)

# ────────────────────────────────────────────────────────────────────────
# Palette (locked from Take 139 design system)
# ────────────────────────────────────────────────────────────────────────
PAPER = colors.HexColor("#f5f1e8")
INK = colors.HexColor("#1d1d1b")
ACCENT = colors.HexColor("#8a4a2c")
ACCENT_HER = colors.HexColor("#4f6b5e")    # used in couples PDFs for the second partner
MUTED = colors.HexColor("#6b6862")
RULE = colors.HexColor("#cfc6b4")
HIGHLIGHT_BG = colors.HexColor("#ece4d3")
SUCCESS = colors.HexColor("#436b32")
ERROR = colors.HexColor("#a04030")

# ────────────────────────────────────────────────────────────────────────
# Page geometry
# ────────────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = letter
MARGIN_L = 0.95 * inch
MARGIN_R = 0.95 * inch
MARGIN_T = 0.95 * inch
MARGIN_B = 0.95 * inch

# ────────────────────────────────────────────────────────────────────────
# Fonts — Fraunces (display/headings) + Inter (body)
# Downloaded once, cached in /tmp.
# ────────────────────────────────────────────────────────────────────────
FONT_DIR = Path("/tmp/take139_walkthrough_fonts")
# NOTE: do not mkdir at import time — defer to ensure_fonts() so a /tmp
# permission issue can never prevent the FastAPI app from booting.

GOOGLE_CSS_URL = (
    "https://fonts.googleapis.com/css2"
    "?family=Fraunces:ital,wght@0,400;0,600;1,400"
    "&family=Inter:ital,wght@0,400;0,500;0,600;1,400"
    "&display=swap"
)

FONT_KEYS = {
    # (family, weight, italic) -> filename
    ("Fraunces", 400, False): "Fraunces-Regular.ttf",
    ("Fraunces", 400, True):  "Fraunces-Italic.ttf",
    ("Fraunces", 600, False): "Fraunces-SemiBold.ttf",
    ("Inter", 400, False):    "Inter-Regular.ttf",
    ("Inter", 400, True):     "Inter-Italic.ttf",
    ("Inter", 500, False):    "Inter-Medium.ttf",
    ("Inter", 600, False):    "Inter-SemiBold.ttf",
}

_FONTS_REGISTERED = False


def _resolve_font_urls():
    req = urllib.request.Request(GOOGLE_CSS_URL, headers={"User-Agent": "Wget/1.20"})
    css = urllib.request.urlopen(req).read().decode("utf-8")
    blocks = re.split(r"@font-face\s*\{", css)
    urls = {}
    for block in blocks[1:]:
        f = re.search(r"font-family:\s*'([^']+)'", block)
        w = re.search(r"font-weight:\s*(\d+)", block)
        s = re.search(r"font-style:\s*(italic|normal)", block)
        u = re.search(r"url\(([^)]+)\)", block)
        if not (f and w and u):
            continue
        key = (f.group(1), int(w.group(1)), (s.group(1) == "italic") if s else False)
        if key in FONT_KEYS:
            urls[key] = u.group(1)
    return urls


def ensure_fonts():
    """Idempotent — downloads + registers fonts on first call, no-op after."""
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return

    FONT_DIR.mkdir(parents=True, exist_ok=True)
    needed = [(k, FONT_DIR / fname) for k, fname in FONT_KEYS.items()
              if not (FONT_DIR / fname).exists() or (FONT_DIR / fname).stat().st_size < 10000]
    if needed:
        urls = _resolve_font_urls()
        for key, dest in needed:
            url = urls.get(key)
            if not url:
                raise RuntimeError(f"Could not resolve font URL for {key}")
            req = urllib.request.Request(url, headers={"User-Agent": "Wget/1.20"})
            with urllib.request.urlopen(req) as r:
                dest.write_bytes(r.read())

    pdfmetrics.registerFont(TTFont("Fraunces", str(FONT_DIR / "Fraunces-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Fraunces-Italic", str(FONT_DIR / "Fraunces-Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Fraunces-SemiBold", str(FONT_DIR / "Fraunces-SemiBold.ttf")))
    pdfmetrics.registerFont(TTFont("Inter", str(FONT_DIR / "Inter-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Inter-Italic", str(FONT_DIR / "Inter-Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Inter-Medium", str(FONT_DIR / "Inter-Medium.ttf")))
    pdfmetrics.registerFont(TTFont("Inter-SemiBold", str(FONT_DIR / "Inter-SemiBold.ttf")))
    _FONTS_REGISTERED = True


# ────────────────────────────────────────────────────────────────────────
# Style sheet — shared across all walkthroughs
# ────────────────────────────────────────────────────────────────────────
def make_styles():
    S = {}

    # Cover
    S["CoverEyebrow"] = ParagraphStyle(
        "CoverEyebrow", fontName="Inter-Medium", fontSize=10, leading=14,
        textColor=ACCENT, alignment=TA_CENTER, spaceAfter=14)
    S["CoverTitle"] = ParagraphStyle(
        "CoverTitle", fontName="Fraunces-SemiBold", fontSize=42, leading=50,
        textColor=INK, alignment=TA_CENTER, spaceAfter=18)
    S["CoverSub"] = ParagraphStyle(
        "CoverSub", fontName="Fraunces-Italic", fontSize=17, leading=26,
        textColor=INK, alignment=TA_CENTER, spaceAfter=22)
    S["CoverNames"] = ParagraphStyle(
        "CoverNames", fontName="Fraunces-SemiBold", fontSize=22, leading=30,
        textColor=INK, alignment=TA_CENTER, spaceAfter=14)
    S["CoverProfileLabel"] = ParagraphStyle(
        "CoverProfileLabel", fontName="Inter-Medium", fontSize=9, leading=14,
        textColor=ACCENT, alignment=TA_CENTER, spaceAfter=4)
    S["CoverProfileVal"] = ParagraphStyle(
        "CoverProfileVal", fontName="Fraunces-SemiBold", fontSize=14, leading=20,
        textColor=INK, alignment=TA_CENTER, spaceAfter=4)
    S["CoverProfileSub"] = ParagraphStyle(
        "CoverProfileSub", fontName="Inter", fontSize=10, leading=15,
        textColor=MUTED, alignment=TA_CENTER, spaceAfter=22)

    # Section headers
    S["SectionEyebrow"] = ParagraphStyle(
        "SectionEyebrow", fontName="Inter-Medium", fontSize=9, leading=14,
        textColor=ACCENT, alignment=TA_LEFT, spaceAfter=10)
    S["SectionTitle"] = ParagraphStyle(
        "SectionTitle", fontName="Fraunces-SemiBold", fontSize=28, leading=34,
        textColor=INK, alignment=TA_LEFT, spaceAfter=12)
    S["SectionSub"] = ParagraphStyle(
        "SectionSub", fontName="Fraunces-Italic", fontSize=14, leading=22,
        textColor=INK, alignment=TA_LEFT, spaceAfter=18)
    S["H3"] = ParagraphStyle(
        "H3", fontName="Inter-SemiBold", fontSize=11, leading=16,
        textColor=ACCENT, alignment=TA_LEFT, spaceBefore=10, spaceAfter=6)
    S["H3Her"] = ParagraphStyle(
        "H3Her", fontName="Inter-SemiBold", fontSize=11, leading=16,
        textColor=ACCENT_HER, alignment=TA_LEFT, spaceBefore=10, spaceAfter=6)

    # Body
    S["BodyJ"] = ParagraphStyle(
        "BodyJ", fontName="Inter", fontSize=11, leading=18,
        textColor=INK, alignment=TA_JUSTIFY, spaceAfter=10)
    S["BlockQuote"] = ParagraphStyle(
        "BlockQuote", fontName="Fraunces-Italic", fontSize=12.5, leading=20,
        textColor=INK, alignment=TA_LEFT, leftIndent=24, rightIndent=18,
        spaceBefore=8, spaceAfter=12)
    S["Prompt"] = ParagraphStyle(
        "Prompt", fontName="Fraunces-Italic", fontSize=12, leading=20,
        textColor=INK, alignment=TA_LEFT, spaceBefore=6, spaceAfter=4)

    # Couple-specific
    S["CommitLabel"] = ParagraphStyle(
        "CommitLabel", fontName="Inter-SemiBold", fontSize=9, leading=13,
        textColor=ACCENT, alignment=TA_LEFT, spaceBefore=2, spaceAfter=4)
    S["CommitLabelHer"] = ParagraphStyle(
        "CommitLabelHer", fontName="Inter-SemiBold", fontSize=9, leading=13,
        textColor=ACCENT_HER, alignment=TA_LEFT, spaceBefore=2, spaceAfter=4)
    S["CommitBody"] = ParagraphStyle(
        "CommitBody", fontName="Fraunces-Italic", fontSize=11.5, leading=18,
        textColor=INK, alignment=TA_LEFT, spaceAfter=8)
    S["ProfileCardName"] = ParagraphStyle(
        "ProfileCardName", fontName="Fraunces-SemiBold", fontSize=16, leading=22,
        textColor=INK, alignment=TA_LEFT, spaceAfter=10)
    S["ProfileCardLabel"] = ParagraphStyle(
        "ProfileCardLabel", fontName="Inter-Medium", fontSize=8.5, leading=12,
        textColor=MUTED, alignment=TA_LEFT, spaceAfter=2)
    S["ProfileCardVal"] = ParagraphStyle(
        "ProfileCardVal", fontName="Fraunces", fontSize=12, leading=16,
        textColor=INK, alignment=TA_LEFT, spaceAfter=8)
    return S


# ────────────────────────────────────────────────────────────────────────
# Page backgrounds & decorations
# ────────────────────────────────────────────────────────────────────────
def draw_content_bg(canvas, doc, brand_text="Take 139  ·  A Counselor's Walkthrough"):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.4)
    canvas.line(MARGIN_L, 0.6 * inch, PAGE_W - MARGIN_R, 0.6 * inch)
    canvas.setFont("Inter", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN_L, 0.4 * inch, brand_text)
    canvas.drawRightString(PAGE_W - MARGIN_R, 0.4 * inch, f"{doc.page}")
    canvas.restoreState()


def draw_cover_bg(canvas, doc, top_label="TAKE 139  ·  COUNSELOR'S WALKTHROUGH", right_label=""):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(0.6)
    canvas.line(MARGIN_L, PAGE_H - 0.7 * inch, PAGE_W - MARGIN_R, PAGE_H - 0.7 * inch)
    canvas.line(MARGIN_L, 0.7 * inch, PAGE_W - MARGIN_R, 0.7 * inch)
    canvas.setFont("Inter-Medium", 9)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN_L, 0.45 * inch, top_label)
    if right_label:
        canvas.drawRightString(PAGE_W - MARGIN_R, 0.45 * inch, right_label)
    canvas.restoreState()


# ────────────────────────────────────────────────────────────────────────
# Common flowable helpers
# ────────────────────────────────────────────────────────────────────────
def section_header(story, S, eyebrow, title, sub=None):
    story.append(Paragraph(eyebrow, S["SectionEyebrow"]))
    story.append(Paragraph(title, S["SectionTitle"]))
    if sub:
        story.append(Paragraph(sub, S["SectionSub"]))
    story.append(HRFlowable(width="100%", thickness=0.4, color=RULE,
                            spaceBefore=4, spaceAfter=16))


def journal_lines(story, n=4):
    story.append(Spacer(1, 12))
    for _ in range(n):
        story.append(HRFlowable(
            width="100%", thickness=0.5, color=RULE,
            spaceBefore=14, spaceAfter=2,
        ))
    story.append(Spacer(1, 10))


def divider(story):
    story.append(Spacer(1, 10))
    story.append(HRFlowable(
        width="40%", thickness=0.6, color=ACCENT,
        hAlign="LEFT", spaceBefore=4, spaceAfter=10,
    ))


# ────────────────────────────────────────────────────────────────────────
# Doc construction helper — every walkthrough builds with this
# ────────────────────────────────────────────────────────────────────────
def make_doc(brand_text, cover_top_label, cover_right_label, title, output=None):
    """Build a BaseDocTemplate with Cover + Content page templates.

    If output is None, returns (doc, buffer) writing to an in-memory buffer.
    Caller does: doc.build(story), then return buffer.getvalue()
    """
    if output is None:
        output = io.BytesIO()

    doc = BaseDocTemplate(
        output, pagesize=letter,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T, bottomMargin=MARGIN_B,
        title=title, author="Perplexity Computer",
    )
    cover_frame = Frame(
        MARGIN_L, MARGIN_B, PAGE_W - MARGIN_L - MARGIN_R,
        PAGE_H - MARGIN_T - MARGIN_B, id="cover",
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    content_frame = Frame(
        MARGIN_L, MARGIN_B, PAGE_W - MARGIN_L - MARGIN_R,
        PAGE_H - MARGIN_T - MARGIN_B, id="content",
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )

    def cover_bg(canvas, doc_):
        draw_cover_bg(canvas, doc_, top_label=cover_top_label, right_label=cover_right_label)

    def content_bg(canvas, doc_):
        draw_content_bg(canvas, doc_, brand_text=brand_text)

    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[cover_frame], onPage=cover_bg),
        PageTemplate(id="Content", frames=[content_frame], onPage=content_bg),
    ])
    return doc, output


def finalize_buffer(buffer) -> bytes:
    """Extract PDF bytes from a BytesIO buffer."""
    if hasattr(buffer, "getvalue"):
        return buffer.getvalue()
    return buffer  # already bytes (file output mode)
