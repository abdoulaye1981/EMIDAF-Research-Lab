"""
=========================================================
EMIDAF Framework v1.0
Dataset Profiler Package
---------------------------------------------------------
Package de profilage des jeux de données.

Auteur : Abdoulaye Wakhab DIOP
Framework : EMIDAF
=========================================================
"""

from .dataset_profiler import DatasetProfiler
from .profile_manager import ProfileManager
from .profile_builder import ProfileBuilder
from .profile_service import ProfileService
from .profile_repository import ProfileRepository
from .profile_controller import ProfileController

from .profile_result import ProfileResult
from .profile_summary import ProfileSummary
from .profile_metadata import ProfileMetadata

__version__ = "1.0.0"

__all__ = [
    "DatasetProfiler",
    "ProfileManager",
    "ProfileBuilder",
    "ProfileService",
    "ProfileRepository",
    "ProfileController",
    "ProfileResult",
    "ProfileSummary",
    "ProfileMetadata",
]