"""IMAGO Content Loader.

Parses the six IMAGO content markdown files into structured Python dicts
at import time. All content is ready to plug directly into a Jinja2 PDF
template; body text is returned as lists of paragraph strings, which
templates consume naturally with ``{% for p in paragraphs %}``.

Data structures provided (module-level):
    SOUL_SHAPES          – Dict[str, dict]
    DOMAINS              – Dict[str, Dict[str, dict]]
    ASPECTS              – Dict[str, dict]
    ARCHETYPES           – Dict[str, dict]
    REFLECTION_QUESTIONS – Dict[str, List[dict]]
"""
from __future__ import annotations

import logging
import re
import textwrap
from pathlib import Path
from typing import Dict, List, Optional

log = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────

_CONTENT_DIR = Path(__file__).parent / "imago_content"

_FILES = {
    "soul_shapes":   _CONTENT_DIR / "soul-shapes.md",
    "domains":       _CONTENT_DIR / "domain-passages.md",
    "aspects":       _CONTENT_DIR / "aspect-passages.md",
    "archetypes_15": _CONTENT_DIR / "archetypes-1-5.md",
    "archetypes_610": _CONTENT_DIR / "archetypes-6-10.md",
    "reflections":   _CONTENT_DIR / "reflection-questions.md",
}


# ─────────────────────────────────────────────────────────────────────────────
# Low-level text utilities
# ─────────────────────────────────────────────────────────────────────────────

def _read(path: Path) -> str:
    """Read a file, raising a clear error if it is missing."""
    if not path.exists():
        raise FileNotFoundError(f"IMAGO content file not found: {path}")
    return path.read_text(encoding="utf-8")


def _strip_blockquote_markers(text: str) -> str:
    """Remove leading '> ' from every line of a blockquote block."""
    lines = text.splitlines()
    stripped = []
    for line in lines:
        if line.startswith("> "):
            stripped.append(line[2:])
        elif line.startswith(">"):
            stripped.append(line[1:])
        else:
            stripped.append(line)
    return "\n".join(stripped)


def _to_paragraphs(text: str) -> List[str]:
    """Split body text into a list of non-empty paragraph strings.

    - Strips blockquote markers.
    - Preserves <i>...</i> inline tags.
    - Trims leading/trailing whitespace from each paragraph.
    - Drops separator lines (``---``) and empty/whitespace-only entries.
    """
    text = _strip_blockquote_markers(text)
    # Split on blank lines (one or more)
    raw_paras = re.split(r"\n{2,}", text)
    result: List[str] = []
    for para in raw_paras:
        para = para.strip()
        if not para:
            continue
        if re.fullmatch(r"-{3,}", para):
            continue
        # Collapse internal single newlines to spaces (handles wrapped markdown)
        para = re.sub(r"\n", " ", para)
        para = para.strip()
        if para:
            result.append(para)
    return result


def _extract_section(text: str, header: str, next_headers: Optional[List[str]] = None) -> str:
    """Extract the body of a named ``### HEADER`` section.

    Args:
        text:          The full block of text to search within.
        header:        The exact header string (case-insensitive, without ``###``).
        next_headers:  List of subsequent headers that mark the end of this section.
                       If None, collect until end of text.

    Returns:
        Raw string body of the section (may be empty if not found).
    """
    pattern = re.compile(
        r"###\s+" + re.escape(header.strip()) + r"\s*\n",
        re.IGNORECASE,
    )
    m = pattern.search(text)
    if not m:
        return ""

    start = m.end()

    # Build a pattern that matches any of the terminating headers
    if next_headers:
        end_pat = re.compile(r"^(?:#{2,3})\s+", re.MULTILINE)
        m_end = end_pat.search(text, start)
        if m_end:
            return text[start:m_end.start()].strip()
    return text[start:].strip()


