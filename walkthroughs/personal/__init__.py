"""Registry of personal walkthrough builders.

Each builder is a callable:  builder(submission) -> bytes (PDF)

Key is (mechanism_code, breakdown_code), both uppercase short codes:
    mechanisms: ARCH ISLE AMB VAULT ADPT CAMP
    breakdowns: ATTY GHOST FLOOD MASK VERD PLEA  (plus legacy: DISAP=GHOST, REM=VERD)

Total possible: 36 personal walkthroughs.
Currently written: 1 (Architect + Attorney — Chris's profile).
"""
from .architect_attorney import build as build_architect_attorney

PERSONAL_REGISTRY = {
    ("ARCH", "ATTY"): build_architect_attorney,
}
