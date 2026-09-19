from pathlib import Path

from emidaf_core.managers.logger_manager import LoggerManager


def test_manager_creation():

    logger = LoggerManager()

    assert logger is not None


def test_loggers_exist():

    logger = LoggerManager()

    assert logger.exists("application")
    assert logger.exists("project")
    assert logger.exists("import")
    assert logger.exists("inspection")
    assert logger.exists("error")


def test_list():

    logger = LoggerManager()

    loggers = logger.list()

    assert isinstance(loggers, list)

    assert "application" in loggers
    assert "project" in loggers
    assert "import" in loggers
    assert "inspection" in loggers
    assert "error" in loggers


def test_get_logger():

    logger = LoggerManager()

    assert logger.get_logger("application") is not None
    assert logger.get_logger("project") is not None
    assert logger.get_logger("xxxx") is None


def test_properties():

    logger = LoggerManager()

    assert logger.application is not None
    assert logger.project is not None
    assert logger.importer is not None
    assert logger.inspection is not None
    assert logger.error is not None


def test_logging():

    logger = LoggerManager()

    logger.info("Test application")
    logger.project.info("Test project")
    logger.importer.info("Test import")
    logger.inspection.info("Test inspection")
    logger.error.error("Test error")

    assert Path("logs/application.log").exists()
    assert Path("logs/project.log").exists()
    assert Path("logs/import.log").exists()
    assert Path("logs/inspection.log").exists()
    assert Path("logs/error.log").exists()


def test_warning():

    logger = LoggerManager()

    logger.warning("Test warning")

    assert logger.application is not None


def test_error_message():

    logger = LoggerManager()

    logger.error_message("Test error")

    assert logger.application is not None


def test_critical():

    logger = LoggerManager()

    logger.critical("Test critical")

    assert logger.application is not None