def _extract_between_headers(text: str, start_header: str) -> str:
    """Return the body text between ``start_header`` and the next ``###`` or ``##`` header."""
    pattern = re.compile(
        r"###\s+" + re.escape(start_header.strip()) + r"[^\n]*\n",
        re.IGNORECASE,
    )
    m = pattern.search(text)
    if not m:
        return ""
    start = m.end()
    end_pat = re.compile(r"^#{2,3}\s+", re.MULTILINE)
    m_end = end_pat.search(text, start)
    body = text[start: m_end.start() if m_end else len(text)]
    return body.strip()


def _extract_blockquote(text: str) -> str:
    """Extract the first contiguous blockquote block from ``text``."""
    lines = text.splitlines()
    in_block = False
    collected: List[str] = []
    for line in lines:
        if line.startswith(">"):
            in_block = True
            collected.append(line)
        elif in_block:
            # Blank line may continue a blockquote in some flavours; stop on
            # non-quote, non-blank line.
            if line.strip():
                break
            # allow a trailing blank line inside blockquote
            # (markdown tables inside blockquotes have blank separators)
        else:
            if collected:
                break
    return "\n".join(collected).strip()


def _parse_blockquote_sidebar(bq_text: str) -> dict:
    """Parse a blockquote into a dict of key/value pairs.

    Handles:
        > **Name**
        > Key: value
        > Key1: val1 · Key2: val2   (compound lines with ·)
        > | table | rows |
    Returns a dict where keys are lowercased field names.
    """
    raw = _strip_blockquote_markers(bq_text)
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    sidebar: dict = {}
    table_rows: List[List[str]] = []
    for line in lines:
        # Bold title → name
        m = re.match(r"^\*\*(.+?)\*\*\s*$", line)
        if m:
            sidebar["name"] = m.group(1).strip()
            continue
        # Table row → collect for "scores"
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            # Skip separator rows (---|---)
            if all(re.fullmatch(r"-+", c) for c in cells if c):
                continue
            if cells and cells[0]:  # non-empty
                table_rows.append(cells)
            continue
        # Compound lines like "Stability: high · Plasticity: high"
        # Split on " · " first, then parse each segment
        if " · " in line:
            segments = line.split(" · ")
            for seg in segments:
                seg = seg.strip()
                m2 = re.match(r"^(.+?):\s*(.+)$", seg)
                if m2:
                    key = m2.group(1).strip().lower().replace(" ", "_")
                    sidebar[key] = m2.group(2).strip()
            continue
        # Key: value lines
        m = re.match(r"^(.+?):\s*(.+)$", line)
        if m:
            key = m.group(1).strip().lower().replace(" ", "_")
            val = m.group(2).strip()
            sidebar[key] = val
            continue
        # Lines without colon may be continuations or stand-alone notes
        if line and "name" not in sidebar:
            sidebar["_raw"] = sidebar.get("_raw", "") + " " + line
    if table_rows:
        # Treat first column as domain name, second as description
        sidebar["scores"] = {row[0].strip("*"): row[1] for row in table_rows if len(row) >= 2}
    return sidebar


# ─────────────────────────────────────────────────────────────────────────────
# Parser 1 — Soul Shapes
# ─────────────────────────────────────────────────────────────────────────────

# Expected shape names
_SOUL_SHAPE_NAMES = ("Host", "Anchor", "Psalmist", "Watchman")


