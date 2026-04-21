"""Pair code generation — memorable, pronounceable, unique."""
import random
import string

# Curated list of biblical / pastoral / meaningful words for pair codes
WORDS = [
    "REFUGE", "ANCHOR", "KINDRED", "HARVEST", "REDEEM", "WITNESS",
    "COVENANT", "SHEPHERD", "PILGRIM", "GRAFTED", "MERCY", "JUSTICE",
    "COMPASS", "LANTERN", "BEACON", "THRESHOLD", "HORIZON", "KINDLE",
    "KEEPER", "HOMESTEAD", "HARBOR", "WILLOW", "CEDAR", "ORCHARD",
    "VIGIL", "GENTLE", "STEADFAST", "PATIENCE", "COURAGE", "VALOR",
    "HONOR", "PSALM", "VINEYARD", "OLIVE", "ALMOND", "GLEAN",
    "FOLDING", "TENDER", "GATHERED", "ABIDE", "LEANING", "RESTFUL",
    "TRUSTED", "MARKED", "CHOSEN", "NAMED", "KNOWN", "SEARCHED",
    "WELLSPRING", "KINDLED", "QUIET", "STILL", "WAITING", "LISTEN",
]


def generate_pair_code(existing_codes: set = None) -> str:
    """Generate a unique memorable code like ANCHOR-4829.

    Args:
        existing_codes: Set of already-used codes to avoid collision

    Returns:
        A unique pair code string
    """
    if existing_codes is None:
        existing_codes = set()

    # Try a reasonable number of times before falling back
    for _ in range(50):
        word = random.choice(WORDS)
        number = random.randint(1000, 9999)
        code = f"{word}-{number}"
        if code not in existing_codes:
            return code

    # Fallback: append a letter if we hit collisions
    while True:
        word = random.choice(WORDS)
        number = random.randint(1000, 9999)
        suffix = random.choice(string.ascii_uppercase)
        code = f"{word}-{number}{suffix}"
        if code not in existing_codes:
            return code
