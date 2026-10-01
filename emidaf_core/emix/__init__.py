"""
EMIX - EMIDAF Mixed Methods Integration Engine.
"""

from .engine import EMIXEngine
from .session import EMIXSession

from .sources import (
    MixedMethodSource,
    SourceRegistry,
)

from .integration import (
    IntegrationLink,
    IntegrationManager,
)

from .joint_display import (
    JointDisplayRow,
    JointDisplayManager,
)

from .inference import (
    MetaInference,
    MetaInferenceManager,
)

from .summary import MixedMethodsSummary


__all__ = [
    "EMIXEngine",
    "EMIXSession",
    "MixedMethodSource",
    "SourceRegistry",
    "IntegrationLink",
    "IntegrationManager",
    "JointDisplayRow",
    "JointDisplayManager",
    "MetaInference",
    "MetaInferenceManager",
    "MixedMethodsSummary",
]