def _parse_soul_shapes(text: str) -> Dict[str, dict]:
    """Parse soul-shapes.md → dict keyed by shape name."""
    result: Dict[str, dict] = {}

    # Split on horizontal rules to get each soul shape block
    # Each block starts right after a "---" and before the next "---"
    # The file structure: preamble --- block --- block --- ... block ---
    blocks = re.split(r"^---\s*$", text, flags=re.MULTILINE)

    # blocks[0] = preamble; remaining blocks contain shape content
    shape_blocks = [b.strip() for b in blocks[1:] if b.strip()]

    for block in shape_blocks:
        # Check for closing paragraph (last block contains "These four…")
        if block.startswith("These four Soul Shapes"):
            continue

        # Extract name from blockquote: "> **The Foo**"
        bq_match = re.search(r"^> \*\*The (\w+)\*\*", block, re.MULTILINE)
        if not bq_match:
            log.warning("Soul shape block has no name: %s…", block[:80])
            continue
        name = bq_match.group(1)

        # Extract full blockquote
        bq_raw = _extract_blockquote(block)
        sidebar = _parse_blockquote_sidebar(bq_raw)

        # The narrative is everything AFTER the blockquote
        # Find where the blockquote ends
        bq_lines = bq_raw.splitlines()
        # Find the line after the last blockquote line in the block
        block_lines = block.splitlines()
        last_bq_idx = -1
        for i, line in enumerate(block_lines):
            if line.startswith(">"):
                last_bq_idx = i
        narrative_text = "\n".join(block_lines[last_bq_idx + 1:]).strip()

        # Extract the italic tagline that often appears right after the blockquote
        tagline = ""
        tagline_match = re.match(r"(<i>[^<]+</i>)", narrative_text)
        if tagline_match:
            tagline = tagline_match.group(1)
            narrative_text = narrative_text[len(tagline):].strip()

        result[name] = {
            "name": name,
            "sidebar_meta": sidebar,
            "tagline": tagline,
            "narrative_paragraphs": _to_paragraphs(narrative_text),
        }

    # Validate
    for expected in _SOUL_SHAPE_NAMES:
        if expected not in result:
            log.warning("Soul shape '%s' was not parsed from file.", expected)

    return result


# ─────────────────────────────────────────────────────────────────────────────
# Parser 2 — Domain Passages
# ─────────────────────────────────────────────────────────────────────────────

_DOMAIN_CODES = {
    "Imagination": "I",
    "Mastery": "M",
    "Animation": "A",
    "Grace-bearing": "G",
    "Ortho-emotion": "O",
}

def _parse_domain_pole(block: str) -> dict:
    """Parse a HIGH or LOW domain pole block into a structured dict.

    Domain passages use **Bold Section Name** markers (not ### headers).
    Sections are:
        "What this wiring looks like"
        "The imago Dei connection"
        "The calling for your pole"
        "The shadow for your pole"
        "One gospel anchor"
        "What your partner will notice"
    """
    # Extract the sidebar blockquote
    bq_raw = _extract_blockquote(block)
    sidebar = _parse_blockquote_sidebar(bq_raw) if bq_raw else {}

    # Find where the blockquote ends in the raw block text
    # Look for the last line starting with '>'
    bq_end_pos = 0
    for m in re.finditer(r"^> ", block, re.MULTILINE):
        bq_end_pos = m.end()
    # Find end of that line
    newline_after_bq = block.find("\n", bq_end_pos)
    after_bq = block[newline_after_bq:].strip() if newline_after_bq >= 0 else block

    # Split on standalone **Bold** section headers (whole line = **Header**)
    section_splits = re.split(
        r"(?m)^\*\*([^*\n]+)\*\*\s*$",
        after_bq,
    )

    # section_splits: [intro_text, sec_name1, sec_body1, sec_name2, sec_body2, ...]
    intro_text = section_splits[0].strip()
    sections: Dict[str, str] = {}
    i = 1
    while i + 1 < len(section_splits):
        sec_name = section_splits[i].strip().lower()
        # Normalise to a simple identifier
        sec_key = re.sub(r"[^a-z0-9]+", "_", sec_name).strip("_")
        sec_body = section_splits[i + 1].strip()
        sections[sec_key] = sec_body
        i += 2

    return {
        "sidebar": sidebar,
        "opening_paragraphs": _to_paragraphs(intro_text),
        "what_this_looks_like": _to_paragraphs(sections.get("what_this_wiring_looks_like", "")),
        "imago_dei_connection": _to_paragraphs(sections.get("the_imago_dei_connection", "")),
        "calling": _to_paragraphs(sections.get("the_calling_for_your_pole", "")),
        "shadow": _to_paragraphs(sections.get("the_shadow_for_your_pole", "")),
        "gospel_anchor": _to_paragraphs(sections.get("one_gospel_anchor", "")),
        "partner_insight": _to_paragraphs(sections.get("what_your_partner_will_notice", "")),
        # Preserve all raw sections in case template needs something unlisted
        "_sections": sections,
    }


