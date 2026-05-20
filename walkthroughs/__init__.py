"""Walkthrough PDF generation system.

Architecture:
    walkthrough_base.py     — shared infrastructure (fonts, palette, helpers)
    personal/__init__.py    — registry of (mechanism, breakdown) -> PDF builder
    personal/architect_attorney.py  — first profile (Chris)
    couples/__init__.py     — registry of (mech_a, mech_b) -> PDF builder
    couples/architect_island.py     — first pair (Chris + Carolyn)
    fallback.py             — "Your walkthrough is being prepared" PDF

The generator package exports two main functions:
    build_personal_walkthrough(submission)  -> bytes
    build_couples_walkthrough(sub_a, sub_b) -> bytes

Both return PDF bytes ready for HTTP response or email attachment.
"""
from .api import build_personal_walkthrough, build_couples_walkthrough

__all__ = ["build_personal_walkthrough", "build_couples_walkthrough"]
