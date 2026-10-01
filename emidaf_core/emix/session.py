"""
=========================================================
EMIDAF Framework v1.0
EMIX - Session State
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .sources import SourceRegistry
from .integration import IntegrationManager
from .joint_display import JointDisplayManager
from .inference import MetaInferenceManager


@dataclass
class EMIXSession:
    """
    Regroupe les gestionnaires constituant
    un état opérationnel EMIX.
    """

    source_registry: SourceRegistry
    integration_manager: IntegrationManager
    joint_display_manager: JointDisplayManager
    meta_inference_manager: MetaInferenceManager

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return {
            "sources": (
                self.source_registry
                .to_dict()
                .get(
                    "sources",
                    [],
                )
            ),
            "links": (
                self.integration_manager
                .to_dict()
                .get(
                    "links",
                    [],
                )
            ),
            "joint_display": (
                self.joint_display_manager
                .to_dict()
                .get(
                    "joint_display",
                    [],
                )
            ),
            "meta_inferences": (
                self.meta_inference_manager
                .to_dict()
                .get(
                    "meta_inferences",
                    [],
                )
            ),
        }