def _parse_domains(text: str) -> Dict[str, Dict[str, dict]]:
    """Parse domain-passages.md → nested dict by code and pole."""
    result: Dict[str, Dict[str, dict]] = {}

    # Split on top-level domain headers: "## I — Imagination"
    domain_blocks = re.split(r"^## ([A-Z]) — (.+)$", text, flags=re.MULTILINE)
    # domain_blocks[0] = preamble
    # Then: code, name, body, code, name, body, ...
    i = 1
    while i + 2 < len(domain_blocks):
        code = domain_blocks[i].strip()
        name = domain_blocks[i + 1].strip()
        body = domain_blocks[i + 2]
        i += 3

        # Split body into HIGH and LOW subsections
        pole_blocks = re.split(r"^### (HIGH|LOW) (.+)$", body, flags=re.MULTILINE)
        # pole_blocks[0] = anything before first pole (likely empty)
        poles: Dict[str, dict] = {}
        j = 1
        while j + 2 < len(pole_blocks):
            pole_label = pole_blocks[j].strip().lower()  # "high" or "low"
            # pole_blocks[j+1] is the domain name repetition; pole_blocks[j+2] is body
            pole_body = pole_blocks[j + 2]
            poles[pole_label] = _parse_domain_pole(pole_body)
            j += 3

        if not poles:
            log.warning("Domain '%s' (%s) has no pole blocks.", name, code)

        result[code] = poles

    # Validate
    for code in ["I", "M", "A", "G", "O"]:
        if code not in result:
            log.warning("Domain '%s' not found in domain-passages.md.", code)
        else:
            for pole in ["high", "low"]:
                if pole not in result[code]:
                    log.warning("Domain '%s' missing '%s' pole.", code, pole)

    return result


# ─────────────────────────────────────────────────────────────────────────────
# Parser 3 — Aspect Passages
# ─────────────────────────────────────────────────────────────────────────────

_ASPECT_CODES = {
    "Artistry": "I1",
    "Intellect": "I2",
    "Industriousness": "M1",
    "Orderliness": "M2",
    "Enthusiasm": "A1",
    "Assertiveness": "A2",
    "Compassion": "G1",
    "Courtesy": "G2",
    "Sensitivity": "O1",
    "Steadiness": "O2",
}


