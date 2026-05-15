"""IMAGO production item set loader.

Loads the 100-item assessment from imago_items.csv at module import time.
Provides:
    ITEMS — list of dicts with keys: item_id, domain, aspect_code, aspect_name,
             item_number, item_text, direction, source
    ITEMS_BY_ID — dict {item_id: item}
    ITEMS_BY_ASPECT — dict {aspect_code: [items]}

Item ordering is preserved for assessment delivery (the order in the CSV is
the order users will see).
"""
import csv
import os
from typing import Dict, List


_HERE = os.path.dirname(os.path.abspath(__file__))
_CSV_PATH = os.path.join(_HERE, "imago_items.csv")


def _load() -> List[dict]:
    items = []
    with open(_CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["item_number"] = int(row["item_number"])
            items.append(row)
    return items


ITEMS: List[dict] = _load()
ITEMS_BY_ID: Dict[str, dict] = {it["item_id"]: it for it in ITEMS}

ITEMS_BY_ASPECT: Dict[str, List[dict]] = {}
for it in ITEMS:
    ITEMS_BY_ASPECT.setdefault(it["aspect_code"], []).append(it)


def get_items_for_assessment(shuffle: bool = False) -> List[dict]:
    """Return items in the order the user should see them.

    By default we deliver in CSV order (grouped by aspect, balanced F/R).
    For production we may want to shuffle WITHIN the deliverable list to
    avoid response-set bias. The frontend can do this; we deliver in
    canonical order so scoring is deterministic.

    Args:
        shuffle: if True, shuffle the items (useful for client-side display).
                 The scoring is identical regardless of order.

    Returns:
        list of dicts, each with keys item_id, item_text, aspect_code,
        domain, direction, source.
    """
    out = list(ITEMS)
    if shuffle:
        import random
        random.shuffle(out)
    return out


if __name__ == "__main__":
    print(f"Loaded {len(ITEMS)} items")
    print(f"Aspects covered: {sorted(ITEMS_BY_ASPECT.keys())}")
    for aspect_code in sorted(ITEMS_BY_ASPECT.keys()):
        n = len(ITEMS_BY_ASPECT[aspect_code])
        f = sum(1 for it in ITEMS_BY_ASPECT[aspect_code] if it["direction"] == "FORWARD")
        r = sum(1 for it in ITEMS_BY_ASPECT[aspect_code] if it["direction"] == "REVERSE")
        print(f"  {aspect_code}: {n} items ({f}F / {r}R)")
