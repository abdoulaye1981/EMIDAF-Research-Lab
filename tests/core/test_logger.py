from emidaf_core.core.logger import Logger


def test_logger():

    logger = Logger()

    logger.info("Hello")

    logger.warning("Warning")

    logger.error("Error")

    assert logger.logger is not None