def _parse_aspects(text: str) -> Dict[str, dict]:
    """Parse aspect-passages.md → dict keyed by aspect code."""
    result: Dict[str, dict] = {}

    # Each aspect starts with: ### AspectName (Code)
    # e.g. "### Artistry (I1)"
    aspect_blocks = re.split(
        r"^### ([\w-]+(?:\s+[\w-]+)*)\s+\(([A-Z]\d)\)\s*$",
        text,
        flags=re.MULTILINE,
    )
    # aspect_blocks[0] = preamble + domain headings
    # Then: name, code, body, name, code, body, ...
    i = 1
    while i + 2 < len(aspect_blocks):
        aspect_name = aspect_blocks[i].strip()
        aspect_code = aspect_blocks[i + 1].strip()
        body = aspect_blocks[i + 2]
        i += 3

        # Sidebar blockquote
        bq_raw = _extract_blockquote(body)
        sidebar = _parse_blockquote_sidebar(bq_raw) if bq_raw else {}

        # After blockquote
        bq_end_idx = -1
        for idx, line in enumerate(body.splitlines()):
            if line.startswith(">"):
                bq_end_idx = idx
        body_lines = body.splitlines()
        after_bq = "\n".join(body_lines[bq_end_idx + 1:]).strip()

        # The body has three natural paragraphs:
        #   1. An intro/contextual paragraph (before "At the high end")
        #   2. "At the high end, ..." paragraph
        #   3. "At the low end, ..." paragraph
        #   4. "Pastoral note: ..." paragraph (starts with "Pastoral note:")
        #
        # Split on "At the high end" / "At the low end" / "Pastoral note:"
        parts = re.split(
            r"(?m)^(At the (?:high|low) end[,.]|Pastoral note:)",
            after_bq,
        )

        intro = parts[0].strip() if parts else ""
        high_para = ""
        low_para = ""
        pastoral = ""

        idx = 1
        while idx + 1 < len(parts):
            label = parts[idx].strip().lower()
            content = parts[idx + 1].strip()
            idx += 2
            if label.startswith("at the high end"):
                high_para = label + " " + content
            elif label.startswith("at the low end"):
                low_para = label + " " + content
            elif label.startswith("pastoral note"):
                pastoral = "Pastoral note: " + content

        result[aspect_code] = {
            "code": aspect_code,
            "name": aspect_name,
            "sidebar": sidebar,
            "opening_paragraphs": _to_paragraphs(intro),
            "high_paragraph": high_para.strip(),
            "low_paragraph": low_para.strip(),
            "pastoral_note": pastoral.strip(),
        }

    # Validate
    for name, code in _ASPECT_CODES.items():
        if code not in result:
            log.warning("Aspect '%s' (%s) not found in aspect-passages.md.", name, code)

    return result


# ─────────────────────────────────────────────────────────────────────────────
# Parser 4 — Archetypes (shared logic for both files)
# ─────────────────────────────────────────────────────────────────────────────

_ARCHETYPE_NAMES = (
    "Shepherd", "Mason", "Reformer", "Herald", "Faithful",
    "Maker", "Attuned", "Initiator", "Learner", "Servant",
)

# Section header → dict key mapping (canonical section names)
_ARCHETYPE_SECTION_MAP = {
    "opening":                       "opening",
    "what this looks like":          "what_this_looks_like",
    "behavioral markers":            "behavioral_markers",
    "what you bring to the body of christ": "what_you_bring",
    "scripture figures":             "scripture_figures",
    "the shadow":                    "shadow",
    "the gospel calling":            "gospel_calling",
    "the deepest call":              "deepest_call",
    "signature prayer":              "prayer",
    "gift to the body":              "gift_to_body",
}


def _parse_behavioral_markers(text: str) -> List[str]:
    """Extract bullet-list behavioral markers from a section body."""
    markers: List[str] = []
    for line in text.splitlines():
        line = line.strip()
        # Match "- marker text" or "* marker text"
        m = re.match(r"^[-*]\s+(.+)", line)
        if m:
            markers.append(m.group(1).strip())
    return markers if markers else _to_paragraphs(text)


def _parse_scripture_figures(text: str) -> List[dict]:
    """Parse scripture figures section into a list of {name, description}.

    Handles two formats:
    1. Archetypes 1-5: bold subsection names on their own lines
       ``**Figure Name (ref)**``
    2. Archetypes 6-10: flowing paragraphs where name is inline italic
       ``<i>Figure Name (ref)</i> are the... text``
    """
    figures: List[dict] = []
    text = text.strip()
    if not text:
        return figures

    # Format 1: paragraphs beginning with **Bold Name**
    # Split by paragraph and check for leading **…**
    paras = re.split(r"\n{2,}", text)

    # Detect which format: if any paragraph starts with **, use format 1
    has_bold_names = any(
        p.strip().startswith("**") for p in paras if p.strip()
    )

    if has_bold_names:
        for para in paras:
            para = para.strip()
            if not para:
                continue
            # Bold name may be followed by content on subsequent lines
            m = re.match(r"\*\*(.+?)\*\*\s*\n?(.*)", para, re.DOTALL)
            if m:
                fig_name = m.group(1).strip()
                # Remove parenthetical refs from name for display
                fig_name_clean = re.sub(r"\s*\([^)]*\)", "", fig_name).strip()
                desc = m.group(2).strip().replace("\n", " ")
                figures.append({"name": fig_name_clean, "ref": fig_name, "description": desc})
            else:
                # Treat whole para as a figure without extracted name
                figures.append({"name": "", "ref": "", "description": para.replace("\n", " ")})
    else:
        # Format 2: <i>Name (ref)</i> inline at paragraph start
        for para in paras:
            para = para.strip()
            if not para:
                continue
            m = re.match(r"<i>(.+?)</i>\s*(.*)", para, re.DOTALL)
            if m:
                fig_name = m.group(1).strip()
                fig_name_clean = re.sub(r"\s*\([^)]*\)", "", fig_name).strip()
                rest = m.group(2).strip().replace("\n", " ")
                # Combine figure name context into description
                desc = para.replace("\n", " ")
                figures.append({"name": fig_name_clean, "ref": fig_name, "description": desc})
            else:
                figures.append({"name": "", "ref": "", "description": para.replace("\n", " ")})

    return figures if figures else [{"name": "", "ref": "", "description": text}]


