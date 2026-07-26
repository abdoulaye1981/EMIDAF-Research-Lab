from emidaf_core.managers.logger_manager import LoggerManager

logger = LoggerManager()

logger.info("Projet créé")

logger.warning("Import CSV")

logger.error("Erreur de lecture")

logger.critical("Erreur critique")

print("LoggerManager OK")