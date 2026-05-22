"""Registry of couples walkthrough builders.

Each builder is a callable:  builder(sub_a, sub_b) -> bytes (PDF)

Key is (mechanism_a, mechanism_b) where the order matches the writer's chosen
ordering (alphabetical by mechanism code, with the exception of architect_island
which was written before the convention was set). The api.py dispatcher tries
both (a, b) and (b, a) before falling back to the generic preparing PDF, so the
order in the key reflects the file naming, not directionality.

Total mechanism pairs: 21 (6 same-mech + 15 cross-mech) — ALL WRITTEN.
"""
from .architect_architect import build as build_architect_architect
from .architect_island import build as build_architect_island
from .architect_ambassador import build as build_architect_ambassador
from .architect_vault import build as build_architect_vault
from .architect_adapter import build as build_architect_adapter
from .architect_performance import build as build_architect_performance

from .island_island import build as build_island_island
from .ambassador_island import build as build_ambassador_island
from .island_vault import build as build_island_vault
from .adapter_island import build as build_adapter_island
from .island_performance import build as build_island_performance

from .ambassador_ambassador import build as build_ambassador_ambassador
from .ambassador_vault import build as build_ambassador_vault
from .adapter_ambassador import build as build_adapter_ambassador
from .ambassador_performance import build as build_ambassador_performance

from .vault_vault import build as build_vault_vault
from .adapter_vault import build as build_adapter_vault
from .performance_vault import build as build_performance_vault

from .adapter_adapter import build as build_adapter_adapter
from .adapter_performance import build as build_adapter_performance
from .performance_performance import build as build_performance_performance


COUPLES_REGISTRY = {
    # Architect line (6 pairs)
    ("ARCH", "ARCH"):  build_architect_architect,
    ("ARCH", "ISLE"):  build_architect_island,
    ("ARCH", "AMB"):   build_architect_ambassador,
    ("ARCH", "VAULT"): build_architect_vault,
    ("ARCH", "ADPT"):  build_architect_adapter,
    ("ARCH", "CAMP"):  build_architect_performance,

    # Island line (5 remaining; ARCH+ISLE handled above)
    ("ISLE", "ISLE"):  build_island_island,
    ("AMB", "ISLE"):   build_ambassador_island,
    ("ISLE", "VAULT"): build_island_vault,
    ("ADPT", "ISLE"):  build_adapter_island,
    ("ISLE", "CAMP"):  build_island_performance,

    # Ambassador line (4 remaining)
    ("AMB", "AMB"):   build_ambassador_ambassador,
    ("AMB", "VAULT"): build_ambassador_vault,
    ("ADPT", "AMB"):  build_adapter_ambassador,
    ("AMB", "CAMP"):  build_ambassador_performance,

    # Vault line (3 remaining)
    ("VAULT", "VAULT"): build_vault_vault,
    ("ADPT", "VAULT"):  build_adapter_vault,
    ("CAMP", "VAULT"):  build_performance_vault,

    # Adapter line (2 remaining)
    ("ADPT", "ADPT"): build_adapter_adapter,
    ("ADPT", "CAMP"): build_adapter_performance,

    # Performance line (1 remaining)
    ("CAMP", "CAMP"): build_performance_performance,
}