def _parse_single_archetype(name: str, block: str) -> dict:
    """Parse one archetype block into a structured dict."""
    # ── Sidebar ──────────────────────────────────────────────────────────────
    bq_raw = _extract_blockquote(block)
    sidebar = _parse_blockquote_sidebar(bq_raw) if bq_raw else {}

    # ── Section bodies ───────────────────────────────────────────────────────
    # Split by "### Header" markers
    section_splits = re.split(r"^### (.+)$", block, flags=re.MULTILINE)
    # section_splits[0] = content before first ### (sidebar etc.)
    # [1, 2] = header, body; [3, 4] = header, body; ...

    sections: Dict[str, str] = {}
    i = 1
    while i + 1 < len(section_splits):
        raw_header = section_splits[i].strip().lower()
        body = section_splits[i + 1]
        # Normalize header
        key = _ARCHETYPE_SECTION_MAP.get(raw_header, raw_header.replace(" ", "_"))
        sections[key] = body.strip()
        i += 2

    # ── Behavioral markers (list) ────────────────────────────────────────────
    bm_raw = sections.get("behavioral_markers", "")
    behavioral_markers = _parse_behavioral_markers(bm_raw)

    # ── Scripture figures (list of dicts) ────────────────────────────────────
    sf_raw = sections.get("scripture_figures", "")
    scripture_figures = _parse_scripture_figures(sf_raw)

    return {
        "name": name,
        "sidebar_scores": sidebar.get("scores", {}),
        "biblical_anchor": sidebar.get("biblical_anchor", ""),
        "opening": _to_paragraphs(sections.get("opening", "")),
        "what_this_looks_like": _to_paragraphs(sections.get("what_this_looks_like", "")),
        "behavioral_markers": behavioral_markers,
        "what_you_bring": _to_paragraphs(sections.get("what_you_bring", "")),
        "scripture_figures": scripture_figures,
        "shadow": _to_paragraphs(sections.get("shadow", "")),
        "gospel_calling": _to_paragraphs(sections.get("gospel_calling", "")),
        "deepest_call": _to_paragraphs(sections.get("deepest_call", "")),
        "prayer": _to_paragraphs(sections.get("prayer", "")),
        "gift_to_body": _to_paragraphs(sections.get("gift_to_body", "")),
    }


def _parse_archetypes(text: str) -> Dict[str, dict]:
    """Parse an archetypes markdown file and return dict keyed by archetype name."""
    result: Dict[str, dict] = {}

    # Split on top-level archetype headers: "## N. The ArchetypeName"
    archetype_blocks = re.split(
        r"^## \d+\.\s+The\s+(\w+)\s*$",
        text,
        flags=re.MULTILINE,
    )
    # archetype_blocks[0] = file preamble
    # Then: name, body, name, body, ...
    i = 1
    while i + 1 < len(archetype_blocks):
        name = archetype_blocks[i].strip()
        body = archetype_blocks[i + 1]
        i += 2
        try:
            result[name] = _parse_single_archetype(name, body)
        except Exception as exc:
            log.warning("Failed to parse archetype '%s': %s", name, exc, exc_info=True)

    return result


