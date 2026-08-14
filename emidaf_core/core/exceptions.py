"""
=========================================================
EMIDAF Framework
Exceptions
=========================================================

Exceptions officielles du framework.

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
"""


class EMIDAFException(Exception):
    """
    Exception de base du framework.
    """

    pass


# ==========================================================
# CORE
# ==========================================================

class ConfigurationError(EMIDAFException):
    pass


class ValidationError(EMIDAFException):
    pass


class ContextError(EMIDAFException):
    pass


class BuilderError(EMIDAFException):
    pass


class EngineError(EMIDAFException):
    pass


class AnalyzerError(EMIDAFException):
    pass


class RepositoryError(EMIDAFException):
    pass


class RegistryError(EMIDAFException):
    pass


class ServiceError(EMIDAFException):
    pass


class ManagerError(EMIDAFException):
    pass


class FactoryError(EMIDAFException):
    pass


class CacheError(EMIDAFException):
    pass


# ==========================================================
# DATASET
# ==========================================================

class DatasetError(EMIDAFException):
    pass


class MissingValuesError(EMIDAFException):
    pass


class OutlierError(EMIDAFException):
    pass


class CorrelationError(EMIDAFException):
    pass


class NormalityError(EMIDAFException):
    pass


# ==========================================================
# MACHINE LEARNING
# ==========================================================

class ModelError(EMIDAFException):
    pass


class TrainingError(EMIDAFException):
    pass


class PredictionError(EMIDAFException):
    pass