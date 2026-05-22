"""Registry of personal walkthrough builders.

Each builder is a callable:  builder(submission) -> bytes (PDF)

Key is (mechanism_code, breakdown_code), both uppercase short codes:
    mechanisms: ARCH ISLE AMB VAULT ADPT CAMP
    breakdowns: ATTY GHOST FLOOD MASK VERD PLEA  (plus legacy: DISAP=GHOST, REM=VERD)

Total: 36 personal walkthroughs (6 mechanisms x 6 breakdowns) — ALL WRITTEN.
"""
from .architect_attorney import build as build_architect_attorney
from .architect_ghost import build as build_architect_ghost
from .architect_flood import build as build_architect_flood
from .architect_mask import build as build_architect_mask
from .architect_verd import build as build_architect_verd
from .architect_plea import build as build_architect_plea

from .island_attorney import build as build_island_attorney
from .island_ghost import build as build_island_ghost
from .island_flood import build as build_island_flood
from .island_mask import build as build_island_mask
from .island_verd import build as build_island_verd
from .island_plea import build as build_island_plea

from .ambassador_attorney import build as build_ambassador_attorney
from .ambassador_ghost import build as build_ambassador_ghost
from .ambassador_flood import build as build_ambassador_flood
from .ambassador_mask import build as build_ambassador_mask
from .ambassador_verd import build as build_ambassador_verd
from .ambassador_plea import build as build_ambassador_plea

from .vault_attorney import build as build_vault_attorney
from .vault_ghost import build as build_vault_ghost
from .vault_flood import build as build_vault_flood
from .vault_mask import build as build_vault_mask
from .vault_verd import build as build_vault_verd
from .vault_plea import build as build_vault_plea

from .adapter_attorney import build as build_adapter_attorney
from .adapter_ghost import build as build_adapter_ghost
from .adapter_flood import build as build_adapter_flood
from .adapter_mask import build as build_adapter_mask
from .adapter_verd import build as build_adapter_verd
from .adapter_plea import build as build_adapter_plea

from .performance_attorney import build as build_performance_attorney
from .performance_ghost import build as build_performance_ghost
from .performance_flood import build as build_performance_flood
from .performance_mask import build as build_performance_mask
from .performance_verd import build as build_performance_verd
from .performance_plea import build as build_performance_plea


PERSONAL_REGISTRY = {
    # Architect line
    ("ARCH", "ATTY"):  build_architect_attorney,
    ("ARCH", "GHOST"): build_architect_ghost,
    ("ARCH", "FLOOD"): build_architect_flood,
    ("ARCH", "MASK"):  build_architect_mask,
    ("ARCH", "VERD"):  build_architect_verd,
    ("ARCH", "PLEA"):  build_architect_plea,

    # Island line
    ("ISLE", "ATTY"):  build_island_attorney,
    ("ISLE", "GHOST"): build_island_ghost,
    ("ISLE", "FLOOD"): build_island_flood,
    ("ISLE", "MASK"):  build_island_mask,
    ("ISLE", "VERD"):  build_island_verd,
    ("ISLE", "PLEA"):  build_island_plea,

    # Ambassador line
    ("AMB", "ATTY"):  build_ambassador_attorney,
    ("AMB", "GHOST"): build_ambassador_ghost,
    ("AMB", "FLOOD"): build_ambassador_flood,
    ("AMB", "MASK"):  build_ambassador_mask,
    ("AMB", "VERD"):  build_ambassador_verd,
    ("AMB", "PLEA"):  build_ambassador_plea,

    # Vault line
    ("VAULT", "ATTY"):  build_vault_attorney,
    ("VAULT", "GHOST"): build_vault_ghost,
    ("VAULT", "FLOOD"): build_vault_flood,
    ("VAULT", "MASK"):  build_vault_mask,
    ("VAULT", "VERD"):  build_vault_verd,
    ("VAULT", "PLEA"):  build_vault_plea,

    # Adapter line
    ("ADPT", "ATTY"):  build_adapter_attorney,
    ("ADPT", "GHOST"): build_adapter_ghost,
    ("ADPT", "FLOOD"): build_adapter_flood,
    ("ADPT", "MASK"):  build_adapter_mask,
    ("ADPT", "VERD"):  build_adapter_verd,
    ("ADPT", "PLEA"):  build_adapter_plea,

    # Performance Campaign line
    ("CAMP", "ATTY"):  build_performance_attorney,
    ("CAMP", "GHOST"): build_performance_ghost,
    ("CAMP", "FLOOD"): build_performance_flood,
    ("CAMP", "MASK"):  build_performance_mask,
    ("CAMP", "VERD"):  build_performance_verd,
    ("CAMP", "PLEA"):  build_performance_plea,
}