# ─────────────────────────────────────────────────────────────────────────────
# Parser 5 — Reflection Questions
# ─────────────────────────────────────────────────────────────────────────────

def _parse_reflection_questions(text: str) -> Dict[str, List[dict]]:
    """Parse reflection-questions.md → dict keyed by archetype name.

    Each value is a list of up to 5 dicts:
        {number, question_text, source_note}
    """
    result: Dict[str, List[dict]] = {}

    # Split on archetype headers: "## N. The ArchetypeName"
    archetype_blocks = re.split(
        r"^## \d+\.\s+The\s+(\w+)\s*$",
        text,
        flags=re.MULTILINE,
    )
    # archetype_blocks[0] = file preamble
    i = 1
    while i + 1 < len(archetype_blocks):
        name = archetype_blocks[i].strip()
        body = archetype_blocks[i + 1]
        i += 2

        questions: List[dict] = []

        # Pattern:
        # **Question N:** text ...
        # *Source: ...*
        # (blank lines between)
        q_blocks = re.split(r"\n(?=\*\*Question\s+\d+)", body)
        for q_block in q_blocks:
            q_block = q_block.strip()
            if not q_block:
                continue
            # Extract question number + text
            q_header_match = re.match(
                r"\*\*Question\s+(\d+)(?::\*\*|:\s*\*\*)?\s*(.+?)(?:\*\*)?$",
                q_block,
                re.DOTALL,
            )
            if not q_header_match:
                # Try alternate format without bold on closing
                q_header_match = re.match(
                    r"\*\*Question\s+(\d+)[:\s]*\*\*\s*(.+)",
                    q_block,
                    re.DOTALL,
                )
            if not q_header_match:
                continue

            number = int(q_header_match.group(1))
            rest = q_block[q_header_match.end():]
            # question text + rest combined
            full_text = q_header_match.group(2).strip() + " " + rest

            # Extract source note: *Source: ...*
            source_match = re.search(r"\*Source:\s*(.+?)\*", full_text, re.DOTALL)
            source_note = source_match.group(1).strip() if source_match else ""

            # Remove source note from question text
            question_text = re.sub(r"\*Source:\s*.+?\*", "", full_text, flags=re.DOTALL)
            question_text = question_text.strip()
            # Clean up stray bold markers
            question_text = re.sub(r"\*{1,2}", "", question_text).strip()

            questions.append({
                "number": number,
                "question_text": question_text,
                "source_note": source_note,
            })

        result[name] = questions

    # Validate
    for archetype in _ARCHETYPE_NAMES:
        if archetype not in result:
            log.warning("Reflection questions for '%s' not found.", archetype)
        elif len(result[archetype]) != 5:
            log.warning(
                "Expected 5 reflection questions for '%s', got %d.",
                archetype,
                len(result[archetype]),
            )

    return result


# ─────────────────────────────────────────────────────────────────────────────
# Module-level loading
# ─────────────────────────────────────────────────────────────────────────────

def _load_all() -> tuple:
    """Load and parse all content files. Returns (SOUL_SHAPES, DOMAINS, ASPECTS, ARCHETYPES, REFLECTION_QUESTIONS)."""
    log.debug("Loading IMAGO content files from %s", _CONTENT_DIR)

    soul_shapes_raw = _read(_FILES["soul_shapes"])
    domains_raw = _read(_FILES["domains"])
    aspects_raw = _read(_FILES["aspects"])
    archetypes_15_raw = _read(_FILES["archetypes_15"])
    archetypes_610_raw = _read(_FILES["archetypes_610"])
    reflections_raw = _read(_FILES["reflections"])

    soul_shapes = _parse_soul_shapes(soul_shapes_raw)
    domains = _parse_domains(domains_raw)
    aspects = _parse_aspects(aspects_raw)

    archetypes: Dict[str, dict] = {}
    archetypes.update(_parse_archetypes(archetypes_15_raw))
    archetypes.update(_parse_archetypes(archetypes_610_raw))

    reflection_questions = _parse_reflection_questions(reflections_raw)

    return soul_shapes, domains, aspects, archetypes, reflection_questions


