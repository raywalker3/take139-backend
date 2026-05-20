"""Registry of couples walkthrough builders.

Each builder is a callable:  builder(sub_a, sub_b) -> bytes (PDF)

Key is (mechanism_a, mechanism_b) where the order matters — the writer chose
which partner gets which color/voice. The API tries both orderings before
falling back to the generic "preparing your walkthrough" PDF.

Total possible mechanism pairs: 15 (Architect+Architect, Architect+Island, ...)
Currently written: 1 (Architect + Island — Chris + Carolyn pattern).
"""
from .architect_island import build as build_architect_island

COUPLES_REGISTRY = {
    ("ARCH", "ISLE"): build_architect_island,
}