# Parse at import time
try:
    SOUL_SHAPES, DOMAINS, ASPECTS, ARCHETYPES, REFLECTION_QUESTIONS = _load_all()
except Exception as _exc:
    log.error("IMAGO content loader failed to initialise: %s", _exc, exc_info=True)
    # Provide empty fallbacks so the module still imports
    SOUL_SHAPES: Dict[str, dict] = {}
    DOMAINS: Dict[str, Dict[str, dict]] = {}
    ASPECTS: Dict[str, dict] = {}
    ARCHETYPES: Dict[str, dict] = {}
    REFLECTION_QUESTIONS: Dict[str, List[dict]] = {}


# ─────────────────────────────────────────────────────────────────────────────
# Self-test
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    print("=" * 60)
    print("IMAGO Content Loader — Self-Test")
    print("=" * 60)

    # ── Soul Shapes ───────────────────────────────────────────────────────────
    print(f"\nSOUL_SHAPES: {len(SOUL_SHAPES)} keys → {list(SOUL_SHAPES.keys())}")
    for name, shape in SOUL_SHAPES.items():
        paras = shape["narrative_paragraphs"]
        print(f"  {name}: sidebar={shape['sidebar_meta']}")
        print(f"         tagline={shape['tagline']!r}")
        print(f"         narrative paragraphs={len(paras)} (first 80 chars: {paras[0][:80]!r})")

    # ── Domains ───────────────────────────────────────────────────────────────
    print(f"\nDOMAINS: {len(DOMAINS)} codes → {list(DOMAINS.keys())}")
    for code, poles in DOMAINS.items():
        print(f"  {code}: poles={list(poles.keys())}")
        for pole, data in poles.items():
            print(f"     {pole}: sidebar={data['sidebar']}")
            print(f"           opening_paragraphs={len(data['opening_paragraphs'])}")
            what_looks = data.get("what_this_looks_like", [])
            print(f"           what_this_looks_like={len(what_looks)} paras")

    # ── Aspects ───────────────────────────────────────────────────────────────
    print(f"\nASPECTS: {len(ASPECTS)} codes → {list(ASPECTS.keys())}")
    for code, asp in ASPECTS.items():
        print(f"  {code} ({asp['name']}): high={asp['high_paragraph'][:60]!r}...")

    # ── Archetypes ────────────────────────────────────────────────────────────
    print(f"\nARCHETYPES: {len(ARCHETYPES)} → {list(ARCHETYPES.keys())}")
    for name, arch in ARCHETYPES.items():
        print(f"  {name}:")
        print(f"    biblical_anchor={arch['biblical_anchor']!r}")
        print(f"    opening paras={len(arch['opening'])}")
        print(f"    behavioral_markers={len(arch['behavioral_markers'])}")
        print(f"    scripture_figures={len(arch['scripture_figures'])}")
        print(f"    shadow paras={len(arch['shadow'])}")
        print(f"    gospel_calling paras={len(arch['gospel_calling'])}")
        print(f"    prayer paras={len(arch['prayer'])}")

    # ── Reflection Questions ──────────────────────────────────────────────────
    print(f"\nREFLECTION_QUESTIONS: {len(REFLECTION_QUESTIONS)} archetypes")
    for name, qs in REFLECTION_QUESTIONS.items():
        print(f"  {name}: {len(qs)} questions")
        if qs:
            print(f"    Q1: {qs[0]['question_text'][:80]!r}...")
            print(f"    Q1 source: {qs[0]['source_note']!r}")
